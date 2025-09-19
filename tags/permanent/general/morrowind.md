##  Failed Compilation: Can't find game Morrowind.

This is caused when you are using a 'Pseudo Portable' instance of Mod organizer, created using the Nexus version of the installer. 

You will need to convert it to a Portable instance using the "loose files" version from the Github.

1. Start by downloading Mod.Organizer-X.X.X.7z ("x.x.x" will be the latest version number) from https://github.com/Modorganizer2/modorganizer/releases and extract it to a folder. (see image below)
2. Start the ModOrganizer.exe follow the first time setup tool to create a portable instance for the game you want to mod. In all the following instructions replace X.X.X with the correct version number (E.G 2.5.2). 
3. Navigate to the downloads folder and paste the Mod.Organizer-X.X.X.7z into there and create a Mod.Organizer-X.X.X.7z.meta containing the following text:

```
   [General]
   installed=true
   directURL=https://github.com/ModOrganizer2/modorganizer/releases/download/vX.X.X/Mod.Organizer-X.X.X.7z
```

### Importing a Global/Pseudo Portable Instance into a Portable one

Once you have your Portable Instance ready then go to your Global/Pseudo Portable Instance and copy the profiles, mods, downloads folders and paste them into your Portable instance. 

Use the new Portable instance for Wabbajack compilation, you can delete your old one.
