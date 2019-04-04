# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:30:46 2019

@author: Rajesh.Gundupalli
"""

import requests 
import html5lib
from bs4 import BeautifulSoup 

#URL which contain GDrive link of Hindhu Paper
URL = "https://www.bitul.in/epaper/the-hindu/"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 
f=0
#Checking all the hyperlinks in the site until drive link
for link in soup.find_all('a'):
  drivelink = link.get('href')
  if "http://www.newspapertoday.xyz" in str(drivelink):
    print(drivelink)
    f=1
    break;
  elif "drive.google.com" in str(drivelink):
    print(drivelink)
    break;
#Now AdFree Hindhu News Paper Link is on drivelink
if f==0:
    Id = drivelink[32:65]
    file_url = "https://drive.google.com/uc?authuser=0&id="+Id+"&export=download"
file_url = drivelink
r = requests.get(file_url, stream = True) 
with open("resources/NewsPaper/NewsPaper.pdf","wb") as pdf: 
	for chunk in r.iter_content(chunk_size=1024): 
		# writing one chunk at a time to pdf file 
		if chunk: 
			pdf.write(chunk) 
#File Will be Downloaded in the current folder

	