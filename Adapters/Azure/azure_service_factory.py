from Common.Contracts import ServiceFactory

from .azure_cosmosdb import AzureCosmosDb
from .azure_storage_queue import AzureStorageQueue
from .azure_resource_service import AzureResourceService
from .azure_subscription_service import AzureSubscriptionService
from .azure_storage_container import AzureStorageContainer
from .azure_config_generator import AzureConfigGenerator

from .Config import AzureConfig


class AzureServiceFactory(ServiceFactory):

    def __init__(self, config: AzureConfig):
        self._config = config
        self._resource_services = dict()

    def table_storage(self):
        return AzureCosmosDb(self._config.cosmos_storage_config)

    def queue(self, name):
        return AzureStorageQueue(
            name,
            self._config.storage_config)

    def _create_resource_service(self, subscription_id):
        return AzureResourceService(self._config.get_resource_config(subscription_id))

    def resource_service(self, subscription_id):
        if subscription_id not in self._resource_services:
            self._resource_services[subscription_id] = self._create_resource_service(subscription_id)
        return self._resource_services[subscription_id]

    def account_service(self):
        return AzureSubscriptionService(self._config.credential_config)

    def config_container(self):
        return AzureStorageContainer(self._config.config_container_name, self._config.storage_config)

    def config_generator(self):
        return AzureConfigGenerator(self.account_service())
