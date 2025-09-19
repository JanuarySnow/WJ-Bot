"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""
import aiohttp
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
import json


# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="potato"):
    def __init__(self, bot) -> None:
        self.bot = bot
    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
        

    @commands.hybrid_command(name="dad_joke", description="Get a random dadjoke.")
    async def dad_joke(self, context: Context) -> None:
        """
        Get a random dadjoke
        
        :param context: The hybrid command context.
        """
        user_agent = "https://github.com/JanuarySnow/RRR-Bot"
        headers  = {"Accept": "application/json", "User-Agent":user_agent}
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://icanhazdadjoke.com/", headers=headers) as request:
                if request.status == 200:
                    data = await request.json(content_type='application/json')
                    embed = discord.Embed(description=data["joke"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(name="dogpic", description="Get a random dog.")
    async def dogpic(self, context: Context) -> None:
        """
        Get a random dog
        
        :param context: The hybrid command context.
        """
        user_agent = "https://github.com/JanuarySnow/RRR-Bot"
        headers  = {"Accept": "application/json", "User-Agent":user_agent}
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://random.dog/woof.json", headers=headers) as request:
                if request.status == 200:
                    data = await request.json(content_type='application/json')
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(data["url"])

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Template(bot))
