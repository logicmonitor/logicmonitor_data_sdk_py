import logging
import sys

sys.path.append("..")
import logicmonitor_api_sdk
from logicmonitor_api_sdk.api.metrics import Metrics

logger = logging.getLogger('lmingest.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_api_sdk.Configuration(company='COMPANY',
                                                   authentication={
                                                     'id': 'ID',
                                                     'key': 'KEY'})

configuration.debug = False

metric_api = Metrics()

response = metric_api.update_resource_property(
    resource_ids={'system.deviceId': '233267'},
    resource_properties={'some.newproperty': 'values'},
    patch=False)
logger.info(response)

response = metric_api.update_instance_property(
    resource_ids={'system.deviceId': '233267'}, datasource='dsname_1',
    instancename='instance_1', instance_properties={
      'ins.property': 'values'},
)
logger.info(response)
