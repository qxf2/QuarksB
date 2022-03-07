"""
This test covers following:
Setup- Purging SQS queue
Step 1: Trigger the message
Step 2: Verify message with staging-newsletter-generator queue
"""
import os
import sys
import ast
import time
import json
import logging
import requests
import unittest
import pytest
from pythonjsonlogger import jsonlogger
import helpers.sqs_helper
import helpers.filter_message_helper
import helpers.skype_helper
import helpers.cloudwatch_helper
import conf.sqs_conf as sqs_conf
import conf.skype_conf as skype_conf
import conf.cloudwatch_conf as cloudwatch_conf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# logging
log_handler = logging.StreamHandler()
log_handler.setFormatter(jsonlogger.JsonFormatter())
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Declaring class for test object
class SkypeMessage():
    """
    Class for test object
    """
    def __init__(self):
        """
        Initilalise class
        """
    def clean_queue(self, queue_url):
        "Method to purge queue"
        result_flag = helpers.sqs_helper.purge_sqs_queue(queue_url)

        return result_flag

    def send_message(self, queue_url, MSG_BODY,MSG_ATTRIBUTES):
        "Method to send message"
        result_flag = helpers.sqs_helper.send_message_to_queue(queue_url,MSG_BODY,MSG_ATTRIBUTES)

        return result_flag
    
    def get_message(self, queue_url):
        "Method to get message"
        result_flag = helpers.sqs_helper.get_message_from_queue(queue_url)

        return result_flag

    def post_message(self, message):
        """
        post message to skype channel
        """
        response = helpers.skype_helper.post_message_on_skype(message)

        return response

    def get_message_from_cloudwatch_log(self):
        """
        Method to get message from cloudwatch log pointer
        """
        message = None
        for i in range(1, 6):
            message_value = helpers.cloudwatch_helper.get_message_value\
                (cloudwatch_conf.url_filter_log_group,cloudwatch_conf.query_url_filter)
            if message_value:
                message = message_value
                break
            time.sleep(60)

        return message


class TestSQSMessage(unittest.TestCase):
    """
    Test class
    """
    def test_send_and_validate_message_from_queue(self):
        """
        Test case
        """
        SkypeMessage_obj = SkypeMessage()
        queue_url = sqs_conf.queue_url
        
        logger.info("Setup- Purge SQS queue")
        logger.info("---------------------------------------------------------------------------")
        response_status = SkypeMessage_obj.clean_queue(queue_url=queue_url)
        assert response_status == 200
        
        logger.info("Sending the message")
        logger.info("---------------------------------------------------------------------------")
        message = skype_conf.MESSAGE
        response = SkypeMessage_obj.post_message(message)
        assert response_status == 200
        
        logger.info("Getting message from SQS Queue")
        logger.info("---------------------------------------------------------------------------")
        message = SkypeMessage_obj.get_message(queue_url=queue_url)
        message_body = helpers.filter_message_helper.get_message_body(message)

        logger.info("Validating message from SQS Queue")
        logger.info("---------------------------------------------------------------------------")
        assert message_body['msg'] == skype_conf.MESSAGE
        
        logger.info("Step 2: Print message from cloudwatch logs------------------------------")
        message = SkypeMessage_obj.get_message_from_cloudwatch_log()
        logger.info("---------------------------------------------------------------------------")
        logger.info(message)