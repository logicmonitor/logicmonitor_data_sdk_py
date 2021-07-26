"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.
=======
"""

import logging
import os
import sys
import time

import psutil as psutil

sys.path.append("..")
import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.response_interface import ResonseInterface
from logicmonitor_data_sdk.models import Resource, DataSource, DataPoint, \
  DataSourceInstance

from logicmonitor_data_sdk.api.metrics import Metrics

logger = logging.getLogger('lmdata.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_data_sdk.Configuration()
# For debug log, set the value to True
configuration.debug = False


class MyResponse(ResonseInterface):
  """
  Sample callback to handle the response from the REST endpoints
  """

  def success_callback(self, request, response, status, request_id):
    logger.info("%s: %s: %s", response, status, request_id)

  def error_callback(self, request, response, status, request_id, reason):
    logger.error("%s: %s: %s %s", response, status, reason, request_id)


def MetricRequest():
  """
  Main function to get the CPU values using `psutil` and send to Metrics REST endpoint
  """
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


if __name__ == "__main__":
  MetricRequest()
