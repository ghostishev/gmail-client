import os
from requests import get, HTTPError
from gmail_viewer.settings import GOOGLE_MESSAGE_API_URL
import logging


def get_message_by_id(access_token, message_id):
    # type: (str, str) -> str
    """
    Returns short version of email content by message_id

    :param access_token: google access token
    :param message_id: gmail message id
    :return: snippet
    """
    url = os.path.join(GOOGLE_MESSAGE_API_URL, message_id)
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    snippet = ''
    try:
        response = get(url, headers=header)

        if response.status_code == 200:
            snippet = response.json().get('snippet', '')
        else:
            logging.error('Gmail API fail with error {}: {}'.format(response.status_code, response.reason))
    except HTTPError as e:
        logging.exception(e)
    return snippet


def get_message_list(access_token, recent_messages_list=None, next_page_token=None):
    # type: (str, list) -> list
    """
    Returns recent 100 messages from GMail

    :param next_page_token: nextPageToken from previous GMail API request (needs for recursion)
    :param recent_messages_list: list with message IDs from previous GMail API request (needs for recursion)
    :param access_token: google access token
    :return: list of 100 recent messages
    """
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    if recent_messages_list is None:
        recent_messages_list = []
    try:
        params = {'pageToken': next_page_token} if next_page_token else None
        response = get(GOOGLE_MESSAGE_API_URL, headers=header, params=params)
        if response.status_code == 200:
            parsed_response = response.json()
            message_list = parsed_response.get('messages', [])
            message_ids_list = [x['id'] for x in message_list]
            recent_messages_list.extend(message_ids_list)
            if len(recent_messages_list) < 100 and 'nextPageToken' in parsed_response:
                get_message_list(access_token, recent_messages_list, parsed_response['nextPageToken'])
        else:
            logging.error('Gmail API fail with error {}: {}'.format(response.status_code, response.reason))
    except HTTPError as e:
        logging.exception(e)

    return recent_messages_list[:100]
