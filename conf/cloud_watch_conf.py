"""
The config file will list config details for aws configuration
"""
# settings for logs
log_group = '/aws/lambda/staging-newsletter-url-filter'

#settings for qxf2-skype-sender
query_skype_sender = f"fields @timestamp, @message | filter strcontains(@message,\"This is \")| sort @timestamp desc"
#log_group_bot_sender='/aws/lambda/qxf2-bot-sender'

# cloudwatch log dictionary keys
ptr_value = 'results_0_1_value'
