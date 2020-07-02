# -*- coding: UTF-8 -*-
import re
import json
import sys
import os

# main process
args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
result = {}

input_parameter_path_json = path + '/' + 'input_parameter.json'
input_parameter_path = path + '/' + 'input_parameter'

# Load json file
with open(input_parameter_path) as file_object:
    lines = file_object.readlines()
for line in lines:
    if 'VAR_Zabbix40AG_WIN_APITempPath' in line:
        result['VAR_Zabbix40AG_WIN_APITempPath'] = line.split(':',1)[1].strip()

with open(input_parameter_path_json) as file_object:
    input_parameter = file_object.read()
parameter = json.loads(input_parameter)

result['VAR_Zabbix40AG_WIN_serverregister'] = True
result['VAR_Zabbix40AG_WIN_Username'] = parameter['VAR_Zabbix40AG_WIN_Username']
result['VAR_Zabbix40AG_WIN_Password'] = parameter['VAR_Zabbix40AG_WIN_Password']
result['VAR_Zabbix40AG_WIN_ServerAddress'] = parameter['VAR_Zabbix40AG_WIN_ServerAddress']
if parameter['VAR_Zabbix40AG_WIN_Hostname'] == "":
    result['VAR_Zabbix40AG_WIN_Hostname'] = "{{ ansible_hostname }}"
else:
    result['VAR_Zabbix40AG_WIN_Hostname'] = parameter['VAR_Zabbix40AG_WIN_Hostname']

result['VAR_Zabbix40AG_WIN_DisplayName'] = parameter['VAR_Zabbix40AG_WIN_DisplayName']
if parameter['VAR_Zabbix40AG_WIN_HostIP'] == "":
    result['VAR_Zabbix40AG_WIN_HostIP'] = "{{ ansible_host }}"
else:
    result['VAR_Zabbix40AG_WIN_HostIP'] = parameter['VAR_Zabbix40AG_WIN_HostIP']

result['VAR_Zabbix40AG_WIN_AgentPort'] = int(parameter['VAR_Zabbix40AG_WIN_AgentPort'])
result['VAR_Zabbix40AG_WIN_SnmpPort'] = int(parameter['VAR_Zabbix40AG_WIN_SnmpPort'])

result['VAR_Zabbix40AG_WIN_HostGroups'] = []
temp = str(parameter['VAR_Zabbix40AG_WIN_HostGroups'])  # [u'test_zabbix', u'linux_zabbix']
for index in range(len(temp.split("'"))):           # ['[u', 'test_zabbix', ', u', 'linux_zabbix', ']']
    if index % 2 == 1:
        result['VAR_Zabbix40AG_WIN_HostGroups'].append(temp.split("'")[index])

result['VAR_Zabbix40AG_WIN_Templates'] = []
temp = str(parameter['VAR_Zabbix40AG_WIN_Templates'])   # [u'test_zabbix', u'linux_zabbix']
for index in range(len(temp.split("'"))):           # ['[u', 'test_zabbix', ', u', 'linux_zabbix', ']']
    if index % 2 == 1:
        result['VAR_Zabbix40AG_WIN_Templates'].append(temp.split("'")[index])
print(json.dumps(result))
