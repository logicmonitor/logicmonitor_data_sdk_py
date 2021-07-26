"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.
=======
"""

import re
from unittest import TestCase

from logicmonitor_data_sdk.utils.object_name_validator import \
  ObjectNameValidator

name_length = "the data length is greater  than 255 character then return false other wise true" \
              "." * 200
valid_resource_name = "resource_name"
invalid_resource_name = "resource name"
valid_resource_id = "system.hostname"
invalid_resource_id = "**system.hostname"
valid_resource_ids = {"system.hostname": "name"}
invalid_resource_ids = {"system.hostname": " name"}
valid_resource_properties = {'abc.sdk': 'true'}
invalid_resource_properties = {'system.sdk': 'true'}
valid_resource_description = "resource_description"
invalid_resource_description = "Resource Description Size should not be greater than 65535 characters." \
                               "." * 1000
valid_datasource_name = "datasource_name-"
invalid_datasource_name = "datasource-name -"
valid_device_display_name = "device_display_name"
invalid_device_display_name = "device_display_name "
valid_datasource_display_name = "datasource_display_name"
invalid_datasource_display_name = "datasource_display_name "
valid_datasource_group_name = "datasource_group_name"
invalid_datasource_group_name = "datasource_group_name -*"
valid_instance_name = "instance_name"
invalid_instance_name = "instance_name*"
valid_instance_displayname = "instance_displayname"
invalid_instance_displayname = " instance_displayname"
valid_instance_properties = {'ssaa.sdk': 'true'}
invalid_instance_properties = {'system.sdk': 'true'}
valid_datapoint_name = "datapoint"
invalid_datapoint_name = "datapoint "
valid_datapoint_description = "datapoint_description"
invalid_datapoint_description = "Data Point Description Should not be greater than 1024 characters." \
                                "." * 1000
valid_datapoint_type = "counter"
invalid_datapoint_type = "any"
valid_datapoint_aggregation_type = "sum"
invalid_datapoint_aggregation_type = "any"


class TestObjectNameValidator(TestCase):
  def setUp(self):
    self.object_name_validator = ObjectNameValidator()

  def test_pass_empty_and_space_check(self):
    result = self.object_name_validator.pass_empty_and_space_check(
        valid_datapoint_name)
    self.assertEqual(True, result)

  def test_pass_empty_and_space_check_fail(self):
    result = self.object_name_validator.pass_empty_and_space_check(
        invalid_datapoint_name)
    self.assertEqual(False, result)

  def test_is_name_length_valid(self):
    result = self.object_name_validator.is_name_length_valid(
        valid_datapoint_name)
    self.assertEqual(True, result)

  def test_is_name_length_valid_fail(self):
    result = self.object_name_validator.is_name_length_valid(name_length)
    self.assertEqual(False, result)

  def test_is_valid_resource_name(self):
    result = self.object_name_validator.is_valid_resource_name(
        valid_resource_name)
    self.assertEqual(True, result)

  def test_is_valid_resource_name_fail(self):
    result = self.object_name_validator.is_valid_resource_name(
        invalid_resource_name)
    self.assertEqual(False, result)

  def test_is_valid_resource_id(self):
    result = self.object_name_validator.is_valid_resource_id(valid_resource_id)
    self.assertEqual(True, result)

  def test_is_valid_resource_id_fail(self):
    result = self.object_name_validator.is_valid_resource_id(
        invalid_resource_id)
    self.assertEqual(False, result)

  def test_is_valid_datasource_name(self):
    result = self.object_name_validator.is_valid_datasource_name(
        valid_datasource_name)
    self.assertEqual(True, result)

  def test_validate_datasource_name_fail(self):
    result = self.object_name_validator.is_valid_datasource_name(
        invalid_datasource_name)
    self.assertEqual(False, result)

  def test_is_valid_instance_name(self):
    result = self.object_name_validator.is_valid_instance_name(
        valid_instance_name)
    self.assertEqual(True, result)

  def test_is_valid_instance_name_fail(self):
    result = self.object_name_validator.is_valid_instance_name(
        invalid_instance_name)
    self.assertEqual(False, result)

  def test_validate_device_display_name(self):
    result = self.object_name_validator.validate_device_display_name(
        valid_device_display_name)
    self.assertEqual(0, len(result))

  def test_validate_device_display_name_fail(self):
    result = self.object_name_validator.validate_device_display_name(
        invalid_device_display_name)
    self.assertNotEqual(0, len(result))

  def test_validate_datapoint_name(self):
    result = self.object_name_validator.validate_datapoint_name(
        valid_datapoint_name)
    self.assertEqual(0, len(result))

  def test_validate_datapoint_name_fail(self):
    result = self.object_name_validator.validate_datapoint_name(
        invalid_datapoint_name)
    self.assertNotEqual(0, len(result))

  def test_is_valid_datasource_display_name(self):
    result = self.object_name_validator.is_valid_datasource_display_name(
        valid_datasource_display_name)
    self.assertEqual(False, result)

  def test_is_valid_datasource_display_name_fail(self):
    result = self.object_name_validator.is_valid_datasource_display_name(
        invalid_datasource_display_name)
    self.assertEqual(True, result)

  def test_validate_datasource_display_name(self):
    result = self.object_name_validator.validate_datasource_display_name(
        valid_datasource_display_name)
    self.assertEqual(0, len(result))

  def test_validate_datasource_display_name_fail(self):
    result = self.object_name_validator.validate_datasource_display_name(
        invalid_datasource_display_name)
    self.assertNotEqual(0, len(result))

  def test_is_valid_datasource_group_name(self):
    result = self.object_name_validator.is_valid_datasource_group_name(
        valid_datasource_group_name)
    self.assertEqual(True, result)

  def test_is_valid_datasource_group_name_fail(self):
    result = self.object_name_validator.is_valid_datasource_group_name(
        invalid_datasource_group_name)
    self.assertEqual(False, result)

  def test_check_resource_name_validation(self):
    result = self.object_name_validator.check_resource_name_validation(False,
                                                                       valid_resource_name)
    self.assertEqual(0, len(result))

  def test_check_resource_name_validation_fail(self):
    result = self.object_name_validator.check_resource_name_validation(True,
                                                                       invalid_resource_name)
    self.assertNotEqual(0, len(result))

  def test_check_resource_description_validation(self):
    result = self.object_name_validator.check_resource_description_validation(
        valid_resource_description)
    self.assertEqual(0, len(result))

  def test_check_resource_description_validation_fail(self):
    result = self.object_name_validator.check_resource_description_validation(
        invalid_resource_description)
    self.assertNotEqual(0, len(result))

  def test_check_resource_ids_validation(self):
    result = self.object_name_validator.check_resource_ids_validation(
        valid_resource_ids)
    self.assertEqual(0, len(result))

  def test_check_resource_ids_validation_fail(self):
    result = self.object_name_validator.check_resource_ids_validation(
        invalid_resource_ids)
    self.assertNotEqual(0, len(result))

  def test_check_resource_properties_validation(self):
    result = self.object_name_validator.check_resource_properties_validation(
        valid_resource_properties)
    self.assertEqual(0, len(result))

  def test_check_resource_properties_validation_fail(self):
    result = self.object_name_validator.check_resource_properties_validation(
        invalid_resource_properties)
    self.assertNotEqual(0, len(result))

  def test_check_datasource_name_validation(self):
    result = self.object_name_validator.check_datasource_name_validation(
        valid_datasource_name)
    self.assertEqual(0, len(result))

  def test_check_datasource_name_validation_fail(self):
    result = self.object_name_validator.check_datasource_name_validation(
        invalid_datasource_name)
    self.assertNotEqual(0, len(result))

  def test_check_datasource_displayname_validation(self):
    result = self.object_name_validator.check_datasource_displayname_validation(
        valid_datasource_display_name)
    self.assertEqual(0, len(result))

  def test_check_datasource_displayname_validation_fail(self):
    result = self.object_name_validator.check_datasource_displayname_validation(
        invalid_datasource_display_name)
    self.assertNotEqual(0, len(result))

  def test_check_datasource_group_validation(self):
    result = self.object_name_validator.check_datasource_group_validation(
        valid_datasource_group_name)
    self.assertEqual(0, len(result))

  def test_check_datasource_group_validation_fail(self):
    result = self.object_name_validator.check_datasource_group_validation(
        invalid_datasource_group_name)
    self.assertNotEqual(0, len(result))

  def test_check_instance_name_validation(self):
    result = self.object_name_validator.check_instance_name_validation(
        valid_instance_name)
    self.assertEqual(0, len(result))

  def test_check_instance_name_validation_fail(self):
    result = self.object_name_validator.check_instance_name_validation(
        invalid_instance_name)
    self.assertNotEqual(0, len(result))

  def test_check_instance_displayname_validation(self):
    result = self.object_name_validator.check_instance_displayname_validation(
        valid_instance_displayname)
    self.assertEqual(0, len(result))

  def test_check_instance_displayname_validation_fail(self):
    result = self.object_name_validator.check_instance_displayname_validation(
        invalid_instance_displayname)
    self.assertNotEqual(0, len(result))

  def test_check_instance_properties_validation(self):
    result = self.object_name_validator.check_instance_properties_validation(
        valid_instance_properties)
    self.assertEqual(0, len(result))

  def test_check_instance_properties_validation_fail(self):
    result = self.object_name_validator.check_instance_properties_validation(
        invalid_instance_properties)
    self.assertNotEqual(0, len(result))

  def test_check_datapoint_name_validation(self):
    result = self.object_name_validator.check_datapoint_name_validation(
        valid_datapoint_name)
    self.assertEqual(0, len(result))

  def test_check_datapoint_name_validation_fail(self):
    result = self.object_name_validator.check_datapoint_name_validation(
        invalid_datapoint_name)
    self.assertNotEqual(0, len(result))

  def test_check_datapoint_description_validation(self):
    result = self.object_name_validator.check_datapoint_description_validation(
        valid_datapoint_description)
    self.assertEqual(0, len(result))

  def test_check_datapoint_description_validation_fail(self):
    result = self.object_name_validator.check_datapoint_description_validation(
        invalid_datapoint_description)
    self.assertNotEqual(0, len(result))

  def test_check_datapoint_type_validation(self):
    result = self.object_name_validator.check_datapoint_type_validation(
        valid_datapoint_type)
    self.assertEqual(0, len(result))

  def test_check_datapoint_type_validation_fail(self):
    self.object_name_validator.name = "datapoint"
    result = self.object_name_validator.check_datapoint_type_validation(
        invalid_datapoint_type)
    self.assertNotEqual(0, len(result))

  def test_check_datapoint_aggregation_type_validation(self):
    result = self.object_name_validator.check_datapoint_aggregation_type_validation(
        valid_datapoint_aggregation_type)
    self.assertEqual(0, len(result))

  def test_check_datapoint_aggregation_type_validation_fail(self):
    self.object_name_validator.name = "datapoint"
    result = self.object_name_validator.check_datapoint_aggregation_type_validation(
        invalid_datapoint_aggregation_type)
    self.assertNotEqual(0, len(result))

  def test__validate(self):
    REGEX_INVALID_DATA_SOURCE_NAME = "[^a-zA-Z #@_0-9:&\\.\\+]"
    PATTERN_INVALID_DATA_SOURCE_NAME = re.compile(
        REGEX_INVALID_DATA_SOURCE_NAME)
    result = self.object_name_validator._validate(valid_datapoint_name,
                                                  "field_name",
                                                  PATTERN_INVALID_DATA_SOURCE_NAME)
    self.assertEqual(0, len(result))

  def test__validate_fail(self):
    REGEX_INVALID_RESOURCE_NAME = "[*<?,;`\\\\]"
    PATTERN_REGEX_INVALID_RESOURCE_NAME = re.compile(
        REGEX_INVALID_RESOURCE_NAME)
    result = self.object_name_validator._validate(invalid_datapoint_name,
                                                  "field_name",
                                                  PATTERN_REGEX_INVALID_RESOURCE_NAME)
    self.assertNotEqual(0, len(result))
