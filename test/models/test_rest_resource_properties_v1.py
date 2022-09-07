import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.rest_resource_properties_v1 import RestResourcePropertiesV1
from logicmonitor_data_sdk.models.map_string_string import MapStringString

resource_ids = MapStringString()
resource_name = 'testResourceName'
resource_properties = MapStringString()

restResourcePropertiesV1 = RestResourcePropertiesV1()


class TestRestResourcePropertiesV1(TestCase):
    def setUp(self) -> None:
        restResourcePropertiesV1.resource_properties = resource_properties
        restResourcePropertiesV1.resource_ids = resource_ids
        restResourcePropertiesV1.resource_name = resource_name

    def test_resource_ids(self):
        self.assertDictEqual(resource_ids, restResourcePropertiesV1.resource_ids)

    def test_resource_name(self):
        self.assertEqual(resource_name, restResourcePropertiesV1.resource_name)

    def test_resource_properties(self):
        self.assertDictEqual(resource_properties, restResourcePropertiesV1.resource_properties)

    def test_to_dict(self):
        expected = {'resource_ids': {}, 'resource_name': 'testResourceName', 'resource_properties': {}}
        self.assertDictEqual(expected, restResourcePropertiesV1.to_dict())

    def test_to_str(self):
        expected = pprint.pformat({'resource_ids': {}, 'resource_name': 'testResourceName', 'resource_properties': {}})
        self.assertEqual(expected, restResourcePropertiesV1.to_str())


if __name__ == '__main__':
    unittest.main()
