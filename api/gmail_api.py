import os
from requests import get, HTTPError
from gmail_viewer.settings import GOOGLE_MESSAGE_API_URL
import logging


def get_message_by_id(access_token, message_id):
    # type: (str, str) -> str
    """
    Return short version of email content by message_id

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
