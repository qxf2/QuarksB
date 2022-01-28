"""
A test to send a message to a specific skype channel and verify if the sqs queue has received the message.
Followed tutorials from here:https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
"""

import boto3
import requests
import os, json, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf.skype_config import channel, FirstName

def test_send_msg_testchannel():
    #send a message to skype channel "Test Qxf2Bot"
    API_KEY = os.environ.get('API_KEY')
    #FirstName = os.environ.get('FirstName')
    
    headers = {'Content-Type': 'application/json',}
	
    msg = "testingsqs"

    data = {"msg" : msg, "channel" : channel, "API_KEY" : API_KEY}

    data = json.dumps(data)
    response = requests.post('https://skype-sender.qxf2.com/send-message', headers=headers, data= data)
    
    print(response.status_code)

def test_received_msg():
    #verify if sqs queue received the message
    sqs = boto3.resource('sqs')

    sqs_client = boto3.client('sqs')
    
    queue_data = sqs.get_queue_by_name(QueueName='staging-newsletter-generator')
    url = queue_data.url
    print(queue_data.url)
    
    #response = queue_data.send_message(MessageBody='testingsqs')
    #print(response.get('MessageId'))

    result1 = queue_data.receive_messages(QueueUrl=url)
    print(result1) #this gives me empty []
    
    result2 = sqs_client.receive_message(QueueUrl=url, AttributeNames=['All'],MaxNumberOfMessages=2,MessageAttributeNames=['All'],WaitTimeSeconds=10)
    
    print(result2)
    #this gives me {'ResponseMetadata': {'RequestId': '.....', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '....', 'date': 'Fri, 28 Jan 2022 13:32:27 GMT', 'content-type': 'text/xml', 'content-length': '240'}, 'RetryAttempts': 0}}    

if __name__=='__main__':
    test_send_msg_testchannel()
    test_received_msg()
    