import imaplib
from email.header import decode_header
import base64
import re
from datetime import datetime
from bs4 import BeautifulSoup
import asyncio
import quopri


def connection(mail, mail_pass, imap_server, imap_port):
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)

    sts, res = imap.login(mail, mail_pass)
    if sts == "OK":
        return imap
    else:
        return False


def encode_att_names(str_pl):
    enode_name = re.findall("\=\?.*?\?\=", str_pl)
    if len(enode_name) == 1:
        encoding = decode_header(enode_name[0])[0][1]
        decode_name = decode_header(enode_name[0])[0][0]
        decode_name = decode_name.decode(encoding)
        str_pl = str_pl.replace(enode_name[0], decode_name)
    if len(enode_name) > 1:
        nm = ""
        for part in enode_name:
            encoding = decode_header(part)[0][1]
            decode_name = decode_header(part)[0][0]
            decode_name = decode_name.decode(encoding)
            nm += decode_name
        str_pl = str_pl.replace(enode_name[0], nm)
        for c, i in enumerate(enode_name):
            if c > 0:
                str_pl = str_pl.replace(enode_name[c], "").replace('"', "").rstrip()
    return str_pl


def get_attachments(msg):
    attachments = list()
    for part in msg.walk():
        if (
            part["Content-Type"]
            and "name" in part["Content-Type"]
            and part.get_content_disposition() == "attachment"
        ):
            str_pl = part["Content-Type"]
            str_pl = encode_att_names(str_pl)
            attachments.append(str_pl)
    return attachments


def date_parse(msg_date):
    if not msg_date:
        return datetime.now()
    else:
        dt_obj = "".join(str(msg_date[:6]))
        dt_obj = dt_obj.strip("'(),")
        dt_obj = datetime.strptime(dt_obj, "%Y, %m, %d, %H, %M, %S")
        return dt_obj


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


async def send_document(document, filename, caption=None, prv=None, rpl=None):
    print('SEND doc')


def get_letter_text_from_html(body):
    body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("div")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text.replace("\xa0", " ")
    except (Exception) as exp:
        print("text ftom html err ", exp)
        return False


def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()


def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part
            count += 1
            return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")


def send_attach(msg, msg_subj, repl):
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            filename = from_subj_decode(filename)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                send_document(
                    part.get_payload(decode=True), filename, caption=msg_subj, rpl=repl
                )
            )


def post_construct(msg_subj, msg_from, msg_email, letter_text, attachments):
    smile_letter = '\U0001F4E8'
    smile_attachments = '\U0001F4CE'

    att_txt = "\n".join(attachments)
    postparts = [
        f"<b>",
        str(msg_subj),
        "</b>\n\n",
        "<pre>",
        str(msg_from),
        "\n",
        msg_email,
        "</pre>\n\n",
        letter_text,
        "\n\n",
        f"<i> вложения: </i>\n",
        str(len(attachments)),
        "\n\n",
        att_txt,
    ]
    txt = "".join(postparts)

    return txt
