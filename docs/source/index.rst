*****************************************
Python Ingestion library for LogicMonitor
*****************************************

This Python Library for ingesting the metrics into the LogicMonitor Platform

PushMetrics - Metrics Ingestion
###############################


Overview
*********

LogicMonitor's Push Metrics feature allows you to send metrics directly
to the LogicMonitor platform via a dedicated API, removing the need to
route the data through a LogicMonitor Collector. Once ingested, these
metrics are presented alongside all other metrics gathered via
LogicMonitor, providing a single pane of glass for metric monitoring and
alerting.

More details are available on `support
site <https://www.logicmonitor.com/support>`__

Version
*******

-  API version: 0.0.1
-  Package version: 0.0.1.beta

Requirements.
*************

Python 2.7 and 3.4+

.. _RST Installation:

Installation
************

pip install
===========

If the python package ishosted on Github, you can install directly from
Github

.. code:: sh

    pip install logicmonitor_api_sdk_py

| (you may need to run ``pip`` with root permission:

``sudo pip install logicmonitor_api_sdk_py``)

Then import the package:

.. code:: python

    import logicmonitor_api_sdk


Getting Started
***************

Please follow the :ref:`RST Installation` and then run below a working example for submitting the metrics to your account:

.. code:: python

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
      values = {str(int(time.time())): random.randint(10, 100)}
      metric_api.send_metrics(resource=resource,
                          datasource=ds,
                          instance=instance,
                          datapoint=dp,
                          values=values)
      time.sleep(10)


.. _RST Configuration:

Configuration
*************
SDK must be configured with logicmonitor_api_sdk.Configuration().
The account name, an API key and its id are required.

.. automodule:: logicmonitor_api_sdk.configuration
   :members:

API Calls
*********

All URIs are relative to *https://<account_name>.logicmonitor.com/rest*

Usage
=====
Be sure to initialize the client using :ref:`RST Configuration` and then use :ref:`RST MetricsAPI`.

.. _RST MetricsAPI:

Metrics Ingestion API
=====================
.. automodule:: logicmonitor_api_sdk.api.metrics
   :members:


Models
******

Resource
==========
.. automodule:: logicmonitor_api_sdk.models.resource
   :members:

DataSource
============
.. automodule:: logicmonitor_api_sdk.models.datasource
   :members:

DataSourceInstance
====================
.. automodule:: logicmonitor_api_sdk.models.datasource_instance
   :members:

DataPoint
============
.. automodule:: logicmonitor_api_sdk.models.datapoint
   :members:


ResonseInterface
==================
.. automodule:: logicmonitor_api_sdk.api.response_interface
    :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. |ss| raw:: html

   <strike>

.. |se| raw:: html

   </strike>
