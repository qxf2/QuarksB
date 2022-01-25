import boto3
import json
import logging
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import aws_conf as aws_conf
import conf.sqs_conf as sqs_conf
from pythonjsonlogger import jsonlogger
 


 
class Sqsmessage():
    # class for all sqs utility methods
    logger = logging.getLogger(__name__)
 
    def get_messages_from_queue(self,queue_url):
        """
        Generates messages from an SQS queue.
        :param queue_url: URL of the SQS queue to drain.
        """
        sqs_client = self.get_sqs_client()
        queue = self.get_sqs_queue(queue_url)
        messages = sqs_client.receive_message(QueueUrl=queue.url)
        if 'Messages' in messages:
            for message in messages['Messages']:
                self.logger.info(message['Body'])
        else:
            self.logger.info("No messages polled from the queue at this moment")
 
 
    def get_sqs_client(self):
        """
        Return sqs_client object
        :param none
        :return sqs_client
        """
        sqs_client = boto3.client('sqs')
        self.logger.info(sqs_client)
 
        return sqs_client
 
    def get_sqs_queue(self,queue_url):
        """
        Return queue object from queue_url
        :param queue_url
        :return queue
        """
        queue = boto3.resource('sqs').get_queue_by_name(QueueName=queue_url)
        self.logger.info(queue)
 
        return queue
 
if __name__=='__main__':
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    #creating instance of object and calling necessary method
    sqsmessage_obj = Sqsmessage()
    sqsmessage_obj.get_messages_from_queue(sqs_url)

