import boto3
import asyncio
import json
import logging
import pytest
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import aws_conf as aws_conf
from conf import sqs_conf as sqs_conf
from conf import channel_conf as channel_conf
from pythonjsonlogger import jsonlogger
from helpers import send_message_to_sqs
from components import read_sqs


# logging
log_handler = logging.StreamHandler()
log_handler.setFormatter(jsonlogger.JsonFormatter())
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
 
#setting environment variable

os.environ['AWS_ACCESS_KEY_ID'] = aws_conf.AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_conf.AWS_SECRET_ACCESS_KEY

#set the QueueName

sqs_url = sqs_conf.QUEUE_URL_LIST



def test_message_in_sqs():
    """Test message_in_sqs"""
  
    sqsmessage_obj = read_sqs.Sqsmessage()
    message=sqsmessage_obj.get_messages_from_queue(sqs_url)
    send_message_to_sqs.test_send_message()
  
    
    logger.info("Getting message from SQS Queue")
    logger.info("---------------------------------------------------------------------------")
    logger.info(message)
    
    logger.info("Validating message from SQS Queue")
    logger.info("---------------------------------------------------------------------------")
    assert channel_conf.MESSAGE in message ,'Message mismatch between Skype and SQS!'

    


if __name__=='__main__':
    test_message_in_sqs()
    



