import os
from datetime import datetime

def convert_date(timestamp):
	d = datetime.utcfromtimestamp(timestamp)
	formatted_date = d.strftime('%d %b %y')
	return formatted_date

print("enter the complete path of the directory to list files")
#path = input()
fh = os.scandir("home/")
print('FILENAME \t LASTMODIFIED \t LASTACCESSED \t SIZE \t MODE')
for entry in fh:
	if entry.is_file():
		info = entry.stat()
		print('{entry.name}\t {convert_date(info.st_mtime)}\t  {convert_date(info.st_atime)}\t {"{0:.2f}".format(round(info.st_size * 0.000001,2))}MB')

