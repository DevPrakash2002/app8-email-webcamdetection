import smtplib
import imghdr
from email.message import EmailMessage

sender = "dev.tiwary5821@gmail.com"
password = "iwvjpnohgxksfhvf"
reciever = "dev.tiwary0014@gmail.com"
def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New Customer showed up"
    email_message.set_content('Hey ,We just saw new customer')

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, reciever, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email("images/Planet9_3840x2160.jpg")