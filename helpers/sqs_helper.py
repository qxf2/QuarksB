"""
Helper module for sqs messages
"""
import os
import sys
import boto3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import sqs_conf as sqs

class Sqs_queue():
    "Helper class for Queues and related methods"
    def __init__(self):
        "Constructor" 

    def get_sqs_client(self):
        "Return sqs_client object"
        try:
            sqs_client = boto3.client('sqs')
        except ClientError as error:                 
            raise Exception('\nUnable to create SQS client!') from error    
        except Exception as error:                    
            raise Exception('\nUnable to create SQS client!') from error
    
        return sqs_client
 
    def get_message_from_queue(self):
        "Get messsage from queue_url"    
        try:
            message_body = []
            sqs_client = self.get_sqs_client()      
            response = sqs_client.receive_message(QueueUrl=sqs.queue_url, AttributeNames=['All'],
                                MaxNumberOfMessages=1,
                                MessageAttributeNames=['All'],
                                WaitTimeSeconds=0)       
            print(f"Number of messages received: {len(response.get('Messages', []))}")
            for message in response.get("Messages", []):
                message_body = message["Body"]
                print(f"Message body: {json.loads(message_body)}")       
        except ClientError:            
            raise Exception('\nCould not receive message from the queue') from error
        except Exception as error:
            raise Exception('\nCould not receive message from the queue') from error
        
        return message_body
       

