"""
 Test script to:
  - Validate message sent to Skype channel against the message received on SQS
"""
import time
from conf import sqs_conf
from conf import skype_conf
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

url = skype_conf.SKYPE_SENDER_ENDPOINT
#aws_owner_id=str(os.environ.get('aws_access_key_id'))


def test_message_received_sqs(sqs_instance, skype_instance, concurrent_obj):
    """
    Validate the message triggered from Skype
    """
    try:
        with concurrent_obj.ThreadPoolExecutor() as executor:
            future = executor.submit(sqs_instance.get_message_from_queue, sqs_conf.SQS_NAME, sqs_conf.config)
            # wait 3 secs before triggering Skype message
            message = skype_conf.MESSAGE
            time.sleep(3)
            trigger_skype_message = skype_instance.post_message_on_skype(message, url)
            sqs_messages = future.result()

        # validate if message found
        if_message_found = False
        for msg in sqs_messages:
            if message in msg:
                if_message_found = True
                break
        assert if_message_found

    except Exception as err:
        raise(err)
