import os
import sys
import boto3
import random
import time
import ast
import collections
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import cloud_watch_conf as cloudwatch_conf

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
def get_response_log_daily_messages(request_id,log_group,query):
    """
    getting response from daily message lambda
    """
    client = boto3.client('logs')
    start_query_response = client.start_query(logGroupName=log_group,\
        startTime=int((datetime.today() - timedelta(minutes=5)).timestamp()),\
            endTime=int(datetime.now().timestamp()),queryString=query)
    query_id = start_query_response['queryId']
    response = None
    while response is None:
        time.sleep(1)
        response = client.get_query_results(queryId=query_id)
    

    return response.get('results')

 

def get_ptr_value(log_group,query):
    """
    getting ptr_value from response
    """
    client = boto3.client('logs')
    start_query_response = client.start_query(logGroupName=log_group,\
        startTime=int((datetime.today() - timedelta(minutes=5)).timestamp()),\
            endTime=int(datetime.now().timestamp()),queryString=query)
    query_id = start_query_response['queryId']
    response = None
    ptr_value = None
    while response is None:
        time.sleep(1)
        response = client.get_query_results(queryId=query_id)
        response_dict = get_data_structure(response)
                
        if cloudwatch_conf.ptr_value in response_dict.keys():
            ptr_value = response_dict[cloudwatch_conf.ptr_value]
        else:
            print(f'log pointer key could not be fetched from response dictionary.')
    
    
    message_test=list(ptr_value.split(','))
    
    return message_test[0]


if __name__ == '__main__':
    message = None
    message_test =get_ptr_value\
        (cloudwatch_conf.log_group,cloudwatch_conf.query_skype_sender)
    print("---------Printing Message ----------")
    print(message_test) 
