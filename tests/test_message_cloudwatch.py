"""
 Test script to:
  - Validate message sent to Skype channel against the message received on SQS
"""
import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import sqs_conf, skype_conf
from conf import cloudwatch_conf
from helpers import cloudwatch_helper


def test_message_received_cloudwatch(sqs_instance, skype_instance, concurrent_obj):
    """
    Validate if message sent over skype is the same as received in the cloudwatch logs
    """
    try:
        sent_message = str(skype_conf.MESSAGE)
        print("Sending message: " + sent_message)
        skype_url = skype_conf.SKYPE_SENDER_ENDPOINT
        skype_instance.post_message_on_skype(sent_message, skype_url)

        time.sleep(2 * 60)

        get_msg_from_cloudwatch = cloudwatch_helper.get_response_value(cloudwatch_conf.log_group,cloudwatch_conf.query)

        matched = False
        expected_message = sent_message
        print("expected message is " + sent_message)
        for query_matches in get_msg_from_cloudwatch['results']:
            for match in query_matches:
                if (match['field'] == 'msg'):
                    received_message = match['value']
                    print("Received message is " + received_message)
                    if expected_message == received_message:
                        matched = True
                        break
        assert matched, "Did not receive the test message"

    except Exception as err:
        raise(err)
