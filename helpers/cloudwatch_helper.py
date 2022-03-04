import boto3
from datetime import datetime, timedelta
import time

client = boto3.client('logs')

log_group = '/aws/lambda/staging-newsletter-url-filter'
#query = 'fields @timestamp, @message | filter logGroup in ["/aws/lambda/staging-newsletter-url-filter"]'
query="fields @timestamp, @message|filter @message like 'Test message received on, 19:1941d15dada14943b5d742f2acdb99aa@thread.skype'"

start_query_response = client.start_query(
    logGroupName=log_group,
    startTime=202202020000,    
    endTime=202203030000,
    queryString=query,
)

query_id = start_query_response['queryId']

response = client.get_query_results(queryId=query_id)
print(response)    
