import smtplib
#this is to check .hpg or.png for images
import mimetypes
#this is an email class will create an email obj instanse
from email.message import EmailMessage
SENDER = "claudenogga1@gmail.com"
password = "kghjpgmhosqamgbx"
def send_email(image_path):
    #creating an obj (this obj is the email contents)
    email_message = EmailMessage()
    #sub of the email
    email_message["subject"] = "New customer showed up!"
    #body of mail
    email_message.set_content("this customer showed up")

    #adding attachment
    #getting and storing img
    with open(image_path, "rb") as file:
        content = file.read()

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "application/octet-stream"
    maintype, subtype = mime_type.split("/")


    #creating the attachment
    #content is the attachment, maintype - type of file,
    # subtype - png or jpg(we import imghdr for this)
    #none arg is required
    email_message.add_attachment(
        content,
        maintype=maintype,
        subtype=subtype,
        filename=image_path
    )
    #sending out email by creating server (SMTP - the server)
    #the "smtp.gmail..." is the host, 587 is the code to use this
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    #starts the gmail server
    gmail.ehlo()
    gmail.starttls()
    #allowss it to login in from the mail you choose
    gmail.login(SENDER, password)
    #finally sends mail 2nd arg is the recipient
    gmail.sendmail(SENDER,SENDER,email_message.as_string())
    #to quit SMTP server object
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path ="images/85.png" )

