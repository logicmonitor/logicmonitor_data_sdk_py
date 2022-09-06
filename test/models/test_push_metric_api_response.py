import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.push_metric_api_response import PushMetricAPIResponse
from logicmonitor_data_sdk.models.map_string_string import MapStringString

pushMetricAPIResponse = PushMetricAPIResponse()

message = 'Test Message'
resource_ids = MapStringString()
timestamp = 123456789


class TestPushMetricAPIResponse(TestCase):
    def setUp(self) -> None:
        pushMetricAPIResponse.message = message
        pushMetricAPIResponse.timestamp = timestamp
        pushMetricAPIResponse.resource_ids = resource_ids

    def test_message(self):
        self.assertEqual(message, pushMetricAPIResponse.message)

    def test_timestamp(self):
        self.assertEqual(timestamp, pushMetricAPIResponse.timestamp)

    def test_resource_ids(self):
        self.assertEqual(resource_ids, pushMetricAPIResponse.resource_ids)

    def test_to_dict(self):
        expected = {'code': None, 'errors': None, 'message': 'Test Message', 'resource_ids': {}, 'timestamp': 123456789}
        self.assertDictEqual(expected, pushMetricAPIResponse.to_dict())

    def test_to_str(self):
        expected = pprint.pformat(
            {'code': None, 'errors': None, 'message': 'Test Message', 'resource_ids': {}, 'timestamp': 123456789})
        self.assertEqual(expected, pushMetricAPIResponse.to_str())


if __name__ == '__main__':
    unittest.main()
