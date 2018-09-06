from Common import Config
from . import AzureResourceServiceConfig
from . import AzureCredentialConfig
from . import AzureStorageConfig
from . import AzureCosmosDbConfig


class AzureConfig:
    def __init__(self, config: Config):
        self._config = config

    @property
    def credential_config(self):
        return AzureCredentialConfig(
            self._config.get_property('AZURE_CLIENT_ID'),
            self._config.get_property('AZURE_TENANT_ID'),
            self._config.get_property('AZURE_CLIENT_SECRET')
        )

    def get_resource_config(self, subscription_id):
        return AzureResourceServiceConfig(
            subscription_id,
            self.credential_config
        )

    @property
    def storage_config(self):
        return AzureStorageConfig(
            self._config.get_property('AZURE_STORAGE_ACCOUNT'),
            self._config.get_property('AZURE_STORAGE_KEY')
        )

    @property
    def cosmos_storage_config(self):
        return AzureCosmosDbConfig(
            self._config.get_property('AZURE_COSMOS_TABLE'),
            AzureStorageConfig(
                self._config.get_property('AZURE_COSMOS_ACCOUNT'),
                self._config.get_property('AZURE_COSMOS_KEY')
            ))

    @property
    def task_queue_name(self):
        return self._config.get_property('AZURE_TASK_QUEUE_NAME')

    @property
    def payload_queue_name(self):
        return self._config.get_property('AZURE_PAYLOAD_QUEUE_NAME')

    @property
    def config_container_name(self):
        return self._config.get_property('AZURE_CONFIG_CONTAINER')
