import os
import random

wallpapers_location = "/home/bhanureddy/Pictures/Wallpapers"
wallpapers_list = []
list = os.listdir(wallpapers_location)
print(list)
for file in list:
    if os.path.isfile(wallpapers_location+"/"+file):
        print(wallpapers_location+file)
        wallpapers_list.append(file)

max_len = len(wallpapers_list)
print("max length is "+str(max_len))
wallpaper_num = random.randint(0, (max_len-1))
print("Random number is "+str(wallpaper_num))
print("wallpaper selected is "+wallpapers_list[wallpaper_num])

os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri "+wallpapers_location+"/"+wallpapers_list[wallpaper_num])
