"""
Helper to run tasks in parallel
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import aws_sqs_queues
from helpers import skype_as_producer
import asyncio
skype_obj = skype_as_producer.Skype()
queue_obj = aws_sqs_queues.AWS_Queues()

async def main():
    "Define the tasks to be run in parallel"
    msg = []
    msg.append(skype_obj.post_message_on_skype())
    await asyncio.sleep(1)
    msg.append(queue_obj.get_messages_from_sqs())
    await asyncio.sleep(1)
    result = await asyncio.gather(*msg)
    return result