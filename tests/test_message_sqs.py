"""
Test script to
 - validate message sent to Skype channel against the message received on SQS
"""
import asyncio
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf as skc
from helpers import parallel_processing as pp

def test_message_received_sqs():
    """
    Validate message correctness between Skype and SQS
    """
    result = asyncio.run(pp.main())
    with pytest.raises(Exception) as exception:
        print(f'\nException: {exception}')
        raise Exception('Pytest Exception!')
    sqs_msgs = result[1]
    if sqs_msgs:
        assert skc.MESSAGE in sqs_msgs, 'Message mismatch between Skype and SQS!'
