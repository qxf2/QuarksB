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
    Cloud watch Helper object
    """

    def get_query_id(self):
        """
        Build a query
     
        """
        query_id = None
        try:           
            client = boto3.client('logs')
            start_query_response = client.start_query(logGroupName=conf.log_group,
                                                    startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                                    endTime=int(datetime.now().timestamp()),
                                                    queryString=query)            
            query_id = start_query_response.get('queryId')
            self.write(f'The Query ID is {query_id}')
        except Exception as err:
            self.write(f'Unable to build query {err}', level='error')

        return query_id

    def get_log_messages(self, log_group, query):
        """
        get cloud watch logs messages
        """
        try:
            response = None    
            query_status_flag = True
            messages = None      
            query_id = self.get_query_id()
            time.sleep(100)
            while query_status_flag:
                response = client.get_query_results(queryId=query_id)
                if response['status'] == 'Complete':
                    query_status_flag = False
                else:
                    self.write('Waiting for query to complete ...')
                time.sleep(1)
            if (response):
                print ("Got the response from the logs")
                messages = logs_query_response.get('results', [])    
                if(messages):
                    self.write(f'CloudWatchLogs messages : {messages}')        
        except Exception as err:
            raise Exception(f'Unable to get the message from logs, due to {err}')    

        return messages    


 