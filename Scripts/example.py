'''
Author: Jack M. Clary

Adapted from: https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ 
'''


from mq import *
import sys, time, csv
import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText



while True:

    
    #Instantiates MQ object to gain data from MQ-8 sensor
    
    try:
        print("Press CTRL+C to abort.")

        mq = MQ();
        while True:
            perc = mq.MQPercentage()
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")
            sys.stdout.write("LPG: %g ppm, CO: %g ppm" % (perc["GAS_LPG"], perc["CO"]))

            
            #Creates csv file "data.csv" once, and then writes 
            #gas data from MQ-8 sensor and 
            #time data from the datetime module
        
            try:
                with open('data.csv', 'a', newline='') as csvfile:
                    csvData = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    dateString = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
                    csvData.writerow([dateString, float(perc["GAS_LPG"]), float(perc["CO"])])

            except:
                print("\n CVS failed to be written to.")
            sys.stdout.flush()
            time.sleep(0.1)

    except:
        print("\nAbort by user")

    
    # Emails the created "data.csv" file 
       
    try:
        emailfrom = "themrclary@gmail.com"
        emailto = "jaclary@davidson.edu"
        fileToSend = "data.csv"
        username = "themrclary"
        password = "ZxAxqqzOP1!"

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "DIG333 Final Project Data"
        #msg.preamble = "help I cannot send an attachment to save my life"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()       
        print("\nEmail succesfully sent.") 
    except:
        print("\n CVS failed to send.")