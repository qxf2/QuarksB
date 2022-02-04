"""
Qxf2's Skype sender helper:
It helps to send messages on Skype channel using Qxf2's Skype Sender Service
"""
import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf as conf

class SkypeHelper():
    "Skype helper class to send messages on Skype channel"
    def __init__(self):
        "Constructor"

    def post_message_on_skype(self, message):
        "Post message on the Skype channel"
        try:
            headers = {'Content-Type': 'application/json'}
            payload = {
                "msg" : message,
                "channel": conf.CHANNEL_ID,
                "API_KEY": conf.API_KEY
                }
            response = requests.post(url = conf.SKYPE_SENDER_ENDPOINT,
                                    json = payload, headers=headers)
        except Exception as err:
            raise Exception(f'Hitting following issue while posting message to Skype channel: \n {err}')
        return response.status_code