#!/usr/bin/env python3
from cortexutils.responder import Responder
import requests
import os.path
from os import path

class Wazuh(Responder):
   def __init__(self):
       Responder.__init__(self)
       self.wazuh_manager = self.get_param('config.wazuh_manager', None, 'https://localhost:55000')
       self.wazuh_user = self.get_param('config.wazuh_user', None, 'Username missing!')
       self.wazuh_password = self.get_param('config.wazuh_password', None, 'Password missing!')
       self.wazuh_agent_id = self.get_param('data.case.customFields.wazuh_agent_id.string', None, "Agent ID Missing!")
       self.wazuh_alert_id = self.get_param('data.case.customFields.wazuh_alert_id.string', None, " Missing!")
       self.wazuh_rule_id = self.get_param('data.case.customFields.wazuh_rule_id.string', None, "Agent ID Missing!")
       self.observable = self.get_param('data.data', None, "Data is empty")
       self.observable_type = self.get_param('data.dataType', None, "Data type is empty")

   def run(self):
       Responder.run(self)
       auth = (self.wazuh_user, self.wazuh_password)
       headers = {'Content-Type': 'application/json'}
       # Check observable to ensure input is file
       if self.observable_type == "filename":
           try:
               path.isfile(self.observable)
           except ValueError:
               self.error({'message': "This is not a File"})
       else:
           self.error({'message': "This is not a File"})
       payload = '{"command":"file-encryptor2.sh", "arguments": ["-", "' +  self.observable + '", "' + self.wazuh_alert_id + '", "' + self.wazuh_rule_id + '", "' + self.wazuh_agent_id + '", "var/log/test.log"], "custom": "True"}'
       r = requests.put(self.wazuh_manager + '/active-response/' + self.wazuh_agent_id, headers=headers, data=payload, verify=False, auth=auth)
       if r.status_code == 200:
           self.report({'message': "File encrypted for " + self.observable  })
       else:
           self.error(r.status_code)

   def operations(self, raw):
      return [self.build_operation('AddTagToCase', tag='Wazuh: File Encrypted')]

if __name__ == '__main__':
  Wazuh().run()
