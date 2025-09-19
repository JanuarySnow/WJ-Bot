from __future__ import annotations

import discord
import math
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.ui import Button, View
import json
import os
import random
import calendar
import requests
import asyncio
from zoneinfo import ZoneInfo
from base64 import b64encode
from dataclasses import dataclass, field
from datetime import timedelta, timezone, datetime,date, time as dtime
from typing import List, Literal, Optional, Tuple, Dict, Any
import json
from urllib.parse import quote
import os
import difflib
import discord, pathlib, itertools
from typing   import Iterable, Optional
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from logger_config import logger
import re, yaml, aiohttp, io, textwrap, asyncio

BLOCKING_IO_EXECUTOR = ThreadPoolExecutor(max_workers=2)
_MARKDOWN_LIMIT = 4096
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_CONFIG_PATH = _PROJECT_ROOT / "tags.yaml"

async def _run_blocking(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(BLOCKING_IO_EXECUTOR, func, *args)

MONITORED_CHANNELS: set[int] = {
    666599178788536331,  #wj-help
    1344813548651548747, #my server
    1380569973889564762, #livelys test
    993694547114729522, # livelys tempus support
    958141029230477382, # livelys magnum support
    1317192691125194855, #livelys rule-11 tempus
    1383373637759012984, #reyqune test
}

MONITORED_FORUMS: set[int] = {
    1118583361808629913,   #wildlander support forum
}

ONLY_LOG_SERVER: set[int] = {
    747463348496367627, #livelys
}


class Wjhelp(commands.Cog, name="wjhelp"):
    def __init__(self, bot) -> None:
        self.bot = bot
        print("loading stats cog")
        self.logger = logger
        yaml.safe_load(open("tags.yaml"))
        self.tags = self.load_tags()
        self.monitored_channels: set[int] = {
            666599178788536331,  #wj-help
            1344813548651548747, #my server
            1380569973889564762, #livelys test
            993694547114729522, # livelys tempus support
            958141029230477382, # livelys magnum support
            1317192691125194855, #livelys rule-11 tempus
            1383373637759012984, #reyqune test
        }

        self.monitored_forums: set[int] = {
            1118583361808629913,   #wildlander support forum
        }

        self.only_log_server: set[int] = {
            #only respond to logs
            747463348496367627, #livelys
        }

    def _load_tags(self) -> Dict[str, Any]:
        with _CONFIG_PATH.open(encoding="utf-8") as fp:
            raw = yaml.safe_load(fp)

        tags: Dict[str, Any] = {}
        for name, cfg in raw.items():
            prompts = [p.lower() for p in cfg.get("prompt", [])]
            logprompts = [p.lower() for p in cfg.get("logprompt", [])]

            cfg["pattern"] = (
                re.compile("|".join(map(re.escape, prompts)), re.I) if prompts else None
            )
            cfg["logpattern"] = (
                re.compile("|".join(map(re.escape, logprompts)), re.I) if logprompts else None
            )
            tags[name] = cfg
        return tags
    
    def load_tags(self) -> Dict[str, Any]:
        with _CONFIG_PATH.open(encoding="utf-8") as fp:
            raw = yaml.safe_load(fp)

        compiled: Dict[str, Any] = {}
        for name, cfg in raw.items():
            prompts = [p.lower() for p in cfg.get("prompt", [])]
            cfg["pattern"] = (
                re.compile("|".join(map(re.escape, prompts)), re.I) if prompts else None
            )
            logprompts = [p.lower() for p in cfg.get("logprompt", [])]
            cfg["logpattern"] = (
                re.compile("|".join(map(re.escape, logprompts)), re.I)
                if logprompts else None
            )
            compiled[name] = cfg
        return compiled
    
    def resolve_asset(self, path_str: str) -> Path:
        path = (_PROJECT_ROOT / path_str.lstrip("/")).resolve()
        print(path)
        return path
    
    def read_markdown(self, path_str: str) -> str:
        md_path = self.resolve_asset(path_str)
        try:
            return md_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return "*(snippet missing)*"
        
    async def send_tag_reply(
        self, message: discord.Message, tagname: str, cfg: Dict[str, Any]
    ):
        print("sending tag reply", tagname)
        md = self.read_markdown(cfg["text"])

        lines = md.splitlines()
        if lines and lines[0].lstrip().startswith("#"):
            lines = lines[1:]
        body = "\n".join(lines).strip()

        if len(body) > 4096:
            body = body[:4093] + "…"

        embed = discord.Embed(
            title=f"📑 {tagname.replace('_', ' ').title()}",
            description=body,
            colour=discord.Colour.blue(),
        )

        img_key = cfg.get("image_url") or cfg.get("image")
        file: discord.File | None = None
        if img_key:
            img_path = self.resolve_asset(img_key)
            if img_path.is_file():
                file = discord.File(img_path, filename=img_path.name)
                embed.set_image(url=f"attachment://{img_path.name}")

        await message.reply(
            embed=embed,
            file=file if file else discord.utils.MISSING,
            mention_author=False,
        )

    @commands.Cog.listener("on_thread_create")
    async def forum_thread_auto_reply(self, thread: discord.Thread):
        print("on_thread_create", thread.id, thread.name)
        if not thread.parent or thread.parent.id not in MONITORED_FORUMS:
            return
        try:
            starter_msg = await thread.fetch_message(thread.id)
        except discord.NotFound:
            starter_msg = None

        content = thread.name
        attachments = []
        if starter_msg:
            content += f"\n{starter_msg.content}"
            attachments = starter_msg.attachments

        text_lc = content.lower()

        log_atts = [a for a in attachments if a.filename.lower().endswith(".log")]
        if log_atts:
            raw = await log_atts[0].read()
            try:
                log_txt = raw.decode("utf-8")
            except UnicodeDecodeError:
                log_txt = raw.decode("latin-1", errors="ignore")

            tag_match = self._find_last_tag_match(log_txt)
            if tag_match:
                tagname, cfg = tag_match
                if tagname == "curios" and self._matches("aecc", log_txt):
                    return
                if tagname == "api" and not self._api_exhausted(log_txt):
                    return
                await self.send_tag_reply(starter_msg or thread, tagname, cfg)
                return

        for tagname, cfg in self.tags.items():
            patt = cfg["pattern"]
            if patt and patt.search(text_lc):
                await self.send_tag_reply(starter_msg or thread, tagname, cfg)
                break


    @commands.hybrid_command(name="addforum", description="addforum")
    @commands.has_permissions(administrator=True)
    async def addforum(self, ctx: Context, forum_id: int):
        """Add a forum to the monitored forums list."""
        if forum_id is None:
            await ctx.send("Please provide a valid forum ID.")
            return
        if forum_id in self.monitored_forums:
            await ctx.send(f"Forum with ID {forum_id} is already monitored.")
            return
        self.monitored_forums.add(forum_id)
        await ctx.send(f"Forum with ID {forum_id} has been added to the monitored forums list.")

    @commands.hybrid_command(name="removeforum", description="removeforum")
    @commands.has_permissions(administrator=True)
    async def removeforum(self, ctx: Context, forum_id: int):
        """removeforum a forum to the monitored forums list."""
        if forum_id is None:
            await ctx.send("Please provide a valid forum ID.")
            return
        if forum_id not in self.monitored_forums:
            await ctx.send(f"Forum with ID {forum_id} is not already monitored.")
            return
        self.monitored_forums.remove(forum_id)
        await ctx.send(f"Forum with ID {forum_id} has been removed from the monitored forums list.")

    @commands.hybrid_command(name="addchannel", description="addchannel")
    @commands.has_permissions(administrator=True)
    async def addchannel(self, ctx: Context, channelid: int):
        """Add a forum to the monitored forums list."""
        if channelid is None:
            await ctx.send("Please provide a valid forum ID.")
            return
        if channelid in self.monitored_channels:
            await ctx.send(f"channel with ID {channelid} is already monitored.")
            return
        self.monitored_channels.add(channelid)
        await ctx.send(f"channel with ID {channelid} has been added to the monitored channels list.")

    @commands.hybrid_command(name="removechannel", description="removeforum")
    @commands.has_permissions(administrator=True)
    async def removechannel(self, ctx: Context, channelid: int):
        """removeforum a forum to the monitored forums list."""
        if channelid is None:
            await ctx.send("Please provide a valid forum ID.")
            return
        if channelid not in self.monitored_channels:
            await ctx.send(f"channel with ID {channelid} is not already monitored.")
            return
        self.monitored_channels.remove(channelid)
        await ctx.send(f"channel with ID {channelid} has been removed from the monitored channel list.")

    @commands.hybrid_command(name="logonly", description="logonly")
    @commands.has_permissions(administrator=True)
    async def logonly(self, ctx: Context):
        self.only_log_server.add(ctx.guild.id)
        await ctx.send(f"Server with ID {ctx.guild.id} has been added to the log-only server list.")

    @commands.hybrid_command(name="removelogonly", description="logonly")
    @commands.has_permissions(administrator=True)
    async def removelogonly(self, ctx: Context):
        self.only_log_server.remove(ctx.guild.id)
        await ctx.send(f"Server with ID {ctx.guild.id} has been removed from the log-only server list.")



    @commands.Cog.listener("on_message")
    async def tag_auto_reply(self, message: discord.Message):
        if message.author.bot:
            return

        chan = message.channel
        parent_chan = chan.parent if isinstance(chan, discord.Thread) else chan

        if (parent_chan.id not in self.monitored_channels
                and parent_chan.id not in self.monitored_forums):
            return

        if message.guild is None:
            return

        server_id = message.guild.id
        only_log = server_id in self.only_log_server

        text_lc = message.content.lower()

        log_atts = [a for a in message.attachments if a.filename.lower().endswith(".log")]
        if log_atts:
            raw = await log_atts[0].read()
            try:
                log_txt = raw.decode("utf-8")
            except UnicodeDecodeError:
                log_txt = raw.decode("latin-1", errors="ignore")

            tag_match = self._find_last_tag_match(log_txt)
            if tag_match:
                tagname, cfg = tag_match
                if tagname == "curios" and self._matches("aecc", log_txt):
                    return
                if tagname == "api" and not self._api_exhausted(log_txt):
                    return
                await self.send_tag_reply(message, tagname, cfg)
                return

        if not only_log:
            for tagname, cfg in self.tags.items():
                pattern = cfg["pattern"]
                if pattern and pattern.search(text_lc):
                    await self.send_tag_reply(message, tagname, cfg)
                    break


    def _find_last_tag_match(self, text: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Returns the tag config whose pattern matches closest to the end of `text`.
        If multiple tags match, respects custom priority rules (e.g. 'notenoughspace' > 'path').
        """
        matches: List[Tuple[str, Dict[str, Any], int]] = []

        for tagname, cfg in self.tags.items():
            if not cfg.get("log"):
                continue

            pattern = cfg.get("logpattern") or cfg.get("pattern")
            if not pattern:
                continue

            found = list(pattern.finditer(text))
            for i in found:
                print(f"Found match for {tagname} at {i.start()} in text of length {len(text)}")
            if found:
                last_match = found[-1]
                matches.append((tagname, cfg, last_match.start()))

        if not matches:
            return None

        # --- Priority override logic ---
        tagnames = [tag for tag, _, _ in matches]
        for tag in tagnames:
            print(f"Tag {tag} matched in text with start positions: {[m[2] for m in matches if m[0] == tag]}")
        if "notenoughspace" in tagnames and "path_not_found" in tagnames:
            # Force 'notenoughspace' if it's present
            for tag, cfg, _ in matches:
                if tag == "notenoughspace":
                    return (tag, cfg)

        # Otherwise return tag with match closest to end
        best = max(matches, key=lambda x: x[2])  # highest start() position
        return (best[0], best[1])




    def _matches(self, tag_key: str, text: str) -> bool:
        """Return True if *either* pattern (log or normal) for the tag is in text."""
        cfg = self.tags[tag_key]
        patt = cfg["logpattern"] or cfg["pattern"]
        return bool(patt and patt.search(text))

    def _api_exhausted(self, log_txt: str) -> bool:
        matches = [int(m.group(1)) for m in re.finditer(r"Remaining\s+Limit:\s*(\d+)", log_txt, re.I)]
        if not matches:
            return False

        zero_count = sum(1 for x in matches if x == 0)
        last_val = matches[-1]
        return last_val == 0 and zero_count > 1



async def setup(bot) -> None:
    await bot.add_cog(Wjhelp(bot))