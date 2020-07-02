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

input_parameter_path = path + '/' + 'input_parameter'

# Load json file
with open(input_parameter_path) as file_object:
    lines = file_object.readlines()
for line in lines:
    if 'VAR_Zabbix40AG_WIN_path' in line:
        result['VAR_Zabbix40AG_WIN_path'] = line.split(':',1)[1].strip()
    if 'VAR_Zabbix40AG_WIN_localpkg_src' in line:
        result['VAR_Zabbix40AG_WIN_localpkg_src'] = line.split(':',1)[1].strip()
    if 'VAR_Zabbix40AG_WIN_localpkg_dst' in line:
        result['VAR_Zabbix40AG_WIN_localpkg_dst'] = line.split(':',1)[1].strip()
result['VAR_Zabbix40AG_WIN_conf'] = 'zabbix_agentd.win.conf'
result['VAR_Zabbix40AG_WIN_localpkg_upload'] = True
result['VAR_Zabbix40AG_WIN_localpkg_Zabbix_file'] = 'zabbix_agents-4.0.0-win-amd64.zip'


print(json.dumps(result))
