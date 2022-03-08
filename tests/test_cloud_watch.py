"""
 Test script to:
  - Validate message sent to Skype channel against the message received on SQS
"""
import time
from datetime import datetime, timedelta
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import sqs_conf
from conf import skype_conf

from conf import cloud_watch_conf as cloudwatch_conf
from helpers import cloud_watch_helper


url = skype_conf.SKYPE_SENDER_ENDPOINT
#aws_owner_id=str(os.environ.get('aws_access_key_id'))


def test_message_received_cloudwatch(skype_instance, concurrent_obj):
    """
    Validate the message triggered from Skype
    """
    try:
    
        #future = executor.submit(sqs_instance.get_message_from_queue, sqs_conf.SQS_NAME, sqs_conf.config)
        # wait 3 secs before triggering Skype message
        
        message = skype_conf.MESSAGE
        time.sleep(3)
        trigger_skype_message = skype_instance.post_message_on_skype(message, url)
        #sqs_messages = future.result()

        # validate if message found
        time.sleep(240)        
        message_found = False
        message_test =cloud_watch_helper.get_ptr_value\
        (cloudwatch_conf.log_group,cloudwatch_conf.query_skype_sender)
        print("---------Printing Message ----------")
        
        print(message_test) 
        
        if message == message_test:
            message_found=True
            
        assert message_found,'Message mismatch between Skype and SQS!'
        
        

    except Exception as err:
        raise(err)
    

  