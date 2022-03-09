from botocore.config import Config

PROFILE_NAME='qxf2'
log_group = '/aws/lambda/staging-newsletter-url-filter'
config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)

# cloodwatch configuration for staging-newsletter-url-filter
query = f"fields @timestamp, @message | sort @timestamp desc | limit 10 | filter strcontains(@message,%s)"