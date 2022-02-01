import asyncio
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_channel_conf as skc
from helpers import async_run as ar
from concurrent.futures import ThreadPoolExecutor

def test_sqs_message_received():
    """
    Validate message correctness between Skype and SQS
    """
    result = asyncio.run(ar.main())
    with pytest.raises(Exception) as exception:
        print(f'Exception: {exception}')
        raise Exception('Pytest Exception')
    sqs_msgs = result[1]
    assert skc.MESSAGE in sqs_msgs, 'Message mismatch between Skype and SQS!'
    
    