from Common.Contracts import ServiceFactory
from . import QueueSimulator
from . import TableStorageSimulator
from . import ResourceServiceSimulator
from . import MockBlobStorageSimulator

class ServiceFactorySimulator(ServiceFactory):

    def table_storage(self):
        return TableStorageSimulator()

    def resource_service(self, subscription_id):
        return ResourceServiceSimulator()

    def account_service(self):
        raise NotImplementedError("account_service is not implemented")

    def queue(self, name):
        return QueueSimulator(name, None)

    def config_container(self):
        return MockBlobStorageSimulator()

    def config_generator(self):
        raise NotImplementedError("config_generator is not implemented")

