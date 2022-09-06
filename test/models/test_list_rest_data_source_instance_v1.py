import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.list_rest_data_source_instance_v1 import ListRestDataSourceInstanceV1

expected = {}
listRestDataSourceInstanceV1 = ListRestDataSourceInstanceV1()


class TestListRestDataSourceInstanceV1(TestCase):
    def test_to_dict(self):
        self.assertDictEqual(expected, listRestDataSourceInstanceV1.to_dict())

    def test_to_str(self):
        self.assertEqual(pprint.pformat(expected), listRestDataSourceInstanceV1.to_str())


if __name__ == '__main__':
    unittest.main()
