"""
Helper module for AWS CloudWatchLogs messages
"""
from datetime import datetime, timedelta
import os
import sys
import time
import boto3
from botocore.exceptions import ClientError
from helpers.base_helper import BaseHelper

class CloudWatchHelper(BaseHelper):
    """
    CloudWatch Helper object
    """
    def __init__(self):
        "Class constructor"
        self.client = boto3.client('logs')

    def get_query_id(self, log_group, query):
        """
        Schedules the CloudWatchLogs query and returns the queryId
        :param self:
        :param log_group: string object
        :param query: string object
        :return query_id: string object
        """
        try:
            start_query_response = self.client.start_query(
                                            logGroupName = log_group,
                                            startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                            endTime=int(datetime.now().timestamp()),
                                            queryString= query
                                            )
        except ClientError as error:
            print(f'Botocore exception :\n {error}\n')
            raise Exception('Unable to schedule CloudWatchLogs query!') from error
        except Exception as error:
            print(f'General exception :\n {error}\n')
            raise Exception('Unable to schedule CloudWatchLogs query!') from error
        return start_query_response.get('queryId', None)

    def get_message_from_logs(self, cloudwatch_log_group, cloudwatch_query):
        """
        Retrieves messages from CloudWatch logs
        :param self:
        :param cloudwatch_log_group : string object
        :param cloudwatch_query : string object
        :return messages_from_log: list object
        """
        try:
            query_id = self.get_query_id(cloudwatch_log_group, cloudwatch_query)
            query_response = None
            messages_from_log = []
            query_status_flag = True
            while query_status_flag:
                query_response = self.client.get_query_results(queryId=query_id)
                if query_response.get('status', None)  == 'Complete':
                    query_status_flag = False
                else:
                    print('Waiting for CloudWatchLogs query to complete..')
                    time.sleep(2)
            messages_from_log = self.extract_messages(query_response)
        except ClientError as error:
            print(f'Botocore exception :\n {error}\n')
            raise Exception('Unable to fetch CloudWatch API response!') from error
        except Exception as error:
            print(f'General exception :\n {error}\n')
            raise Exception('Unable to fetch CloudWatch API response!') from error
        return messages_from_log

    def extract_messages(self, logs_query_response):
        """
        Extract messages from the CloudWatch API response
        :param self:
        :param logs_query_response: dict object
        :return messages: list object
        """
        messages = logs_query_response.get('results', [])
        return messages
