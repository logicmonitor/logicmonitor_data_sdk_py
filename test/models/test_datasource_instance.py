import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
from logicmonitor_data_sdk.models.map_string_string import MapStringString

description = 'This is description test.'
display_name = 'testDisplayName'
name = 'testName'
properties = MapStringString()
instanceId = 7

datasourceinstance = DataSourceInstance()

class TestDataSourceInstance(TestCase):
    def setUp(self) -> None:
        datasourceinstance.description = description
        datasourceinstance.display_name = display_name
        datasourceinstance.name = name
        datasourceinstance.properties = properties
        datasourceinstance.instanceId = instanceId

    def test_description(self):
        result = datasourceinstance.description
        self.assertEqual(description,result)

    def test_display_name(self):
        result = datasourceinstance.display_name
        self.assertEqual(display_name,result)

    def test_name(self):
        result = datasourceinstance.name
        self.assertEqual(name,result)

    def test_properties(self):
        result = datasourceinstance.properties
        self.assertEqual(properties,result)

    def test_instanceId(self):
        result = datasourceinstance.instanceId
        self.assertEqual(instanceId,result)

    def test_to_str(self):
        expected = pprint.pformat({'description': 'This is description test.',
                                   'display_name': 'testDisplayName',
                                   'instanceId': 7,
                                   'name': 'testName',
                                   'properties': {}})
        self.assertEqual(expected,datasourceinstance.to_str())

    def test_to_dict(self):
        expected = {'description': 'This is description test.', 'display_name': 'testDisplayName', 'name': 'testName', 'properties': {}, 'instanceId': 7}
        self.assertDictEqual(expected,datasourceinstance.to_dict())

if __name__ == '__main__':
    unittest.main()