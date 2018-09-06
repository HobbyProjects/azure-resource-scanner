from . import AzureCredentialConfig


class AzureResourceServiceConfig:
    def __init__(self, subscription_id, creds: AzureCredentialConfig):
        self.credentials = creds.credentials
        self.subscription_id = subscription_id
