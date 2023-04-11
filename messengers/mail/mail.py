import configparser
import email
import os
from email.header import decode_header
import sys
import asyncio
import traceback
from time import sleep

# Считываем учетные данные
config = configparser.ConfigParser()
config.read(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config.ini'))

ENCODING = "utf-8"
sys.path.insert(0, os.path.dirname(__file__))

# Тема письма при ответе
SUBJECT = "Ответ на вопрос от ректора"

def start_mail():
    while True:
        import utils

        imap = utils.connection(config['Mail']['mail'],
                                config['Mail']['mail_pass'],
                                config['Mail']['imap_server'],
                                config['Mail']['imap_port'],)
        if not imap:
            sys.exit()

        status, messages = imap.select("INBOX")  # папка входящие
        res, unseen_msg = imap.uid("search", "UNSEEN", "ALL")
        unseen_msg = unseen_msg[0].decode(ENCODING).split(" ")

        if unseen_msg[0]:
            for letter in unseen_msg:
                attachments = []
                res, msg = imap.uid("fetch", letter, "(RFC822)")
                if res == "OK":
                    msg = email.message_from_bytes(msg[0][1])
                    msg_date = utils.date_parse(email.utils.parsedate_tz(msg["Date"]))
                    msg_from = utils.from_subj_decode(msg["From"])
                    msg_subj = utils.from_subj_decode(msg["Subject"])
                    if msg["Message-ID"]:
                        msg_id = msg["Message-ID"].lstrip("<").rstrip(">")
                    else:
                        msg_id = msg["Received"]
                    if msg["Return-path"]:
                        msg_email = msg["Return-path"].lstrip("<").rstrip(">")
                    else:
                        msg_email = msg_from

                    if not msg_email:
                        encoding = decode_header(msg["From"])[0][1]  # не проверено
                        msg_email = (
                            decode_header(msg["From"])[1][0]
                            .decode(encoding)
                            .replace("<", "")
                            .replace(">", "")
                            .replace(" ", "")
                        )

                    letter_text = utils.get_letter_text(msg)
                    attachments = utils.get_attachments(msg)

                    post_text = utils.post_construct(
                        msg_subj, msg_from, msg_email, letter_text, attachments
                    )
                    if len(post_text) > 4000:
                        post_text = post_text[:4000]

                    from messengers.manage_data import send_data
                    try:
                        loop2 = asyncio.new_event_loop()
                        loop2.run_in_executor(send_data({'id': msg_email,
                                                         'username': msg_email,
                                                         'message': post_text,
                                                         'date': msg_date,
                                                         'messenger': 'email'}))
                    except Exception:
                        pass

                    # loop = asyncio.new_event_loop()
                    # asyncio.set_event_loop(loop)
                    #
                    # reply_id = loop.run_until_complete(
                    #     utils.send_message(post_text, )
                    # )
                    # if config.send_attach:
                    #     utils.send_attach(msg, msg_subj, reply_id)
            imap.logout()
        else:
            imap.logout()

        time = 120
        print('Почта: сон ', time, 'сек')
        sleep(time)


def send_email(email_to, message):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg["From"] = config['Mail']['mail']
    msg["To"] = email_to
    msg["Subject"] = SUBJECT  # тема письма

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP_SSL(config['Mail']['smtp_server'],
                          int(config['Mail']['smtp_port']))
    # server.starttls()
    server.login(config['Mail']['mail'], config['Mail']['mail_pass'])
    text = msg.as_string()
    server.sendmail(config['Mail']['mail'], email_to, text)
    server.quit()


if __name__ == "__main__":
    try:
        # check()
        send_email('bekkerrdm@gmail.com', 'Привет')
    except (Exception) as exp:
        text = str("ошибка: " + str(exp))
        print(traceback.format_exc())

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete()
