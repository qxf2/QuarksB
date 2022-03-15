"""
Verify the message sent to Skype channel along with the cloudwatch logs
"""
import time, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf, cloudwatch_conf

def test_cloudwatch_logs(cloudwatch_instance, skype_instance):
    """
    verify the cloud watch logs
    """
    try:    
            message = skype_conf.MESSAGE
            trigger_skype_message = skype_instance.post_message_on_skype(message)            
            time.sleep(15)
            log_messages = cloudwatch_instance.get_clougwatch_log_messages(cloudwatch_conf.log_group, cloudwatch_conf.query)
            print (log_messages)            
    except Exception as err:
        raise(err)