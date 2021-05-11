from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

import os
import pickle

myEmail = 'petergelgor7@gmail.com'
GmailScopes = ['https://mail.google.com/']


def gmailAuthenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret_file.json', GmailScopes)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# adds an attachment (specified by its filename) to a premade message object
# not gonna lie i directly copied and pasted this function, so i don't entirely
# know what's going on here
def addAttachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


# returns a message object
def makeMessage(to, subject, body, attachments=[]):
    # no attachments
    if (not attachments):
        message = MIMEText(body)
        message['to'] = to
        message['from'] = myEmail
        message['subject'] = subject

    # attachments incoming!
    else:
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = myEmail
        message['subject'] = subject
        message.attach(MIMEText(body))
        for file in attachments:
            addAttachment(message, file)

    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


# u can guess what this does
def sendMessage(service, to, subject, body, attachments=[]):
    return service.users().messages().send(
        userId='me',
        body=makeMessage(to, subject, body, attachments)
    ).execute()
