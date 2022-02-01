"""
Skype Helper Class which produces the messages for SQS
"""
import asyncio
import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_channel_conf as skc

class Skype():
    "Skype helper class and associated methods"
    def __init__(self):
        "Constructor"

    async def post_message_on_skype(self):
        "Posts a predefined message on the set Skype channel"
        try:
            headers = {
                'Content-Type': 'application/json'
                }
            payload = {
                "msg" : skc.MESSAGE,
                "channel": os.environ['CHANNEL_ID'],
                "API_KEY": os.environ['SKYPE_API_KEY']
                }
            response = requests.post(url = skc.SKYPE_SENDER_ENDPOINT,
                                    json = payload, headers=headers)
        except Exception as exception:
            print(f'\n Exception: {exception}')
            raise Exception('\nUnable to post message to Skype channel!') from exception
        return response.json()