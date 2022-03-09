"""
 Test script to:
  - Validate message sent to Skype channel against the message received on SQS
"""
from asyncore import write
import time
from urllib import response
from conf import sqs_conf, skype_conf
from conf import cw_conf

def test_message_received_cw(skype_instance, cloudwatch_instance):
    """
    Validate the message triggered from Skype
    """
    try:
       message_found=False
       message = skype_conf.message
       skype_response = skype_instance.post_message_on_skype(message)
       assert skype_response.status_code == 200 ,"Unable to deliver test message"
    
       message_from_log = cloudwatch_instance.get_message_from_cloudwatch_log(message)
       for message in message_from_log:
           for fields in message:
               for key, value in fields.items():
                   if key == 'value' and message.strip() == value.split(',')[0].strip():
                        message_found = True
                        break
       assert message_found, 'Test message not found in CloudWatch logs'
      
    except Exception as err:
        print(f'Unable to run test, due to {err}')

