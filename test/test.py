import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from subprocess import Popen, PIPE

print("==============================")
print(datetime.datetime.now())


response = requests.get("https://sneakerresellcalculator.com/background_process?proglang=https%3A%2F%2Fstockx.com%2Fnike-air-fear-of-god-strap-light-bone&tax=0.07")
print(response.text)

me = 'sneakerresellcalculator@gmail.com'
you = 'sneakerresellcalculator@gmail.com'
if response.status_code == 200:
    print("Success!")
    msg = MIMEText('Daily test passed')

    msg['Subject'] = "Sneaker Calculator working properly!"
    msg['From'] = me
    msg['To'] = you
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
    p.communicate(msg.as_string())


