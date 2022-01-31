"""
This is a test to send a message via Skype Sender and 
verify if the staging-newsletter-generator SQS received the message.

"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.skype_conf as conf
from helpers import skype_helper
from helpers import sqs_helper

def test_get_message_sqs():
    "Tests to check the message in the queue."       
    skype_obj= skype_helper.Skype()
    skype_obj.skype_send_message()      
    sqs_obj= sqs_helper.Sqs_queue()      
    messages = sqs_obj.get_message_from_queue()    
    assert len(messages)>0, 'Messages not found in SQS!'               
    
#---START OF SCRIPT
if __name__ == '__main__':    
    test_get_message_sqs()