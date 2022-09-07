import datetime
import platform
import time
import unittest
from unittest import TestCase, mock

import urllib3
from urllib3._collections import HTTPHeaderDict

import logicmonitor_data_sdk
from logicmonitor_data_sdk import PushMetricAPIResponse
from logicmonitor_data_sdk.version import __version__
from logicmonitor_data_sdk.api_client import ApiClient

configuration = logicmonitor_data_sdk.Configuration(company='company',
                                                    id='id',
                                                    key='key')

apiClient = ApiClient()

path = '/v2/metric/ingest'
method = 'POST'
path_params = {}
query_params = [('create', True)]
header_params = {'Accept': 'application/json', 'Content-Type': 'application/json'}
body_params = [{'data_source': 'SampleDS',
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
                'resource_properties': {'using.sdk': 'true'},
                'singleInstanceDS': False}]

post_params = []
files = {}
response_type = PushMetricAPIResponse
auth_settings = ['LMv1']
async_req = False
_return_http_data_only = None
collection_formats = {}
_preload_content = None
_request_timeout = {}

pushMetricAPIResponse = PushMetricAPIResponse()
pushMetricAPIResponse.timestamp = int(datetime.datetime.now().timestamp())
pushMetricAPIResponse.resource_ids = None
pushMetricAPIResponse.message = 'The request has been accepted for processing, but the processing has not been ' \
                                'completed. '
expected = (pushMetricAPIResponse, 202, HTTPHeaderDict(
    {'date': time.strftime("%a, %d %b %Y %I:%M:%S " + 'GMT', time.gmtime()), 'content-type': 'application/json',
     'content-length': '178', 'x-request-id': 'a386b529-9172-43c2-bc58-105b291496e6', 'server': 'LM',
     'strict-transport-security': 'max-age=31536000;'}))

restResponse = urllib3.response.HTTPResponse(headers=HTTPHeaderDict(
    {'date': time.strftime("%a, %d %b %Y %I:%M:%S " + 'GMT', time.gmtime()), 'content-type': 'application/json',
     'content-length': '178', 'x-request-id': 'a386b529-9172-43c2-bc58-105b291496e6', 'server': 'LM',
     'strict-transport-security': 'max-age=31536000;'}), version=11,
    status=200, strict=0,
    body=b'{"code":202,"errors":[],"message":"The request has been accepted '
         b'for processing, but the processing has not been completed.", ')
header_params = header_params.update({'User-Agent': apiClient.user_agent, 'X-version': '1'})
company = 'company'
url = 'https://' + company + '.logicmonitor.com/rest/v2/metric/ingest'


class TestApiClient(TestCase):
    def setUp(self) -> None:
        apiClient.user_agent = 'logicmonitor_data_sdk/{version} (python {pyver}; os {os}; arch {arch})'.format(
            version=__version__,
            pyver=platform.python_version(),
            os=platform.system().lower(),
            arch=platform.machine().lower(),
        )

    def test_call_api(self):
        with mock.patch.object(apiClient, '_ApiClient__call_api', return_value=expected):
            result = apiClient.call_api(
                path, method,
                path_params,
                query_params,
                header_params,
                body=body_params,
                post_params=post_params,
                files=files,
                response_type=response_type,
                auth_settings=auth_settings,
                async_req=async_req,
                _return_http_data_only=_return_http_data_only,
                _preload_content=_preload_content,
                _request_timeout=_request_timeout,
                collection_formats=collection_formats)
        self.assertEqual(expected, result)

    def test_user_agent(self):
        result = 'logicmonitor_data_sdk/{version} (python {pyver}; os {os}; arch {arch})'.format(
            version=__version__,
            pyver=platform.python_version(),
            os=platform.system().lower(),
            arch=platform.machine().lower(),
        )
        expected1 = apiClient.user_agent
        self.assertEqual(expected1, result)

    def test__call_api(self):
        with mock.patch.object(apiClient, '_ApiClient__call_api', return_value=expected):
            result = apiClient._ApiClient__call_api(path, method,
                                                    path_params,
                                                    query_params,
                                                    header_params,
                                                    body=body_params,
                                                    post_params=post_params,
                                                    files=files,
                                                    response_type=response_type,
                                                    auth_settings=auth_settings,
                                                    _return_http_data_only=_return_http_data_only,
                                                    _preload_content=_preload_content,
                                                    _request_timeout=_request_timeout,
                                                    collection_formats=collection_formats)
        self.assertEqual(expected, result)

    @mock.patch('logicmonitor_data_sdk.api_client.ApiClient.sanitize_for_serialization', return_value=header_params)
    def test_sanitize_for_serialization(self, mock_sanitize_for_serialization):
        result = apiClient.sanitize_for_serialization(header_params)
        self.assertEqual(header_params, result)

    def test_deserialize(self):
        with mock.patch.object(apiClient, '_ApiClient__deserialize', return_value=expected):
            result = apiClient.deserialize(restResponse, 'PushMetricAPIResponse')
            self.assertEqual(expected, result)

    def test__deserialize(self):
        with mock.patch.object(apiClient, '_ApiClient__deserialize',
                               return_value="The request has been accepted for processing, but the processing has not been completed"):
            result = apiClient._ApiClient__deserialize(restResponse.data, 'PushMetricAPIResponse')

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.GET', return_value=restResponse)
    def test_request_GET(self, mock__rest_GET):
        result = apiClient.request_limit_handler(method="GET", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.POST', return_value=restResponse)
    def test_request_POST(self, mock__rest_POST):
        result = apiClient.request_limit_handler(method="POST", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.PUT', return_value=restResponse)
    def test_request_PUT(self, mock__rest_PUT):
        result = apiClient.request_limit_handler(method="PUT", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.PATCH', return_value=restResponse)
    def test_request_PATCH(self, mock__rest_PATCH):
        result = apiClient.request_limit_handler(method="PATCH", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.OPTIONS', return_value=restResponse)
    def test_request_OPTIONS(self, mock__rest_OPTIONS):
        result = apiClient.request_limit_handler(method="OPTIONS", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.DELETE', return_value=restResponse)
    def test_request_DELETE(self, mock__rest_DELETE):
        result = apiClient.request_limit_handler(method="DELETE", url=url)
        self.assertEqual(result, restResponse)

    @mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.HEAD', return_value=restResponse)
    def test_request_HEAD(self, mock__rest_HEAD):
        result = apiClient.request_limit_handler(method="HEAD", url=url)
        self.assertEqual(result, restResponse)


if __name__ == '__main__':
    unittest.main()
