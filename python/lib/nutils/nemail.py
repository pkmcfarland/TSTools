#!/usr/bin/env python3

import smtplib
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import sys

__all__ = ["send_email"]

def _prepare_attach(path):
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == 'text':
        with open(path) as fp:
            # Note: we should handle calculating the charset
            att = MIMEText(fp.read(), _subtype=subtype)

    elif maintype == 'image':
        with open(path, 'rb') as fp:
            att = MIMEImage(fp.read(), _subtype=subtype)

    elif maintype == 'audio':
        with open(path, 'rb') as fp:
            att = MIMEAudio(fp.read(), _subtype=subtype)

    else:
        with open(path, "rb") as fp:
            att = MIMEBase(maintype, subtype)
            att.set_payload(fp.read())
        encoders.encode_base64(att)

    att.add_header("Content-Disposition", "attachment", filename=path)
    
    return att


def send_email(sender, recipient, subject="", body="", attachL=[]):

    msg = MIMEMultipart()
    
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # add message body
    msg.attach(MIMEText(body, "plain"))

    # attach files
    for tmp in attachL:
        att = _prepare_attach(tmp)
        msg.attach(att)

    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()

