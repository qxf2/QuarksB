"""
Queues Helper class
"""
import asyncio
import os
import sys
import boto3
from botocore.exceptions import ClientError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import aws_credentials as awsc, queues_conf as qc

class Queues():
    "Queues helper class and associated methods"
    def __init__(self):
        "Constructor"

    def create_sqs_resource(self):
        "Returns AWS SQS resource object"
        sqs_resouce = boto3.resource('sqs',
                            aws_access_key_id = awsc.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key = awsc.AWS_SECRET_ACCESS_KEY,
                            region_name=awsc.REGION_NAME)
        return sqs_resouce

    def create_sqs_client(self):
        "Returns AWS SQS client object"
        try:
            sqs_client = boto3.client('sqs',
                            aws_access_key_id = awsc.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key = awsc.AWS_SECRET_ACCESS_KEY,
                            region_name=awsc.REGION_NAME)
        except ClientError as error:
            print(f'\nBotocore exception: {error}\n')
            raise Exception('\nUnable to create SQS client!') from error
        except Exception as error:
            print(f'\nException: {error}\n')
            raise Exception('\nUnable to create SQS client!') from error
        return sqs_client

    def get_sqs_url(self):
        "Returns the URL of the SQS"
        try:
            sqs_client = self.create_sqs_client()
            response = sqs_client.get_queue_url(QueueName=qc.SQS_NAME)
        except ClientError as error:
            print(f'\nBotocore exception: {error}\n')
            raise Exception('\nUnable to get URL of the SQS!') from error
        except Exception as error:
            print(f'\nException: {error}\n')
            raise Exception('\nUnable to get URL of the SQS!') from error
        return response['QueueUrl'], sqs_client

    def extract_messages(self, response_object):
        "Extracts the body of the message from the API response object"
        msg_body = []
        messages = response_object.get('Messages',[])
        if messages:
            for msg in messages:
                msg_body.append(msg.get('Body', ''))
        return msg_body

    async def get_messages_from_sqs(self):
        "Returns the messages from SQS"
        messages_text=[]
        try:
            queue_url, sqs_client = self.get_sqs_url()
            print(f'\nSQS URL : {queue_url}\n')
            response = sqs_client.receive_message(
                            QueueUrl=queue_url,
                            AttributeNames=['All'],
                            MaxNumberOfMessages=10,
                            MessageAttributeNames=['All'],
                            WaitTimeSeconds=20
                            )
            messages_text = self.extract_messages(response)
        except ClientError as error:
            print(f'\nBotocore exception: {error}\n')
            raise Exception('\nUnable to receive message from SQS!') from error
        except Exception as error:
            print(f'Unable to receive message from SQS: {error}')
        return messages_text
