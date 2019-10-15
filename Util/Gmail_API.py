import smtplib
import sys
sys.path.append("../")
from Settings.Gmail_Settings import gmail_password,gmail_user



def send_email(Receiver_Email, subject, html):
    sent_from = gmail_user
    to = [Receiver_Email]
    subject = subject
    email_text = html

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')
