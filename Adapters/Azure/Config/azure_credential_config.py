from azure.common.credentials import ServicePrincipalCredentials


class AzureCredentialConfig:
    def __init__(self, client_id, tenant, secret):
        self.clientId = client_id
        self.secret = secret
        self.tenant = tenant

    @property
    def credentials(self):
        return ServicePrincipalCredentials(
            self.clientId,
            self.secret,
            tenant=self.tenant)
