"""
Helper module for Skype
"""
import os
import requests

# add project root to sys path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.base_helper import BaseHelper
from conf import skype_conf as conf

class SkypeHelper(BaseHelper):
    """
    Skype Helper object
    """

    def post_message_on_skype(self, message, skype_url=None):
        "Posts a predefined message on the set Skype channel"
        try:
            if skype_url is None:
                skype_url = conf.SKYPE_SENDER_ENDPOINT
            headers = {'Content-Type': 'application/json'}
            payload = {"msg" : message,
                      "channel": os.environ['CHANNEL_ID'],
                      "API_KEY": os.environ['API_KEY']}

            response = requests.post(url=skype_url,
                                     json=payload, headers=headers)
            if response.status_code == 200:
                self.write(f'Successfully sent the Skype message - {message}')
            else:
                self.write(f'Failed to send Skype message', level='error')
        except Exception as err:
            raise Exception(f'Unable to post message to Skype channel, due to {err}')

        return response
