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

from __future__ import absolute_import

import copy
import logging
import multiprocessing
import os
import platform
import six
from six.moves import http_client as httplib

from logicmonitor_data_sdk.utils.object_name_validator import ObjectNameValidator
from logicmonitor_data_sdk.version import __version__

objectNameValidator = ObjectNameValidator()

class TypeWithDefault(type):
  def __init__(cls, name, bases, dct):
    super(TypeWithDefault, cls).__init__(name, bases, dct)
    cls._default = None

  def __call__(cls, **kwargs):
    if cls._default is None:
      cls._default = type.__call__(cls, **kwargs)
    return copy.copy(cls._default)

  def set_default(cls, default):
    cls._default = copy.copy(default)


class Configuration(six.with_metaclass(TypeWithDefault, object)):
  """
  This model is used to defining the configuration.

  Args:
      company (:obj:`str`): The account name. If it is not provided then we will
        use the 'LM_COMPANY' environment variable.

      authentication (:obj:`dict` of `id` and `key`):  LogicMonitor supports
        verious types of the authentication. This variable will be used to
        specify the authentication key. If it is not provided then 'LM_ACCESS_ID'
        and 'LM_ACCESS_KEY' environment variable will be used to find the id and key.
      id (:obj:`str`): The access token id. If it is not provided then we will
        use the 'LM_ACCESS_ID' environment variable or authentication variable.
      key (:obj:`str`): The access token key. If it is not provided then we will
        use the 'LM_ACCESS_KEY' environment variable or authentication variable.
  Examples:
    >>> import logicmonitor_data_sdk
    >>> # Or use 'id' and 'key' variables to specify the access token.
    >>> conf = logicmonitor_data_sdk.Configuration(company="ACCOUNT_NAME", id='API_ACCESS_ID', key= 'API_ACCESS_KEY')
  """

  def __init__(self, company=None, authentication=None, id=None, key=None):
    """Constructor"""
    # Default Base url
    company = company or os.environ.get('LM_COMPANY')
    if company == None or company == '':
      raise ValueError(
          'Company must have your account name'
      )
    if not objectNameValidator.is_valid_company_name(company):
      raise ValueError(
          'Invalid Company Name'
      )
    if not authentication:
      id = os.environ.get('LM_ACCESS_ID', id)
      key = os.environ.get('LM_ACCESS_KEY', key)
      # type = os.environ.get('LM_ACCESS_TYPE', 'LMv1')
      if (id and key):
        authentication = {'id': id, 'key': key}
    if not authentication or not isinstance(authentication,
                                            dict) or 'id' not in authentication or 'key' not in authentication:
      raise ValueError(
          'Authentication must provide the `id` and `key`'
      )
    if not objectNameValidator.is_valid_auth_id(authentication.get('id', None)):
      raise ValueError(
          'Invalid Access ID'
      )
    if authentication.get('key', None):
      if not objectNameValidator.is_valid_auth_key(authentication.get('key', None)):
        raise ValueError(
          'Invalid Access Key'
        )
    self._company = company
    self._host = "https://" + self._company + ".logicmonitor.com/rest"
    self.check_authentication(authentication)
    self._async_req = False
    # Temp file folder for downloading files
    self.temp_folder_path = None

    # Logging Settings
    self.logger = {}
    self.logger["package_logger"] = logging.getLogger("lmdata")
    self.logger["urllib3_logger"] = logging.getLogger("urllib3")
    # Log format
    self.logger_format = '%(asctime)s %(levelname)s %(message)s'
    # Log stream handler
    self.logger_stream_handler = None
    # Log file handler
    self.logger_file_handler = None
    # Debug file location
    self.logger_file = None
    # Debug switch
    self.debug = False

    # SSL/TLS verification
    # Set this to false to skip verifying SSL certificate when calling API
    # from https server.
    self.verify_ssl = True
    # Set this to customize the certificate file to verify the peer.
    self.ssl_ca_cert = None
    # client certificate file
    self.cert_file = None
    # client key file
    self.key_file = None
    # Set this to True/False to enable/disable SSL hostname verification.
    self.assert_hostname = None

    # urllib3 connection pool's maximum number of connections saved
    # per pool. urllib3 uses 1 connection as default value, but this is
    # not the best value when you are making a lot of possibly parallel
    # requests to the same host, which is often the case here.
    # cpu_count * 5 is used as default value to increase performance.
    self.connection_pool_maxsize = multiprocessing.cpu_count() * 5

    # Proxy URL
    self.proxy = None
    # Safe chars for path_param
    self.safe_chars_for_path_param = ''

  @property
  def logger_file(self):
    """The logger file.

    If the logger_file is None, then add stream handler and remove file
    handler. Otherwise, add file handler and remove stream handler.

    :param value: The logger_file path.
    :type: str
    """
    return self.__logger_file

  @logger_file.setter
  def logger_file(self, value):
    """The logger file.

    If the logger_file is None, then add stream handler and remove file
    handler. Otherwise, add file handler and remove stream handler.

    :param value: The logger_file path.
    :type: str
    """
    self.__logger_file = value
    if self.__logger_file:
      # If set logging file,
      # then add file handler and remove stream handler.
      self.logger_file_handler = logging.FileHandler(self.__logger_file)
      self.logger_file_handler.setFormatter(self.logger_formatter)
      for _, logger in six.iteritems(self.logger):
        logger.addHandler(self.logger_file_handler)
        if self.logger_stream_handler:
          logger.removeHandler(self.logger_stream_handler)
    else:
      # If not set logging file,
      # then add stream handler and remove file handler.
      self.logger_stream_handler = logging.StreamHandler()
      self.logger_stream_handler.setFormatter(self.logger_formatter)
      for _, logger in six.iteritems(self.logger):
        logger.addHandler(self.logger_stream_handler)
        if self.logger_file_handler:
          logger.removeHandler(self.logger_file_handler)

  @property
  def debug(self):
    """Debug status

    :param value: The debug status, True or False.
    :type: bool
    """
    return self.__debug

  @debug.setter
  def debug(self, value):
    """Debug status

    :param value: The debug status, True or False.
    :type: bool
    """
    self.__debug = value
    if self.__debug:
      # if debug status is True, turn on debug logging
      for _, logger in six.iteritems(self.logger):
        logger.setLevel(logging.DEBUG)
      # turn on httplib debug
      httplib.HTTPConnection.debuglevel = 1
    else:
      # if debug status is False, turn off debug logging,
      # setting log level to default `logging.WARNING`
      for _, logger in six.iteritems(self.logger):
        logger.setLevel(logging.INFO)
      # turn off httplib debug
      httplib.HTTPConnection.debuglevel = 0

  @property
  def async_req(self):
    """The async request.

    :param value: enable async request string.
    :type: bool
    """
    return self._async_req

  @async_req.setter
  def async_req(self, value):
    """The async request.

    :param value: enable async request string.
    :type: bool
    """
    self._async_req = value

  @property
  def logger_format(self):
    """The logger format.

    The logger_formatter will be updated when sets logger_format.

    :param value: The format string.
    :type: str
    """
    return self.__logger_format

  @logger_format.setter
  def logger_format(self, value):
    """The logger format.

    The logger_formatter will be updated when sets logger_format.

    :param value: The format string.
    :type: str
    """
    self.__logger_format = value
    self.logger_formatter = logging.Formatter(self.__logger_format)

  @property
  def company(self):
    self._company

  @company.setter
  def company(self, value):
    self._company = value
    self._host = "https://" + self._company + ".logicmonitor.com/rest"

  @property
  def authentication(self):
    self._authentication

  @authentication.setter
  def authentication(self, value):
    self.check_authentication(value)

  def check_authentication(self, authentication):
    if not authentication or not isinstance(authentication,
                                            dict) or 'id' not in authentication or 'key' not in authentication:
      raise ValueError(
          'Authentication must provide the `id` and `key`'
      )
    self._authentication = authentication
    self._authentication['type'] = 'LMv1'

  @property
  def host(self):
    return self._host

  def auth_settings(self):
    if self._authentication != None and 'type' in self._authentication and 'key' in self._authentication and 'id' in self._authentication:
      return {
        self._authentication['type']:
          {
            'type': 'api_key',
            'in': 'header',
            'key': 'Authorization',
            'value': self._authentication['key'],
            'id': self._authentication['id']
          },
      }
    else:
      return {
        'LMv1': {'type': 'api_key',
                 'in': 'header',
                 'key': 'Authorization',
                 'value': '',
                 'id': ''
                 }
      }

  def to_debug_report(self):
    """Gets the essential information for debugging.

    :return: The report for debugging.
    """
    return 'Python SDK Debug Report {version} (python {pyver}; os {os}; arch {arch})'.format(
        version=__version__,
        pyver=platform.python_version(),
        os=platform.system().lower(),
        arch=platform.machine().lower(),
    )
