"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.
=======
"""

import time
from random import seed, random

import logicmonitor_data_sdk

# LogicMonitor metric data model is as below
#
#Company
#  |--- Resource (like device/service. Ex: VM)
#  |--- Data Source   (Ex. CPU)
#         |--- Instance (of a Data Source on a resource. Ex. CPU-1)
#               |--- Data Point (the metric which is being monitored. Ex. %Used)
#                     |- <Time> : <Metric Value>
#                     |- <Time> : <Metric Value>
#                     |...
#
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.api.response_interface import ResonseInterface
from logicmonitor_data_sdk.api_client import ApiClient
from logicmonitor_data_sdk.models import DataSource, \
  Resource, DataSourceInstance, DataPoint
from example import system_properties

# Configure SDK with Account and access information
# On your LogicMonitor portal, create API token (LMv1) for user and get
# Access Id and Access Key
configuration = logicmonitor_data_sdk.Configuration(company='your_company',
                                                    id='API_ACCESS_ID',
                                                    key='API_ACCESS_KEY')
class MyResponse(ResonseInterface):
    """
    Sample callback to handle the response from the REST endpoints
    """

    def success_callback(self, request, response, status, request_id):
        #logging.info("%s: %s: %s", response, status, request_id)
        print(response, status, request_id)


    def error_callback(self, request, response, status, request_id, reason):
        #logging.error("%s: %s: %s %s", response, status, reason, request_id)
        print(response, status, reason, request_id)


# Create api handle for Metrics use case (we also support Logs)
api_client = ApiClient(configuration=configuration)
metric_api = Metrics(batch=False,interval=10,response_callback=MyResponse(),api_client=api_client)
return_val = metric_api.send_metrics(
               resource=Resource(
                   ids={"system.hostname": "SampleDevice"},  #Core Properties of the Resource
                   create=True,                              #Auto-create resource if does not exist
                   name="SampleDevice",                      #Name of the resource
                   properties=system_properties.get_system_info()),        #Additional Properties [Optional]
               datasource=DataSource(
                   name="SampleDS"),                         #Name of data source is must. Rest optional
               instance=DataSourceInstance(
                   name="SampleInstance"),                   #Name of instance is must. Rest optional
               datapoint=DataPoint(
                  name="SampleDataPoint"),                  #The metric
               values={str(int(time.time())): str(random())} #Values at specific time(s)
)
print("Return Value = ",return_val)