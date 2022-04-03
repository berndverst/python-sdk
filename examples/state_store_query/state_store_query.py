
"""
dapr run python3 state_store_query.py
"""

import asyncio
from dapr.clients import DaprClient

import json


async def runAsync():
    with DaprClient() as d:
        storeName = 'statestore'

        # Wait for sidecar to be up within 5 seconds.
        await d.wait(5)

        # Query the state store

        query = open('query.json', 'r').read()
        res = await d.query_state(store_name=storeName, query=query)
        for r in res.results:
            print(r.key, json.dumps(json.loads(str(r.value, 'UTF-8')), sort_keys=True))
        print("Token:", res.token)

        # Get more results using a pagination token

        query = open('query-token.json', 'r').read()
        res = await d.query_state(store_name=storeName, query=query)
        for r in res.results:
            print(r.key, json.dumps(json.loads(str(r.value, 'UTF-8')), sort_keys=True))
        print("Token:", res.token)

asyncio.run(runAsync())
