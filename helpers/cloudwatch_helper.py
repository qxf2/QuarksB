import boto3
from datetime import datetime, timedelta
import time

def get_response_value(log_group,query):
    client = boto3.client('logs')
    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=1)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=query,
    )
    query_id = start_query_response['queryId']

    response = None

    while response == None or response['status'] == 'Running':
        print('Waiting for query to complete')
        time.sleep(1)
        response = client.get_query_results(queryId=query_id)
    return response

        