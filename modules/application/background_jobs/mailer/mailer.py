import smtplib
from email.mime.text import MIMEText

def send_mail(subject,sender,recipient,html_path):
    with open(html_path, 'rb') as fp:
        msg = MIMEText(fp.read())

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    print(f"Hey look I'm sending emails")
    s = smtplib.SMTP('mail.nib-bahamas.com')
    s.sendmail(sender, [recipient], msg.as_string())
    s.quit()