# coding: utf-8

from setuptools import setup  # noqa: H301

NAME = "logicmonitor_api_sdk"
VERSION = "0.0.1b1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="LogicMonitor API-Ingest Rest API",
    author="LogicMonitor",
    author_email="support@logicmonitor.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/logicmonitor/logicmonitor_api_sdk_py",
    classifiers=[
      'Development Status :: 4 - Beta',
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.4',
    ],
    python_requires='>=3.4,>=2.7',
    project_urls={
      'Documentation': 'https://logicmonitor-api-sdk-py.readthedocs.io/en/latest/',
      # 'Source': 'https://github.com/logicmonitor/logicmonitor_api_sdk_py',
      'Tracker': 'https://github.com/logicmonitor/logicmonitor_api_sdk_py/issues',
    },

)
