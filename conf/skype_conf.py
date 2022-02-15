"""
Skype conf
"""
import random
import time

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
#MESSAGE = 'This is a test message - ' + ''.join(random.choices(['s', 'h', 'i', 'v', 'a']))
# Can the message change to use time.time()? That gives us infinite variety.
MESSAGE = 'This is a test message - ' + ''.join(time.time().__str__().split('.'))
