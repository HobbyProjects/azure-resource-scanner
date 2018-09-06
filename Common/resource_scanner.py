import logging
from Common.Contracts import ServiceFactory, Queue
import json


class ResourceScanner:
    def __init__(self, factory: ServiceFactory, output_queue: Queue):
        self._factory = factory
        self._queue = output_queue

    def execute(self, message):
        subscription_id = message.get('subscriptionId')
        if subscription_id is None:
            raise Exception("Couldn't find a subscriptionId for the task: " + json.dumps(message))
        r_type = message.get('typeName', None)
        logging.info(f"Received task for subscription {subscription_id} and resource type {r_type}")
        reader = self._factory.resource_service(subscription_id)
        filter = reader.get_filter(r_type)
        resources = reader.get_resources(filter)

        if self._queue:
            for resource in resources:
                self._queue.push(json.dumps(resource.to_dict()))
