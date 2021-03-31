
import logging
import os
import time

import psutil as psutil

import logicmonitor_data_sdk

from logicmonitor_data_sdk.api.logs import Logs
from logicmonitor_data_sdk.models import Resource

logger = logging.getLogger('lmdata.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_data_sdk.Configuration(company='yourcompany',
                                                    id='accessID',
                                                    key='accessKey')
                                                    

resource = Resource(ids={"System.ips": "192.168.1.33"})
log_api = Logs(batch = False)
log_api.send_logs(resource = resource,msg= "this is smaple log")

		




