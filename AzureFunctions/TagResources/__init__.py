import logging

from Adapters.Azure import AzureConfig, AzureServiceFactory, AzureResource
from Common import ResourceTagger, Config

from azure.functions import QueueMessage


def parse_message(msg):
        logging.info(f"Processing queue message {msg.id}")

        # Convert message into a list if it isn't already
        resource_list = msg.get_json()
        if not isinstance(resource_list, list):
            resource_list = [resource_list]

        logging.info(f"Found {len(resource_list)} resources to process")

        resource_list = [AzureResource(resource) for resource in resource_list]

        return resource_list


def main(msg: QueueMessage):
    config = Config()
    azure_config = AzureConfig(config)
    factory = AzureServiceFactory(azure_config)
    table_storage = factory.table_storage()

    resource_tags = {
        'tag1': 'value'
    }
    resource_tagger = ResourceTagger(factory, resource_tags)

    resources = parse_message(msg)

    for resource in resources:
        resource_tagger.execute(resource)
        table_storage.write_entries(resource.to_dict())
