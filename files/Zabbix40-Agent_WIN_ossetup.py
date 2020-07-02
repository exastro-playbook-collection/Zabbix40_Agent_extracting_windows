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

file_path = []
file_path.append(path + '/command/1/stdout.txt')
file_path.append(path + '/command/2/stdout.txt')

result['VAR_Zabbix40AG_WIN_Started'] = False
result['VAR_Zabbix40AG_WIN_Enable'] = False
for path in file_path:
    if os.path.isfile(path):
        with open(path) as file_object:
            lines = file_object.readlines()
        for line in lines:
            if (re.match( '\s*Running\s+Zabbix\s+Agent\s+Zabbix\s+Agent\s*', line,re.I) != None):
                result['VAR_Zabbix40AG_WIN_Started'] = True
            elif (re.match( '\s*Auto\s*', line,re.I) != None):
                result['VAR_Zabbix40AG_WIN_Enable'] = True
    else:
        result = {}

print(json.dumps(result))
