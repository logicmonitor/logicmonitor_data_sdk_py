import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.list_rest_data_point_v1 import ListRestDataPointV1

listRestDataPointV1 = ListRestDataPointV1()
expected = {}


class TestListRestDataPointV1(TestCase):
    def test_to_dict(self):
        self.assertDictEqual(expected, listRestDataPointV1.to_dict())

    def test_to_str(self):
        self.assertEqual(pprint.pformat(expected), listRestDataPointV1.to_str())


if __name__ == '__main__':
    unittest.main()
