## Hash Fails 

Hashes for BSA or TEMP_BSA_FILES failures are usually caused by running out of drive space (especially if your primary drive or install drive is fairly low on free space) while it's unzipping and/or patching. You should generally make sure you have **30GB** more than the list requires free on both drives.

Most users can generally brute force it through by running the install over and over until it succeeds, especially if it's failing on different files every time. You may need to tick "overwrite install" after you restart the install.

If you are getting **consistent failures** on the same files, the hash fail mentions a **"SHA1"** fail, or you have retried **10+ times**, you can try deleting the zip file for the mod zip file for the mod which is failing - As its possible is a corrupt download causing the problem.

As a last resort (note this will not work if the list requires downloads from MEGA)

 **Downgrade Wabbajack to [3.6.1.1](https://github.com/wabbajack-tools/wabbajack/releases/download/3.6.1.1/3.6.1.1.zip)**  
   Get that zip file, unzip it somewhere (**a folder called 3.6.1.1 inside the directory where you're currently running Wabbajack from is a good idea**).  
   Run Wabbajack from inside that folder and choose the same folders as you currently do.  

### UNDER NO CIRCUMSTANCES SHOULD YOU DELETE ANY PART OF THE MODLIST 
