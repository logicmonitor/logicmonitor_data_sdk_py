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

# Metrics API client: It formats and submit REST API calls to LogicMonitor.

from __future__ import absolute_import

import copy
import logging
import re  # noqa: F401
from multiprocessing.pool import ApplyResult

import six

from logicmonitor_data_sdk import RestMetricsV1, RestDataSourceInstanceV1, \
  RestDataPointV1
from logicmonitor_data_sdk.internal.internal_cache import BatchingCache
# python 2 and python 3 compatibility library
from logicmonitor_data_sdk.rest import ApiException

logger = logging.getLogger('lmdata.api')


class Metrics(BatchingCache):
  """
  This API client is for ingesting the metrics in LogicMonitor.

  Args:
      batch (:obj:`bool`): Enable the batching support.
      interval (:obj:`int`): Batching flush interval. If batching is enabled then after that second we will flush the data to REST endpoint.
      response_callback (:class:`logicmonitor_data_sdk.api.response_interface.ResonseInterface`): Callback for response handling.
      api_client (:class:`logicmonitor_data_sdk.api_client.ApiClient`): The RAW HTTP REST client.

  Examples:
    >>> from logicmonitor_data_sdk.api.metrics import Metrics
    >>> from logicmonitor_data_sdk.configuration import Configuration
    >>> conf = Configuration(company="ACCOUNT_NAME", id='API_ACCESS_ID', key='API_ACCESS_KEY')
    >>> # Create the Metrics client with batching support and flush interval as 30 sec.
    >>> metricsApi = Metrics(batch=True, interval=30)
  """

  def __init__(self, batch=True, interval=30, response_callback=None,
      api_client=None):
    super(Metrics, self).__init__(api_client=api_client, batch=batch,
                                  interval=interval,
                                  response_callback=response_callback,
                                  request_cb=self._do_request,
                                  merge_cb=self._merge_request)

  def send_metrics(self, **kwargs):  # noqa: E501
    """
    This send_metrics method is used to send the metrics to rest endpoint.

    Args:
        resource (:class:`logicmonitor_data_sdk.models.resource.Resource`): The Resource object.
        datasource (:class:`logicmonitor_data_sdk.models.datasource.DataSource`): The datasource object.
        instance (:class:`logicmonitor_data_sdk.models.datasource_instance.DataSourceInstance`): The instance object.
        datapoint (:class:`logicmonitor_data_sdk.models.datapoint.DataPoint`): The datapoint object.
        values (:obj:`dict`): The values dictionary.

    Return:
        If in :class:`Metrics` batching is enabled then None
        Otherwise the REST response will be return.

    Examples:
      >>> import time
      >>> from logicmonitor_data_sdk.api.metrics import Metrics
      >>> from logicmonitor_data_sdk.configuration import Configuration
      >>> from logicmonitor_data_sdk.models.resource import Resource
      >>> from logicmonitor_data_sdk.models.datasource import DataSource
      >>> from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
      >>> from logicmonitor_data_sdk.models.datapoint import DataPoint
      >>>
      >>> conf = Configuration(company="ACCOUNT_NAME", id='API_ACCESS_ID', key='API_ACCESS_KEY')
      >>> # Create the Metrics client with batching disabled
      >>> metric_api = Metrics(batch=False)
      >>> # Create the Resource object using the 'system.deviceId' properties.
      >>> resource = Resource(ids={"system.hostname": "SampleDevice"}, create=True, name="SampleDevice", properties={'using.sdk': 'true'})
      >>> # Create the LMDataSource object for CPU monitoring
      >>> ds = DataSource(name="CPU")
      >>> # Create the DataSourceInstance object for CPU-0 instance monitoring
      >>> instance = DataSourceInstance(name="CPU-0")
      >>> # Create the DataPoint object for cpu-time
      >>> dp = DataPoint(name='cpu_time', aggregation_type='sum')
      >>> metric_api.send_metrics(resource=resource, datasource=ds, instance=instance, \
datapoint=dp, values={ time.time() : '23'})
    """
    all_params = ['resource', 'datasource', 'instance', 'datapoint',
                  'values']  # noqa: E501
    params = locals()
    for key, val in six.iteritems(params['kwargs']):
      if key not in all_params:
        raise TypeError(
            "Got an unexpected keyword argument '%s' to method SendMetrics" % key
        )
      params[key] = val
    del params['kwargs']
    del params['self']
    del params['all_params']
    for one in all_params:
      if not params.__contains__(one):
        raise TypeError(
            "Some arguments are missing keys='%s'" %
            str(params.keys())
        )
    # logger.debug("Request Send for {}".format(str(params['resource'].ids)))
    if self.batch:
      # self.add_request(**kwargs)
      self.add_request(resource=copy.deepcopy(kwargs['resource']),
                       datasource=copy.deepcopy(kwargs['datasource']),
                       instance=copy.deepcopy(kwargs['instance']),
                       datapoint=copy.deepcopy(kwargs['datapoint']),
                       values=kwargs['values'])
    else:
      return self._single_request(**kwargs)

  def update_resource_property(self, resource_ids, resource_properties,
      patch=True):  # noqa: E501
    #
    # This update_resource_property method is used to update the property of the resource.

    # Args:
    #    resource_ids (dict): The Resource ids.
    #    resource_properties (dict): The properties which you want to add/update.
    #    patch (bool): PATCH or PUT request.

    # Return:
    #    REST response will be return.
    #
    if not resource_ids or not isinstance(resource_ids, dict):
      raise ValueError(
          'resourceId must provide and it should be type `dict`'
      )
    if not resource_properties or not isinstance(resource_properties, dict):
      raise ValueError(
          'resourceProperties must provide and it should be type `dict`'
      )
    for key in resource_properties:
      if key.startswith('system.') or key.startswith('auto.'):
        raise ValueError(
            'Properties can not have system or auto properties'
        )

    payload = {}
    payload['resourceIds'] = resource_ids
    payload['resourceProperties'] = resource_properties
    method = 'PATCH'
    if not patch:
      method = 'PUT'
    return self.make_request(path='/resource_property/ingest', method=method,
                             body=payload, async_req=False)

  def update_instance_property(self, resource_ids, datasource, instancename,
      instance_properties, patch=True):  # noqa: E501
    #
    # This update_resource_property method is used to update the property of the resource.

    # Args:
    #    resource_ids (dict): The Resource ids.
    #    datasource (str): The datasource name.
    #    instancename (str): The instance name.
    #    instance_properties (dict): The properties which you want to add/update.
    #    patch (bool): PATCH or PUT request.

    # Return:
    #    REST response will be return.

    if not resource_ids or not isinstance(resource_ids, dict):
      raise ValueError(
          'resourceId must provide and it should be type `dict`'
      )
    if not datasource:
      raise ValueError(
          'dataSource must provide'
      )
    if not instancename:
      raise ValueError(
          'instanceName must provide'
      )
    if not instance_properties or not isinstance(instance_properties, dict):
      raise ValueError(
          'instanceProperties must provide and it should be type `dict`'
      )
    for key in instance_properties:
      if key.startswith('system.') or key.startswith('auto.'):
        raise ValueError(
            'Properties can not have system or auto properties'
        )
    payload = {}
    payload['resourceIds'] = resource_ids
    payload['dataSource'] = datasource
    payload['instanceName'] = instancename
    payload['instanceProperties'] = instance_properties
    method = 'PATCH'
    if not patch:
      method = 'PUT'
    return self.make_request(path='/instance_property/ingest', method=method,
                             body=payload, async_req=False)

  def _single_request(self, **kwargs):
    host = kwargs['resource']
    datasource = kwargs['datasource']
    instance = kwargs['instance']
    data_point = kwargs['datapoint']
    values = kwargs['values']
    data_points = []
    rest_data_point = RestDataPointV1(
        data_point_aggregation_type=data_point.aggregation_type,
        data_point_description=data_point.description,
        data_point_name=data_point.name,
        data_point_type=data_point.type,
        values=values)
    data_points.append(rest_data_point)
    rest_instance = RestDataSourceInstanceV1(
        instance_name=instance.name,
        instance_display_name=instance.display_name,
        instance_properties=instance.properties,
        instance_description=instance.description,
        data_points=data_points)
    instances = [rest_instance]
    rest_metrics = RestMetricsV1(resource_ids=host.ids,
                                 resource_name=host.name,
                                 resource_properties=host.properties,
                                 resource_description=host.description,
                                 data_source=datasource.name,
                                 data_source_display_name=datasource.display_name,
                                 data_source_group=datasource.group,
                                 data_source_id=datasource.id,
                                 instances=instances)
    return self.make_request(path='/metric/ingest', method='POST',
                             body=rest_metrics, create=host.create,
                             async_req=False)

  def _do_request(self):
    rest_request = []
    try:
      self.Lock()
      logger.debug("Calling do request")
      self._counter.update(BatchingCache._PAYLOAD_BUILD)
      for host, dsvalues in self._payload_cache.items():
        for datasource, instanceValues in dsvalues.items():
          datapoints_added = False
          instances = []
          for instance, datapointsValues in instanceValues.items():
            data_points = []
            rest_instance = RestDataSourceInstanceV1(
                instance_name=instance.name,
                instance_display_name=instance.display_name,
                instance_properties=instance.properties,
                instance_description=instance.description,
                data_points=data_points)
            instances.append(rest_instance)
            for data_point, v in datapointsValues.items():
              values = {}
              for key, value in v.items():
                values[str(key)] = str(value)
                datapoints_added = True

              rest_data_point = RestDataPointV1(
                  data_point_aggregation_type=data_point.aggregation_type,
                  data_point_description=data_point.description,
                  data_point_name=data_point.name,
                  data_point_type=data_point.type,
                  values=values)
              data_points.append(rest_data_point)
          if datapoints_added:
            rest_metrics = RestMetricsV1(resource_ids=host.ids,
                                         resource_name=host.name,
                                         resource_properties=host.properties,
                                         resource_description=host.description,
                                         data_source=datasource.name,
                                         data_source_display_name=datasource.display_name,
                                         data_source_group=datasource.group,
                                         data_source_id=datasource.id,
                                         instances=instances)
            # pprint.pprint(rest_metrics)
            rest_request.append((rest_metrics, host.create))
      # pprint.pprint(self._payload_cache)
      self.get_payload().clear()
    finally:
      self.UnLock()
      self._counter.update({BatchingCache._PAYLOAD_TOTAL:
                              len(rest_request)})
    response_list = []
    for request in rest_request:
      rest_metrics = request[0]
      create = request[1]
      try:
        logger.debug("Sending request as '%s'", rest_metrics)
        response = self.make_request(path='/metric/ingest', method='POST',
                                     body=rest_metrics, create=create)
        response_list.append(response)
      except ApiException as ex:
        # logger.exception("Got Exception " + str(ex), exc_info=ex)
        logger.exception("Got exception Status:%s body=%s reason:%s", ex.status,
                         ex.body, ex.reason)
        self._response_handler(rest_metrics, ex.body, ex.status, ex.headers,
                               ex.reason)
        self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)

    for one_result in response_list:
      try:
        if isinstance(one_result, ApplyResult):
          response = one_result.get()
        else:
          response = one_result
        self._counter.update(BatchingCache._PAYLOAD_SEND)
        self._response_handler(rest_metrics, response[0], response[1],
                               response[2])
      except ApiException as ex:
        # logger.exception("Got Exception " + str(ex), exc_info=ex)
        logger.exception("Got exception Status:%s body=%s reason:%s", ex.status,
                         ex.body, ex.reason)
        self._response_handler(rest_metrics, ex.body, ex.status, ex.headers,
                               ex.reason)
      self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)

  def _merge_request(self, single_request):
    resource = single_request['resource']
    datasource = single_request['datasource']
    instance = single_request['instance']
    datapoint = single_request['datapoint']
    values = single_request['values']
    payload_host = self._payload_cache.get(resource)
    if payload_host == None:
      self._payload_cache[resource] = {}
      payload_host = self._payload_cache[resource]
    payload_ds = payload_host.get(datasource)
    if payload_ds == None:
      payload_host[datasource] = {}
      payload_ds = payload_host[datasource]
    payload_instance = payload_ds.get(instance)
    if payload_instance == None:
      payload_ds[instance] = {}
      payload_instance = payload_ds[instance]
    payload_datapoint = payload_instance.get(datapoint)
    if payload_datapoint == None:
      payload_instance[datapoint] = {}
      payload_datapoint = payload_instance[datapoint]
    payload_datapoint.update(values)
