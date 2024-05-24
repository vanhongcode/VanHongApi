import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests
def cr_api():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(40))
api = f'VH-{cr_api()}'
def send_api():
    sender_email = "vanhongapi@gmail.com"
    sender_password = "lqxv vjhk kjjz zopn"
    receiver_email = "2fa.remix@gmail.com"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "VanHongApi"

    # Nội dung email
    body = f"""<h2>Xin chào {receiver_email},</h2><br>
    <h4>Chúng tôi là VanHongApi.</h4><br>
    <h4>Mã API cho VanHongApi của bạn là </h4><br>
    <span style="background-color:green; font-size:35px;">{api}</span><br>
    <h4>Hãy Public api này tại http://vanhong.mywebcommunity.org/ để dùng được api</h4><br>
    <h4>Đừng chia sẻ API này cho bất kỳ ai.</h4><br>
    <h3>From VanHongApi</h3><br>
    <h2>TRÂN TRỌNG ./.</H2>"""
    message.attach(MIMEText(body, "html"))
    image_url = "https://media.discordapp.net/attachments/1228716682059710615/1243407569847058432/learn.png?ex=66515d0a&is=66500b8a&hm=a38f00ffb747930c08da6bed2bf00bd0cbc4f4a3c23ffa5613114776a13dd6cd&=&format=webp&quality=lossless"
    image_data = requests.get(image_url).content
    image = MIMEImage(image_data)
    image.add_header("Content-Disposition", "attachment", filename="learn.png") 
    message.attach(image)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print("[VANHONGAPI] Đã gửi api qua email của bạn")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
send_api()
