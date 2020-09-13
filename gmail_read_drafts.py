from gmail_connect_and_get_labels import getCredits
import base64
from googleapiclient.errors import HttpError


def get_drafts_object(service, user_id):
    try:
        drafts = service.users().drafts()
        return drafts
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_draft_message(service, user_id, id):
    try:
        drafts = (service.users().drafts().get(
            userId=user_id, id=id).execute())
        return drafts
    except HttpError as error:
        print('An error occurred: %s' % error)


def list_drafts(service, user_id):
    try:
        drafts = (service.users().drafts().list(
            userId=user_id, maxResults=5).execute())
        return drafts
    except HttpError as error:
        print('An error occurred: %s' % error)


def delete_draft_message(service, user_id, id):
    try:
        message = (service.users().drafts().delete(
            userId=user_id, id=id).execute())
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)
