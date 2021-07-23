"""
=======
Copyright, 2021, LogicMonitor, Inc.
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
=======
"""

# Sample Program to send Logs to LogicMonitor Platform
#
import os
import logicmonitor_data_sdk

from logicmonitor_data_sdk.api.logs import Logs
from logicmonitor_data_sdk.models import Resource

# Initialize LM SDK and provide required authentication parameters
# On LM Portal, create 'API Token' for the user to get access Id and access Key
configuration = logicmonitor_data_sdk.Configuration( company='your_company',
                                                          id='API access id',
                                                         key='API access key')

# The resource which is already present on LM Platform. Use a unique property to match
# the resource and send log for that.                                                    
resource = Resource(ids={"system.hostname": 'your_system'})

#Create an api handle for sending the logs 
# "batch" would club logs for 8MB size or 30 Sec - whichever is earlier. Its default is "True".
log_api = Logs(batch = False)

return_value = log_api.send_logs(resource=resource, msg= "this is sample log")

print(return_value)
