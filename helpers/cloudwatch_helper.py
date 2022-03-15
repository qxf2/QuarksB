"""
Helper module for CloudWatch
"""
import boto3
import os
import sys
from datetime import datetime, timedelta
import time
import collections
from helpers.base_helper import BaseHelper

class CloudWatchHelper(BaseHelper):
    """
    CloudWatch helper object
    """
    def get_client(self):
        "Get cloud watch logs client"
        try:           
            client = boto3.client('logs')         
        except Exception as e:
            self.write(f'Unable to create client due to {err}', level='error')
        return client

    def get_query_id(self, log_group, query):
        """
        Build query to fetch the log messages
        """
        query_id = None
        try:           
            client = self.get_client()
            cloudwatch_query = client.start_query(logGroupName=log_group,
                                                    startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                                    endTime=int(datetime.now().timestamp()),
                                                    queryString=query)            
            query_id = cloudwatch_query.get('queryId')
            self.write(f'query ID is {query_id}')
        except Exception as err:
            self.write(f'There was an error in query {err}', level='error')

        return query_id

    def get_log_messages(self, log_group, query):
        """
        Fetch the log messages from cloudwatch
        """
        try:
            #response = None   
            messages = None 
            query_status_flag = True                  
            query_id = self.get_query_id(log_group, query)
            time.sleep(100)
            client = self.get_client()
            while query_status_flag:
                response = client.get_query_results(queryId=query_id)
                if response['status'] == 'Complete':
                    query_status_flag = False
                else:
                    self.write('Cloudwatchlog query is running....')
                time.sleep(1)
            if (response):
                messages = response.get('results', [])    
                if(messages):
                    self.write(f'CloudWatchLogs messages : {messages}')        
        except Exception as err:
            raise Exception(f'Error getting messages from logs, due to {err}')    

        return messages    
