from mailgun import send_message_mailgun

text = "your message"
subject = "subject of message"
recipient = "williamsgchenelle@gmail.com"
sender = "you@" + str(os.environ["MAILGUN_DOMAIN"])
smtp_login = str(os.environ["MAILGUN_SMTP_LOGIN"])
password = str(os.environ["MAILGUN_SMTP_PASSWORD"])
port = str(os.environ["MAILGUN_SMTP_PORT"])
send_message_mailgun(text, subject, recipient, sender, smtp_login, password, port)