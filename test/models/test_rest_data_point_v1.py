import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.rest_data_point_v1 import RestDataPointV1
from logicmonitor_data_sdk.models.map_string_string import MapStringString

data_point_name = 'name'
values = MapStringString()
data_point_aggregation_type = 'percentile'
data_point_description = 'This is description test.'
data_point_type = 'counter'

restDataPointV1 = RestDataPointV1()


class TestRestDataPointV1(TestCase):
    def setUp(self) -> None:
        restDataPointV1.data_point_description = data_point_description
        restDataPointV1.data_point_type = data_point_type
        restDataPointV1.data_point_name = data_point_name
        restDataPointV1.data_point_aggregation_type = data_point_aggregation_type
        restDataPointV1.values = values

    def test_data_point_aggregation_type(self):
        self.assertEqual(data_point_aggregation_type, restDataPointV1.data_point_aggregation_type)

    def test_data_point_description(self):
        self.assertEqual(data_point_description, restDataPointV1.data_point_description)

    def test_data_point_name(self):
        self.assertEqual(data_point_name, restDataPointV1.data_point_name)

    def test_data_point_type(self):
        self.assertEqual(data_point_type, restDataPointV1.data_point_type)

    def test_values(self):
        self.assertEqual(values, restDataPointV1.values)

    def test_to_dict(self):
        expected = {'data_point_aggregation_type': 'percentile', 'data_point_description': 'This is description test.',
                    'data_point_name': 'name', 'data_point_type': 'counter', 'percentile': None, 'values': {}}
        self.assertDictEqual(expected, restDataPointV1.to_dict())

    def test_to_str(self):
        expected = pprint.pformat(
            {'data_point_aggregation_type': 'percentile', 'data_point_description': 'This is description test.',
             'data_point_name': 'name', 'data_point_type': 'counter', 'percentile': None, 'values': {}})
        self.assertEqual(expected, restDataPointV1.to_str())


if __name__ == '__main__':
    unittest.main()
