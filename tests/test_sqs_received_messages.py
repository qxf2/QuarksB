"""
Test details:
1. Post message on Skype channel
2. Get SQS messages and verify Skype message exist in SQS queue
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import sqs_received_messages_test_conf as conf
from helpers import skype_helper
from helpers import sqs_helper

def test_sqs_received_messages():
    "Tests to check the sqs received message" 
    # test configurations
    message = conf.SKYPE_MESSAGE 
    queue_url = conf.QUEUE_URL

    # Post Message on Skype Channel   
    print("\nPost message on Skype Channel")  
    skype_obj = skype_helper.SkypeHelper()
    skype_response = skype_obj.post_message_on_skype(message)  
    print("\nSkype status response code:", skype_response)
    
    # Get SQS queue message 
    print("\nGet messages from SQS queue")   
    sqs_obj = sqs_helper.SqsHelper()      
    queue_messages = sqs_obj.get_message_from_queue(queue_url)
    print("\nReceived SQS message:", queue_messages)

    # Verify SQS queue messages
    print("\nVerifying SQS messages")
    result_flag = False
    if queue_messages is not None:
      for msg in queue_messages:
          if msg["Body"] == message:
            print("\nPASS: Skype message found in the sqs queue")
            result_flag = True
            break
    else:
      print("\nFAIL: Message not found in the sqs queue")
            
    assert result_flag == True  
                   

#---START OF SCRIPT
if __name__ == '__main__':    
    test_sqs_received_messages()