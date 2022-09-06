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
import time

import psutil as psutil

import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.metrics import Metrics
from logicmonitor_data_sdk.api.response_interface import ResponseInterface
from logicmonitor_data_sdk.models import Resource, DataSource, DataPoint, \
    DataSourceInstance

logger = logging.getLogger('lmdata.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_data_sdk.Configuration()
# For debug log, set the value to True
configuration.debug = False


class MyResponse(ResponseInterface):
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
    datasource = DataSource(name="DiskUsingSDK")
    datapoints = ['total', 'used', 'free']
    metric_api = Metrics(batch=True, interval=30, response_callback=MyResponse())
    while True:
        partitions = psutil.disk_partitions()
        for p in partitions:
            # Using the device as instance name. We can use the mountpoint as well.

            instance_name = p.device
            usage = psutil.disk_usage(instance_name)._asdict()

            # Create the instance object for every device. Name should not have the
            # special characters so replacing it with the '-'.
            instance = DataSourceInstance(name=instance_name.replace('/', '-'),
                                          display_name=instance_name)
            for one_datapoint in datapoints:
                datapoint = DataPoint(name=one_datapoint)
                values = {str(int(time.time())): str(usage[one_datapoint])}
                metric_api.send_metrics(resource=resource,
                                        datasource=datasource,
                                        instance=instance,
                                        datapoint=datapoint,
                                        values=values)
        time.sleep(5)


if __name__ == "__main__":
    MetricRequest()
