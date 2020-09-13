from string import Template
# import the smtplib module. It should be included in Python by default
import smtplib
# set up the SMTP server
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from gmail_connect_and_get_labels import getCredits
import base64
from googleapiclient.errors import HttpError
from gmail_read_drafts import list_drafts, get_drafts_object, get_draft_message, delete_draft_message


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
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
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


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    #message = message_template.substitute(PERSON_NAME=name.title())

    # setup the parameters of the message
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


names, emails = get_contacts('emails.txt')  # read contacts
service = getCredits()
drafts_list = list_drafts(service, 'me')
drafts = get_drafts_object(service, 'me')
draft_id = drafts_list['drafts'][0]['id']
message = get_draft_message(service, 'me', draft_id)
headers = message['message']['payload']['headers']
content_type = headers[5]
# for name, email in zip(names, emails):
#special_draft = get_draft_message(service, 'me', draft['id'])
#message = special_draft['message']
for name, email in zip(names, emails):
    headers[5] = {'name': 'To', 'value': email}
    headers.append(content_type)
    drafts.send(userId='me', body=message).execute()
# print(message['snippet'])
# if 'Automatisieren' in message['payload']['headers'][3]['value'] or 'Projekt' in message['payload']['headers'][3]['value']:
# continue
#delete_draft_message(service, 'me', draft['id'])
#message = read_file('email_message.txt')
# For each contact, send the email:
    msg = create_message('software@alexander-weber.com', email,
                         "Automatisieren Sie Ihren Computer", message)
    #send_message(service, 'me', msg)

    #del msg
