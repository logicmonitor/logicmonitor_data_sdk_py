import unittest
from unittest import TestCase

from logicmonitor_data_sdk.configuration import Configuration

company = 'company'
id = 'id'
key = 'key'
domain_name="logicmonitor.com"
configuration = Configuration(company=company, id=id, key=key,domain_name=domain_name)


class TestConfiguration(TestCase):
    def setUp(self) -> None:
        configuration.company = company

    def test_logger_file(self):
        self.assertEqual(None, configuration.logger_file)

    def test_debug(self):
        self.assertEqual(False, configuration.debug)

    def test_async_req(self):
        self.assertEqual(False, configuration.async_req)

    def test_logger_format(self):
        self.assertEqual('%(asctime)s %(levelname)s %(message)s', configuration.logger_format)

    def test_company(self):
        self.assertEqual(None, configuration.company)

    def test_authentication(self):
        self.assertEqual(None, configuration.authentication)

    def test_host(self):
        self.assertEqual('https://'+company+'.logicmonitor.com/rest', configuration.host)
    
    def test_domain_name(self):
        self.assertEqual('logicmonitor.com', configuration.domain_name)

    def test_auth_settings(self):
        expected = {'LMv1': {'type': 'api_key', 'in': 'header', 'key': 'Authorization',
                             'value': key, 'id': id}}
        self.assertDictEqual(expected, configuration.auth_settings())


if __name__ == '__main__':
    unittest.main()
