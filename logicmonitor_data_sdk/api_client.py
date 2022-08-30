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

import base64
import datetime
import hashlib
import hmac
import json
import logging
import mimetypes
import os
import platform
import re
import tempfile
import time
from multiprocessing.pool import ThreadPool

import six
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import unquote

import logicmonitor_data_sdk.models
from logicmonitor_data_sdk import rest
from logicmonitor_data_sdk.configuration import Configuration
from logicmonitor_data_sdk.version import __version__
import io
import gzip
import urllib3.response

# python 2 and python 3 compatibility library

logger = logging.getLogger('lmdata.api')
metrics_company_and_method_based_counter = {}
metrics_method_based_last_time = {}
logs_company_and_method_based_counter = {}
logs_method_based_last_time = {}
requestLimit = 100
timeInSec = 60


class ApiClient(object):
  """
  Generic API client for HTTP client library builds. This client handles the
  client-server communication, and is invariant across implementations.

  Args:
    configuration (:class:`logicmonitor_data_sdk.configuration.Configuration`): The configuration for this REST client.
    header_name (:obj:`str`, optional): a header to pass when making calls to the API..
    header_value (:obj:`str`, optional): a header value to pass when making calls to
      the API.
    cookie (:obj:`str`, optional): a cookie to include in the header when making calls
      to the API.
  """

  PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
  NATIVE_TYPES_MAPPING = {
    'int': int,
    'long': int if six.PY3 else long,  # noqa: F821
    'float': float,
    'str': str,
    'bool': bool,
    'date': datetime.date,
    'datetime': datetime.datetime,
    'object': object,
  }

  def __init__(self, configuration=None, header_name=None, header_value=None,
      cookie=None):
    if configuration is None:
      configuration = Configuration()
    self.configuration = configuration

    self.pool = ThreadPool()
    self.rest_client = rest.RESTClientObject(configuration)
    self.default_headers = {}
    # Set default API version
    self.default_headers['X-version'] = '1';
    if header_name is not None:
      self.default_headers[header_name] = header_value
    self.cookie = cookie
    # Set default User-Agent.
    self.user_agent = 'logicmonitor_data_sdk/{version} (python {pyver}; os {os}; arch {arch})'.format(
        version=__version__,
        pyver=platform.python_version(),
        os=platform.system().lower(),
        arch=platform.machine().lower(),
    )

  def __del__(self):
    self.pool.close()
    self.pool.terminate()
    # self.pool.join()

  @property
  def user_agent(self):
    """User agent for this API client. Default value is
    "logicmonitor_data_sdk/{version} (python {pyver}; os {os}; arch {arch})"

    :return: The type of User-Agent.
    :rtype: str
    """
    return self.default_headers['User-Agent']

  @user_agent.setter
  def user_agent(self, value):
    self.default_headers['User-Agent'] = value

  def set_default_header(self, header_name, header_value):
    self.default_headers[header_name] = header_value

  def __call_api(
      self, resource_path, method, path_params=None,
      query_params=None, header_params=None, body=None, post_params=None,
      files=None, response_type=None, auth_settings=None,
      _return_http_data_only=None, collection_formats=None,
      _preload_content=True, _request_timeout=None, api_type=None, gzip_flag=None):
    config = self.configuration

    # header parameters
    header_params = header_params or {}
    header_params.update(self.default_headers)
    if self.cookie:
      header_params['Cookie'] = self.cookie
    if header_params:
      header_params = self.sanitize_for_serialization(header_params)
      header_params = dict(self.parameters_to_tuples(header_params,
                                                     collection_formats))

    # path parameters
    if path_params:
      path_params = self.sanitize_for_serialization(path_params)
      path_params = self.parameters_to_tuples(path_params,
                                              collection_formats)
      for k, v in path_params:
        # specified safe chars, encode everything
        resource_path = resource_path.replace(
            '{%s}' % k,
            quote(str(v), safe=config.safe_chars_for_path_param)
        )

    # query parameters
    if query_params:
      query_params = self.sanitize_for_serialization(query_params)
      query_params = self.parameters_to_tuples(query_params,
                                               collection_formats)

    # post parameters
    if post_params or files:
      post_params = self.prepare_post_parameters(post_params, files)
      post_params = self.sanitize_for_serialization(post_params)
      post_params = self.parameters_to_tuples(post_params,
                                              collection_formats)

    # body
    if body:
      body = self.sanitize_for_serialization(body)

    # request url
    url = self.configuration.host + resource_path

    # auth setting
    self.update_params_for_auth(
        header_params,
        query_params,
        auth_settings,
        unquote(resource_path),
        method,
        body,
        files)

    # gzip compression
    body = json.dumps(body)
    if gzip_flag is None:
        gzip_flag = config.gzip_flag
    if gzip_flag:
        buf = io.BytesIO()
        with gzip.GzipFile(mode='wb', fileobj=buf) as file:
            file.write(body.encode("utf-8"))
        file.close()
        compressed = buf.getvalue()
        header_params.update({'Content-Encoding': 'gzip'})
        body = compressed

    # perform request and return response
    response_data = self.request_limit_handler(
        method, url, query_params=query_params, headers=header_params,
        post_params=post_params, body=body,
        _preload_content=_preload_content,
        _request_timeout=_request_timeout, api_type=api_type)

    self.last_response = response_data

    return_data = response_data
    if _preload_content:
      # deserialize response data
      if response_type:
        return_data = self.deserialize(response_data, response_type)
      else:
        return_data = None

    if _return_http_data_only:
      return (return_data)
    else:
      return (return_data, response_data.status,response_data.getheaders())

  def sanitize_for_serialization(self, obj):
    if obj is None:
      return None
    elif isinstance(obj, self.PRIMITIVE_TYPES):
      return obj
    elif isinstance(obj, list):
      return [self.sanitize_for_serialization(sub_obj)
              for sub_obj in obj]
    elif isinstance(obj, tuple):
      return tuple(self.sanitize_for_serialization(sub_obj)
                   for sub_obj in obj)
    elif isinstance(obj, (datetime.datetime, datetime.date)):
      return obj.isoformat()

    if isinstance(obj, dict):
      obj_dict = obj
    else:
      # Convert model obj to dict except
      # attributes `swagger_types`, `attribute_map`
      # and attributes which value is not None.
      # Convert attribute name to json key in
      # model definition for request.
      obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                  for attr, _ in six.iteritems(obj.swagger_types)
                  if getattr(obj, attr) is not None}

    return {key: self.sanitize_for_serialization(val)
            for key, val in six.iteritems(obj_dict)}

  def deserialize(self, response, response_type):
    # handle file downloading
    # save response body into a tmp file and return the instance
    if response_type == "file":
      return self.__deserialize_file(response)

    # fetch data from response object
    try:
      data = json.loads(response.data)
    except ValueError:
      data = response.data

    return self.__deserialize(data, response_type)

  def __deserialize(self, data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
      return None

    if type(klass) == str:
      if klass.startswith('list['):
        sub_kls = re.match('list\[(.*)\]', klass).group(1)
        return [self.__deserialize(sub_data, sub_kls)
                for sub_data in data]

      if klass.startswith('dict('):
        sub_kls = re.match('dict\(([^,]*), (.*)\)', klass).group(2)
        return {k: self.__deserialize(v, sub_kls)
                for k, v in six.iteritems(data)}

      # convert str to class
      if klass in self.NATIVE_TYPES_MAPPING:
        klass = self.NATIVE_TYPES_MAPPING[klass]
      else:
        klass = getattr(logicmonitor_data_sdk.models, klass)

    if klass in self.PRIMITIVE_TYPES:
      return self.__deserialize_primitive(data, klass)
    elif klass == object:
      return self.__deserialize_object(data)
    elif klass == datetime.date:
      return self.__deserialize_date(data)
    elif klass == datetime.datetime:
      return self.__deserialize_datatime(data)
    else:
      return self.__deserialize_model(data, klass)

  # @classmethod
  def call_api(self, resource_path, method,
      path_params=None, query_params=None, header_params=None,
      body=None, post_params=None, files=None,
      response_type=None, auth_settings=None, async_req=None,
      _return_http_data_only=None, collection_formats=None,
      _preload_content=True, _request_timeout=None, gzip_flag=None, api_type=None):
    """Makes the HTTP request (synchronous) and returns deserialized data.

    To make an async request, set the async_req parameter.

    :param gzip_flag: flag for gzip compression
    :param resource_path: Path to method endpoint.
    :param method: Method to call.
    :param path_params: Path parameters in the url.
    :param query_params: Query parameters in the url.
    :param header_params: Header parameters to be
        placed in the request header.
    :param body: Request body.
    :param post_params dict: Request post form parameters,
        for `application/x-www-form-urlencoded`, `multipart/form-data`.
    :param auth_settings list: Auth Settings names for the request.
    :param response: Response data type.
    :param files dict: key -> filename, value -> filepath,
        for `multipart/form-data`.
    :param async_req bool: execute request asynchronously
    :param _return_http_data_only: response data without head status code
                                   and headers
    :param collection_formats: dict of collection formats for path, query,
        header, and post parameters.
    :param _preload_content: if False, the urllib3.HTTPResponse object will
                             be returned without reading/decoding response
                             data. Default is True.
    :param _request_timeout: timeout setting for this request. If one
                             number provided, it will be total request
                             timeout. It can also be a pair (tuple) of
                             (connection, read) timeouts.
    :return:
        If async_req parameter is True,
        the request will be called asynchronously.
        The method will return the request thread.
        If parameter async_req is False or missing,
        then the method will return the response directly.
    """
    logger.debug("Making request path:'%s' body:'%s' query_params:%s",
                 resource_path, body, query_params)
    if not async_req:
      return self.__call_api(resource_path, method,
                             path_params, query_params, header_params,
                             body, post_params, files,
                             response_type, auth_settings,
                             _return_http_data_only, collection_formats,
                             _preload_content, _request_timeout, gzip_flag, api_type)
    else:
      thread = self.pool.apply_async(self.__call_api, (resource_path,
                                                       method, path_params,
                                                       query_params,
                                                       header_params, body,
                                                       post_params, files,
                                                       response_type,
                                                       auth_settings,
                                                       _return_http_data_only,
                                                       collection_formats,
                                                       _preload_content,
                                                       _request_timeout,
                                                       gzip_flag,
                                                       api_type))
    return thread

  def request(self, request_params):
    if request_params["method"] == "GET":
      return self.rest_client.GET(request_params["url"],
                                  query_params=request_params["query_params"],
                                  _preload_content=request_params["_preload_content"],
                                  _request_timeout=request_params["_request_timeout"],
                                  headers=request_params["headers"])
    elif request_params["method"] == "HEAD":
      return self.rest_client.HEAD(request_params["url"],
                                   query_params=request_params["query_params"],
                                   _preload_content=request_params["_preload_content"],
                                   _request_timeout=request_params["_request_timeout"],
                                   headers=request_params["headers"])
    elif request_params["method"] == "OPTIONS":
      return self.rest_client.OPTIONS(request_params["url"],
                                      query_params=request_params["query_params"],
                                      headers=request_params["headers"],
                                      post_params=request_params["post_params"],
                                      _preload_content=request_params["_preload_content"],
                                      _request_timeout=request_params["_request_timeout"],
                                      body=request_params["body"])
    elif request_params["method"] == "POST":
      return self.rest_client.POST(request_params["url"],
                                   query_params=request_params["query_params"],
                                   headers=request_params["headers"],
                                   post_params=request_params["post_params"],
                                   _preload_content=request_params["_preload_content"],
                                   _request_timeout=request_params["_request_timeout"],
                                   body=request_params["body"])
    elif request_params["method"] == "PUT":
      return self.rest_client.PUT(request_params["url"],
                                  query_params=request_params["query_params"],
                                  headers=request_params["headers"],
                                  post_params=request_params["post_params"],
                                  _preload_content=request_params["_preload_content"],
                                  _request_timeout=request_params["_request_timeout"],
                                  body=request_params["body"])
    elif request_params["method"] == "PATCH":
      return self.rest_client.PATCH(request_params["url"],
                                    query_params=request_params["query_params"],
                                    headers=request_params["headers"],
                                    post_params=request_params["post_params"],
                                    _preload_content=request_params["_preload_content"],
                                    _request_timeout=request_params["_request_timeout"],
                                    body=request_params["body"])
    elif request_params["method"] == "DELETE":
      return self.rest_client.DELETE(request_params["url"],
                                     query_params=request_params["query_params"],
                                     headers=request_params["headers"],
                                     _preload_content=request_params["_preload_content"],
                                     _request_timeout=request_params["_request_timeout"],
                                     body=request_params["body"])
    else:
      raise ValueError(
          "http method must be `GET`, `HEAD`, `OPTIONS`,"
          " `POST`, `PATCH`, `PUT` or `DELETE`."
      )

  def request_limit_handler(self, method, url, query_params=None, headers=None, post_params=None,
                            body=None, _preload_content=True, _request_timeout=None, api_type=None,):
    request_params = {"method": method, "url": url, "query_params": query_params, "headers": headers,
                      "post_params": post_params, "body": body, "_preload_content": _preload_content,
                      "_request_timeout": _request_timeout, "api_type": api_type}
    dummy_response = urllib3.response.HTTPResponse(status=413, reason="OK",
                                                   body='{"code": 413, "errors": [],''"message": "The number of '
                                                        'requests exceeds the rate limit.", ''"timestamp": ' + str(
                                                     int(time.time())) + '}')
    company = self.configuration._company
    if request_params["api_type"] == "metrics":
      if company in metrics_company_and_method_based_counter.keys():
        if request_params["method"] + "_counter" in metrics_company_and_method_based_counter[company].keys():
          metrics_company_and_method_based_counter[company][request_params["method"] + "_counter"] += 1
        else:
          metrics_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 1
          metrics_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(
            time.time())
      else:
        metrics_company_and_method_based_counter[company] = {}
        metrics_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 1
        metrics_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(
          time.time())
      current_time = int(time.time())
      timediff = current_time - metrics_method_based_last_time[
        company + "_" + request_params["method"] + "_last_time"]
      if metrics_company_and_method_based_counter[company][
        request_params["method"] + "_counter"] >= requestLimit and timediff <= timeInSec:
        time.sleep(1)
        return dummy_response
      if timediff >= timeInSec:
        metrics_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 0
        metrics_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(
          time.time())
      return self.request(request_params)
    else:
      if company in logs_company_and_method_based_counter.keys():
        if request_params["method"] + "_counter" in logs_company_and_method_based_counter[company].keys():
          logs_company_and_method_based_counter[company][request_params["method"] + "_counter"] += 1
        else:
          logs_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 1
          logs_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(
            time.time())
      else:
        logs_company_and_method_based_counter[company] = {}
        logs_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 0
        logs_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(time.time())
      current_time = int(time.time())
      timediff = current_time - logs_method_based_last_time[
        company + "_" + request_params["method"] + "_last_time"]
      if logs_company_and_method_based_counter[company][
        request_params["method"] + "_counter"] >= requestLimit and timediff <= timeInSec:
        time.sleep(1)
        return dummy_response
      if timediff >= timeInSec:
        logs_company_and_method_based_counter[company][request_params["method"] + "_counter"] = 0
        logs_method_based_last_time[company + "_" + request_params["method"] + "_last_time"] = int(
          time.time())
      return self.request(request_params)

  def parameters_to_tuples(self, params, collection_formats):
    new_params = []
    if collection_formats is None:
      collection_formats = {}
    for k, v in six.iteritems(params) if isinstance(params,
                                                    dict) else params:  # noqa: E501
      if k in collection_formats:
        collection_format = collection_formats[k]
        if collection_format == 'multi':
          new_params.extend((k, value) for value in v)
        else:
          if collection_format == 'ssv':
            delimiter = ' '
          elif collection_format == 'tsv':
            delimiter = '\t'
          elif collection_format == 'pipes':
            delimiter = '|'
          else:  # csv is the default
            delimiter = ','
          new_params.append(
              (k, delimiter.join(str(value) for value in v)))
      else:
        new_params.append((k, v))
    return new_params

  def prepare_post_parameters(self, post_params=None, files=None):
    params = []

    if post_params:
      params = post_params

    if files:
      for k, v in six.iteritems(files):
        if not v:
          continue
        file_names = v if type(v) is list else [v]
        for n in file_names:
          with open(n, 'rb') as f:
            filename = os.path.basename(f.name)
            filedata = f.read()
            mimetype = (mimetypes.guess_type(filename)[0] or
                        'application/octet-stream')
            params.append(
                tuple([k, tuple([filename, filedata, mimetype])]))

    return params

  def select_header_accept(self, accepts):
    if not accepts:
      return

    accepts = [x.lower() for x in accepts]

    if 'application/json' in accepts:
      return 'application/json'
    else:
      return ', '.join(accepts)

  def select_header_content_type(self, content_types):
    if not content_types:
      return 'application/json'

    content_types = [x.lower() for x in content_types]

    if 'application/json' in content_types or '*/*' in content_types:
      return 'application/json'
    else:
      return content_types[0]

  def update_params_for_auth(self,
      headers,
      querys,
      auth_settings,
      resource_path,
      method,
      body=None,
      files=None):
    if not auth_settings:
      return

    for auth in auth_settings:
      auth_setting = self.configuration.auth_settings().get(auth)
      if auth_setting:
        if not auth_setting['value']:
          continue
        elif auth_setting['in'] == 'header':
          if not auth_setting.get('id'):
            headers[auth_setting['key']] = auth_setting['value']
          else:
            # Get current time in milliseconds
            epoch = str(int(time.time() * 1000))

            # Concatenate Request details
            if body is not None:
              request_vars = method + epoch + json.dumps(body) + resource_path
            elif files is not None:
              filedata = ''
              for k, v in six.iteritems(files):
                if not v:
                  continue
                file_names = v if type(v) is list else [v]
                for n in file_names:
                  with open(n, 'rb') as f:
                    filedata = filedata + f.read().decode()
              request_vars = method + epoch + filedata + resource_path
            else:
              request_vars = method + epoch + resource_path

            # Construct signature
            signature = base64.b64encode(hmac.new(
                auth_setting['value'].encode('utf-8'),
                msg=request_vars.encode('utf-8'),
                digestmod=hashlib.sha256).hexdigest().encode('utf-8'))

            # Construct headers
            auth_hash = (
                'LMv1 ' +
                auth_setting['id'] + ':' +
                signature.decode() + ':' +
                epoch)

            headers[auth_setting['key']] = auth_hash
        elif auth_setting['in'] == 'query':
          querys.append((auth_setting['key'], auth_setting['value']))
        else:
          raise ValueError(
              'Authentication token must be in `query` or `header`'
          )

  def __deserialize_file(self, response):
    """Deserializes body to file

    Saves response body into a file in a temporary folder,
    using the filename from the `Content-Disposition` header if provided.

    :param response:  RESTResponse.
    :return: file path.
    """
    fd, path = tempfile.mkstemp(dir=self.configuration.temp_folder_path)
    os.close(fd)
    os.remove(path)

    content_disposition = response.getheader("Content-Disposition")
    if content_disposition:
      filename = re.search(r'filename=[\'"]?([^\'"\s]+)[\'"]?',
                           content_disposition).group(1)
      path = os.path.join(os.path.dirname(path), filename)

    with open(path, "wb") as f:
      f.write(response.data)

    return path

  def __deserialize_primitive(self, data, klass):
    """Deserializes string to primitive type.

    :param data: str.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    """
    try:
      return klass(data)
    except UnicodeEncodeError:
      return six.text_type(data)
    except TypeError:
      return data

  def __deserialize_object(self, value):
    """Return a original value.

    :return: object.
    """
    return value

  def __deserialize_date(self, string):
    """Deserializes string to date.

    :param string: str.
    :return: date.
    """
    try:
      from dateutil.parser import parse
      return parse(string).date()
    except ImportError:
      return string
    except ValueError:
      raise rest.ApiException(
          status=0,
          reason="Failed to parse `{0}` as date object".format(string)
      )

  def __deserialize_datatime(self, string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :return: datetime.
    """
    try:
      from dateutil.parser import parse
      return parse(string)
    except ImportError:
      return string
    except ValueError:
      raise rest.ApiException(
          status=0,
          reason=(
            "Failed to parse `{0}` as datetime object"
              .format(string)
          )
      )

  def __hasattr(self, object, name):
    return name in object.__class__.__dict__

  def __deserialize_model(self, data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :param klass: class literal.
    :return: model object.
    """

    if not klass.swagger_types and not self.__hasattr(klass,
                                                      'get_real_child_model'):
      return data

    kwargs = {}
    if klass.swagger_types is not None:
      for attr, attr_type in six.iteritems(klass.swagger_types):
        if (data is not None and
            klass.attribute_map[attr] in data and
            isinstance(data, (list, dict))):
          value = data[klass.attribute_map[attr]]
          kwargs[attr] = self.__deserialize(value, attr_type)

    instance = klass(**kwargs)

    if (isinstance(instance, dict) and
        klass.swagger_types is not None and
        isinstance(data, dict)):
      for key, value in data.items():
        if key not in klass.swagger_types:
          instance[key] = value
    if self.__hasattr(instance, 'get_real_child_model'):
      klass_name = instance.get_real_child_model(data)
      if klass_name:
        instance = self.__deserialize(data, klass_name)
    return instance
