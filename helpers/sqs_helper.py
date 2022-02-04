"""
AWS SQS helper:
It helps to connect with AWS SQS Service.

To Do:
Add following methods:
- get all queues
- verify specific queue exist
- create queue
- send message to queue
- update queue
- delete queue
- verify specific message exist
- etc
"""
import os
import sys
import boto3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SqsHelper():
    "AWS SQS helper class to connect with queues"

    def get_sqs_client(self):
        "Return sqs_client object"
        try:
            sqs_client = boto3.client('sqs')
        except ClientError as error:                 
            raise Exception('\nUnable to create SQS client!') from error    
        except Exception as error:                    
            raise Exception('\nUnable to create SQS client!') from error

        return sqs_client

    def get_message_from_queue(self,queue_url):
        "Get messsage from queue_url"    
        try:
            sqs_client = self.get_sqs_client()      
            response = sqs_client.receive_message(QueueUrl=queue_url, AttributeNames=['All'],
                                MaxNumberOfMessages=10,
                                MessageAttributeNames=['All'],
                                WaitTimeSeconds=0)       
            messages = response.get("Messages", None)       
        except ClientError:            
            raise Exception('\nCould not receive message from the queue') from error
        except Exception as error:
            raise Exception('\nCould not receive message from the queue') from error

        return messages