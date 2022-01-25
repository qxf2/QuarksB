"""
Test to verify that message is sent to Skype channel and able to see the message received in the SQS queue
"""
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
from helpers import send_skype_message
from components import check_messages_SQS 

if __name__ == "__main__":
    send_skype_message.send_skype_message()
    sqsmessage_obj = check_messages_SQS.Sqsmessage()
    messages = sqsmessage_obj.get_messages_from_queue('')
    print("The message is ", str(messages['Messages'][0]['Body']))

    



