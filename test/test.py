import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from subprocess import Popen, PIPE

print("==============================")
print(datetime.datetime.now())


response = requests.get("https://sneakerresellcalculator.com/background_process?proglang=https%3A%2F%2Fstockx.com%2Fair-jordan-1-retro-high-court-purple-gs&tax=0.07")
print(response.text)

me = 'sneakerresellcalculator@gmail.com'
you = 'sneakerresellcalculator@gmail.com'
msg = MIMEText(response.text)

msg['Subject'] = "Sneaker Calculator Result"
msg['From'] = me
msg['To'] = you
p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
p.communicate(msg.as_string())


