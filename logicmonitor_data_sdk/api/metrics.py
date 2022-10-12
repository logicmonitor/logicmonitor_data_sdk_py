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
from logicmonitor_data_sdk.utils.object_name_validator import ObjectNameValidator
import gzip
import json

objectNameValidator = ObjectNameValidator()

logger = logging.getLogger('lmdata.api')
compressed_body_max_size = 104858
body_max_size = 1048576
max_number_instances = 100


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
    >>> metricsApi = Metrics(batch=True, interval=10)
  """

    def __init__(self, batch=True, interval=10, response_callback=None,
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
            if val is None:
                raise ValueError(
                    "Key '%s' should NOT be None" % key
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

        payload = {'resourceIds': resource_ids, 'resourceProperties': resource_properties}
        method = 'PATCH'
        if not patch:
            method = 'PUT'
        return self.make_request(path='/resource_property/ingest', method=method,
                                 body=payload, async_req=False)

    def update_instance_property(self, resource_ids, datasource, instance_name,
                                 instance_properties, patch=True):  # noqa: E501
        #
        # This update_resource_property method is used to update the property of the resource.

        # Args:
        #    resource_ids (dict): The Resource ids.
        #    datasource (str): The datasource name.
        #    instance_name (str): The instance name.
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
        if not instance_name:
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
        payload['instanceName'] = instance_name
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
            values=values,
            percentile=data_point.percentile)
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
                                     instances=instances,
                                     singleInstanceDS=datasource.singleInstanceDS)
        # size limiting
        if instances is not None and len(instances) > max_number_instances:
            return None
        serialized_rest_metrics = self.api_client.sanitize_for_serialization([rest_metrics])
        try:
            single_request_json = json.dumps(serialized_rest_metrics)
        except TypeError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise TypeError(msg)
        compressed_single_request = gzip.compress(single_request_json.encode("utf-8"))
        if compressed_single_request.__sizeof__() > compressed_body_max_size or serialized_rest_metrics.__sizeof__() > body_max_size:
            return None
        return self.make_request(path='/v2/metric/ingest', method='POST',
                                 body=[rest_metrics], create=host.create,
                                 async_req=False, api_type="metrics")

    def _do_request(self):
        rest_request = []
        try:
            self.Lock()
            logger.debug("Calling do request")
            self._counter.update(BatchingCache._PAYLOAD_BUILD)
            rest_request, create = self.rest_metrics_conversion()
            self.get_payload().clear()
        finally:
            self.UnLock()
            self._counter.update({BatchingCache._PAYLOAD_TOTAL: len(rest_request)})
        response = None
        try:
            logger.debug("Sending request as '%s'", rest_request)
            response = self.make_request(path='/v2/metric/ingest', method='POST',
                                         body=rest_request, create=create, api_type="metrics")
        except ApiException as ex:
            # logger.exception("Got Exception " + str(ex), exc_info=ex)
            logger.exception("Got exception Status:%s body=%s reason:%s", ex.status,
                             ex.body, ex.reason)
            self._response_handler(rest_request, ex.body, ex.status, ex.headers,
                                   ex.reason)
            self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)

        try:
            if isinstance(response, ApplyResult):
                response = response.get()
            else:
                response = response
            self._counter.update(BatchingCache._PAYLOAD_SEND)
            self._response_handler(rest_request, response[0], response[1],
                                   response[2])
        except ApiException as ex:
            # logger.exception("Got Exception " + str(ex), exc_info=ex)
            logger.exception("Got exception Status:%s body=%s reason:%s", ex.status,
                             ex.body, ex.reason)
            self._response_handler(rest_request, ex.body, ex.status, ex.headers,
                                   ex.reason)
        self._counter.update(BatchingCache._PAYLOAD_EXCEPTION)

    def _merge_request(self, single_request):
        # size limiting
        rest_request, _ = self.rest_metrics_conversion()
        serialized_payload_cache = self.api_client.sanitize_for_serialization(rest_request)
        serialized_single_request = self.api_client.sanitize_for_serialization(single_request)
        try:
            payload_cache_json = json.dumps(serialized_payload_cache)
            single_request_json = json.dumps(serialized_single_request)
        except TypeError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise TypeError(msg)
        compressed_payload_cache = gzip.compress(payload_cache_json.encode("utf-8"))
        compressed_single_request = gzip.compress(single_request_json.encode("utf-8"))
        if (
                compressed_payload_cache.__sizeof__() + compressed_single_request.__sizeof__() > compressed_body_max_size) or \
                (self._payload_cache.__sizeof__() + single_request.__sizeof__() > body_max_size):
            pass
        resource = single_request['resource']
        datasource = single_request['datasource']
        instance = single_request['instance']
        datapoint = single_request['datapoint']
        values = single_request['values']
        payload_host = self._payload_cache.get(resource)
        if payload_host is None:
            self._payload_cache[resource] = {}
            payload_host = self._payload_cache[resource]
        payload_ds = payload_host.get(datasource)
        if payload_ds is None:
            payload_host[datasource] = {}
            payload_ds = payload_host[datasource]
        payload_instance = payload_ds.get(instance)
        if payload_instance is not None and len(payload_instance) > max_number_instances:
            pass
        if payload_instance is None:
            payload_ds[instance] = {}
            payload_instance = payload_ds[instance]
        payload_datapoint = payload_instance.get(datapoint)
        if payload_datapoint is None:
            payload_instance[datapoint] = {}
            payload_datapoint = payload_instance[datapoint]
        payload_datapoint.update(values)

    def _valid_field(self, instance):
        instance_id = instance.instance_id

        err_msg = ""
        # instance_name Validations
        if instance_id is None or instance_id == 0:
            err_msg += objectNameValidator.check_instance_name_validation(instance.name)

            # instance_displayname Validations
            err_msg += objectNameValidator.check_instance_displayname_validation(
                instance.display_name)

            # instance_properties Validation
            err_msg += objectNameValidator.check_instance_properties_validation(
                instance.properties)
        elif instance_id != 0:
            if instance_id is not None and instance_id < 0:
                err_msg += "Instance ID {%s} should not be negative." % instance_id

            err_msg += objectNameValidator.check_instance_name_validation(instance.name)

            # instance_displayname Validations
            err_msg += objectNameValidator.check_instance_displayname_validation(
                instance.display_name)

            # instance_properties Validation
            err_msg += objectNameValidator.check_instance_properties_validation(
                instance.properties)

        return err_msg

    def rest_metrics_conversion(self):
        rest_request = []
        create = None
        for host, dsvalues in self._payload_cache.items():
            for datasource, instanceValues in dsvalues.items():
                datapoints_added = False
                instances = []
                for instance, datapointsValues in instanceValues.items():
                    data_points = []
                    if not datasource.singleInstanceDS:
                        error_msg = self._valid_field(instance)
                        if error_msg is not None and len(error_msg) > 0:
                            raise ValueError(error_msg)
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
                            values=values,
                            percentile=data_point.percentile)
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
                                                 instances=instances,
                                                 singleInstanceDS=datasource.singleInstanceDS)
                    create = host.create
            rest_request.append(rest_metrics)
        return rest_request, create
