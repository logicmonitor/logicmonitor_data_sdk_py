import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.rest_metrics_v1 import RestMetricsV1
from logicmonitor_data_sdk.models.list_rest_data_source_instance_v1 import ListRestDataSourceInstanceV1
from logicmonitor_data_sdk.models.map_string_string import MapStringString

data_source = 'testDS'
data_source_display_name = 'testDataSourceDisplayName'
data_source_group = 'testDataSourceGroup'
data_source_id = 7
instances = ListRestDataSourceInstanceV1()
resource_description = 'testResourceDescription'
resource_ids = MapStringString()
resource_name = 'testResourceName'
resource_properties = MapStringString()
singleInstanceDS = False

restMetricsV1 = RestMetricsV1()


class TestRestMetricsV1(TestCase):
    def setUp(self) -> None:
        restMetricsV1.data_source = data_source
        restMetricsV1.data_source_display_name = data_source_display_name
        restMetricsV1.data_source_group = data_source_group
        restMetricsV1.data_source_id = data_source_id
        restMetricsV1.instances = instances
        restMetricsV1.resource_description = resource_description
        restMetricsV1.resource_ids = resource_ids
        restMetricsV1.resource_name = resource_name
        restMetricsV1.resource_properties = resource_properties
        restMetricsV1.singleInstanceDS = singleInstanceDS

    def test_data_source(self):
        self.assertEqual(data_source, restMetricsV1.data_source)

    def test_data_source_display_name(self):
        self.assertEqual(data_source_display_name, restMetricsV1.data_source_display_name)

    def test_data_source_group(self):
        self.assertEqual(data_source_group, restMetricsV1.data_source_group)

    def test_data_source_id(self):
        self.assertEqual(data_source_id, restMetricsV1.data_source_id)

    def test_instances(self):
        self.assertEqual(instances, restMetricsV1.instances)

    def test_resource_description(self):
        self.assertEqual(resource_description, restMetricsV1.resource_description)

    def test_resource_ids(self):
        self.assertDictEqual(resource_ids, restMetricsV1.resource_ids)

    def test_resource_name(self):
        self.assertEqual(resource_name, restMetricsV1.resource_name)

    def test_resource_properties(self):
        self.assertDictEqual(resource_properties, restMetricsV1.resource_properties)

    def test_singleInstanceDS(self):
        self.assertEqual(singleInstanceDS, restMetricsV1.singleInstanceDS)

    def test_to_dict(self):
        expected = {'data_source': 'testDS', 'data_source_display_name': 'testDataSourceDisplayName',
                    'data_source_group': 'testDataSourceGroup', 'data_source_id': 7, 'instances': {},
                    'resource_description': 'testResourceDescription', 'resource_ids': {},
                    'resource_name': 'testResourceName', 'resource_properties': {}, 'singleInstanceDS': False}
        self.assertDictEqual(expected, restMetricsV1.to_dict())

    def test_to_str(self):
        expected = pprint.pformat({'data_source': 'testDS', 'data_source_display_name': 'testDataSourceDisplayName',
                                   'data_source_group': 'testDataSourceGroup', 'data_source_id': 7, 'instances': {},
                                   'resource_description': 'testResourceDescription', 'resource_ids': {},
                                   'resource_name': 'testResourceName', 'resource_properties': {},
                                   'singleInstanceDS': False})
        self.assertEqual(expected, restMetricsV1.to_str())


if __name__ == '__main__':
    unittest.main()
