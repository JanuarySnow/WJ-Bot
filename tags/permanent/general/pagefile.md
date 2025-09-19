## Page Files and Memory Crashes

Bigger Skyrim modlists need a lot of memory, and when there is not enough available it may fail allocating more. To fix this, you'll want to have a bigger pagefile.

A pagefile is a file on your disk Windows will use when there is not enough RAM available.

**Never disable the pagefile - this may lead to various issues on your system, such as this Skyrim crash.**

If you've never touched the pagefile, try performing the following steps:
1. Press `Windows + R` on your keyboard and enter `sysdm.cpl ,3`
1. Under the Performance section, press `Settings`
1. Go to the Advanced tab at the top, and at the Virtual memory section press `Change...`
1. Disable `Automatically manage paging file size for all drives`
1. If you have more than one drive, try enabling it for at least one more drive as a backup (make sure it has a decent bit of free space, like 15GB). Set the size to `System managed size`.
   
Otherwise, set a custom size for the drive it's currently on and increase the maximum size to be at least 20GB.
