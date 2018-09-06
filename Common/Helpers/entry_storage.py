import json
import uuid


class EntryOperations:
    @staticmethod
    def prepare_entry_for_insert(json_entry):

        # using location as the partition key. This will keep all the data from
        # the same location on the same node for fastest access
        location = json_entry['location']
        json_entry['PartitionKey'] = location
        json_entry['RowKey'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, json_entry['id']))
        data_to_write = json.dumps(json_entry)
        dict = json.loads(data_to_write)

        # cosmos does not allow for an entry with key 'id'
        modified_data = {}
        for key, value in dict.items():
            if key == 'id':
                modified_data['resourceid'] = str(value)
            else:
                modified_data[key] = str(value)

        return modified_data
