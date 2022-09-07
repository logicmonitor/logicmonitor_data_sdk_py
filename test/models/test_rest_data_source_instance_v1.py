import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.rest_data_source_instance_v1 import RestDataSourceInstanceV1
from logicmonitor_data_sdk.models.list_rest_data_point_v1 import ListRestDataPointV1
from logicmonitor_data_sdk.models.map_string_string import MapStringString

instance_description = 'This is description test.'
instance_display_name = 'testDisplayName'
instance_name = 'testName'
instance_group = 'testGroupName'
instance_properties = MapStringString()
data_points = ListRestDataPointV1()

restDataSourceInstanceV1 = RestDataSourceInstanceV1()


class TestRestDataSourceInstanceV1(TestCase):
    def setUp(self) -> None:
        restDataSourceInstanceV1.instance_description = instance_description
        restDataSourceInstanceV1.instance_display_name = instance_display_name
        restDataSourceInstanceV1.instance_name = instance_name
        restDataSourceInstanceV1.instance_group = instance_group
        restDataSourceInstanceV1.instance_properties = instance_properties
        restDataSourceInstanceV1.data_points = data_points

    def test_instance_description(self):
        result = restDataSourceInstanceV1.instance_description
        self.assertEqual(instance_description, result)

    def test_instance_display_name(self):
        result = restDataSourceInstanceV1.instance_display_name
        self.assertEqual(instance_display_name, result)

    def test_instance_name(self):
        result = restDataSourceInstanceV1.instance_name
        self.assertEqual(instance_name, result)

    def test_instance_properties(self):
        result = restDataSourceInstanceV1.instance_properties
        self.assertEqual(instance_properties, result)

    def test_instance_group(self):
        result = restDataSourceInstanceV1.instance_group
        self.assertEqual(instance_group, result)

    def test_data_points(self):
        self.assertEqual(data_points, restDataSourceInstanceV1.data_points)

    def test_to_str(self):
        expected = pprint.pformat({'data_points': {},
                                   'instance_description': 'This is description test.',
                                   'instance_display_name': 'testDisplayName',
                                   'instance_group': 'testGroupName',
                                   'instance_name': 'testName',
                                   'instance_properties': {}})
        self.assertEqual(expected, restDataSourceInstanceV1.to_str())

    def test_to_dict(self):
        expected = {'data_points': {},
                    'instance_description': 'This is description test.',
                    'instance_display_name': 'testDisplayName',
                    'instance_group': 'testGroupName',
                    'instance_name': 'testName',
                    'instance_properties': {}}
        self.assertDictEqual(expected, restDataSourceInstanceV1.to_dict())


if __name__ == '__main__':
    unittest.main()
