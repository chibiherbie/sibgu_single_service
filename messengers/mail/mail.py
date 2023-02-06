import utils
import configparser
import email
from email.header import decode_header
import base64
import sys
import time
import asyncio
import traceback


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("../config.ini")

ENCODING = "utf-8"


def start_mail():
    imap = utils.connection(config['Mail']['mail_pass'],
                            config['Mail']['mail'],
                            config['Mail']['imap_server'])
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

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                reply_id = loop.run_until_complete(
                    utils.send_message(post_text, config.chat_id)
                )
                if config.send_attach:
                    utils.send_attach(msg, msg_subj, reply_id)
        imap.logout()
    else:
        imap.logout()
        sys.exit()


if __name__ == "__main__":
    try:
        start_mail()
    except (Exception) as exp:
        text = str("ошибка: " + str(exp))
        print(traceback.format_exc())

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete()
