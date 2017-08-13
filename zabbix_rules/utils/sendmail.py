# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
import smtplib

mail_server="smtp.qq.com"
user_from="xxxx"
user_pass="xxxx"


def mail_send(subject,user_to,content):
    try:
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = user_from
        msg['To'] = ",".join(user_to)
        msg['Subject'] = subject
        server = smtplib.SMTP(mail_server, 25)
        server.login(user_from, user_pass)
        server.sendmail(user_from, user_to, msg.as_string())
        server.quit()
    except Exception as e:
        print e.message

def send_mail(mail_dict):
    if int(mail_dict["status"]) == 0:
        subject = "[Recovery][%s] %s" % (mail_dict['level'], mail_dict["trigger_name"])
    else:
        subject = "[Problem][%s] %s" % (mail_dict['level'], mail_dict["trigger_name"])
    user_to = mail_dict["to_user"]
    content = mail_dict["content"]
    mail_send(subject,user_to,content)