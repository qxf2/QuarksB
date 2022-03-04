"""
Queue conf
"""
from botocore.config import Config
import os

SQS_NAME = "staging-newsletter-generator"
config: os.environ['configuration']