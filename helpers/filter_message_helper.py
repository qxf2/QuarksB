"""
Helper module for filter message functionality
"""
import os
import sys
import json
import pytest
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Declaring class Style
class Style():
    """
    Declaring Style class
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def get_dict(body_string):
    """
    Generates dict from message body
    :param string
    :return dict object
    """
    body_string = json.dumps(body_string)
    body_string = body_string.replace("'", "\"")
    body_string = json.loads(body_string)
    message_body_obj = json.loads(body_string)

    return message_body_obj

def get_message_body(message):
    """
    This method will return message body
    """
    msg_body = ""
    if 'Messages' in message:
        for message in message['Messages']:
            if 'Body' in message.keys():
                message_body_obj = get_dict(message['Body'])
                if 'Message' in message_body_obj.keys():
                    msg_body = get_dict(message_body_obj['Message'])
                else:
                    print("Message key is not present in the Message Body")
                    sys.exit()
            else:
                print("Message does not contain Body")
                sys.exit()

    else:
        print("No messages are retrieved")
        with pytest.raises(SystemExit):
            sys.exit()

    return msg_body


def filter_message(message):
    """
    Fetches message from sqs queue
    """
    message_body = get_message_body(message)

    if message_body is not None:
        if "msg" in message_body:
            return message_body['msg']
        else:
            print(f'Message body does not contain message key')
    else:
        print(f'Message body is none')
    
    return message_body

