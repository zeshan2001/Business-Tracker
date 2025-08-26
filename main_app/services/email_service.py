import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

import os

# EMAIL_ADDRESS = "the.business.trackers@gmail.com"
# EMAIL_PASSWORD = '8usinessTracker'
EMAIL_ADDRESS = "the.business.trackers@gmail.com"
EMAIL_PASSWORD = '8usinessTracker'


email_sender = 'the.business.trackers@gmail.com'
email_receiver = 'mahmoodish873@gmail.com'


with smtplib.SMTP('smto.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = ('death')
    body = ('Body text ')

    msg = f'Subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDRESS, email_receiver,msg )