# GFPGANLOOP

Requires: https://github.com/TencentARC/GFPGAN

Put 'GFPGANLOOP.py' & 'GFPGANLOOP.bat' in the same directory as GFPGAN's main py script. 

Make a 'LOOPINPUT' folder in that same directory and put any images you want there. I do not think folders will work yet. Your final result images will be in the 'LOOPRESULT' folder.

This script will take an image, use GFPGAN at 2x scale on it, then use GFPGAN at 1x scale on it, then again use GFPGAN at 1x scale on it. You have the ability to select which model you want to use.

This is not very useful, but sometimes it works good on really messed up AI generated faces when a single pass of GFPGAN doesn't work.
