import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailBot:
    def __init__(self, fromaddr = "andreitaganov25@gmail.com",pwd = ""):
        self.msg = MIMEMultipart()
        self.msg['From'] = fromaddr
        self.pwd = pwd

    def send_email(self,to='',body="testtest",subject = 'None'):
        self.msg['To'] = to
        self.body = body
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.msg['From'], self.pwd)
        text = self.msg.as_string()
        server.sendmail(self.msg['From'], self.msg['To'], text)
        server.quit()

    def send_email_with_attach(self,to='ervik993@gmail.com',body="testtest",subject = 'None',path_to_attachment=''):
        self.msg['To'] = to
        self.body = body
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body, 'plain'))
        self.filename = path_to_attachment
        attachment = open(self.filename, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % 'attachment.jpg')
        self.msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.msg['From'], self.pwd)
        text = self.msg.as_string()
        server.sendmail(self.msg['From'], self.msg['To'], text)
        server.quit()

        #http://naelshiab.com/tutorial-send-email-python/

#send_em = EmailBot()
#send_em.send_email(body='Привет, это провека моего бота',subject='hey')
#path = r'c:\Users\15764\Downloads\Telegram Desktop\photo_2018-03-01_23-04-36.jpg'
#send_em.send_email_with_attach(body='Привет, это новая провека моего бота',subject='Привет',path_to_attachment=path)