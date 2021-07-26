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

from logicmonitor_data_sdk.utils.object_name_validator import \
  ObjectNameValidator

objectNameValidator = ObjectNameValidator()


class DataPoint(object):
  """
  This model is used to defining the datapoint object.

  Args:
    name (:obj:`str`): Datapoint name. If no existing datapoint  matches for specified
      DataSource, a new datapoint is created with this name.
    aggregation_type (:obj:`str`, optional): The aggregation method, if any, that should be used
      if data is pushed in sub-minute intervals. Allowed options are "sum", "average" and "none"(default) 
      where "none" would take last value for that minute. Only considered when creating
      a new datapoint. See the About the Push Metrics REST API section of this
      guide for more information on datapoint value aggregation intervals.
    description (:obj:`str`, optional) : Datapoint description. Only considered when creating a
      new datapoint.
    type (:obj:`str`, optional) : Metric type as a number in string format. Allowed options are 
      "guage" (default) and "counter". Only considered when creating a new datapoint.

  Examples:
      >>> from logicmonitor_data_sdk.models.datapoint import DataPoint
      >>> # Create the DataPoint object for cpu_time
      >>> dp = DataPoint(name='cpu_time', aggregation_type='sum')
  """
  swagger_types = {
    'aggregation_type': 'str',
    'description': 'str',
    'name': 'str',
    'type': 'str',
  }

  attribute_map = {
    'aggregation_type': 'dataPointAggregationType',
    'description': 'dataPointDescription',
    'name': 'dataPointName',
    'type': 'dataPointType',
  }

  def __init__(self, name, aggregation_type=None,
      description=None, type=None):  # noqa: E501

    self._aggregation_type = None
    self._description = None
    self._name = None
    self._type = None
    self.discriminator = None

    if aggregation_type is not None:
      self.aggregation_type = aggregation_type
    if description is not None:
      self.description = description
    if name is not None:
      self.name = name
    if type is not None:
      self.type = type

    error_msg = self.valid_field()
    if error_msg is not None and len(error_msg) > 0:
      raise ValueError(error_msg)

  def __hash__(self):
    return hash(str(self.name))

  @property
  def aggregation_type(self):
    """The aggregation method, if any, that should be used if data is pushed in
    sub-minute intervals. Aloowed values are 'sum', 'average' and 'none'(default). Only considered when creating a new datapoint.

    :return: The type of this DataPoint.
    :rtype: str
    """
    return self._aggregation_type

  @aggregation_type.setter
  def aggregation_type(self, aggregation_type):
    err_msg = objectNameValidator.check_datapoint_aggregation_type_validation(
        aggregation_type)
    if err_msg:
      raise ValueError(err_msg)
    self._aggregation_type = aggregation_type

  @property
  def description(self):
    """Datapoint description. Only considered when creating a new datapoint.


    :return: The description of this DataPoint.
    :rtype: str
    """
    return self._description

  @description.setter
  def description(self, description):
    err_msg = objectNameValidator.check_datapoint_description_validation(
        description)
    if err_msg:
      raise ValueError(err_msg)
    self._description = description

  @property
  def name(self):
    """Datapoint name. If no existing datapoint matches for specified
    DataSource, a new datapoint is created with this name.


    :return: The name of this DataPoint.
    :rtype: str
    """
    return self._name

  @name.setter
  def name(self, name):
    err_msg = objectNameValidator.check_datapoint_name_validation(name)
    if err_msg:
      raise ValueError(err_msg)

    self._name = name

  @property
  def type(self):
    """Metric type (guage or counter) as a number in string format. Only considered when creating a new datapoint.

    :return: The type of this DataPoint.
    :rtype: str
    """
    return self._type

  @type.setter
  def type(self, type):
    err_msg = objectNameValidator.check_datapoint_type_validation(type)
    if err_msg:
      raise ValueError(err_msg)
    self._type = type

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
    if issubclass(DataPoint, dict):
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
    if not isinstance(other, DataPoint):
      return False

    return self.__dict__ == other.__dict__

  def __ne__(self, other):
    """Returns true if both objects are not equal"""
    return not self == other

  def valid_field(self):
    err_msg = ""
    # dataPointName Validations
    err_msg += objectNameValidator.check_datapoint_name_validation(self.name)

    # dataPointDescription Validations
    err_msg += objectNameValidator.check_datapoint_description_validation(
        self.description)

    # DataPointType Validation
    err_msg += objectNameValidator.check_datapoint_type_validation(self.type)

    # dataPointAggregationType Validation
    err_msg += objectNameValidator.check_datapoint_aggregation_type_validation(
        self.aggregation_type)

    return err_msg
