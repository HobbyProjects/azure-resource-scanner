from azure.mgmt.resource import ResourceManagementClient
from Common.Contracts import ResourceService, ResourceFilter
from .Config import AzureResourceServiceConfig
from .azure_resource import AzureResource

import logging


class NoFilter(ResourceFilter):
    def normalized_filter(self):
        return None


class AzureResourceTypeFilter(ResourceFilter):
    def __init__(self, resource_type):
        self._filter = "resourceType eq '" + resource_type + "'"

    def normalized_filter(self):
        return self._filter


class AzureResourceService(ResourceService):
    def __init__(self, config: AzureResourceServiceConfig):
        self._client = ResourceManagementClient(config.credentials, config.subscription_id)
        self._resource_type_apis = dict()

        self._knownTypes = {
            'vm': 'Microsoft.Compute/virtualMachines',
            'storage': 'Microsoft.Storage/storageAccounts',
            'Microsoft.Compute/virtualMachines': 'Microsoft.Compute/virtualMachines',
            'Microsoft.Storage/storageAccounts': 'Microsoft.Storage/storageAccounts'
        }

    def get_resources(self, filter: ResourceFilter=None):
        resources = self._client.resources.list(expand="tags", filter=filter.normalized_filter())
        return [AzureResource(resource.serialize(True)) for resource in resources]

    def get_filter(self, payload):
        try:
            resource_type = self._knownTypes[payload.lower()]
            return AzureResourceTypeFilter(resource_type)
        except AttributeError:
            return NoFilter()
        except KeyError:
            logging.warning("The filter " + payload + " is not supported and will be ignored")
            return NoFilter()
        except Exception:
            raise NotImplementedError("The payload " + payload + " is not a supported filter")

    def update_resource(self, resource: AzureResource):
        api_version = self._resolve_api_for_resource_type(resource.type)
        if api_version is None:
            raise Exception(f"Unabled to find api version to update {resource.id}")

        self._client.resources.update_by_id(resource.id, api_version, resource.to_dict())

    # Internal Helper function to resolve API version to access Azure with
    def _resolve_api_for_resource_type(self, resource_type):
        if resource_type in self._resource_type_apis:
            return self._resource_type_apis[resource_type]

        resource_type_info = resource_type.split('/', 1)
        resource_provider = resource_type_info[0]
        resource_provider_type = resource_type_info[1]

        provider = self._client.providers.get(resource_provider)
        provider_details = next((t for t in provider.resource_types
            if t.resource_type == resource_provider_type), None)

        if provider_details and 'api_versions' in provider_details.__dict__:
            # Remove preview API versions
            api_version = [v for v in provider_details.__dict__['api_versions'] if 'preview' not in v.lower()]
            # Get most recent remaining API
            chosen_api = api_version[0] if api_version else provider_details.__dict__['api_versions'][0]
            self._resource_type_apis[resource_type] = chosen_api

            return chosen_api

        return None
