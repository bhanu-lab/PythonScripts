import requests 
import html5lib
from bs4 import BeautifulSoup 

'''
Author: R@jesh
A simple python script to download a News Paper and to send as email attachment to users dialy. 
***requirements***
need to install required packages for this script
'''

#URL which contain GDrive linkof Hindhu Paper
URL = "https://www.bitul.in/epaper/the-hindu/"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 
c=0
#Checking all the hyperlinks in the site until drive link
for link in soup.find_all('a'):
  drivelink = link.get('href')
  if "drive.google.com" in str(drivelink):
    print(drivelink)
    if(c==1):
      break
    c=1
#Now AdFree Hindhu News Paper Link is on drivelink


'''
#Code to Download PDF file and save it locally
#Working With Links like this http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf
#But facing issues with Google Drive Link - ToDo

import requests 
file_url = "https://drive.google.com/uc?authuser=0&id=1qtII2G6XhIBS8yZ7bCbTRyL7dgtTbNp4&export=download"

r = requests.get(file_url, stream = True) 

with open("NewsPaper.pdf","wb") as pdf: 
	for chunk in r.iter_content(chunk_size=1024): 
		# writing one chunk at a time to pdf file 
		if chunk: 
			pdf.write(chunk) 
'''

#Now Downloaded File can be sent as email attachment - Already Done
