from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import datetime 
import csv
import logging

'''
Author: @blackram
A simple python script to track and log whats user total online time

***requirements***
need to install selenium package

***Known Bugs***
1.user has to be in recent chat list which should be visible for selenium on opening whats web page
2.If the browser tab with whats web is closed then need to open browser and scan QR code every time
'''


# function to write data into a CSV file
def write_time_to_file(target, onlinetime):
	# opening in append mode
	with open('TimeTracker.csv', 'a+') as csv_file:
		fieldNames = ['Target', 'onlinetime']
		writer = csv.DictWriter(csv_file, fieldNames)
		writer.writerow({'Target': target, 'onlinetime': onlinetime})


# opening chrome browser
driver = webdriver.Chrome('/home/pi/Downloads/chromium-driver/chromedriver')

# opening whats web page
driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 600) 

target = '"your target name"'  # change your target which is in your recent history of whats app chat

target_argument = '//span[contains(@title,' + target + ')]'
# clicking on the target user name for checking whether user status is online
target_user = wait.until(EC.presence_of_element_located((By.XPATH, target_argument))) 
target_user.click()

# initializing variables for using inside infinite loop
online_time = 0
came_from_online = False

# infinite loop to check and log online time spent by the user
while True:
	if('online' in driver.page_source):
		if(not came_from_online):
			t1 = datetime.datetime.now()
		logging.info("Online Time start: "+str(t1))
		logging.info("User is online")
		came_from_online = True
	else:
		logging.info("User is offline")
		if(came_from_online):
			t2 = datetime.datetime.now()
			logging.info("Online Time stop: "+str(t2))
			online_time = t2 - t1
			logging.info("Online Time start: "+str(t1))
			logging.info("Online Time stop: "+str(t2))
			logging.info(online_time)
			came_from_online = False
			write_time_to_file(target, str(online_time)+" on "+str(datetime.datetime.now()))