# The LogicMonitor Python Ingestion library
This Python Library is suitable for ingesting the metrics into the LogicMonitor Platform

[![Build](https://circleci.com/gh/mukundneharkar/lmsdk.svg?style=svg)](https://circleci.com/gh/mukundneharkar/lmsdk.svg?style=svg)
[![Documentation Status](https://readthedocs.org/projects/logicmonitor-api-sdk-py/badge/?version=latest)](https://logicmonitor-api-sdk-py.readthedocs.io/en/latest/?badge=latest)
[![PyPI - Version](https://img.shields.io/pypi/v/logicmonitor-api-sdk-py.svg)](https://pypi.org/project/logicmonitor-api-sdk-py)
[![PyPI - Downloads](https://pepy.tech/badge/logicmonitor-api-sdk-py)](https://pepy.tech/project/logicmonitor-api-sdk-py)


- Library Documentation: https://logicmonitor-api-sdk-py.readthedocs.io/en/latest/
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

Getting Started
---------------

Please install using pip and then run below a working example for submitting the metrics to your account:

```python

    from __future__ import print_function
    import time
    import random
    import logicmonitor_api_sdk

    from logicmonitor_api_sdk.api.metrics import Metrics
    from logicmonitor_api_sdk.models.resource import Resource
    from logicmonitor_api_sdk.models.datasource import DataSource
    from logicmonitor_api_sdk.models.datasource_instance import DataSourceInstance
    from logicmonitor_api_sdk.models.datapoint import DataPoint

    # Configure API key authorization: LMv1
    configuration = logicmonitor_api_sdk.Configuration(company = 'YOUR_COMPANY', authentication={ 'id': 'YOUR_ACCESS_ID', 'key' : 'YOUR_ACCESS_KEY'})

    # create an instance of the API class
    metric_api = Metrics(interval=20, batch = True)
    resource = Resource(ids={"system.hostname": "SampleDevice"}, create=True, name="SampleDevice", properties={'using.sdk': 'true'})
    ds = DataSource(name="DSName")
    instance = DataSourceInstance(name="instance")
    dp = DataPoint(name="dataPoint")

    while True:
      # Generate the random data for current epoch.
      values = {str(int(time.time())): random.randint(10, 100)}
      metric_api.send_metrics(resource=resource,
                          datasource=ds,
                          instance=instance,
                          datapoint=dp,
                          values=values)
      time.sleep(10)
```


