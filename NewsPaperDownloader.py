import requests 
import html5lib
from bs4 import BeautifulSoup 

'''
Author: R@jesh
A simple python script to download a News Paper and to send as email attachment to users dialy. 
***requirements***
need to install required packages(requests, BeautifulSoup, html5lib) for this script
'''

#URL which contain GDrive link of Hindhu Paper
URL = "https://www.bitul.in/epaper/the-hindu/"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 
#Checking all the hyperlinks in the site until drive link
for link in soup.find_all('a'):
  drivelink = link.get('href')
  if "drive.google.com" in str(drivelink):
    print(drivelink)
    break;
#Now AdFree Hindhu News Paper Link is on drivelink

Id = drivelink[32:65]
file_url = "https://drive.google.com/uc?authuser=0&id="+Id+"&export=download"
r = requests.get(file_url, stream = True) 
with open("resources/NewsPaper/NewsPaper.pdf","wb") as pdf: 
	for chunk in r.iter_content(chunk_size=1024): 
		# writing one chunk at a time to pdf file 
		if chunk: 
			pdf.write(chunk) 
#File Will be Downloaded in the current folder

	