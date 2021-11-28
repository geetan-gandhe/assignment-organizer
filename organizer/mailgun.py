import smtplib
from email.mime.text import MIMEText

def send_message_mailgun(text, subject, recipient, sender, smtp_login, port, password):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['To'] = recipient
    msg['From'] = sender
    s = smtplib.SMTP(smtp_login, port)
    s.login(smtp_login, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()