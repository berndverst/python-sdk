from fastapi import FastAPI
from fastapi.testclient import TestClient
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel

import unittest


class Message(BaseModel):
    body: str


class DaprAppTest(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.dapr_app = DaprApp(self.app)
        self.client = TestClient(self.app)

    def test_subscribe_subscription_registered(self):
        @self.dapr_app.subscribe(pubsub="pubsub", topic="test")
        def event_handler(event_data: Message):
            return "default route"

        self.assertEqual(len(self.dapr_app._subscriptions), 1)

        self.assertIn("/dapr/subscribe", [route.path for route in self.app.router.routes])
        self.assertIn("/events/pubsub/test", [route.path for route in self.app.router.routes])

        response = self.client.get("/dapr/subscribe")
        self.assertEqual(
            [{'pubsubname': 'pubsub',
                'topic': 'test',
                'route': '/events/pubsub/test',
                'metadata': {}
              }], response.json())

        response = self.client.post("/events/pubsub/test", json={"body": "new message"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"default route"')

    def test_subscribe_with_route_subscription_registered_with_custom_route(self):
        @self.dapr_app.subscribe(pubsub="pubsub", topic="test", route="/do-something")
        def event_handler(event_data: Message):
            return "custom route"

        self.assertEqual(len(self.dapr_app._subscriptions), 1)

        self.assertIn("/dapr/subscribe", [route.path for route in self.app.router.routes])
        self.assertIn("/do-something", [route.path for route in self.app.router.routes])

        response = self.client.get("/dapr/subscribe")
        self.assertEqual(
            [{'pubsubname': 'pubsub',
              'topic': 'test',
              'route': '/do-something',
              'metadata': {}
              }], response.json())

        response = self.client.post("/do-something", json={"body": "new message"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"custom route"')

    def test_subscribe_metadata(self):
        handler_metadata = {"rawPayload": "true"}

        @self.dapr_app.subscribe(pubsub="pubsub",
                                 topic="test",
                                 metadata=handler_metadata)
        def event_handler(event_data: Message):
            return "custom metadata"

        self.assertEqual((self.dapr_app._subscriptions[0]["metadata"]["rawPayload"]), "true")

        response = self.client.get("/dapr/subscribe")
        self.assertEqual(
            [{'pubsubname': 'pubsub',
              'topic': 'test',
              'route': '/events/pubsub/test',
              'metadata': {"rawPayload": "true"}
              }], response.json())

        response = self.client.post("/events/pubsub/test", json={"body": "new message"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"custom metadata"')
    
    def test_router_tag(self):
        app1 = FastAPI()
        app2 = FastAPI()
        DaprApp(app_instance=app1, router_tags=['MyTag', 'PubSub']).subscribe(
            pubsub="mypubsub", topic="test")
        DaprApp(app_instance=app2).subscribe(pubsub="mypubsub", topic="test")

        PATHS_WITH_EXPECTED_TAGS = [
            '/dapr/subscribe',
            '/events/mypubsub/test'
        ]

        foundTags = False
        for route in app1.router.routes:
            if hasattr(route, "tags"):
                self.assertIn(route.path, PATHS_WITH_EXPECTED_TAGS)
                self.assertEqual(['MyTag', 'PubSub'], route.tags)
                foundTags = True
        if not foundTags:
            self.fail('No tags found')
        
        foundTags = False
        for route in app2.router.routes:
            if hasattr(route, "tags"):
                self.assertIn(route.path, PATHS_WITH_EXPECTED_TAGS)
                self.assertEqual(['PubSub'], route.tags)
                foundTags=True
        if not foundTags:
            self.fail('No tags found')


if __name__ == '__main__':
    unittest.main()
