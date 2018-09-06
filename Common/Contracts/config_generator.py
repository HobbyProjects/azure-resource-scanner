from abc import ABC, abstractmethod
from Common.Contracts import StorageContainer


class ConfigGenerator(ABC):

    @abstractmethod
    def generate_config(self, types):
        raise NotImplementedError("generate_config not implemented")

    @abstractmethod
    def output_config(self, container: StorageContainer, config):
        raise NotImplementedError("output_config not implemented")

    def execute(self, types, container: StorageContainer):
        config = self.generate_config(types)
        self.output_config(container, config)
