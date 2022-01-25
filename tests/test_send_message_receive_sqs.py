import boto3
import json
import logging
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import aws_conf as aws_conf
import conf.sqs_conf as sqs_conf
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



def test_message_in_sqs(self,queue_url):
    """Test message_in_sqs"""
    """ TODO
    Extract the message from the read_sqs
    and compare it with the one that send from the test_send message 
    
    """




if __name__=='__main__':
    send_message_to_sqs.test_send_message()
    sqsmessage_obj = read_sqs.Sqsmessage()
    sqsmessage_obj.get_messages_from_queue(sqs_url)
else:
    print('ERROR: Received incorrect comand line input arguments')


