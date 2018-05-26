import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

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
      MY_ADDRESS = ""
      MY_PASSWORD = ""
      with open(file_name, mode='r') as template_file:
            template_file_content = template_file.read()
      return Template(template_file_content)

# function to get my account details to send mail
def get_my_account_info(file_name):
      with open(file_name, mode='r') as my_details:
            for my_det in my_details:
                  MY_ADDRESS = my_det.split()[0]
                  MY_PASSWORD = my_det.split()[1]
      return MY_ADDRESS, MY_PASSWORD

# main function
def main():

      MY_ADDRESS, MY_PASSWORD = get_my_account_info('resources/from_mail.txt') # get my account details
      names, emails = get_contacts('resources/my_contacts.txt')  # read contacts
      message_template = get_message_template('resources/email_template.txt') # read template

      # using gmail smtp
      server = smtplib.SMTP(host='smtp.gmail.com', port='587')
      server.starttls()

      # Log into server
      server.login(MY_ADDRESS, MY_PASSWORD)

      for name, email in zip(names, emails):
            msg = MIMEMultipart()
            message = message_template.substitute(PERSON_NAME=name.title())
            print message

            msg['From'] = MY_ADDRESS
            msg['To'] = email
            msg['Subject'] = "Test Subject"
            msg.attach(MIMEText(message, 'plain'))

            # send the mail
            server.sendmail(msg.as_string())
            del msg

      server.quit()

if __name__ == '__main__':
    main()