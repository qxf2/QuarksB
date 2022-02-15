"Helper module for sqs"
import boto3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Sqs():
    "Sqs helper class to get sqs client and messages from sqs"
    def __init__(self):
        "Constructor" 

    def get_client(self):
        "Get sqs client"
        try:
            sqs_client = boto3.client('sqs')
        except Exception as error:                    
            raise Exception('\nUnable to create SQS client!') from error

        return sqs_client

    def get_message(self):
        "Method to fet messsage from queue"    
        try:
            sqs_client = self.get_client()      
            response = sqs_client.receive_message(
                QueueUrl='staging-newsletter-generator', 
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
            )      
            print(f"Number of messages received: {len(response.get('Messages', []))}")
            if 'Messages' in response:
                for message in response['Messages']:
                    print(message['Body'])
            else:
                print("No messages in the queue at this moment")

        except Exception as error:
            raise Exception('\nError getting message') from error

        return response