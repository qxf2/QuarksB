"""
 Test script to:
  - Validate message sent to Skype channel against the message received on cloudwatch logs
"""
import time, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf, cloud_watch_conf

def test_message_received_lambda(cloudwatch_instance, skype_instance):
    """
    Validate the message triggered by lambda
    """
    try:    
            message = skype_conf.MESSAGE
            time.sleep(3)
            trigger_skype_message = skype_instance.post_message_on_skype(message)            
            time.sleep(12)
            log_messages = cloudwatch_instance.get_log_messages(cloud_watch_conf.log_group, cloud_watch_conf.query)
            print (log_messages)            
    except Exception as err:
        raise(err)
