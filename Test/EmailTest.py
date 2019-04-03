import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
'''
Author: R@jesh
This script is to test sending a mail to single recipient to understand SMTP and MIMEMultipart and their functionallities
hard code values used for sake of ease
***requirements***
need to install email package for this script
'''
#Give from address 
fromaddr = "mail@domain.com"
#Give to address 
toaddr = ["mail@domain.com", "mail@domain.com"]
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ', '.join(toaddr)
msg['Subject'] = "SUBJECT OF THE MAIL"
body = "YOUR MESSAGE HERE"
msg.attach(MIMEText(body, 'plain'))

#gmail SMTP with port 587
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

#Logging into server with MailID and Password
server.login(fromaddr, "Password")
text = msg.as_string()

#Sending Mail with Subject and Body
server.sendmail(fromaddr, toaddr, text)
#Connection End
server.quit()
