import asyncio
import json
import time

from dapr.clients import DaprClient


async def runAsync():
    async with DaprClient() as d:
        req_data = {
            'id': 1,
            'message': 'hello world'
        }

        while True:
            # Create a typed message with content type and body
            resp = await d.invoke_method(
                'invoke-receiver',
                'my-method',
                data=json.dumps(req_data),
            )

            # Print the response
            print(resp.content_type, flush=True)
            print(resp.text(), flush=True)

            time.sleep(2)

asyncio.run(runAsync())
