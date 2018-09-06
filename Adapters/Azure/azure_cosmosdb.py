from azure.cosmosdb.table.tableservice import TableService
from Common.Contracts import TableStorage
from .Config import AzureCosmosDbConfig
from Common.Helpers import entry_storage


class AzureCosmosDb(TableStorage):

    def __init__(self, config:AzureCosmosDbConfig):
        self._tableService = TableService(account_name=config.account_name, account_key=config.account_key)
        self._tableName = config.table_name

    def check_entry_exists(self, entry):
        try:
            self.query(entry['PartitionKey'], entry['RowKey'])
            return True
        except:
            return False

    def write(self, entry):
        prepared = entry_storage.EntryOperations.prepare_entry_for_insert(entry)

        if not self.check_entry_exists(prepared):
            self._tableService.insert_entity(self._tableName, prepared)
        else:
            self._tableService.update_entity(self._tableName, prepared)

    def query(self, partitionkey, rowkey):
        task = self._tableService.get_entity(self._tableName, partitionkey, rowkey)
        return task

    def delete(self, partitionkey, rowkey):
        self._tableService.delete_entity(self._tableName, partitionkey, rowkey)
