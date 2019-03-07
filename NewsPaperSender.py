import requests 
import html5lib
from bs4 import BeautifulSoup 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os.path as op
import os
import sys

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
with open("resources/HindhuNewsPaper.pdf","wb") as pdf: 
	for chunk in r.iter_content(chunk_size=1024): 
		# writing one chunk at a time to pdf file 
		if chunk: 
			pdf.write(chunk) 
#File Will be Downloaded in the resources/NewsPaper/ folder

###                                                                                            ###
#================================================================================================#
###                                                                                            ###

# function for reading names and emails from text file
def get_contacts(file_name):
    names = []
    emails = []
    with open(file_name, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


# function for reading a message template
def get_message_template(file_name):
    with open(file_name, mode='r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# function to get my account details to send mail
def get_my_account_info(file_name):
    with open(file_name, mode='r') as my_details:
        for my_det in my_details:
            my_address = my_det.split()[0]
            my_password = my_det.split()[1]
    return my_address, my_password


# main function
def main():

    my_address, my_password = get_my_account_info('resources/from_mail.txt')  # get my account details
    #print(my_address)
    #print(my_password)
    names, emails = get_contacts('resources/test_contacts.txt')  # read contacts
    message_template = get_message_template('resources/email_template.txt')  # read template

    # using gmail smtp
    server = smtplib.SMTP(host='smtp.gmail.com', port='587')
    server.starttls()

    # Log into server
    server.login(my_address, my_password)
    failed_rcpts = {}
    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        message = message_template.substitute(PERSON_NAME=name.title())
        print(message)

        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = "Email Notification Test "+str(datetime.date.today())
        msg.attach(MIMEText(message, 'plain'))

        part = MIMEBase('application', "octet-stream")

        # adding attachement to the mail message
        #Todo - Take Command Line Argument to send files - may be path to files
        path = 'resources/NewsPaper/' 			#ToDo
        files = os.listdir(path)    #f.name for f in os.scandir(path) if f.is_file() #os.listdir(path)
        # for fname in os.scandir(path):
		# 	if(fname.is_file()):
		# 		print fname

        #Attaching all the files in the directory
        for name in files:
			print(name)
			filePath = path + name
			attachment = open(filePath, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			part.add_header('Content-Disposition', "attachment; filename= %s" % name)
			msg.attach(part)
        #send the mail
        failed_rcpts = server.sendmail(my_address, email, msg.as_string())
        del msg
        # failed receipt will be printed here
        print failed_rcpts

    server.quit()  # stopping SMTP server


if __name__ == '__main__':
    main()