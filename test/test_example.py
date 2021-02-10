from __future__ import print_function

import sys

sys.path.append("..")

import time
import random
import logicmonitor_data_sdk

from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.models.datapoint import DataPoint
from logicmonitor_data_sdk.models.datasource import DataSource
from logicmonitor_data_sdk.models.datasource_instance import DataSourceInstance
from logicmonitor_data_sdk.models.resource import Resource

# Configure API key authorization: LMv1
configuration = logicmonitor_data_sdk.Configuration(company='COMPANY',
                                                    authentication={
                                                     'id': 'ID',
                                                     'key': 'KEY'})
configuration.debug = True
# create an instance of the API class
metric_api = Metrics(interval=20, batch=True)
resource = Resource(ids={"system.hostname": "SampleDevice"}, create=True,
                    name="SampleDevice", properties={'using.sdk': 'true'})
ds = DataSource(name="DSName")
instance = DataSourceInstance(name="instance")
dp = DataPoint(name="dataPoint")

while True:
  values = {str(int(time.time())): random.randint(10, 100)}
  metric_api.send_metrics(resource=resource,
                          datasource=ds,
                          instance=instance,
                          datapoint=dp,
                          values=values)
  time.sleep(10)
