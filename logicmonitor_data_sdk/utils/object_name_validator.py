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

"""
Field validation Conventions see https://confluence.logicmonitor.com/display/Product/Field+validation+Conventions
"""

REGEX_RESOURCE_NAME = "[a-z:A-Z0-9\\._\\-]+$"
PATTERN_RESOURCE_NAME = re.compile(REGEX_RESOURCE_NAME)

REGEX_INVALID_RESOURCE_NAME = "[*<?,;`\\\\]"
PATTERN_REGEX_INVALID_RESOURCE_NAME = re.compile(REGEX_INVALID_RESOURCE_NAME)

REGEX_INVALID_DATA_SOURCE_NAME = "[^a-zA-Z #@_0-9:&\\.\\+]"
PATTERN_INVALID_DATA_SOURCE_NAME = re.compile(REGEX_INVALID_DATA_SOURCE_NAME)

REGEX_INSTANCE_NAME = "[a-z:A-Z0-9\\._\\-\\t ]+$"
PATTERN_INSTANCE_NAME = re.compile(REGEX_INSTANCE_NAME)

REGEX_INVALID_DEVICE_DISPLAY_NAME = "[*<?,;`\\n]"
PATTERN_INVALID_DEVICE_DISPLAY_NAME = re.compile(
    REGEX_INVALID_DEVICE_DISPLAY_NAME)

REGEX_DATA_POINT = "[a-zA-Z_0-9]+$"
PATTERN_DATA_POINT = re.compile(REGEX_DATA_POINT)

REGEX_INVALID_DATA_SOURCE_DISPLAY_NAME = "[^a-zA-Z:/ _0-9\\(\\)\\.#\\+@<>]"
PATTERN_INVALID_DATA_SOURCE_DISPLAY_NAME = re.compile(
    REGEX_INVALID_DATA_SOURCE_DISPLAY_NAME)

REGEX_DATA_SOURCE_GROUP_NAME = "[a-zA-Z0-9_\\- ]+$"
PATTERN_DATA_SOURCE_GROUP_NAME = re.compile(REGEX_DATA_SOURCE_GROUP_NAME)

REGEX_COMPANY_NAME = "^[a-zA-Z0-9_.\\-]+$"
PATTERN_COMPANY_NAME = re.compile(REGEX_COMPANY_NAME)

REGEX_AUTH_ID = "^[a-zA-Z0-9]+$"
PATTERN_AUTH_ID = re.compile(REGEX_AUTH_ID)

REGEX_AUTH_KEY = "[\s]"
PATTERN_AUTH_KEY = re.compile(REGEX_AUTH_KEY)

_INVALID_DATA_POINT_NAME_SET = {
  "SIN",
  "COS",
  "LOG",
  "EXP",
  "FLOOR",
  "CEIL",
  "ROUND",
  "POW",
  "ABS",
  "SQRT",
  "RANDOM",

  "LT",
  "LE",
  "GT",
  "GE",
  "EQ",
  "NE",
  "IF",
  "MIN",
  "MAX",
  "LIMIT",
  "DUP",
  "EXC",
  "POP",
  "UN",
  "UNKN",
  "NOW",
  "TIME",
  "PI",
  "E",

  "AND",

  "OR",

  "XOR",

  "INF",
  "NEGINF",
  "STEP",
  "YEAR",
  "MONTH",
  "DATE",
  "HOUR",
  "MINUTE",
  "SECOND",
  "WEEK",

  "SIGN",
  "RND",
  "SUM2",
  "AVG2",
  "PERCENT",
  "RAWPERCENTILE",
  "IN",
  "NANTOZERO",
  "MIN2",
  "MAX2"
}


class ObjectNameValidator:
  def __init__(self):
    pass

  def pass_empty_and_space_check(self, name):
    return not (len(name) == 0 or name.startswith(" ") or name.endswith(" "))

  def is_name_length_valid(self, name):
    if len(name) <= 255:
      return True
    return False

  def is_valid_resource_name(self, resource_name):
    return bool(PATTERN_RESOURCE_NAME.match(resource_name))

  def is_valid_resource_id(self, resource_id):
    return not bool(PATTERN_REGEX_INVALID_RESOURCE_NAME.search(resource_id))

  def is_valid_datasource_name(self, name):
    return len(self.validate_datasource_name(name)) == 0

  """
  * a-zA-Z #@_0-9():&.+ Spaces allowed except at start and end. In generally, we don't support
  * "(" ")" for this name
  """

  def validate_datasource_name(self, name):
    if len(name) == 0:
      return "datasource name can't be empty"
    # We only support the "-" for datasource name when it is the last char.
    if "-" in name:
      if name.index("-") == len(name) - 1:
        if len(name) == 1:
          return "datasource name can't be single \"-\""
        name = name.replace(" -", "")  # handle string: 'abc -'
        if len(name) == 0:
          return "space is not allowed at start and end"
      else:
        return "support the \"-\" for datasource name when it is the last char"

    return self._validate(name, "datasource name",
                          PATTERN_INVALID_DATA_SOURCE_NAME)

  def _validate(self, name, field_name, invalid_patten):
    if not name:
      return "%s can't be empty" % field_name
    if name.startswith(" ") or name.endswith(" "):
      return "space is not allowed at start and end in %s" % field_name

    matcher = invalid_patten.match(name)
    if matcher:
      return "%s is not allowed in %s" % (matcher.group(), field_name)
    return ""

  def is_valid_instance_name(self, instance_name):
    return bool(PATTERN_INSTANCE_NAME.match(instance_name))

  def is_valid_company_name(self, company_name):
    return bool(PATTERN_COMPANY_NAME.match(company_name))

  def is_valid_auth_id(self, auth_id):
    return bool(PATTERN_AUTH_ID.match(auth_id))

  def is_valid_auth_key(self, auth_key):
    return not bool(PATTERN_AUTH_KEY.search(auth_key))

  def validate_device_display_name(self, name):
    return self._validate(name, "instance display name",
                          PATTERN_INVALID_DEVICE_DISPLAY_NAME)

  def validate_datapoint_name(self, name):
    if not name:
      return "Data point name can't be null."
    if not bool(PATTERN_DATA_POINT.match(name)):
      return "Invalid DataPoint name : %s." % name

    if name.upper() in _INVALID_DATA_POINT_NAME_SET:
      return "%s is the reserved word and can't be used as the datapoint name." % name
    return ""

  def is_valid_datasource_display_name(self, name):
    return bool(self.validate_datasource_display_name(
        name))  # Strings.isNullOrEmpty(validateDataSourceDisplayName(name));

  def validate_datasource_display_name(self, name):
    if not name:
      return "datasource display name can't be empty"
    if "-" in name:
      if name.index("-") == len(name) - 1:
        if len(name) == 1:
          return "datasource display name can't be single \"-\""
        name = name.replace(" -", "")  # handle string: 'abc  -'
        if len(name) == 0:
          return "space is not allowed at start and end"
      else:
        return "support the \"-\" for datasource display name when it is the last char"

    return self._validate(name, "datasource display name",
                          PATTERN_INVALID_DATA_SOURCE_DISPLAY_NAME)

  def is_valid_datasource_group_name(self, datasource_group_name):
    return bool(PATTERN_DATA_SOURCE_GROUP_NAME.match(datasource_group_name))

  def check_resource_name_validation(self, create_flag, resource_name):
    err_msg = ""
    if create_flag or resource_name is not None:
      if resource_name is None:
        err_msg += "Resource Name is mandatory."
      elif not self.pass_empty_and_space_check(resource_name):
        err_msg += "Resource Name Should not be empty or have tailing spaces."
      elif not self.is_name_length_valid(resource_name):
        err_msg += "Resource Name size should not be greater than 255 characters."
      elif not self.is_valid_resource_name(resource_name):
        err_msg += "Invalid resource name : %s." % resource_name
    return err_msg

  def check_resource_description_validation(self, description):
    err_msg = ""
    if description is not None:
      if len(description) > 65535:
        err_msg += "Resource Description Size should not be greater than 65535 characters."
    return err_msg

  def check_resource_ids_validation(self, resource_ids):
    err_msg = ""
    if resource_ids is None:
      err_msg += "Resource Ids is mandatory."
    else:
      # resourceId is found, but there is no element in it
      if len(resource_ids) == 0:
        err_msg += "No Element in Resource Id."
      else:
        for key, value in resource_ids.items():
          if not self.pass_empty_and_space_check(key):
            err_msg += "Resource Id Key should not be null, empty or have trailing spaces."
          elif not self.is_name_length_valid(key):
            err_msg += "Resource Id Key should not be greater than 255 characters."
          elif not self.is_valid_resource_id(key):
            err_msg += "Invalid resource Id Key : %s." % key

          if not self.pass_empty_and_space_check(value):
            err_msg += "Resource Id Value should not be null, empty or have trailing spaces."
          elif len(value) > 24000:
            err_msg += "Resource Id Value should not be greater than 24000 characters."
          elif not self.is_valid_resource_id(value):
            err_msg += "Invalid resource Id Value : %s for Key : %s." % (
              value, key)
    return err_msg

  def check_resource_properties_validation(self, resource_properties):
    err_msg = ""
    if resource_properties is not None:
      if len(resource_properties) > 0:
        for key, value in resource_properties.items():
          if not self.pass_empty_and_space_check(key):
            err_msg += "Resource Property Key should not be null, empty or have trailing spaces."
          elif not self.is_name_length_valid(key):
            err_msg += "Resource Property Key should not be greater than 255 characters."
          elif "##" in key:
            err_msg += "Cannot use '##' in property name."
          elif key.lower().startswith("system.") or key.lower().startswith(
              "auto."):
            err_msg += "Resource Properties Should not contain System or auto properties :: %s." % key
          elif not self.is_valid_resource_id(key):
            err_msg += "Invalid resource Property Key : %s." % key

          if not self.pass_empty_and_space_check(value):
            err_msg += "Resource Property Value should not be null, empty or have trailing spaces for Key : %s." % key
          elif len(value) > 24000:
            err_msg += "Resource Id Value should not be greater than 24000 characters for Key : %s." % key
          elif not self.is_valid_resource_id(value):
            err_msg += "Invalid resource Property Value : %s for Key : %s." % (
              value, key)
    return err_msg

  def check_datasource_name_validation(self, datasource):
    err_msg = ""
    if datasource is None:
      # errMsg in case of datasource and dataSourceId is not provided
      err_msg += "DataSource or dataSourceId is mandatory"
    elif not self.pass_empty_and_space_check(datasource):
      err_msg += "DataSource should not be empty or have tailing spaces."
    elif len(datasource) > 64:
      err_msg += "DataSource length should not be greater than 64 characters."
    elif not self.is_valid_datasource_name(datasource):
      err_msg += "Invalid datasource : %s." % datasource
    return err_msg

  def check_datasource_displayname_validation(self, datasource_displayname):
    err_msg = ""
    if datasource_displayname is not None:
      if not self.pass_empty_and_space_check(datasource_displayname):
        err_msg += "DataSource Display name should not be null, empty or have tailing spaces."
      elif len(datasource_displayname) > 64:
        err_msg += "DataSource Display name length should not be greater than 64 characters."
      elif self.is_valid_datasource_display_name(datasource_displayname):
        err_msg += "Invalid datasource display name : %s." % datasource_displayname
    return err_msg

  def check_datasource_group_validation(self, datasource_group):
    err_msg = ""
    if datasource_group is not None:
      if not self.pass_empty_and_space_check(datasource_group):
        err_msg += "DataSource group should not be null, empty or have tailing spaces."
      elif len(datasource_group) < 2:
        err_msg += "DataSource group length should have minimum 2 characters."
      elif len(datasource_group) > 128:
        err_msg += "DataSource group length should not be greater than 128 characters."
      elif not self.is_valid_datasource_group_name(datasource_group):
        err_msg += "Invalid datasource group : %s." % datasource_group
    return err_msg

  def check_instance_name_validation(self, instance_name):
    err_msg = ""
    if instance_name is None:
      err_msg += "Instance Name is mandatory."
    elif not self.pass_empty_and_space_check(instance_name):
      err_msg += "Instance Name Should not be empty or have tailing spaces."

    elif not self.is_name_length_valid(instance_name):
      err_msg += "Instance Name size should not be greater than 255 characters."
    elif not self.is_valid_instance_name(instance_name):
      err_msg += "Invalid instance name : %s." % instance_name
    return err_msg

  def check_instance_displayname_validation(self, instance_display_name):
    err_msg = ""
    if instance_display_name is not None:
      if not self.pass_empty_and_space_check(instance_display_name):
        err_msg += "Instance Display Name Should not be empty or have tailing spaces."
      elif not self.is_name_length_valid(instance_display_name):
        err_msg += "Instance Display Name size should not be greater than 255 characters."
      elif self.validate_device_display_name(instance_display_name):
        err_msg += "Invalid instance display name : %s." % instance_display_name
    return err_msg

  def check_instance_properties_validation(self, instance_properties):
    err_msg = ""
    if instance_properties is not None:
      if len(instance_properties) > 0:
        for key, value in instance_properties.items():
          if not self.pass_empty_and_space_check(key):
            err_msg += "Instance Property Key should not be null, empty or have trailing spaces."
          elif not self.is_name_length_valid(key):
            err_msg += "Instance Property Key should not be greater than 255 characters."
          elif key.lower().startswith("system.") or key.lower().startswith(
              "auto."):
            err_msg += "Instance Properties Should not contain System or auto properties :: %s." % key
          elif not self.is_valid_resource_id(key):
            err_msg += "Invalid instance Property Key : %s." % key

          if not self.pass_empty_and_space_check(value):
            err_msg += "Instance Property Value should not be null, empty or have space for Key : %s." % key
          elif len(value) > 24000:
            err_msg += "Instance Property Value should not be greater than 24000 characters for Key : %s." % key
          elif not self.is_valid_resource_id(value):
            err_msg += "Invalid instance Property Value : %s for Key : %s." % (
              key, value)

    return err_msg

  def check_datapoint_name_validation(self, datapoint_name):
    err_msg = ""
    if datapoint_name is None:
      err_msg += "DataPoint Name is mandatory."
    elif len(datapoint_name) > 128:
      err_msg += "Datapoint Name should not be greater than 128 characters."
    else:
      strs = self.validate_datapoint_name(datapoint_name)
      if strs:
        err_msg += strs
    return err_msg

  def check_datapoint_description_validation(self, datapoint_description):
    err_msg = ""
    if datapoint_description is not None:
      if len(datapoint_description) > 1024:
        err_msg += "Data Point Description Should not be greater than 1024 characters."
    return err_msg

  def check_datapoint_type_validation(self, data_point_type):
    err_msg = ""
    if data_point_type is not None:
      data_point_types = {"counter", "guage", "derive"}
      data_point_type = data_point_type.lower()
      if data_point_type not in data_point_types:
        err_msg += "The datapoint %s is having invalid dataPointType %s." % (
          'type', data_point_type)
    return err_msg

  def check_datapoint_aggregation_type_validation(self,
      data_point_aggregation_type):
    err_msg = ""
    data_point_aggregation_types = {"none", "avg", "sum"}
    if data_point_aggregation_type is not None:
      data_point_aggregation_type = data_point_aggregation_type.lower()
      if data_point_aggregation_type not in data_point_aggregation_types:
        err_msg += "The datapoint %s is having invalid data_point_aggregation_type %s." % (
          'aggregation_type', data_point_aggregation_type)
    return err_msg
