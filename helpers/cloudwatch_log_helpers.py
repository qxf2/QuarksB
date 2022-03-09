import json
import profile

import boto3
from boto3 import session
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import time
from helpers.base_helper import BaseHelper
from conf import cw_conf, skype_conf

"""
Helper module for sqs messages
"""

class CWhelper(BaseHelper):
    """
    CloudWatch helper Object.
    """
    def get_query_id(self,message):
        """
        Frame a query and schedule it
        :param self:
        :param message: Message triggered from Skype
        :return query_id: Query ID
        """
        query_id = None
        try:
            query = cw_conf.query % (message)
            self.write(f'The query is {query}')
            client = self.get_cloudwatch_client(cw_conf.config, cw_conf.PROFILE_NAME)
            start_query_response = self.client.start_query(
                                            logGroupName = cw_conf.log_group,
                                            startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                            endTime=int(datetime.now().timestamp()),
                                            queryString= query
            )

            self.write(f'The Query rsponse is {start_query_response}')
            query_id = start_query_response.get('queryId')
            self.write(f'The Query ID is {query_id}')
        except Exception as err:
            self.write(f'Unable to frame query and schedule logs due to {err}', level='error')

        return query_id

    def get_cloudwatch_client(self, config, profile_name):
        """
        Return cw_log object
        :param self:
        :return cw_client: cw client object
        """
        try:
            session = boto3.Session(profile_name=profile_name)
            self.client = session.client('logs', config=config)
            self.write(f'Created CloudWatch client')
        except ClientError as err:
            self.write(f'Exception - {err}, Unable to create CW client', level='error')
        except Exception as err:
            self.write(f'Unable to create CW client, due to {err}', level='error') 

        return self.client
 
    def extract_message(self, query_response):
        """
        Extract message from Cloudwatch logs
        :param self:
        :param query_response: query search response from logs
        :return message: Message from the log
        """
        message = None
        try:
            messages = query_response.get('results', [])
            if messages:
                for message in messages:
                    print(message)
                    for fields in message:
                        for key, value in fields.items():
                            if key == '@message':
                                message = value
                                self.write('Extracted {message} from the logs')
            else:
                self.write(f'Unable to fetch message from logs', level='error')

            return message
        except Exception as err:
            self.write(f'Unable to extract  message from logs due to {err}!', level='error')
            
    def get_message_from_cloudwatch_log(self, message):
        """
        Get message from cloudwatch log
        :param self:
        :param attempts: number of attempts to get the message
        :return messages: messages list object
        """
        query_response=None
        message_from_log=None
        query_status_flag=True

        try:
            query_id = self.get_query_id(message)
            client = self.get_cloudwatch_client(cw_conf.config,cw_conf.PROFILE_NAME)
            while query_status_flag:
                query_response = client.get_query_results(queryId=query_id)
                if query_response.get('status', None)  == 'Complete':
                    query_status_flag = False
                else:
                    self.write(f'Running cloudwatchlog query')
                    time.sleep(2)
            if query_response:
                self.write(f'Response object from cloudwatch {query_response}')
                message_from_log = self.extract_message(query_response)
                if message_from_log:
                    self.write(f'Fetched {message_from_log} from log')

            return message_from_log
        except Exception as err:
            self.write(f'Unable to get message from logs due to {err}!', level='error')