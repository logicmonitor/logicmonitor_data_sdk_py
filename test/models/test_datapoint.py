import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.datapoint import DataPoint

name = 'name'
percentile = 1
aggregation_type = 'percentile'
description = 'This is description test.'
type = 'counter'

datapoint = DataPoint(name)


class TestDataPoint(TestCase):
    def setUp(self):
        datapoint.aggregation_type = aggregation_type
        datapoint.description = description
        datapoint.percentile = percentile
        datapoint.type = type

    def test_aggregation_type(self):
        result = datapoint.aggregation_type
        self.assertEqual(aggregation_type, result)

    def test_description(self):
        result = datapoint.description
        self.assertEqual(description, result)

    def test_name(self):
        result = datapoint.name
        self.assertEqual(name, result)

    def test_type(self):
        result = datapoint.type
        self.assertEqual(type, result)

    def test_percentile(self):
        result = datapoint.percentile
        self.assertEqual(percentile, result)

    def test_to_str(self):
        expected = pprint.pformat(
            {'aggregation_type': 'percentile', 'description': 'This is description test.', 'name': 'name', 'percentile': 1,
             'type': 'counter'})
        self.assertEqual(expected, datapoint.to_str())

    def test_to_dict(self):
        expected = {'aggregation_type': 'percentile', 'description': 'This is description test.', 'name': 'name', 'type': 'counter', 'percentile': 1}
        self.assertDictEqual(expected, datapoint.to_dict())

    def test_valid_field(self):
        self.assertEqual('', datapoint.valid_field())


if __name__ == '__main__':
    unittest.main()
