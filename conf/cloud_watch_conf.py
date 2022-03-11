"""
The config file will list config details for aws configuration
"""

# settings for qxf2-employee-messages
log_group = '/aws/lambda/staging-newsletter-url-filter'

#settings for qxf2-skype-sender
query = f"fields @timestamp, @message|filter @message like 'Test message received on, 19:1941d15dada14943b5d742f2acdb99aa@thread.skype'"
