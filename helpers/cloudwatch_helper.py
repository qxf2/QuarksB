"""
Helper module for Cloud Watch Logs
"""
import boto3
from datetime import datetime, timedelta
import time
import os
import sys
import collections

# add project root to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.base_helper import BaseHelper

class CloudWatchHelper(BaseHelper):
    """
    Cloud watch Helper class
    """
    def get_cloudwatch_log_messages(self, log_group, query):
        """
        get cloud watch logs
        """
        try:
            messages = None      
            query_flag = True
            query_id = self.get_query_id(log_group, query)
            time.sleep(100)
            client = boto3.client('logs')
            while query_flag:
                response = client.get_query_results(queryId=query_id)
                if response['status'] == 'Complete':
                    query_flag = False
                else:
                    self.write('not completed the query')
                time.sleep(1)
            if (response):
                messages = response.get('results', [])    
                if(messages):
                    self.write(f'CloudWatchLogs messages : {messages}')        
        except Exception as err:
            raise Exception(f'messages not found! {err}')    

        return messages    


    def get_query_id(self, log_group, query):
        """
        get query id
        """
        query_id = None
        try:           
            client = boto3.client('logs')
            query_response = client.start_query(logGroupName=log_group,
                                                    startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                                    endTime=int(datetime.now().timestamp()),
                                                    queryString=query)            
            query_id = query_response.get('queryId')
            self.write(f'The Query ID is {query_id}')
        except Exception as err:
            self.write(f'Error Not found {err}', level='error')

        return query_id

    def get_log_messages(self, log_group, query):
        """
        get cloud watch logs
        """
        try:
            messages = None      
            query_flag = True
            query_id = self.get_query_id(log_group, query)
            time.sleep(100)
            client = boto3.client('logs')
            while query_flag:
                response = client.get_query_results(queryId=query_id)
                if response['status'] == 'Complete':
                    query_flag = False
                else:
                    self.write('not completed the query')
                time.sleep(1)
            if (response):
                messages = response.get('results', [])    
                if(messages):
                    self.write(f'CloudWatchLogs messages : {messages}')        
        except Exception as err:
            raise Exception(f'messages not found! {err}')    

        return messages    
