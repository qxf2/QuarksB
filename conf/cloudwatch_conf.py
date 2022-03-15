"""
You can add details of the log group and the message to look for in clowatch in this configuration file
"""

log_group = "/aws/lambda/staging-newsletter-url-filter"
query = f"fields @timestamp, @message|filter @message like 'This is a test message'"
