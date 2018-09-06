import Common

from azure.storage.queue import QueueService, QueueMessageFormat
from .Config import AzureStorageConfig


class AzureStorageQueue(Common.Contracts.Queue):

    def __init__(self, queue_name, config: AzureStorageConfig):
        self._queue_name = queue_name
        self._queue_service = QueueService(account_name=config.account_name, account_key=config.account_key)

        self._queue_service.encode_function = QueueMessageFormat.text_base64encode
        self._queue_service.decode_function = QueueMessageFormat.text_base64decode

    def push(self, message):
        self._queue_service.create_queue(self._queue_name)
        self._queue_service.put_message(self._queue_name, message)

    def pop(self):
        self._queue_service.create_queue(self._queue_name)
        messages = self._queue_service.peek_messages(self._queue_name)
        for message in messages:
            result = message.content
            self._queue_service.delete_message(self._queue_name, message.id, message.pop_receipt)
            return result

    def peek(self):
        self._queue_service.create_queue(self._queue_name)
        messages = self._queue_service.peek_messages(self._queue_name)
        for message in messages:
            return message.content
