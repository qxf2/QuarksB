"""
Test to send a message to skype channel using "/send-message" endpoint of Qxf2's Skype sender

"""
import json
import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf as creds


class Skype():
    "Skype helper class and associated methods"
    def __init__(self):
        "Constructor"

    def skype_send_message(self):   
        "Send the given message" 
        try:            
            data = json.dumps({"msg": creds.SKYPE_MESSAGE, "channel": creds.SKYPE_CHANNEL_ID, "API_KEY": creds.API_KEY})    
            headers = {'Content-Type': 'application/json'}  
            response = requests.post(creds.SKYPE_ENDPOINT, headers=headers, data=data)    
        except Exception as exception:
            print(f'\n Exception: {exception}')
            raise Exception('\nUnable to post message to Skype channel!') from exception

        return response.json()
            