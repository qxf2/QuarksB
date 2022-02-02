"""Send message to newsletter generator queue through api endpoint and verify if it appears in the sqs"""

import os,sys,json
from urllib.error import HTTPError
import pytest
import requests
import boto3
from botocore.exceptions import ClientError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

s_message = "Hi , I am testing.."

def skype_sender():
  ss_url = os.environ["SKYPE_URL"]
  s_channel_id = os.environ["S_CHANNEL_ID"]
  ss_api_key = os.environ["SS_API_KEY"]

  payload = json.dumps({
    "msg": s_message,
    "channel": s_channel_id,
    "API_KEY": ss_api_key
  })
  headers = {
    'Content-Type': 'application/json'
  }
  try:
    response = requests.request("POST", ss_url, headers=headers, data=payload)
    print(f'Skype sender post call status: {response.status_code}')
  except HTTPError as error:
    print(f'\n skype sender error: {error}')
  
  return response.status_code


def verify_sqs():
  sqs_url = os.environ["QUEUE_URL"]
  try:
    sqs = boto3.client('sqs')
    response = sqs.receive_message(QueueUrl=sqs_url,MessageAttributeNames=['All'],MaxNumberOfMessages=10)
    messages = response.get("Messages", None)
    if messages is not None:
      for msg in messages:
          if msg["Body"]==s_message:
            print("Message posted by skype sender is found in the sqs queue")
            print(f'Here is the message body in the SQS Queue:{msg["Body"]}')
    else:
      print("Message not found in the sqs queue")
  except ClientError as error:
    print(error)

if __name__=='__main__':
    skype_sender()
    verify_sqs()

