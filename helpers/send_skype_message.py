"""
Send skype message to specified channel
"""
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
from conf import skype_config as config

def send_skype_message():

    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {}
    data["msg"] = config.MESSAGE
    data["channel"] = config.SKYPE_CHANNEL
    data["API_KEY"] = config.API_KEY

    response = requests.post(config.SKYPE_URL, headers=headers, data=json.dumps(data))

    print(response.status_code)


if __name__ == '__main__':
    send_skype_message()    