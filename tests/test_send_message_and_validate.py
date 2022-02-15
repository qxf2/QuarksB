"""
Test to send message on skype using skype-sender and validation if the message was recieved by the newsletter-staging-SQS
"""
import json
import os
import requests
import boto3
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.skype_conf as conf
import conf.aws_conf as awconf
from helpers import sqs_helper

skype_sender = conf.skype_sender
API_TOKEN = conf.API_TOKEN
test_channel_id = conf.channel_id
queue_url = awconf.queue_url


def post_message():
    "Send message using skype sender"

    msg = "https://www.test_newsletter.com"
    channel_id = test_channel_id
    url = skype_sender
    data = {'API_KEY' : API_TOKEN,
        'msg' : msg,
        'channel' : channel_id}
    response = requests.post(url, json=data)
    print(f'Received {response.json()} for {msg}') 

def receive_message():
    "Recieve message from sqs"

    sqs_obj= sqs_helper.Sqs()
    messages = sqs_obj.get_message()                   
    print(messages)


if __name__=='__main__':
    post_message()
    receive_message()


