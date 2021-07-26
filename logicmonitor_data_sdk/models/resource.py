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


class Resource(object):
  """
  This model is used to define the resource.

  Args:
    ids (:obj:`dict`): An array of existing resource properties that  will be
      used to identify the resource. See Managing Resources that Ingest
      Push Metrics for information on the types of properties that can be used.
      If no resource is matched and the create parameter is set to TRUE, a
      new resource is created with these specified resource IDs set on it.
      If the system.displayname and/or system.hostname property is included
      as resource IDs, they will be used as host name and display name
      respectively in the resulting resource.
    name (:obj:`str`): Resource unique name. Only considered when creating a new resource.
    properties (:obj:`dict` of :obj:`str`, optional): New properties for resource. Updates to existing resource
      properties are not considered. Depending on the property name, we will
      convert these properties into system, auto, or custom properties.
    description(:obj:`str`, optional): Resource description. Only considered when creating a new resource.
    create (:obj:`bool`, optional): Do you want to create the resource.

  Examples:
      >>> from logicmonitor_data_sdk.models.resource import Resource
      >>> # Create the Resource object using the 'system.deviceId' properties.
      >>> resource = Resource(ids={'system.deviceId' : '1234'}, name='DeviceName', create=False)

  """
  swagger_types = {
    'description': 'str',
    'ids': 'MapStringString',
    'name': 'str',
    'properties': 'MapStringString',
    'create': 'bool'
  }

  attribute_map = {
    'description': 'resourceDescription',
    'ids': 'resourceIds',
    'name': 'resourceName',
    'properties': 'resourceProperties',
    'create': 'create'
  }

  def __init__(self, ids, name='None', description=None, properties=None,
      create=False):  # noqa: E501

    self._description = None
    self._ids = None
    self._name = None
    self._properties = None
    self.discriminator = None
    self._create = False
    self.create = create
    if description is not None:
      self.description = description
    if ids is not None:
      self.ids = ids
    if name is not None:
      self.name = name
    if properties is not None:
      self.properties = properties
    error_msg = self._valid_field()
    if error_msg is not None and len(error_msg) > 0:
      raise ValueError(error_msg)

  def __hash__(self):
    return hash(str(self._ids))

  @property
  def ids(self):
    """An array of existing resource properties that  will be used to identify
    the resource. See Managing Resources that Ingest Push Metrics for
    information on the types of properties that can be used. If no resource
    is matched and the create parameter is set to TRUE, a new resource is
    created with these specified resource IDs set on it. If the
    system.displayname and/or system.hostname property is included as
    resource IDs, they will be used as host name and display name respectively
    in the resulting resource.

    :return: The ids of this Resource.
    :rtype: dict
    """
    return self._ids

  @ids.setter
  def ids(self, ids):
    err_msg = objectNameValidator.check_resource_ids_validation(ids)
    if err_msg:
      raise ValueError(err_msg)

    self._ids = ids

  @property
  def name(self):
    """Resource unique name. Only considered when creating a new resource.

    :return: The name of this Resource.
    :rtype: str
    """
    return self._name

  @name.setter
  def name(self, name):
    err_msg = objectNameValidator.check_resource_name_validation(self._create,
                                                                 name)
    if err_msg:
      raise ValueError(err_msg)

    self._name = name

  @property
  def description(self):
    """Resource description. Only considered when creating a new resource.

    :return: The description of this Resource.
    :rtype: str
    """
    return self._description

  @description.setter
  def description(self, description):
    err_msg = objectNameValidator.check_resource_description_validation(
        description)
    if err_msg:
      raise ValueError(err_msg)

    self._description = description

  @property
  def properties(self):
    """New properties for resource. Updates to existing resource properties are
    not considered. Depending on the property name, we will convert these
    properties into system, auto, or custom properties.

    :return: The properties of this Resource.
    :rtype: dict
    """
    return self._properties

  @properties.setter
  def properties(self, properties):
    """Sets the properties of this Resource.

    :param properties: The properties of this Resource.
    :type: dict
    """
    err_msg = objectNameValidator.check_resource_properties_validation(
        properties)
    if err_msg:
      raise ValueError(err_msg)

    self._properties = properties

  @property
  def create(self):
    """Gets the create flag.

    :return: create flag.
    :rtype: bool
    """
    return self._create

  @create.setter
  def create(self, create):
    """Sets the create flag.

    :param ids: The boolean flag of this Resource.
    :type: boolean
    """
    self._create = create

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
    if issubclass(Resource, dict):
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
    if not isinstance(other, Resource):
      return False

    return self.__dict__ == other.__dict__

  def __ne__(self, other):
    """Returns true if both objects are not equal"""
    return not self == other

  def _valid_field(self):
    err_msg = ""
    # resourceName Validations
    err_msg += objectNameValidator.check_resource_name_validation(self.create,
                                                                  self.name)

    # resourceDescription Validations
    err_msg += objectNameValidator.check_resource_description_validation(
        self.description)

    # resourceIds Validation
    err_msg += objectNameValidator.check_resource_ids_validation(self.ids)

    # resourceProperties Validation
    err_msg += objectNameValidator.check_resource_properties_validation(
        self.properties)

    return err_msg
