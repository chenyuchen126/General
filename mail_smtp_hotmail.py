import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(send_from, send_to, subject, text, files=None, host="127.0.0.1", port=587):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(host=host, port=port)
    smtp.starttls()
    smtp.login(send_from, 'aaxxcc') # 改密碼
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

my_email = "xxxx@hotmail.com"
receivers = ['xxx@xxx.com;sxxx@xxxx.com;xxx@xxx.com']
file = [r'D:\code\ABC.txt']
subject ="TEST sent 0905"
msg = "ABC"
send_mail(my_email, receivers, subject, msg, files=file, host="smtp-mail.outlook.com", port=587)