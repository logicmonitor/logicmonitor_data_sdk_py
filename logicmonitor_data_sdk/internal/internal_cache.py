
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

#    LogicMonitor API-Ingest Rest API

#    LogicMonitor is a SaaS-based performance monitoring platform that provides full visibility into complex, hybrid infrastructures, offering granular performance monitoring and actionable data and insights. API-Ingest provides the entry point in the form of public rest APIs for ingesting metrics into LogicMonitor. For using this application users have to create LMAuth token using access id and key from santaba.  # noqa: E501

#    OpenAPI spec version: 3.0.0



from __future__ import absolute_import

import collections
import logging
import queue
import threading
import time

import six

from logicmonitor_data_sdk import ApiClient
from logicmonitor_data_sdk.api.response_interface import ResonseInterface

logger = logging.getLogger('lmdata.api')
_DEFAULT_QUEUE = 100


class BatchingCache(object):
  _ADD_REQUEST = 'A'
  _MERGE_REQUEST = 'M'
  _PAYLOAD_SEND = 'S'
  _PAYLOAD_BUILD = 'B'
  _PAYLOAD_TOTAL = 'T'
  _PAYLOAD_EXCEPTION = 'E'

  _RESPONSE_CODE = {200: ('O', "OK"), 202: ('O', "OK"),
                    207: ("M", "MULTI_STATUS"),
                    400: ('B', "BAD_REQUEST"), 401: ('U', "UNAUTHORIZED"),
                    402: ('P', "PAYMENT"), 403: ('F', "FORBIDDEND"),
                    404: ('N', "NOT_FOUND"), 406: ('A', "NOT_ACCEPTABLE"),
                    408: ('T', "TIMEOUT"), 500: ('I', "INTERNAL_ERROR"),
                    503: ('D', "UNAVAILABLE")}

  def __init__(self, api_client, interval, batch, response_callback, request_cb,
      merge_cb):
    if api_client is None:
      api_client = ApiClient()
    self.api_client = api_client
    self._lock = threading.Lock()
    self._raw_requests = queue.Queue(_DEFAULT_QUEUE)
    self._has_request = threading.Semaphore(value=0)  # ADDED THIS
    self._payload_cache = {}
    self._last_time_send = int(time.time())
    self.__init = True
    self._batch = batch
    self._interval = interval
    # self._size = size
    self._size = None
    self._request_cb = request_cb
    self._merge_cb = merge_cb
    if not response_callback and not isinstance(response_callback,
                                                ResonseInterface):
      logger.warn("Response callback is not defined or valid.")
      self._response_callback = None
    else:
      self._response_callback = response_callback
    # self._count = count
    self._count = None
    self._counter = collections.Counter()
    self._request_counter = collections.Counter()
    self._last_time_stat = int(time.time())
    if self._batch:
      self._merge_thread = threading.Thread(target=self.merge_request)
      self._merge_thread.daemon = True
      self._merge_thread.start()
      self._request_thread = threading.Thread(target=self.do_request)
      self._request_thread.daemon = True
      self._request_thread.start()
      # self._stat_thread = threading.Thread(target=self._print_stats)
      # self._stat_thread.daemon = True
      # self._stat_thread.start()
      logger.info(
          "{} api processor is initialized with interval={}".format(
              self.__class__.__name__,
              interval))
    else:
      logger.info(
          "{} initialized without batch support".format(
              self.__class__.__name__))

  @property
  def batch(self):
    return self._batch

  @batch.setter
  def batch(self, batch):
    self._batch = batch

  def merge_request(self):
    while self.has_request().acquire():  # ADDED THIS: Acquire a Semaphore, or sleep until the counter of semaphore is larger than zero
      single_request = self.get_requests().get()
      try:
        self.Lock()
        self._counter.update(BatchingCache._MERGE_REQUEST)
        self._merge_cb(single_request)
      finally:
        self.UnLock()

  def do_request(self):
    while True:
      current_time = int(time.time())
      if current_time > (self._last_time_stat + 10):
        self._print_stats()
        self._last_time_stat = current_time
      if current_time > (self._last_time_send + self._interval):
        try:
          self._request_cb()
        except Exception as ex:
          logger.exception("Got Exception " + str(ex), exc_info=ex)
        self._last_time_send = current_time
      else:
        time.sleep(1)

  def _print_stats(self):
    add_request = self._counter.get(BatchingCache._ADD_REQUEST)
    merge_request = self._counter.get(BatchingCache._MERGE_REQUEST)
    payload_send = self._counter.get(BatchingCache._PAYLOAD_SEND)
    payload_build = self._counter.get(BatchingCache._PAYLOAD_BUILD)
    payload_total = self._counter.get(BatchingCache._PAYLOAD_TOTAL)
    payload_exception = self._counter.get(BatchingCache._PAYLOAD_EXCEPTION)
    smsg = "{} CurrentTime:'{}' LastReqestTime:'{}' SendMetricsCalls:{} MergedRequest:{} " \
           "BuildingRestPayload:{} RestApiSend:{} PossibleRestApiReqests:{} RestException:{}".format(
        self.__class__.__name__,
        time.strftime("%H:%M:%S %Z", time.localtime(time.time())),
        time.strftime("%H:%M:%S %Z", time.localtime(self._last_time_send)),
        add_request, merge_request, payload_build, payload_send,
        payload_total, payload_exception)
    logger.debug(smsg)
    smsg = "{} Couter:'{}'".format(self.__class__.__name__,
                                   self._request_counter)
    logger.debug(smsg)

  def _response_handler(self, request, response, status, headers, reason=None):
    logger.debug("Response is {%s} {%s} {%s}", response, status, headers)
    codes = BatchingCache._RESPONSE_CODE[status]
    if codes is not None:
      self._request_counter.update(codes[0])
    else:
      self._request_counter.update("E")
    try:
      if self._response_callback and str(status) in ['200', '202']:
        self._response_callback.success_callback(request, response, status,
                                                 headers['x-request-id'])
      if self._response_callback and int(status) >= 300:
        self._response_callback.error_callback(request, response, status,
                                               headers['x-request-id'], reason)
    except Exception as ex:
      logger.exception("Got Exception in response callback " + str(ex))

  def add_request(self, **kwargs):
    self._raw_requests.put(kwargs)
    self._counter.update(BatchingCache._ADD_REQUEST)
    self._has_request.release()

  def has_request(self):
    return self._has_request

  def get_requests(self):
    return self._raw_requests

  def get_payload(self):
    return self._payload_cache

  def Lock(self):
    self._lock.acquire()

  def UnLock(self):
    self._lock.release()

  def make_request(self, path, method, **kwargs):  # noqa: E501

    all_params = ['create', 'body']  # noqa: E501
    all_params.append('async_req')
    all_params.append('_return_http_data_only')
    all_params.append('_preload_content')
    all_params.append('_request_timeout')

    params = locals()
    for key, val in six.iteritems(params['kwargs']):
      if key not in all_params:
        raise TypeError(
            "Got an unexpected keyword argument '%s'"
            " to method metric_ingest_post" % key
        )
      params[key] = val
    del params['kwargs']

    collection_formats = {}

    path_params = {}

    query_params = []
    if 'create' in params and path == '/metric/ingest':
      query_params.append(('create', params['create']))  # noqa: E501

    if 'async_req' not in params:
      params['async_req'] = self.api_client.configuration.async_req
    header_params = {}

    form_params = []
    local_var_files = {}

    body_params = None
    if 'body' in params:
      body_params = params['body']
    # HTTP header `Accept`
    header_params['Accept'] = self.api_client.select_header_accept(
        ['application/json'])  # noqa: E501

    # HTTP header `Content-Type`
    header_params['Content-Type'] = self.api_client.select_header_content_type(
        # noqa: E501
        ['application/json'])  # noqa: E501

    # Authentication setting
    auth_settings = ['LMv1']  # noqa: E501
    # if the response type is a file, set _preload_content_value=false.
    # Because python 3.0+ 'utf-8' codec can't decode the binary string
    _response_type = 'PushMetricAPIResponse'
    _preload_content_value = True
    if _response_type == 'file':
      _preload_content_value = False

    return self.api_client.call_api(
        path, method,
        path_params,
        query_params,
        header_params,
        body=body_params,
        post_params=form_params,
        files=local_var_files,
        response_type=_response_type,
        auth_settings=auth_settings,
        async_req=params.get('async_req'),
        _return_http_data_only=params.get('_return_http_data_only'),
        _preload_content=params.get('_preload_content', _preload_content_value),
        _request_timeout=params.get('_request_timeout'),
        collection_formats=collection_formats)
