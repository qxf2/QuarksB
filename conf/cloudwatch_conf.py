"""
Configuration details for Cloudwatch logs
"""
log_group = '/aws/lambda/staging-newsletter-url-filter'

query = "fields @message | parse @message \"*, live:*, 19:*\" as msg, user, channel | filter user like /\./"
