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

from logicmonitor_data_sdk.models.map_string_string import MapStringString  # noqa: F401,E501

"""
    LogicMonitor API-Ingest Rest API

    LogicMonitor is a SaaS-based performance monitoring platform that provides full visibility into complex, hybrid infrastructures, offering granular performance monitoring and actionable data and insights. API-Ingest provides the entry point in the form of public rest APIs for ingesting metrics into LogicMonitor. For using this application users have to create LMAuth token using access id and key from santaba.  # noqa: E501

    OpenAPI spec version: 3.0.0

"""


class RestInstancePropertiesV1(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'data_source': 'str',
        'data_source_display_name': 'str',
        'instance_name': 'str',
        'instance_properties': 'MapStringString',
        'resource_ids': 'MapStringString'
    }

    attribute_map = {
        'data_source': 'dataSource',
        'data_source_display_name': 'dataSourceDisplayName',
        'instance_name': 'instanceName',
        'instance_properties': 'instanceProperties',
        'resource_ids': 'resourceIds'
    }

    def __init__(self, data_source=None, data_source_display_name=None,
                 instance_name=None, instance_properties=None,
                 resource_ids=None):  # noqa: E501
        """RestInstancePropertiesV1 - a model defined in Swagger"""  # noqa: E501

        self._data_source = None
        self._data_source_display_name = None
        self._instance_name = None
        self._instance_properties = None
        self._resource_ids = None
        self.discriminator = None

        if data_source is not None:
            self.data_source = data_source
        if data_source_display_name is not None:
            self.data_source_display_name = data_source_display_name
        if instance_name is not None:
            self.instance_name = instance_name
        if instance_properties is not None:
            self.instance_properties = instance_properties
        if resource_ids is not None:
            self.resource_ids = resource_ids

    @property
    def data_source(self):
        """Gets the data_source of this RestInstancePropertiesV1.  # noqa: E501


    :return: The data_source of this RestInstancePropertiesV1.  # noqa: E501
    :rtype: str
    """
        return self._data_source

    @data_source.setter
    def data_source(self, data_source):
        """Sets the data_source of this RestInstancePropertiesV1.


    :param data_source: The data_source of this RestInstancePropertiesV1.  # noqa: E501
    :type: str
    """

        self._data_source = data_source

    @property
    def data_source_display_name(self):
        """Gets the data_source_display_name of this RestInstancePropertiesV1.  # noqa: E501


    :return: The data_source_display_name of this RestInstancePropertiesV1.  # noqa: E501
    :rtype: str
    """
        return self._data_source_display_name

    @data_source_display_name.setter
    def data_source_display_name(self, data_source_display_name):
        """Sets the data_source_display_name of this RestInstancePropertiesV1.


    :param data_source_display_name: The data_source_display_name of this RestInstancePropertiesV1.  # noqa: E501
    :type: str
    """

        self._data_source_display_name = data_source_display_name

    @property
    def instance_name(self):
        """Gets the instance_name of this RestInstancePropertiesV1.  # noqa: E501


    :return: The instance_name of this RestInstancePropertiesV1.  # noqa: E501
    :rtype: str
    """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this RestInstancePropertiesV1.


    :param instance_name: The instance_name of this RestInstancePropertiesV1.  # noqa: E501
    :type: str
    """

        self._instance_name = instance_name

    @property
    def instance_properties(self):
        """Gets the instance_properties of this RestInstancePropertiesV1.  # noqa: E501


    :return: The instance_properties of this RestInstancePropertiesV1.  # noqa: E501
    :rtype: MapStringString
    """
        return self._instance_properties

    @instance_properties.setter
    def instance_properties(self, instance_properties):
        """Sets the instance_properties of this RestInstancePropertiesV1.


    :param instance_properties: The instance_properties of this RestInstancePropertiesV1.  # noqa: E501
    :type: MapStringString
    """

        self._instance_properties = instance_properties

    @property
    def resource_ids(self):
        """Gets the resource_ids of this RestInstancePropertiesV1.  # noqa: E501


    :return: The resource_ids of this RestInstancePropertiesV1.  # noqa: E501
    :rtype: MapStringString
    """
        return self._resource_ids

    @resource_ids.setter
    def resource_ids(self, resource_ids):
        """Sets the resource_ids of this RestInstancePropertiesV1.


    :param resource_ids: The resource_ids of this RestInstancePropertiesV1.  # noqa: E501
    :type: MapStringString
    """

        self._resource_ids = resource_ids

    def to_dict(self):
        """Returns the model properties as a dict"""
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
                result[attr] = value
        if issubclass(RestInstancePropertiesV1, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RestInstancePropertiesV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
