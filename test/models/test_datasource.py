import pprint
import unittest
from unittest import TestCase
from logicmonitor_data_sdk.models.datasource import DataSource

name = 'name'
display_name = 'test display'
singleInstanceDS = True
group = 'test-group'
id = 7

datasource = DataSource('name')


class TestDataSource(TestCase):
    def setUp(self) -> None:
        datasource.display_name = display_name
        datasource.singleInstanceDS = singleInstanceDS
        datasource.group = group
        datasource.id = id

    def test_name(self):
        self.assertEqual('name', datasource.name)

    def test_display_name(self):
        result = datasource.display_name
        self.assertEqual(display_name, result)

    def test_group(self):
        result = datasource.group
        self.assertEqual(group, result)

    def test_id(self):
        result = datasource.id
        self.assertEqual(id, result)

    def test_singleInstanceDS(self):
        result = datasource.singleInstanceDS
        self.assertEqual(singleInstanceDS, result)

    def test_to_str(self):
        expected = pprint.pformat({'display_name': 'test display',
                                   'group': 'test-group',
                                   'id': 7,
                                   'name': 'name',
                                   'singleInstanceDS': True})
        self.assertEqual(expected, datasource.to_str())

    def test_to_dict(self):
        expected = {'name': 'name', 'display_name': 'test display', 'group': 'test-group', 'id': 7, 'singleInstanceDS': True}
        self.assertDictEqual(expected, datasource.to_dict())

    def test__valid_field(self):
        self.assertEqual('', datasource._valid_field())


if __name__ == '__main__':
    unittest.main()
