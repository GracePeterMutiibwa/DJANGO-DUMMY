import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart


class MessengerUtils:
    # sender
    senderEmail = "mariahillsite@gmail.com"   

    def resetCoreEngine(self, receiverEmail, messageToSend, emailSubject):
        # Create an instance of MIMEMultipart
        msg = MIMEMultipart()

        # Add the subject to the message
        msg['From'] = self.senderEmail
        
        msg['To'] = receiverEmail
        
        msg['Subject'] = emailSubject

        # Attach the email body as plain text
        msg.attach(MIMEText(messageToSend, 'plain'))
    
        # create server instance
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)

        # start tls
        mailServer.starttls()

        # login
        mailServer.login(self.senderEmail, "gvbqtwcokrnqooqp")

        # send the email message
        mailServer.sendmail(from_addr=self.senderEmail, to_addrs=receiverEmail, msg=msg.as_string())
    
        return
