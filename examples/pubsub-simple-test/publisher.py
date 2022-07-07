# ------------------------------------------------------------
# Copyright 2022 The Dapr Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------

import json
import time

from dapr.clients import DaprClient
from cloudevents.http import CloudEvent, to_binary

with DaprClient() as d:
    id = 0
    while id < 3:
        id += 1

        attributes = {
  "id" : "name:test_server;lsn:33227720;txId:578",
  "source" : "/debezium/postgresql/test_server",
  "specversion" : "1.0",
  "type" : "io.debezium.postgresql.datachangeevent",
  "time" : "2020-01-13T14:04:18.597Z",
  "datacontenttype" : "application/avro",            
  "dataschema" : "http://my-registry/schemas/ids/1", 
  "iodebeziumop" : "r",
  "iodebeziumversion" : "1.9.4.Final",
  "iodebeziumconnector" : "postgresql",
  "iodebeziumname" : "test_server",
  "iodebeziumtsms" : "1578924258597",
  "iodebeziumsnapshot" : "true",
  "iodebeziumdb" : "postgres",
  "iodebeziumschema" : "s1",
  "iodebeziumtable" : "a",
  "iodebeziumtxId" : "578",
  "iodebeziumlsn" : "33227720",
  "iodebeziumxmin" : None,
  "iodebeziumtxid": "578",
  "iodebeziumtxtotalorder": "1",
  "iodebeziumtxdatacollectionorder": "1",                 
}
        
        req_data = {
            'id': id,
            'message': 'hello world'
        }

        event = CloudEvent(attributes=attributes, data=req_data)

        headers, body = to_binary(event)

        print(body)

        # Create a typed message with content type and body
        resp = d.publish_event(
            pubsub_name='pubsub',
            topic_name='TOPIC_A',
            data=json.dumps(req_data),
            data_content_type='application/octet-stream',
        )

        # Print the request
        print(req_data, flush=True)

        time.sleep(1)
