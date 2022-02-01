"""
Helper module for sqs messages
"""
import os
import sys
import boto3
from botocore.exceptions import ClientError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import sqs_utilities_config as sqs

class SQS():
    "SQS helper class methods"

    def __init__(self):
        "Constructor"

    def get_sqs_client(self):
        """
        Return sqs_client object
        """
        sqs_client = boto3.client('sqs')
        return sqs_client

    def get_sqs_queue_url(self):
        """
        Return queue object from queue_url
        """
        try:
            sqs_client = self.get_sqs_client()
            queue = sqs_client.get_queue_url(QueueName=sqs.QUEUE_URL)
        except ClientError as error:
            print(f'\nBotocore exception: {error}\n')
            raise Exception('\n Unable to get URL of queue') from error
        except Exception as error:
            print(f'\nException: {error}\n')
            raise Exception('\n Unable to get URL of queue') from error
        return queue['QueueUrl']

    def get_message_from_queue(self):
        """
        get messsage from queue_url
        """
        try: 
            message = []
            sqs_client = self.get_sqs_client()
            queue_url = self.get_sqs_queue_url()
            message = sqs_client.receive_message(
                            QueueUrl=queue_url,
                            AttributeNames=['All'],
                            MaxNumberOfMessages=1,
                            MessageAttributeNames=['All'],
                            WaitTimeSeconds=20
                            )
        except ClientError as error:
            print(f'\nBotocore exception: {error}\n')
            raise Exception('\nUnable to receive message from queue') from error
        except Exception as error:
            print(f'Unable to receive message from queue : {error}')
        return message
