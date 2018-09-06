from abc import ABC, abstractmethod


class TableStorage(ABC):

    @abstractmethod
    def write(self, entry):
        raise NotImplementedError("Should have implemented write_entry")

    def write_entries(self, entries):
        for entry in entries:
            self.write(entry)

    @abstractmethod
    def query(self, partitionkey, rowkey):
        raise NotImplementedError("Should have implemented query")

    @abstractmethod
    def delete(self, partitionkey, rowkey):
        raise NotImplementedError("Should have implemented delete")
