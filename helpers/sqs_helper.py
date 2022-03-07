"""
Helper module for sqs messages
"""
import os
import sys
import json
import boto3
import collections
import conf.sqs_conf as sqs_conf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_data_structure(data):
    """
    Method used for converting nested dictionary/list to data similar to tabular form
    """
    obj = collections.OrderedDict()
    def recurse(dataobject,parent_key=""):
        """
        Method will recurse through object
        """
        if isinstance(dataobject,list):
            # loop through list and call recurse()
            for i in range(len(dataobject)):
                recurse(dataobject[i],parent_key + "_" + str(i) if parent_key else str(i))
        elif isinstance(dataobject,dict):
            # loop through dictionary and call recurse()
            for key,value in dataobject.items():
                recurse(value,parent_key + "_" + key if parent_key else key)
        else:
            # use the parent_key and store the value to obj
            obj[parent_key] = dataobject

    recurse(data)

    return obj

def get_sqs_client():
    """
    Return sqs_client object
    :param none
    :return sqs_client
    """
    sqs_client = boto3.client('sqs')

    return sqs_client

def get_sqs_queue(queue_url):
    """
    Return queue object from queue_url
    :param queue_url
    :return queue
    """
    queue = boto3.resource('sqs').get_queue_by_name(QueueName=queue_url)

    return queue

def send_message_to_queue(queue_url, MSG_BODY,MSG_ATTRIBUTES):
    """
    Return result flag
    :param queue_url, message
    : MSG_ATTRIBUTES = {'Author': {'DataType': 'String','StringValue': 'Rahul'}}
    : MSG_BODY = 'Test'
    :return response status code
    """
    sqs_client = get_sqs_client()
    queue = get_sqs_queue(queue_url)
    response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=MSG_BODY, MessageAttributes=MSG_ATTRIBUTES)
    response_metadata=response[sqs_conf.ResponseMetadata]
    response_status = response_metadata[sqs_conf.HTTPStatusCode]
    
    return response_status

def get_message_from_queue(queue_url):
    """
    get raw messsage from queue_url
    """
    sqs_client = get_sqs_client()
    queue = get_sqs_queue(queue_url)
    message = sqs_client.receive_message(QueueUrl=queue.url)

    return message

def purge_sqs_queue(queue_url):
    """
    Reteun status
    """
    queue = get_sqs_queue(queue_url)
    client = get_sqs_client()
    response = client.purge_queue(QueueUrl=queue.url)
    response_metadata=response[sqs_conf.ResponseMetadata]
    response_status = response_metadata[sqs_conf.HTTPStatusCode]
    
    return response_status
