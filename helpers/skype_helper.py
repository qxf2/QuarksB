"""
Helper module for Skype
"""
import os
import sys
import requests

# add project root to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf import skype_conf

def post_message_on_skype(message):
    "Posts a predefined message on the set Skype channel"
   
    headers = {'Content-Type': 'application/json'}
    payload = {"msg" : message,
                "channel": os.environ['CHANNEL_ID'],
                "API_KEY": os.environ['API_KEY']}

    response = requests.post(url=skype_conf.SKYPE_SENDER_ENDPOINT,json=payload, headers=headers)
       
    return response