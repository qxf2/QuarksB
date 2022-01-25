"""
Exercise the /send-message endpoint of Skype sender
"""


import os
import sys
import requests
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import channel_conf as ch_cred
from conf import sqs_conf as sqs_cred


API_KEY = ch_cred.API_KEY
BASE_URL = sqs_cred.BASE_URL
MESSAGE = ch_cred.MESSAGE
CHANNEL_ID = ch_cred.CHANNEL_ID


def test_send_message():
    "Send the message"
    
    headers = {'Content-Type': 'application/json'}

    
    if not ch_cred.API_KEY:
        print('No API key')
        return False
    if not MESSAGE or not CHANNEL_ID:
        print("No Message and Channel ID specified")
        return False   
        
    post_data = {"msg":MESSAGE, "API_KEY":API_KEY, "channel":CHANNEL_ID}
    json_data = json.dumps(post_data)
    response = requests.post(BASE_URL, headers=headers , data=json_data)
    print(response)
    return True

#---START OF SCRIPT
if __name__ == '__main__':
    
    test_send_message()
    