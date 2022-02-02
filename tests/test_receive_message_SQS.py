"""
Test to verify that message is sent to Skype channel and able to see the message received in the SQS queue
"""
import os
import sys
import pytest
from concurrent.futures import ThreadPoolExecutor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_config
from helpers.send_skype_message import Skype
from helpers import sqs_helper

def send_message():
    from time import sleep
    sleep(2)
    skype = Skype()
    skype.send_skype_message()

def receive_message():
    sqs = sqs_helper.SQS()
    received_message = None
    queue_msg = sqs.get_message_from_queue()
    if 'Messages' in queue_msg:
        for message in queue_msg['Messages']:
            received_message = message['Body']['Message']['msg']
            break
    print("The message is ", received_message)
            
    return received_message == skype_config.MESSAGE

def test_receive_message_SQS():
    """
    Test the message received in SQS is the same as one sent to Skype channel
    """
    executor = ThreadPoolExecutor(max_workers=2)
    a = executor.submit(receive_message)
    b = executor.submit(send_message)

    b.result()
    assert a.result()

