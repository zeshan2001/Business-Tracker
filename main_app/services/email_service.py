import smtplib

from email.message import EmailMessage
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

import os

# EMAIL_ADDRESS = "the.business.trackers@gmail.com"
# EMAIL_PASSWORD = '8usinessTracker'
EMAIL_ADDRESS = "the.business.trackers@gmail.com"
EMAIL_PASSWORD = '8usinessTracker'


business_email = 'the.business.trackers@gmail.com'
client_email = 'mahmoodish873@gmail.com'


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = ('death')
    body = ('Body text ')
    subjectauto = ("We Received Your Request")
    bodyauto = ("Thank you for reaching out to us. We have received your message and our team will contact you as soon as possible.")

    msg = f'Subject: {subject}\n\n{body}'
    msgauto = f'Subject: {subjectauto}\n\n{bodyauto}'
    smtp.sendmail(client_email, business_email,msg )
    smtp.sendmail(business_email, client_email,msgauto )