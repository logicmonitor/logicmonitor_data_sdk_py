import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.rest_instance_properties_v1 import RestInstancePropertiesV1
from logicmonitor_data_sdk.models.map_string_string import MapStringString

data_source = 'testDS'
data_source_display_name = 'testDisplayName'
instance_name = 'testInstanceName'
instance_properties = MapStringString()
resource_ids = MapStringString()

restInstancePropertiesV1 = RestInstancePropertiesV1()


class TsetRestInstancePropertiesV1(TestCase):
    def setUp(self) -> None:
        restInstancePropertiesV1.instance_properties = instance_properties
        restInstancePropertiesV1.instance_name = instance_name
        restInstancePropertiesV1.data_source_display_name = data_source_display_name
        restInstancePropertiesV1.data_source = data_source
        restInstancePropertiesV1.resource_ids = resource_ids

    def test_data_source(self):
        self.assertEqual(data_source, restInstancePropertiesV1.data_source)

    def test_data_source_display_name(self):
        self.assertEqual(data_source_display_name, restInstancePropertiesV1.data_source_display_name)

    def test_instance_name(self):
        self.assertEqual(instance_name, restInstancePropertiesV1.instance_name)

    def test_instance_properties(self):
        self.assertEqual(instance_properties, restInstancePropertiesV1.instance_properties)

    def test_resource_ids(self):
        self.assertEqual(resource_ids, restInstancePropertiesV1.resource_ids)

    def test_to_dict(self):
        expected = {'data_source': 'testDS', 'data_source_display_name': 'testDisplayName',
                    'instance_name': 'testInstanceName', 'instance_properties': {}, 'resource_ids': {}}
        self.assertDictEqual(expected, restInstancePropertiesV1.to_dict())

    def test_to_str(self):
        expected = pprint.pformat({'data_source': 'testDS', 'data_source_display_name': 'testDisplayName',
                                   'instance_name': 'testInstanceName', 'instance_properties': {}, 'resource_ids': {}})
        self.assertEqual(expected, restInstancePropertiesV1.to_str())


if __name__ == '__main__':
    unittest.main()
