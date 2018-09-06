from Common.Contracts import ConfigGenerator
from .azure_subscription_service import AzureSubscriptionService
import json
from datetime import datetime


class AzureConfigGenerator(ConfigGenerator):

    def __init__(self, subscription_service: AzureSubscriptionService):
        self._subscription_service = subscription_service

    def generate_config(self, types: list):
        subs = []
        for sub in self._subscription_service.accounts:
            subs.append({
                'subscriptionId': sub['subscriptionId'],
                'displayName': sub['displayName']
            })
        resource_types = []
        for t in types:
            resource_types.append({
                'typeName': t
            })
        return json.dumps({
            'subscriptions': subs,
            'resourceTypes': resource_types
        })

    def output_config(self, container, config):
        blob_name = 'config-{date:%Y-%m-%d-%H-%M-%S}.json'.format(date=datetime.now())
        container.upload_text(blob_name, config)
