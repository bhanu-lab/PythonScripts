import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

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

    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        message = message_template.substitute(PERSON_NAME=name.title())
        print message

        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = "Test Subject"
        msg.attach(MIMEText(message, 'plain'))

        # send the mail
        server.sendmail(my_address, email, msg.as_string())
        del msg

    server.quit()  # stopping SMTP server


if __name__ == '__main__':
    main()
