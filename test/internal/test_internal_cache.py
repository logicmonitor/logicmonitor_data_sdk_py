import datetime
import time
import unittest
from unittest import TestCase, mock

from urllib3._collections import HTTPHeaderDict

import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.api.response_interface import ResponseInterface
from logicmonitor_data_sdk.internal.internal_cache import BatchingCache
from logicmonitor_data_sdk.models.push_metric_api_response import PushMetricAPIResponse

configuration = logicmonitor_data_sdk.Configuration(company='company',
                                                    id='id',
                                                    key='key')


class MyResponse(ResponseInterface):

    def success_callback(self, request, response, status, request_id):
        print("%s: %s: %s", response, status, request_id)

    def error_callback(self, request, response, status, request_id, reason):
        print("%s: %s: %s %s", response, status, reason, request_id)


batchingcache = BatchingCache(api_client=None, batch=True,
                              interval=10,
                              response_callback=MyResponse,
                              request_cb=Metrics._do_request,
                              merge_cb=Metrics._merge_request)

pushMetricAPIResponse = PushMetricAPIResponse()
pushMetricAPIResponse.timestamp = int(datetime.datetime.now().timestamp())
pushMetricAPIResponse.resource_ids = None
pushMetricAPIResponse.message = 'The request has been accepted for processing, but the processing has not been completed.'
expected = (pushMetricAPIResponse, 202, HTTPHeaderDict(
    {'date': time.strftime("%a, %d %b %Y %I:%M:%S " + 'GMT', time.gmtime()), 'content-type': 'application/json',
     'content-length': '178', 'x-request-id': 'a386b529-9172-43c2-bc58-105b291496e6', 'server': 'LM',
     'strict-transport-security': 'max-age=31536000;'}))


path = '/v2/metric/ingest'
method = 'POST'
body = [{'data_source': 'SampleDS',
         'data_source_display_name': None,
         'data_source_group': None,
         'data_source_id': None,
         'instances': [{'data_points': [{'data_point_aggregation_type': None,
                                         'data_point_description': None,
                                         'data_point_name': 'SampleDataPoint',
                                         'data_point_type': None,
                                         'values': {'1646329753': '0.5415720953475276'}}],
                        'instance_description': None,
                        'instance_display_name': None,
                        'instance_group': None,
                        'instance_name': 'SampleInstance',
                        'instance_properties': None}],
         'resource_description': None,
         'resource_ids': {'system.hostname': 'SampleDevice'},
         'resource_name': 'SampleDevice',
         'resource_properties': {'using.sdk': 'true'}}]
create = True


class TestInternalCache(TestCase):
    def test_batch(self):
        self.assertEqual(True, batchingcache.batch)

    def test_has_request(self):
        self.assertEqual(0, batchingcache.has_request().__dict__['_value'])

    def test_get_requests(self):
        self.assertEqual(0, batchingcache.get_requests().__dict__['unfinished_tasks'])

    def test_get_payload(self):
        self.assertEqual({}, batchingcache.get_payload())

    def test_Lock(self):
        self.assertEqual(None, batchingcache.Lock())

    def test_UnLock(self):
        self.assertEqual(None, batchingcache.UnLock())

    @mock.patch('logicmonitor_data_sdk.api_client.ApiClient.call_api', return_value=expected)
    def test_make_request(self, mock_call_api):
        result = batchingcache.make_request(path=path, method=method, body=body, create=create)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
