*****************************************
Python Data SDK library for LogicMonitor
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

The :mod:`logicmonitor_data_sdk` module provides
  - :mod:`logicmonitor_data_sdk.api.metrics`: a HTTP Api client for ingesting the metrics data.

Requirements.
*************

Python 2.7 and 3.4+

.. _RST Installation:

Installation
************

pip install
===========

Install from PyPI.

.. code:: sh

    pip install logicmonitor_data_sdk


Then import the package:

.. code:: python

    import logicmonitor_data_sdk


Getting Started
***************

Please follow the :ref:`RST Installation` and then run below a working example for submitting the disk
metrics to your LM account. This script will monitor the Usage, Free and Total of the disk at
every 5 sec interval.

.. literalinclude:: ../../example/disk_metrics.py
  :language: python

Then run the program as:

.. code:: python

    pip install psutil
    LM_COMPANY=<ACOUNT_NAME> LM_ACCESS_ID=<ID> LM_ACCESS_KEY='<KEY>' python disk_metrics.py


.. _RST Configuration:

Configuration
*************
SDK must be configured with logicmonitor_data_sdk.Configuration().
The account name, an API key and its id are required.

.. automodule:: logicmonitor_data_sdk.configuration
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
.. automodule:: logicmonitor_data_sdk.api.metrics
   :members:


Models
******

Resource
==========
.. automodule:: logicmonitor_data_sdk.models.resource
   :members:

DataSource
============
.. automodule:: logicmonitor_data_sdk.models.datasource
   :members:

DataSourceInstance
====================
.. automodule:: logicmonitor_data_sdk.models.datasource_instance
   :members:

DataPoint
============
.. automodule:: logicmonitor_data_sdk.models.datapoint
   :members:


ResonseInterface
==================
.. automodule:: logicmonitor_data_sdk.api.response_interface
    :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. |ss| raw:: html

   <strike>

.. |se| raw:: html

   </strike>


Get in Touch
============
If you have questions in general, reach out to our support@logicmonitor.com