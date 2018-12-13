import os
import random
import logging

# TODO: check previously set wallpaper is not selected again to set
# TODO: check for allowed file extensions like jpg, jpeg, png

logger = logging.getLogger()

# read all wallpapers stored location
wallpapers_location = "/home/bhanureddy/Pictures/Wallpapers"
wallpapers_list = []

# getting list of all files in the folder
list = os.listdir(wallpapers_location)
logger.info(list)

# iterate through the list of wallpapers list
for file in list:
    if os.path.isfile(wallpapers_location+"/"+file): ''' for checking whether it is a file
    os.path.isfile needs complete file path instead of file name alone '''
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
