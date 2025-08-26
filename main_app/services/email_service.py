import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

import os

# EMAIL_ADDRESS = "the.business.trackers@gmail.com"
# EMAIL_PASSWORD = '8usinessTracker'
EMAIL_ADDRESS = "the.business.trackers@gmail.com"
EMAIL_PASSWORD = '8usinessTracker'

# Email content
# msg = MIMEMultipart()
# msg["From"] = "the.business.trackers@gmail.com"
# msg["To"] = "abdulla4433@gmail.com"
# msg["Subject"] = "Hello from Python"

# body = "This is a test email."
# msg.attach(MIMEText(body, "plain"))

# Send email via Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("the.business.trackers@gmail.com", "8usinessTracker")
    server.sendmail(msg["From"], msg["To"], msg.as_string())

# email_sender = 'the.business.trackers@gmail.com'
# email_receiver = 'mahmoodish873@gmail.com'
# subject = ('SUBJECT: ')
# message = ('MESSAGE: ')

# text = f'Subject: {subject}\n\n{message}'

with smtplib.SMTP('smto.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)