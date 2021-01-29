import logging
import os
import sys
import time

import psutil as psutil

sys.path.append("..")
from logicmonitor_api_sdk.api.response_interface import ResonseInterface
from logicmonitor_api_sdk.models import Resource, DataSource, DataPoint, \
  DataSourceInstance

import logicmonitor_api_sdk
from logicmonitor_api_sdk.api.metrics import Metrics

logger = logging.getLogger('lmingest.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_api_sdk.Configuration(company='COMPANY_NAME',
                                                   authentication={
                                                     'id': 'ID',
                                                     'key': 'KEY'})

configuration.debug = False


class MyResponse(ResonseInterface):

  def success_callback(self, request, response, status, request_id):
    logger.info("%s: %s: %s", response, status, request_id)

  def error_callback(self, request, response, status, request_id, reason):
    logger.error("%s: %s: %s %s", response, status, reason, request_id)


def MetricRequest():
  device_name = os.uname()[1]
  resource = Resource(ids={'system.displayname': device_name}, name=device_name,
                      create=True)
  datasource = DataSource(name="CPU")
  instance = DataSourceInstance(name='cpu-1')
  datapoint = DataPoint(name="cpu_utilization")
  metric_api = Metrics(batch=True, interval=10, response_callback=MyResponse())
  while True:
    values = {str(int(time.time())): str(psutil.cpu_percent())}

    metric_api.send_metrics(resource=resource,
                            datasource=datasource,
                            instance=instance,
                            datapoint=datapoint,
                            values=values)
    time.sleep(10)


MetricRequest()
