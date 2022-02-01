"""
Helper to run tasks in parallel
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import queues
from helpers import skype

async def main():
    "Define the tasks to be run in parallel"
    skype_obj = skype.Skype()
    queue_obj = queues.Queues()
    tasks = []
    #Send message to Skype and receive message from SQS
    tasks.append(skype_obj.post_message_on_skype())
    tasks.append(queue_obj.get_messages_from_sqs())
    result = await asyncio.gather(*tasks)
    return result
