from Common.Contracts import ResourceService, ResourceFilter
from Adapters.Azure import AzureResource


class ResourceServiceSimulator(ResourceService):

    resources = [{
                'id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/microsoft.insights/components/wwwwwwwwwwww',
                'name': 'wwwwwwwwwwww',
                'type': 'microsoft.insights/components',
                'location': 'southcentralus',
                'tags': {
                    'hidden-link:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/Microsoft.Web/sites/wwwwwwwwwwww': 'Resource'
                },
                'kind': 'web'
                }, {
                'id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/Microsoft.ServiceBus/namespaces/wwwwwwwwwwww',
                'name': 'wwwwwwwwwwww',
                'type': 'Microsoft.ServiceBus/namespaces',
                'location': 'southcentralus',
                'tags': {},
                'sku': {
                    'name': 'Standard',
                    'tier': 'Standard'
                }
                }, {
                'id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/Microsoft.Storage/storageAccounts/wwwwwwwwwwww',
                'name': 'wwwwwwwwwwww',
                'type': 'Microsoft.Storage/storageAccounts',
                'location': 'southcentralus',
                'tags': {},
                'kind': 'Storage',
                'sku': {
                    'name': 'Standard_LRS',
                    'tier': 'Standard'
                }
                }, {
                'id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/Microsoft.Web/serverFarms/wwwwwwwwwwww',
                'name': 'wwwwwwwwwwww',
                'type': 'Microsoft.Web/serverFarms',
                'location': 'southcentralus',
                'kind': 'functionapp'
                }, {
                'id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyyyyy/providers/Microsoft.Web/sites/wwwwwwwwwwww',
                'name': 'wwwwwwwwwwww',
                'type': 'Microsoft.Web/sites',
                'location': 'southcentralus',
                'kind': 'functionapp'
                }]

    def get_resources(self, filter: ResourceFilter=None):
        return [AzureResource(resource) for resource in self.resources]

    def update_resource(self, resource):
        return None

    def get_filter(self, payload) -> ResourceFilter:
        pass
