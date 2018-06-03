import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from email.mime.base import MIMEBase
import os.path as op
import sys


'''
Author: @blackram
A simple python script to send email notifications for multiple receipeints based on the
SMPT lib available in python. 

***requirements***
need to install email package for this script
'''


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


# function to get attachment to the mail
def get_attachment(file_name):
    return open(file_name, mode='r').read()


# main function
def main():

    my_address, my_password = get_my_account_info('resources/from_mail')  # get my account details
    names, emails = get_contacts('resources/my_contacts.txt')  # read contacts
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
        print message

        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = "3GRM Call Drill Reminder 1"
        msg.attach(MIMEText(message, 'plain'))

        part = MIMEBase('application', "octet-stream")

        # adding attachement to the mail message
        param_length = len(sys.argv)

        # attaching only if file name mentioned in parameter
        if param_length > 0:
            part.set_payload(get_attachment(sys.argv[0]))
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(sys.argv[0])))
            msg.attach(part)

        # send the mail
        failed_rcpts = server.sendmail(my_address, email, msg.as_string())
        del msg
        # failed receipt will be printed here
        print failed_rcpts

    server.quit()  # stopping SMTP server


if __name__ == '__main__':
    main()
