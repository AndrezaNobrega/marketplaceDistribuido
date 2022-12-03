import asyncio
import time
from .peers import marketplaces


async def orderEvent(items):
    # await res from all peers
    print('orderEvent')
    time.sleep(5)
    return 'OK'