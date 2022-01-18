# cloodwatch configuration for url filter lambda
url_filter_log_group = '/aws/lambda/URLFilteringLambdaRohini'
query_url_filter = f"fields @timestamp, @message|filter @message like 'This is a test message -'"

# cloudwatch log dictionary keys
message_value = 'results_0_1_value'
record_body = 'logRecord_Records.0.body'
record_messageid = 'logRecord_Records.0.messageId'