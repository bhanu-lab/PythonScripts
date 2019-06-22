import os
from datetime import datetime
from os import scandir

basepath=input('Enter the directory pathname:')

entries=os.listdir(basepath)


# function to get time in desired format
def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date


# function to get information about files present in given directory
def get_files():
    dir_entries = scandir(basepath)
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            print("{:50} {:40} {:1} KB".format(entry.name, convert_date(info.st_mtime), str(os.path.getsize(os.path.join(basepath, entry.name))/1000)))


print("{:50} {:40} {:1}".format("FILE NAME", "LAST MODIFIED", "SIZE"))
# function call
get_files()

