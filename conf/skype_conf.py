"""
Skype conf
"""
import random
import time

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
time_str = time.asctime(time.localtime())
MESSAGE = 'This is a test message - ' + time_str
