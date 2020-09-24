from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build, HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


def getCredits():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

    return service


def get_sent_label_objects(service, user_id):
    try:
        sent = service.users().labels().get(userId=user_id, id='SENT')
        return sent
    except HttpError as error:
        print('An error occurred: %s' % error)


def list_messages(service, user_id):
    try:
        msgs = (service.users().messages().list(
            userId=user_id, maxResults=5).execute())
        return msgs
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_messages_object(service, user_id):
    try:
        msgs = service.users().messages()
        return msgs
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_message(service, user_id, id):
    try:
        msg = (service.users().messages().get(
            userId=user_id, id=id).execute())
        return msg
    except HttpError as error:
        print('An error occurred: %s' % error)
