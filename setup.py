"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the 
Mozilla Public License, v. 2.0. If a copy of the MPL 
was not distributed with this file, You can obtain 
one at https://mozilla.org/MPL/2.0/.
=======
"""

# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

NAME = "logicmonitor_data_sdk"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

version = {}
with open("logicmonitor_data_sdk/version.py") as fp:
  exec(fp.read(), version)

setup(
    name=NAME,
    version=version["__version__"],
    description="LogicMonitor Rest API",
    author="LogicMonitor",
    author_email="support@logicmonitor.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/logicmonitor/logicmonitor_data_sdk_py",
    classifiers=[
      'Development Status :: 4 - Beta',
      "Operating System :: OS Independent",
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.4',
    ],
    python_requires='>=3.4,>=2.7',
    project_urls={
      'Documentation': 'https://logicmonitor-data-sdk-py.readthedocs.io/en/latest/',
      # 'Source': 'https://github.com/logicmonitor/logicmonitor_data_sdk_py',
      'Tracker': 'https://github.com/logicmonitor/logicmonitor_data_sdk_py/issues',
    },
    packages=find_packages(),
    install_requires=REQUIRES,

)
