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


class RestResourcePropertiesV1(object):
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
        'resource_ids': 'MapStringString',
        'resource_name': 'str',
        'resource_properties': 'MapStringString'
    }

    attribute_map = {
        'resource_ids': 'resourceIds',
        'resource_name': 'resourceName',
        'resource_properties': 'resourceProperties'
    }

    def __init__(self, resource_ids=None, resource_name=None,
                 resource_properties=None):  # noqa: E501
        """RestResourcePropertiesV1 - a model defined in Swagger"""  # noqa: E501

        self._resource_ids = None
        self._resource_name = None
        self._resource_properties = None
        self.discriminator = None

        if resource_ids is not None:
            self.resource_ids = resource_ids
        if resource_name is not None:
            self.resource_name = resource_name
        if resource_properties is not None:
            self.resource_properties = resource_properties

    @property
    def resource_ids(self):
        """Gets the resource_ids of this RestResourcePropertiesV1.  # noqa: E501


    :return: The resource_ids of this RestResourcePropertiesV1.  # noqa: E501
    :rtype: MapStringString
    """
        return self._resource_ids

    @resource_ids.setter
    def resource_ids(self, resource_ids):
        """Sets the resource_ids of this RestResourcePropertiesV1.


    :param resource_ids: The resource_ids of this RestResourcePropertiesV1.  # noqa: E501
    :type: MapStringString
    """

        self._resource_ids = resource_ids

    @property
    def resource_name(self):
        """Gets the resource_name of this RestResourcePropertiesV1.  # noqa: E501


    :return: The resource_name of this RestResourcePropertiesV1.  # noqa: E501
    :rtype: str
    """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """Sets the resource_name of this RestResourcePropertiesV1.


    :param resource_name: The resource_name of this RestResourcePropertiesV1.  # noqa: E501
    :type: str
    """

        self._resource_name = resource_name

    @property
    def resource_properties(self):
        """Gets the resource_properties of this RestResourcePropertiesV1.  # noqa: E501


    :return: The resource_properties of this RestResourcePropertiesV1.  # noqa: E501
    :rtype: MapStringString
    """
        return self._resource_properties

    @resource_properties.setter
    def resource_properties(self, resource_properties):
        """Sets the resource_properties of this RestResourcePropertiesV1.


    :param resource_properties: The resource_properties of this RestResourcePropertiesV1.  # noqa: E501
    :type: MapStringString
    """

        self._resource_properties = resource_properties

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
        if issubclass(RestResourcePropertiesV1, dict):
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
        if not isinstance(other, RestResourcePropertiesV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
