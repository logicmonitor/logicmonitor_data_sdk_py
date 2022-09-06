import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
from logicmonitor_data_sdk.models.map_string_string import MapStringString

description = 'This is description test.'
display_name = 'testDisplayName'
name = 'testName'
properties = MapStringString()
instance_id = 7

datasourceInstance = DataSourceInstance("name")


class TestDatasourceInstance(TestCase):
    def setUp(self) -> None:
        datasourceInstance.description = description
        datasourceInstance.display_name = display_name
        datasourceInstance.name = name
        datasourceInstance.properties = properties
        datasourceInstance.instance_id = instance_id

    def test_description(self):
        result = datasourceInstance.description
        self.assertEqual(description, result)

    def test_display_name(self):
        result = datasourceInstance.display_name
        self.assertEqual(display_name, result)

    def test_name(self):
        result = datasourceInstance.name
        self.assertEqual(name, result)

    def test_properties(self):
        result = datasourceInstance.properties
        self.assertEqual(properties, result)

    def test_instanceId(self):
        result = datasourceInstance.instance_id
        self.assertEqual(instance_id, result)

    def test_to_str(self):
        expected = pprint.pformat({'description': 'This is description test.',
                                   'display_name': 'testDisplayName',
                                   'instance_id': 7,
                                   'name': 'testName',
                                   'properties': {}})
        self.assertEqual(expected, datasourceInstance.to_str())

    def test_to_dict(self):
        expected = {'description': 'This is description test.', 'display_name': 'testDisplayName', 'name': 'testName', 'properties': {}, 'instance_id': 7}
        self.assertDictEqual(expected, datasourceInstance.to_dict())


if __name__ == '__main__':
    unittest.main()
