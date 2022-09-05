import datetime
import time
import unittest
from unittest import TestCase, mock

from urllib3._collections import HTTPHeaderDict

import logicmonitor_data_sdk
from logicmonitor_data_sdk import PushMetricAPIResponse
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.api.response_interface import ResponseInterface
from logicmonitor_data_sdk.models import Resource, DataSource, DataSourceInstance, DataPoint

configuration = logicmonitor_data_sdk.Configuration(company='company',
                                                    id='id',
                                                    key='key')


class MyResponse(ResponseInterface):
    def success_callback(self, request, response, status, request_id):
        pass

    def error_callback(self, request, response, status, request_id, reason):
        pass


pushMetricAPIResponse = PushMetricAPIResponse()
pushMetricAPIResponse.timestamp = int(datetime.datetime.now().timestamp())
pushMetricAPIResponse.resource_ids = None
pushMetricAPIResponse.message = 'The request has been accepted for processing, but the processing has not been ' \
                                'completed. '
expected = (pushMetricAPIResponse, 202, HTTPHeaderDict(
    {'date': time.strftime("%a, %d %b %Y %I:%M:%S " + 'GMT', time.gmtime()), 'content-type': 'application/json',
     'content-length': '178', 'x-request-id': 'a386b529-9172-43c2-bc58-105b291496e6', 'server': 'LM',
     'strict-transport-security': 'max-age=31536000;'}))

t = Metrics()
test_metric_api1 = Metrics(batch=True, interval=10, response_callback=MyResponse())
test_metric_api2 = Metrics(batch=False, interval=10, response_callback=MyResponse())
resource = Resource(ids={"system.hostname": "SampleDevice"},  # Core Properties of the Resource
                    create=True,  # Auto-create resource if does not exist
                    name="SampleDevice",  # Name of the resource
                    properties={"using.sdk": "true"})
datasource = DataSource(name="SampleDS")
datasource_instance = DataSourceInstance(name="SampleInstance")
datapoint = DataPoint(name="SampleDataPoint",
                      aggregation_type="percentile",percentile=17)
values = {str(int(time.time())): "10"}


class TestMetrics(TestCase):
    @mock.patch('logicmonitor_data_sdk.internal.internal_cache.BatchingCache.add_request', return_value=None)
    def test_send_metrics_batch_true(self, mock_add_request):
        result = test_metric_api1.send_metrics(resource=resource, datasource=datasource,
                                               instance=datasource_instance, datapoint=datapoint,
                                               values=values)
        self.assertEqual(None, result)

    @mock.patch('logicmonitor_data_sdk.internal.internal_cache.BatchingCache.make_request', return_value=expected)
    def test_update_resource_property(self, mock_make_request):
        actual = test_metric_api1.update_resource_property(resource_ids={'system.hostname': 'SampleDevice'},
                                                           resource_properties={"using.sdk": "true"},
                                                           patch=True)
        self.assertEqual(expected, actual)

    @mock.patch('logicmonitor_data_sdk.internal.internal_cache.BatchingCache.make_request', return_value=expected)
    def test__single_request(self, mock_make_request):
        actual = test_metric_api2._single_request(resource=resource, datasource=datasource,
                                                  instance=datasource_instance, datapoint=datapoint, values=values)

        self.assertEqual(expected, actual)

    @mock.patch('logicmonitor_data_sdk.internal.internal_cache.BatchingCache.make_request', return_value=expected)
    def test_update_instance_property(self, mock_make_request):
        actual = test_metric_api2.update_instance_property(resource_ids={'system.hostname': 'SampleDevice'},
                                                           datasource='SampleDS1',
                                                           instancename='SampleInstance1',
                                                           instance_properties={'ins.property': 'values'}, )
        self.assertEqual(expected, actual)

    def test__valid_field(self):
        instanceObj = DataSourceInstance(instanceId=7, name='SampleInstance', display_name='SampleInstance',
                                         properties={'x': 'true'})
        self.assertEqual('', t._valid_field(instance=instanceObj))


if __name__ == '__main__':
    unittest.main()
