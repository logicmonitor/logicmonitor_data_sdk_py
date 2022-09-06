import time
import unittest
from unittest import TestCase, mock

import urllib3
from urllib3._collections import HTTPHeaderDict

import logicmonitor_data_sdk
from logicmonitor_data_sdk.rest import RESTResponse, RESTClientObject

httpHeaderDict = HTTPHeaderDict(
    {'date': time.strftime("%a, %d %b %Y %I:%M:%S " + 'GMT', time.gmtime()), 'content-type': 'application/json',
     'content-length': '148', 'x-request-id': '63d50f8efd0448da89155899e31e7ab0', 'server': 'LM',
     'strict-transport-security': 'max-age=31536000;'})
rest_responce = urllib3.response.HTTPResponse(headers=httpHeaderDict, version=11,
                                              status=200, strict=0,
                                              body=b'{"code":202,"errors":[],"message":"The request has been accepted '
                                                   b'for processing, but the processing has not been completed.", ')
rESTResponse = RESTResponse(rest_responce)

company = 'company'
url = 'https://' + company + '.logicmonitor.com/rest/v2/metric/ingest'
configuration = logicmonitor_data_sdk.Configuration(company=company,
                                                    id='id',
                                                    key='key')

rESTClientObject = RESTClientObject(configuration=configuration)


class TestRESTResponse(TestCase):
    def test_getheaders(self):
        result = rESTResponse.getheaders()
        self.assertEqual(result, httpHeaderDict)

    def test_getheader(self):
        result = rESTResponse.getheader(name='Simple1')
        self.assertEqual(None, result)


class TestRESTClientObject(TestCase):
    def setUp(self) -> None:
        self.patcher = mock.patch('logicmonitor_data_sdk.rest.RESTClientObject.request', return_value=rESTResponse)
        self.patcher.start()

    def test_request(self):
        result = rESTClientObject.request(method='POST', url=url)
        self.assertEqual(rESTResponse, result)

    def test_GET(self):
        result = rESTClientObject.GET(url)
        self.assertEqual(rESTResponse, result)

    def test_HEAD(self):
        result = rESTClientObject.HEAD(url)
        self.assertEqual(rESTResponse, result)

    def test_OPTIONS(self):
        result = rESTClientObject.OPTIONS(url)
        self.assertEqual(rESTResponse, result)

    def test_DELETE(self):
        result = rESTClientObject.DELETE(url)
        self.assertEqual(rESTResponse, result)

    def test_POST(self):
        result = rESTClientObject.POST(url)
        self.assertEqual(rESTResponse, result)

    def test_PUT(self):
        result = rESTClientObject.PUT(url)
        self.assertEqual(rESTResponse, result)

    def test_PATCH(self):
        result = rESTClientObject.PATCH(url)
        self.assertEqual(rESTResponse, result)

    def tearDown(self) -> None:
        self.patcher.stop()


if __name__ == '__main__':
    unittest.main()
