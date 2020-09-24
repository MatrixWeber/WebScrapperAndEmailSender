from string import Template
# import the smtplib module. It should be included in Python by default
import smtplib
import os
# set up the SMTP server
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from gmail_connect_and_get_labels import getCredits, get_sent_label_objects, get_messages_object, list_messages, get_message
import base64
from googleapiclient.errors import HttpError
from gmail_read_drafts import list_drafts, get_drafts_object, get_draft_message, delete_draft_message
from email.mime.application import MIMEApplication


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()
    return file_content


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split('/')[0])
            emails.append(a_contact.split('/')[1])
    return names, emails


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_template):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    msg = MIMEMultipart('alternative')

    # add in the actual person name to the message template
    messageT = message_template.substitute(PERSON_NAME=name.title())

    # setup the parameters of the message
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(messageT, 'plain'))

    attachmentFile = './qr-code.png'
    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        message = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        message = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        message = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        message = MIMEBase(main_type, sub_type)
        message.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    message.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(message)

    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


names, emails = get_contacts('emails.txt')  # read contacts
service = getCredits()
#sent = get_sent_label_objects(service, 'me')
# print(sent)
# drafts_list = list_drafts(service, 'me')
drafts = get_drafts_object(service, 'me')
# draft_id = drafts_list['drafts'][0]['id']
# special_draft = get_draft_message(service, 'me', draft_id)
# for name, email in zip(names, emails):
#     headers = special_draft['message']['payload']['headers']
#     headers.insert(7, {'name': 'To', 'value': email.replace('\n', '')})
#     drafts.update(userId='me', id=draft_id,
#                   body={'raw': base64.urlsafe_b64encode(special_draft['message'].as_string().encode()).decode()}).execute()
messages_list = list_messages(service, 'me')
messages = get_messages_object(service, 'me')
for message in messages_list['messages']:
    msg_id = message['id']
    msg = get_message(service, 'me', msg_id)
    if('Kundenzufriedenheit ist mir nämlich sehr wichtig' not in msg['snippet']):
        continue
    for name, email in zip(names, emails):
        headers = msg['payload']['headers']
        headers.insert(7, {'name': 'To', 'value': email.replace('\n', '')})
        drafts.create(userId='me', body=msg).execute()
        messages.send(userId='me', body=msg).execute()
    break
# content_type = headers[7]
# special_draft = get_draft_message(service, 'me', draft['id'])
# message = special_draft['message']
    # headers.append(content_type)
print(message['snippet'])
# if 'Automatisieren' in message['payload']['headers'][3]['value'] or 'Projekt' in message['payload']['headers'][3]['value']:
# continue
#delete_draft_message(service, 'me', draft['id'])
message = read_file('email_message.txt')
# For each contact, send the email:
for name, email in zip(names, emails):
    msg = create_message('software@alexander-weber.com', email,
                         "Automatisieren Sie Ihren Computer", Template(message))
    send_message(service, 'me', msg)

    del msg
