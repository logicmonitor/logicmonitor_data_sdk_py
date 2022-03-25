# The LogicMonitor Python Data library
This Python Library is suitable for ingesting the metrics into the LogicMonitor Platform

[![Documentation Status](https://readthedocs.org/projects/logicmonitor-data-sdk-py/badge/?version=latest)](https://logicmonitor-data-sdk-py.readthedocs.io/en/latest/?badge=latest)
[![PyPI - Version](https://img.shields.io/pypi/v/logicmonitor-data-sdk.svg)](https://pypi.org/project/logicmonitor-data-sdk)
[![PyPI - Downloads](https://pepy.tech/badge/logicmonitor-data-sdk)](https://pepy.tech/project/logicmonitor-data-sdk)


- Library Documentation: https://logicmonitor-data-sdk-py.readthedocs.io/en/latest/
- LogicMonitor: https://LogicMonitor.com

Overview
--------

LogicMonitor's Push Metrics feature allows you to send metrics directly
to the LogicMonitor platform via a dedicated API, removing the need to
route the data through a LogicMonitor Collector. Once ingested, these
metrics are presented alongside all other metrics gathered via
LogicMonitor, providing a single pane of glass for metric monitoring and
alerting.

Requirements.
------------

Python 2.7 and 3.4+

Documentation
-------------
https://logicmonitor-data-sdk-py.readthedocs.io/en/latest/


Getting Started
---------------

Please install using pip and then run below a working example for submitting the disk metrics to 
your LM account. This script will monitor the Usage, Free and Total of the disk at every 10 sec 
interval.

```python
    import logging
    import os
    import sys
    import time
    
    import psutil as psutil
    
    import logicmonitor_data_sdk
    from logicmonitor_data_sdk.api.response_interface import ResonseInterface
    from logicmonitor_data_sdk.models import Resource, DataSource, DataPoint, \
      DataSourceInstance
    
    from logicmonitor_data_sdk.api.metrics import Metrics
    
    logger = logging.getLogger('lmdata.api')
    logger.setLevel(logging.INFO)
    
    configuration = logicmonitor_data_sdk.Configuration()
    # For debug log, set the value to True
    configuration.debug = True
    
    
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
      datasource = DataSource(name="DiskUsingSDK")
      datapoints = ['total', 'used', 'free']
      metric_api = Metrics(batch=True, interval=30, response_callback=MyResponse())
      while True:
        partitions = psutil.disk_partitions()
        for p in partitions:
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

```

Then run the program as:

```python

    pip install psutil
    LM_COMPANY=<ACOUNT_NAME> LM_ACCESS_ID=<ID> LM_ACCESS_KEY='<KEY>' python disk_metrics.py
```


Get in Touch
------------
If you have questions in general, reach out to our [support](mailto:support@logicmonitor.com)


------------
Copyright, 2021, LogicMonitor, Inc.

This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.


