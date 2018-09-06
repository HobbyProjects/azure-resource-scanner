from Common.Contracts.account_service import AccountService
from azure.mgmt.resource.subscriptions import SubscriptionClient
from .Config import AzureCredentialConfig


class AzureSubscriptionService(AccountService):

    def __init__(self, config: AzureCredentialConfig):
        self._client = SubscriptionClient(config.credentials)

    @property
    def accounts(self):
        return [sub.serialize(True) for sub in self._client.subscriptions.list()]
