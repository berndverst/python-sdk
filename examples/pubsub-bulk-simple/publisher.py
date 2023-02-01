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

from dapr.clients import DaprClient

data = []
id = 0
while id < 3:
    id += 1
    data.append(
        json.dumps(
            {
                'id': id,
                'message': 'hello world'
            }
        )
    )

with DaprClient() as d:
    # Create a typed message with content type and body
    resp = d.publish_event_bulk(
        pubsub_name='pubsub',
        topic_name='TOPIC_A',
        data=data,
        data_content_type='application/json',
    )

    # Print the request
    print(data, flush=True)
