import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.resource import Resource

description = "This description is in test."
name = 'simpleresource'
create = True
ids = {'adasd': '1234'}
properties = {}

resource = Resource(ids)


class TestDataSourceInstance(TestCase):
    def setUp(self):
        resource.description = description
        resource.name = name
        resource.create = create
        resource.ids = ids
        resource.properties = {}

    def test_ids(self):
        result = resource.ids
        self.assertEqual(ids, result)

    def test_name(self):
        result = resource.name
        self.assertEqual(name, result)

    def test_description(self):
        result = resource.description
        self.assertEqual(description, result)

    def test_properties(self):
        result = resource.properties
        self.assertEqual(properties, result)

    def test_create(self):
        result = resource.create
        self.assertEqual(create, result)

    def test__valid_field(self):
        result = resource._valid_field()
        self.assertEqual('', result)

    def test_to_dict(self):
        expected = {'description': 'This description is in test.', 'ids': {'adasd': '1234'}, 'name': 'simpleresource', 'properties': {}, 'create': True}
        self.assertDictEqual(expected, resource.to_dict())

    def test_to_str(self):
        expected = pprint.pformat({'description': 'This description is in test.', 'ids': {'adasd': '1234'}, 'name': 'simpleresource', 'properties': {}, 'create': True})
        self.assertEqual(expected, resource.to_str())


if __name__ == '__main__':
    unittest.main()
