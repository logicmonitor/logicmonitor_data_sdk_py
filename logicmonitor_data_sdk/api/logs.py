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

# Logs API client: It formats and submit REST API calls to LogicMonitor.


from __future__ import absolute_import

import copy
import logging
import re  # noqa: F401
from multiprocessing.pool import ApplyResult

import six

from logicmonitor_data_sdk.internal.internal_cache import BatchingCache
# python 2 and python 3 compatibility library
from logicmonitor_data_sdk.rest import ApiException

logger = logging.getLogger('lmdata.api')


class Logs(BatchingCache):
  """
  This API client is for ingesting the logs in LogicMonitor.

  Args:
      batch (:obj:`bool`): Enable the batching support.
      interval (:obj:`int`): Batching flush interval. If batching is enabled then after that second we will flush the data to REST endpoint.
      response_callback (:class:`logicmonitor_data_sdk.api.response_interface.ResonseInterface`): Callback for response handling.
      api_client (:class:`logicmonitor_data_sdk.api_client.ApiClient`): The RAW HTTP REST client.

  Examples:
    >>> from logicmonitor_data_sdk.api.logs import Logs
    >>> from logicmonitor_data_sdk.configuration import Configuration
    >>> conf = Configuration(company="ACCOUNT_NAME", id='API_ACCESS_ID', key='API_ACCESS_KEY')
    >>> # Create the Logs client with batching support and flush interval as 30 sec.
    >>> logsAPi = Logs(batch=True, interval=30)
  """

  def __init__(self, batch=True, interval=30, response_callback=None,
      api_client=None):
    super(Logs, self).__init__(api_client=api_client, batch=batch,
                               interval=interval,
                               response_callback=response_callback,
                               request_cb=self._do_request,
                               merge_cb=self._merge_request)
    self._payload_cache = []

  def send_logs(self, **kwargs):  # noqa: E501
    """
    This send_logs method is used to sending the logs to rest endpoint.

    Args:
        resource (:class:`logicmonitor_data_sdk.models.resource.Resource`): The Resource object.
        msg (:obj:`str`): The log message. e.g. msg = "this is sample log msg".
        timestamp (:obj:`str` or :obj:`int`, Optional): The timestamp when the event occurred. Supported date formats are ISO8601 and Unix Epoch (in secs, ms, ns).
        metadata (:obj:`dict`,Optional): Metadata which can be used for defining logsource and other properties.

    Return:
        If in :class:`Logs` batching is enabled then None
        Otherwise the REST response will be return.

    Examples:
      >>> import time
      >>> from logicmonitor_data_sdk.api.logs import Logs
      >>> from logicmonitor_data_sdk.configuration import Configuration
      >>> from logicmonitor_data_sdk.models.resource import Resource
      >>>
      >>> conf = Configuration(company="ACCOUNT_NAME", id= 'API_ACCESS_ID', key= 'API_ACCESS_KEY')
      >>> # Create the Log client with batching enable
      >>> log_api = Logs() # By default batching is enabled with interval of 30 sec.
      >>> # Create the Resource object using the 'system.hostname' properties.
      >>> resource = Resource(ids={"system.hostname": "SampleDevice"}, name="SampleDevice", properties={'using.sdk': 'true'})
      >>> log_api.send_logs(resource=resource, msg = "this is a sample log")
    """

    """LogIngestApi  # noqa: E501

    LogIngestApi is used for the purpose of ingesting raw metrics to the LM application. It needs metrics in the format of RestMetricsV1 object. Payload is then validated with series of validation, successfully verified metrics will be ingested to Kafka. Only POST method is applied to this API  # noqa: E501
    This method makes a synchronous HTTP request by default. To make an
    asynchronous HTTP request, please pass async_req=True
    >>> thread = api.log_ingest_post(async_req=True)
    >>> result = thread.get()

    :param async_req bool
    :param bool create: Do you want to create resource? true/false
    :param RestMetricsV1 body:
    :return: PushMetricAPIResponse
             If the method is called asynchronously,
             returns the request thread.
    """

    all_params = ['resource', 'msg','timestamp', 'metadata']  # noqa: E501
    params = locals()
    for key, val in six.iteritems(params['kwargs']):
      if key not in all_params:
        raise TypeError(
            "Got an unexpected keyword argument '%s' to method send_logs()" % key
        )
      params[key] = val
    del params['kwargs']
    del params['self']
    del params['all_params']
    for one in all_params:
      if (one!='timestamp' and one!='metadata') and (not params.__contains__(one)):
        raise TypeError(
            "Some arguments are missing keys='%s'" %
            one
        )
    # logger.debug("Request Send for {}".format(str(params['resource'].ids)))
    if self.batch:
      # self.add_request(**kwargs)
      logs = {}
      logs['msg'] = kwargs['msg']
      if kwargs.__contains__('timestamp'):
        logs['timestamp'] = kwargs['timestamp']
      if kwargs.__contains__('metadata'):
        logs['metadata'] = kwargs['metadata']
      self.add_request(resource=copy.deepcopy(kwargs['resource']),
                       logs=logs)
    else:
      return self._single_request(**kwargs)

  def _do_request(self):
    try:
      self.Lock()
      if len(self._payload_cache) > 0:
        self._counter.update({BatchingCache._PAYLOAD_TOTAL:
                                len(self._payload_cache)})
        try:
          logger.debug("Sending request as '%s'", self._payload_cache)
          response = self.make_request(path='/log/ingest', method='POST',
                                       body=self._payload_cache)
          if isinstance(response, ApplyResult):
            response = response.get()
          self._response_handler(self._payload_cache, response[0], response[1],
                                 response[2])
        except ApiException as ex:
          # logger.exception("Got Exception " + str(ex), exc_info=ex)
          logger.exception("Got exception Status:%s body=%s reason:%s",
                           ex.status,
                           ex.body, ex.reason)
          self._response_handler(self._payload_cache, ex.body, ex.status,
                                 ex.headers,
                                 ex.reason)
          self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)

        self._payload_cache = []
        self._counter.update(BatchingCache._PAYLOAD_SEND)
      self._counter.update(BatchingCache._PAYLOAD_BUILD)
    except Exception as ex:
      logger.exception("Got Exception " + str(ex), exc_info=ex)
      self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)
    finally:
      self.UnLock()

  def _merge_request(self, single_request):
    resource = single_request['resource']
    logs = single_request['logs']
    logs['_lm.resourceId'] = resource.ids   
    self._payload_cache.append(logs)

  def _single_request(self, **kwargs):
    resource = kwargs['resource']
    logs = {}
    logs['msg']= kwargs['msg']
    logs['_lm.resourceId'] = resource.ids
    if kwargs.__contains__('timestamp'):
      logs['timestamp'] = kwargs['timestamp']
    if kwargs.__contains__('metadata'):
      logs['metadata'] = kwargs['metadata']
    body = []
    body.append(logs)
    return self.make_request(path='/log/ingest', method='POST',
                             body=body, async_req=False)
