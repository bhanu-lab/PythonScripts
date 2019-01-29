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
import logging


'''
Author: @blackram
Contributer: R@jesh
A simple python script to send email notifications for multiple receipeints based on the
SMPT lib available in python.

***requirements***
need to install email package for this script
'''

# Setting up logger

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        logger.info("Message being sent is : "+message)

        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = "Email Notification Test "+str(datetime.date.today())
        msg.attach(MIMEText(message, 'plain'))

        part = MIMEBase('application', "octet-stream")

        # adding attachement to the mail message
        # param_length = sys.argv[0]
        attachment = True

        #Todo - Take Command Line Argument to send files - may be path to files

        # attaching only if file name mentioned in parameter
        if attachment:
			path = 'resources/EMailAttachments/'
			files = os.listdir(path)
			#Attaching all the files in the directory
			for name in files:
				print(name)
				filePath = path + name
				attachment = open(filePath, "rb")
				part = MIMEBase('application', 'octet-stream')
				part.set_payload((attachment).read())
				part.add_header('Content-Disposition', "attachment; filename= %s" % name)
				msg.attach(part)
        # send the mail
        failed_rcpts = server.sendmail(my_address, email, msg.as_string())
        del msg
        # failed receipt will be printed here
        logger.info("failed receipeints are "+ failed_rcpts)

    server.quit()  # stopping SMTP server


if __name__ == '__main__':
    main()
