import os
import random
import logging
import platform
import blackram_utils

# TODO: check previously set wallpaper is not selected again to set
# TODO: check for allowed file extensions like jpg, jpeg, png
# TODO: pick up folder location from a file instead of hardcoding

logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# read all wallpapers stored location
wallpapers_location = blackram_utils.get_param_value("blackscripts.settings.wallpaper")
logger.info("wallpapers location is "+wallpapers_location)
wallpapers_list = []

# getting list of all files in the folder
list = os.listdir(wallpapers_location)
logger.info(list)

#Checking the OS
if platform.system()=='Windows':
    print("Not updated for Windows")
elif platform.system()=='Darwin':
    print("Not updated for Mac")
    
# iterate through the list of wallpapers list
for file in list:
    # for checking whether it is a file
    # os.path.isfile needs complete file path instead of file name alone
    if os.path.isfile(wallpapers_location+"/"+file):
        logger.info(wallpapers_location+file)
        wallpapers_list.append(file)

# find total wallpaper files present in the directory
max_len = len(wallpapers_list)
logger.info("max length is "+str(max_len))

# generate a random number to get the wallpaper number to be set
wallpaper_num = random.randint(0, (max_len-1))
logger.info("Random number is "+str(wallpaper_num))
logger.info("wallpaper selected is "+wallpapers_list[wallpaper_num])

# for running Ubuntu 18.04 gsettings has to be changed to set wallpaper
os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri "+wallpapers_location+"/"+wallpapers_list[wallpaper_num])
