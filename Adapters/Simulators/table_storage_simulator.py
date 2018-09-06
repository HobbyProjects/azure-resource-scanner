from Common.Contracts import TableStorage
from Common.Helpers import entry_storage


class TableStorageSimulator(TableStorage):

    def __init__(self):
        self._data = dict()

    # entry is of json type
    def write(self, entry):
        prepared = entry_storage.EntryOperations.prepare_entry_for_insert(entry)
        key = entry['PartitionKey'] + '-' + entry['RowKey']
        self._data[key] = prepared

    def query(self, partitionkey, rowkey):
        task = self._data[partitionkey + '-' + rowkey]
        return task

    def delete(self, partitionkey, rowkey):
        del self._data[partitionkey + '-' + rowkey]
