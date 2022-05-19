from pyfiglet import Figlet
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib
import time
import mimetypes
import os


def send_email(sender: str, password: str, recipient: str, template=None, subject=None, file_name=None, message=None):
    # СОЗДАЕМ ОБЬЕКТ И УКАЗЫВАЕМ СЕРВЕР И ПОРТ ДЛЯ GMAIL.COM
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # СОЗДАЕМ ОБЬЕКТ И УКАЗЫВАЕМ СЕРВЕР И ПОРТ ДЛЯ MAIL.RU
    # server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # СОЗДАЕМ ОБЬЕКТ И УКАЗЫВАЕМ СЕРВЕР И ПОРТ ДЛЯ YANDEX.RU
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    # server = smtplib.SMTP_SSL('smtp.rambler.ru', 465)
    # server = smtplib.SMTP('smtp.yandex.ru', 587)
    # server.set_debuglevel(False)
    # ЗАПУСКАЕМ ШИФРОВАНИЯ ПО TLS ТОЛЬКО ДЛЯ GMAIL.COM!!!
    # server.starttls()

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

    except:
        return False


def send_or_alert_emails(start, counter, sender, password, recipient, subject, template, file_name, message):
    if send_email(sender=sender, password=password, recipient=recipient, subject=subject,
                  template=template, file_name=file_name, message=message):
        print(
            f'\033[33m\033[1m\033[4m#{start}\033[0m  Message to \033[31m\033[1m{recipient}\033[0m sent successfully!')
        counter += 1
        time.sleep(random.randint(1, 3))
    else:
        print(f"\033[33m\033[1m\033[4m#{start}\033[0m \033[33m\033[1mNOT SENT, socket.gaierror!\033[0m")
        # counter_error += 1
        # if counter_error > 3:
        #     print(
        #         f'\n\033[31m\033[1m[ERROR]\033[0m Sending STOPPED! PROBLEM WITH SOCKET. Sent \033[31m\033[1m{counter}\033[0m letters.\n'
        #         f'\033[31m\033[1m[ERROR]\033[0m Please, try again after a while or change your email-address.\n')
        #     break

    if counter == 999:
        print(
            f'\n\033[32m\033[1m[INFO]\033[0m Sending stopped, LIMIT is EXHAUSTED.\n'
            f'Please try again in a couple of hours.\n'
            f'Sent \033[31m\033[1m{counter}\033[0m letters. Good work!\n')
        exit()
    return counter


def main():
    try:
        with open('emails.txt') as f:
            list_emails = f.read().split('\n')
            list_emails = set(list_emails)
            list_emails = list(list_emails)

    except FileNotFoundError:
        print(f"\n\033[31m\033[1m[ERROR]\033[0m PLease check if file \033[31m\033[4memails.txt\033[0m is exist")
        exit()

    sender = input('\033[32m\033[1m[ACTION]\033[0m Input your \033[31m\033[1memail\033[0m: ')
    password = input('\033[32m\033[1m[ACTION]\033[0m Input \033[31m\033[1mpassword\033[0m: ')

    try:
        start = int(input("\033[32m\033[1m[ACTION]\033[0m Input \033[31m\033[1mlist-number email-address\033[0m start"
                          " \033[31m\033[1m(0 or other number)\033[0m #: "))
    except ValueError:
        print(f"\n\033[31m\033[1m[ERROR]\033[0m Check your input, please!")
        exit()
    print("\033[31m\033[1m-\033[0m" * 100)
    print()

    counter = 0
    # counter_error = 0
    for email in list_emails[start:]:
        recipient = email.strip()

        subject = Subject
        message = None
        file_name = None
        template = 'template.html'

        send_or_alert_emails(start, counter, sender, password, recipient, subject, template, file_name,
                             message)
        start += 1


if __name__ == "__main__":
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('E M A I L    S P A M M E R')
    print(f'\033[31m\033[1m{text}\033[0m')
    print("\033[31m\033[1m-\033[0m" * 100)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31m\033[1m[ERROR]\033[0m PROGRAM STOPPED BY USER\n")
