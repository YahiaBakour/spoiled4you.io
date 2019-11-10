import smtplib
import sys
sys.path.append("../")
from Settings.Gmail_Settings import gmail_password,gmail_user
import yagmail



def send_email(Receiver_Email, subject, html):
    sent_from = gmail_user
    to = [Receiver_Email]
    subject = subject
    email_text = html

    try:
        yag = yagmail.SMTP(user=gmail_user,password=gmail_password)
        yag.send(
            to=to,
            subject=subject,
            contents=html, 
        )

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')

