import json

from mock import PropertyMock, MagicMock

from Adapters.Azure import AzureConfigGenerator
from Common.Test import TestCase


class ConfigGeneratorTest(TestCase):

    subs = [
        {'subscriptionId': '00000000-0000-0000-0000-000000000000',
         'displayName': 'Sub1'},
        {'subscriptionId': '00000000-0000-0000-0000-000000000001',
         'displayName': 'Sub2'}
    ]
    types = ['vm', 'storage']

    expected_config = {
        "subscriptions": [
            {"subscriptionId": "00000000-0000-0000-0000-000000000000",
             "displayName": "Sub1"},
            {"subscriptionId": "00000000-0000-0000-0000-000000000001",
             "displayName": "Sub2"}],
        "resourceTypes": [
            {"typeName": "vm"},
            {"typeName": "storage"}
        ]
    }

    def test_azure_generator(self):

        mock_sub_service = MagicMock()
        type(mock_sub_service).accounts = PropertyMock(return_value=self.subs)
        config_generator = AzureConfigGenerator(mock_sub_service)
        config = config_generator.generate_config(self.types)

        # Asserting both string comparison and dictionary comparison
        # just to show serialization/deserialization isn't a problem
        self.assertEqual(config, json.dumps(self.expected_config))
        self.assertDictEqual(json.loads(config), self.expected_config)
