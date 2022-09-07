import pprint
import unittest
from unittest import TestCase

from logicmonitor_data_sdk.models.map_string_string import MapStringString

expected = {}
mapStringString = MapStringString()


class TestMapStringString(TestCase):
    def test_to_dict(self):
        self.assertDictEqual(expected, mapStringString.to_dict())

    def test_to_str(self):
        self.assertEqual(pprint.pformat(expected), mapStringString.to_str())


if __name__ == '__main__':
    unittest.main()
