import logging
import azure.functions

from Common.scheduler import create_tasks, read_config_from_blob, push_tasks_to_queue
from Adapters.Azure import AzureConfig, AzureServiceFactory
from Common import Config


def main(timer: azure.functions.TimerRequest):

    config_reader = Config()
    azure_config = AzureConfig(config_reader)
    factory = AzureServiceFactory(azure_config)
    blob_service = factory.config_container()
    queue = factory.queue(azure_config.task_queue_name)

    config = read_config_from_blob(blob_service)

    if not config:
        logging.error("No config found")

    tasks = create_tasks(config)
    push_tasks_to_queue(queue, tasks)
