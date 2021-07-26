"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.
=======
"""

# coding: utf-8


import pprint
import re  # noqa: F401

import six

from logicmonitor_data_sdk.models.map_string_string import \
  MapStringString  # noqa: F401,E501
from logicmonitor_data_sdk.utils.object_name_validator import \
  ObjectNameValidator

objectNameValidator = ObjectNameValidator()


class DataSourceInstance(object):
  """
  This model is used to defining the datasource object.

  Args:
    name (:obj:`str`): Instance name. If no existing instance matches, a new instance
      is created with this name.
    display_name (:obj:`str`, optional): Instance display name. Only considered when creating a
      new instance.
    properties (:obj:`dict` of :obj:`str`, optional) : New properties for instance. Updates to existing instance
      properties are not considered. Depending on the property name, we will
      convert these properties into system, auto, or custom properties.

  Examples:
      >>> from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
      >>> # Create the DataSourceInstance object for CPU-0 instance monitoring
      >>> instance = DataSourceInstance(name='CPU-0')
  """
  swagger_types = {
    'description': 'str',
    'display_name': 'str',
    'name': 'str',
    'properties': 'MapStringString'
  }

  attribute_map = {
    'description': 'instanceDescription',
    'display_name': 'instanceDisplayName',
    'name': 'instanceName',
    'properties': 'instanceProperties'
  }

  def __init__(self, name, description=None,
      display_name=None, properties=None):  # noqa: E501

    self._description = None
    self._display_name = None
    self._name = None
    self._properties = None
    self.discriminator = None

    if description is not None:
      self.description = description
    if display_name is not None:
      self.display_name = display_name
    if name is not None:
      self.name = name
    if properties is not None:
      self.properties = properties
    error_msg = self._valid_field()
    if error_msg is not None and len(error_msg) > 0:
      raise ValueError(error_msg)

  def __hash__(self):
    return hash(str(self.name))

  @property
  def description(self):
    return self._description

  @description.setter
  def description(self, description):
    self._description = description

  @property
  def display_name(self):
    """Instance display name. Only considered when creating a new instance.

    :param display_name: The display_name of this DataSourceInstance.
    :type: str
    """
    return self._display_name

  @display_name.setter
  def display_name(self, display_name):
    err_msg = objectNameValidator.check_instance_displayname_validation(
        display_name)
    if err_msg:
      raise ValueError(err_msg)
    self._display_name = display_name

  @property
  def name(self):
    """Instance name. If no existing instance matches, a new instance is
    created with this name.

    :return: The name of this DataSourceInstance.
    :rtype: str
    """
    return self._name

  @name.setter
  def name(self, name):
    err_msg = objectNameValidator.check_instance_name_validation(name)
    if err_msg:
      raise ValueError(err_msg)
    self._name = name

  @property
  def properties(self):
    """New properties for instance. Updates to existing instance properties are
    not considered. Depending on the property name, we will convert these
    properties into system, auto, or custom properties.

    :return: The properties of this DataSourceInstance.
    :rtype: MapStringString
    """
    return self._properties

  @properties.setter
  def properties(self, properties):
    err_msg = objectNameValidator.check_instance_properties_validation(
        properties)
    if err_msg:
      raise ValueError(err_msg)
    self._properties = properties

  def to_dict(self):
    result = {}

    for attr, _ in six.iteritems(self.swagger_types):
      value = getattr(self, attr)
      if isinstance(value, list):
        result[attr] = list(map(
            lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
            value
        ))
      elif hasattr(value, "to_dict"):
        result[attr] = value.to_dict()
      elif isinstance(value, dict):
        result[attr] = dict(map(
            lambda item: (item[0], item[1].to_dict())
            if hasattr(item[1], "to_dict") else item,
            value.items()
        ))
      else:
        if value != None:
          result[attr] = value
    if issubclass(DataSourceInstance, dict):
      for key, value in self.items():
        result[key] = value

    return result

  def to_str(self):
    return pprint.pformat(self.to_dict())

  def __repr__(self):
    """For `print` and `pprint`"""
    return self.to_str()

  def __eq__(self, other):
    """Returns true if both objects are equal"""
    if not isinstance(other, DataSourceInstance):
      return False

    return self.__dict__ == other.__dict__

  def __ne__(self, other):
    """Returns true if both objects are not equal"""
    return not self == other

  def _valid_field(self):
    err_msg = ""
    # instance_name Validations
    err_msg += objectNameValidator.check_instance_name_validation(self.name)

    # instance_displayname Validations
    err_msg += objectNameValidator.check_instance_displayname_validation(
        self.display_name)

    # instance_properties Validation
    err_msg += objectNameValidator.check_instance_properties_validation(
        self.properties)

    return err_msg
