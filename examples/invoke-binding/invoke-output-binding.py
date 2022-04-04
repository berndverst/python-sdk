import json
import time
import asyncio

from dapr.clients import DaprClient


async def runAsync():
    async with DaprClient() as d:
        n = 0
        while True:
            n += 1
            req_data = {
                'id': n,
                'message': 'hello world'
            }

            print(f'Sending message id: {req_data["id"]}, message "{req_data["message"]}"',
                  flush=True)

            # Create a typed message with content type and body
            await d.invoke_binding('kafkaBinding', 'create', json.dumps(req_data))

            time.sleep(1)


asyncio.run(runAsync())
