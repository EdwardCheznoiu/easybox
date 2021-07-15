import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def sendMail(imgFileName):
    
    email_user = 'easybox12341@gmail.com'
    email_sender = 'easybox12341@gmail.com'
    email_pass = 'parolasupersecreta'
    email_subj = 'Comanda [FIRMA]'
    
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_sender
    msg['Subj'] = email_subj
    
    body = MIMEText("Buna ziua \n Comanda dumneavoastra a ajuns in easybox. \n Puteti ridica coletul chiar acum. \n Multumim.")
    msg.attach(body)
    attachment = open(imgFileName, 'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+imgFileName)
    msg.attach(part)
    text = msg.as_string()
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_pass) 
    server.sendmail(email_user, email_sender, text)
    server.quit()

 