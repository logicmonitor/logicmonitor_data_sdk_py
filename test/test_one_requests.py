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
import random
import sys
import time

sys.path.append("..")

import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.models.datapoint import DataPoint
from logicmonitor_data_sdk.models.datasource import DataSource
from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
from logicmonitor_data_sdk.models.resource import Resource

max_host = 1
max_ds = 1
max_inst = 2
max_dp = 5
max_values = 5

logger = logging.getLogger('lmdata.api')
logger.setLevel(logging.INFO)


def random_string(max):
  return "_" + str(random.randint(1, max))


def random_object(type):
  if type == 'resource':
    name = "LMDevice" + random_string(max_host)
    return Resource(ids={"system.hostname": name},
                    create=True, name=name, properties={'using.sdk': 'true'})
  if type == 'datasource':
    return DataSource(name="DS" + random_string(max_ds))
  if type == 'instance':
    return DataSourceInstance(name="instance" + random_string(max_inst))
  if type == 'datapoint':
    return DataPoint(name="dp1" + random_string(max_dp))
  if type == 'values':
    values = {}
    t = int(time.time())
    for i in range(random.randint(1, max_values)):
      values[t] = random.randint(0, 100)
      t = t - 1
    return values


configuration = logicmonitor_data_sdk.Configuration(company='COMPANY',
                                                    authentication={
                                                      'id': 'ID',
                                                      'key': 'KEY'})

configuration.debug = False


# configuration.logger_file = None


def MetricRequest():
  metric_api = Metrics()
  resource = random_object("resource")
  datasource = random_object("datasource")
  instance = random_object("instance")
  datapoint = random_object("datapoint")
  response = metric_api.send_metrics(resource=resource,
                                     datasource=datasource,
                                     instance=instance,
                                     datapoint=datapoint,
                                     values=random_object("values"))

  print(response)


MetricRequest()
# LogRequest()
