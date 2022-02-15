"""
Queue conf
"""
from botocore.config import Config

SQS_NAME = "staging-newsletter-generator"
#SQS_NAME = "https://sqs.ap-south-1.amazonaws.com/285993504765/staging-newsletter-generator"
config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)
