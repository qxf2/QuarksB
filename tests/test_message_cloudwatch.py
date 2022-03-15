"""
 Test to validate skype messages messages on cloudwatch logs
"""
import time, sys, os
from conf import skype_conf, cloudwatch_conf

def test_cloudwatch_logs(cloudwatch_instance, skype_instance):
    """
    send meesage on skype and validate the message on cloudwatch logs
    """
    try:    
            message = skype_conf.MESSAGE
            send_message_skype = skype_instance.post_message_on_skype(message)            
            time.sleep(10)
            cloudwatch_log = cloudwatch_instance.get_log_messages(cloudwatch_conf.log_group, cloudwatch_conf.query)          
    except Exception as err:
        raise(err)
