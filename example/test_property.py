"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
=======
"""

import logging
import sys

sys.path.append("..")
import logicmonitor_data_sdk
from logicmonitor_data_sdk.api.metrics import Metrics

logger = logging.getLogger('lmdata.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_data_sdk.Configuration(company='COMPANY',
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
