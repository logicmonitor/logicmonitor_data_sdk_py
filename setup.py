# coding: utf-8


from setuptools import setup, find_packages  # noqa: H301

NAME = "logicmoniter_api_sdk"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="LogicMonitor Rest API SDK",
    author_email="",
    url="",
    keywords=["LogicMonitor Rest API SDK"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This Python Library is suitable for ingesting the metrics, logs into the LogicMonitor Platform
    """
)
