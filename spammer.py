import smtplib
import folium
import time
import mimetypes
import os
import random
from pyfiglet import Figlet
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender: str, password: str, recipient: str, subject=None, file_name=None, template=None,
               message=None):
    counter = 0

    # sender = 'email'
    # password = 'pass'

    # СОЗДАЕМ ОБЬЕКТ И УКАЗЫВАЕМ СЕРВЕР И ПОРТ
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(False)
    # ЗАПУСКАЕМ ШИФРОВАНИЯ ПО TLS
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject

        if message:
            msg.attach(MIMEText(message))

        if template:
            # ОТПРАВКА HTML ШАБЛОНА
            with open(template, encoding='utf-8') as f:
                template_o = f.read()
            msg.attach(MIMEText(template_o, "html"))

        if file_name:
            filename = os.path.basename(file_name)
            ftype, encoding = mimetypes.guess_type(file_name)
            file_type, subtype = ftype.split('/')

            with open(f'{file_name}', 'rb') as f:
                file = MIMEBase(file_type, subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)

        server.sendmail(sender, recipient, msg.as_string())

        return True

    except Exception as ex:
        return ex


def main():
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('E M A I L   S P A M M E R')
    print(f'\033[31m\033[1m{text}\033[0m')

    with open('emails.txt') as f:
        emails = f.readlines()

    sender = input("Input your email: ")
    password = input("Input your password: ")
    start = input("Input number start #: ")
    print()

    counter = 0
    for email in emails[start:]:
        recipient = email.strip()

        subject = 'Информация для патриотически настроенных'
        # subject = input('Input SUBJECT')
        message = f'Уважаемый гражданин Российской Федерации, прошу ознакомиться с информацией ниже ' \
                  f'и передать информацию своим коллегам. Спасибо.\n'
        # message = input('Input your MESSAGE: ')
        file_name = None
        # file_name = input('File name: ')
        template = 'Document.html'
        # template = input('Select your TEMPLATE: ')
        # recipient = input('Recipient EMAIL: ')
        counter += 1
        time.sleep(random.randint(1, 5))
        if send_email(sender=sender, password=password, recipient=recipient, subject=subject,
                      template=template, file_name=file_name, message=message):
            print(f'#{counter}  Message to \033[31m\033[1m{email}\033[0m sent successfully!')
        else:
            print(
                send_email(sender=sender, password=password, recipient=recipient, subject=subject, file_name=file_name,
                           message=message))
        if counter == 499:
            print('[INFO]   Sending stopped, LIMIT is EXHAUSTED. Please try again in a couple of hours.')
            break


if __name__ == "__main__":
    main()
