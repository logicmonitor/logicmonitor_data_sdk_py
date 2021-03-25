import time
from random import seed, random

import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.models import DataSource, \
  Resource, DataSourceInstance, DataPoint

# Configure API key authorization: LMv1
configuration = logicmonitor_data_sdk.Configuration(company='COMPANY',
                                                    id='ACCESS_ID',
                                                    key='ACCESS_KEY')
# create an instance of the API class
metric_api = Metrics(batch=True)
seed(1)
while True:
  metric_api.send_metrics(resource=Resource(
      ids={"system.hostname": "SampleDevice"}, create=True, name="SampleDevice",
      properties={"using.sdk": "true"}), datasource=DataSource(
      name="PusMetricsDS"), instance=DataSourceInstance(name="instance"),
      datapoint=DataPoint(name="dataPoint"),
      values={str(int(time.time())): str(random())})
  time.sleep(10)
