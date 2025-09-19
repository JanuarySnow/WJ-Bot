## Sanity check error with Rayek's End - SSE Expanded Edition 

This is caused by your System locale causing one of the files in this modlist to not extract with the correct filename.

Cause: there is the archived file `Meshes\Oaristys\Clutter\Mirror°.nif` which is expected by WJ... but when a Windows install with a different System locale (E.G Japanese) (note: ENGLISH is used as main language, but Windows may still interpret symbols differently) it reads the file as `Meshes\Oaristys\Clutter\Mirror・nif` which does not match. Thus, the installation fails

The Work around

1. Find your reyak's end Mod folder inside Install directory\Mods
2. Create Meshes\Oaristys\Clutter\ inside this folder
3. Extract Meshes\Oaristys\Clutter\Mirror°.nif from the zip file to the folder you just created.
4. rename it to Mirror°.nif
5. Run Wabbajack again installing using the same paths - it will now skip this file.
