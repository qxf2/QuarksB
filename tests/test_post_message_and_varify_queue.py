"""
Post message to skype channel through Api Endpoint using API key.
Verify the message on staging-newsletter-generator sqs queue.
"""

import requests
import os
import requests
import json
import boto3
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.credentials as credentials

def send_message():
    "post request to send a message"
    headers = {'Content-Type': 'application/json'}    
    body = {'API_KEY' : credentials.API_KEY,
    'msg' : 'https://test-example.com',
    'channel' : credentials.CHANNEL }
    json_data = json.dumps(body)
    response = requests.post(credentials.BASE_URL, headers = headers, data = json_data)
    if response.status_code == 200:
        print("message posted to test channel")
    else:   
        print("Failed to post message to test channel")



def verify_message():
    "verify message from sqs queue"     
    sqs_client =  boto3.client('sqs')
    queue = boto3.resource('sqs').get_queue_by_name(QueueName=credentials.QUEUE_URL)
    messages = sqs_client.receive_message(QueueUrl=queue.url, AttributeNames=['All'], MaxNumberOfMessages=2,MessageAttributeNames=['All'], WaitTimeSeconds=20)
    
    if 'Messages' in messages:
        for message in messages['Messages']:
            print(message['Body'])
    else:
        print("No messages to verify")


if __name__ == '__main__':
    send_message()
    verify_message()