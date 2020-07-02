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
zab_conf_win_path = path + '/command/0/stdout.txt'
input_parameter_path = path + '/' + 'input_parameter'

with open(input_parameter_path) as file_object:
    lines = file_object.readlines()
for line in lines:
    if 'VAR_Zabbix40AG_WIN_path' in line:
        result['VAR_Zabbix40AG_WIN_path'] = line.split(':',1)[1].strip()


# Filter specified entries for key-value
def functionname( para_name, content_name, line):
    if (re.match( '\s*' + content_name + '\s*=\s*(.*)', line,re.I) != None):
        temp_var = line.split('=',1)[1].strip()
        result[para_name] = temp_var

# Filter specified entries for key-value and value is number
def functionname_int( para_name, content_name, line):
    if (re.match( '\s*' + content_name + '\s*=\s*(.*)', line,re.I) != None):
        temp_var = line.split('=',1)[1].strip()
        if temp_var != "":
            result[para_name] = int(temp_var)

# Filter specified entries for key-list
def functionname_list( para_name, content_name, line):
    if (re.match( '\s*' + content_name + '\s*=\s*(.*)', line,re.I) != None):
        temp_var = line.split('=',1)[1].strip()
        if not para_name in result:
            result[para_name]=[]
        result[para_name].append(temp_var)

zabbix_conf_dict={
    'VAR_Zabbix40AG_WIN_LogType':'LogType',
    'VAR_Zabbix40AG_WIN_LogFile':'LogFile',
    'VAR_Zabbix40AG_WIN_SourceIP':'SourceIP',
    'VAR_Zabbix40AG_WIN_Server':'Server',                 #Must be defined
    'VAR_Zabbix40AG_WIN_ListenIP':'ListenIP',
    'VAR_Zabbix40AG_WIN_ServerActive':'ServerActive',       #Must be defined
    # 'VAR_Zabbix40AG_WIN_Hostname':'Hostname',               #Must be defined
    'VAR_Zabbix40AG_WIN_HostnameItem':'HostnameItem',
    'VAR_Zabbix40AG_WIN_HostMetadata':'HostMetadata',
    'VAR_Zabbix40AG_WIN_HostMetadataItem':'HostMetadataItem',
    'VAR_Zabbix40AG_WIN_TLSConnect':'TLSConnect',
    'VAR_Zabbix40AG_WIN_TLSAccept':'TLSAccept',
    'VAR_Zabbix40AG_WIN_TLSCAFile':'TLSCAFile',
    'VAR_Zabbix40AG_WIN_TLSCRLFile':'TLSCRLFile',
    'VAR_Zabbix40AG_WIN_TLSServerCertIssuer':'TLSServerCertIssuer',
    'VAR_Zabbix40AG_WIN_TLSServerCertSubject':'TLSServerCertSubject',
    'VAR_Zabbix40AG_WIN_TLSCertFile':'TLSCertFile',
    'VAR_Zabbix40AG_WIN_TLSKeyFile':'TLSKeyFile',
    'VAR_Zabbix40AG_WIN_TLSPSKIdentity':'TLSPSKIdentity',
    'VAR_Zabbix40AG_WIN_TLSPSKFile':'TLSPSKFile'
    }
zabbix_conf_int_dict={
    'VAR_Zabbix40AG_WIN_LogFileSize':'LogFileSize',
    'VAR_Zabbix40AG_WIN_DebugLevel':'DebugLevel',
    'VAR_Zabbix40AG_WIN_EnableRemoteCommands':'EnableRemoteCommands',
    'VAR_Zabbix40AG_WIN_LogRemoteCommands':'LogRemoteCommands',
    'VAR_Zabbix40AG_WIN_ListenPort':'ListenPort',
    'VAR_Zabbix40AG_WIN_StartAgents':'StartAgents',
    'VAR_Zabbix40AG_WIN_RefreshActiveChecks':'RefreshActiveChecks',
    'VAR_Zabbix40AG_WIN_BufferSend':'BufferSend',
    'VAR_Zabbix40AG_WIN_BufferSize':'BufferSize',
    'VAR_Zabbix40AG_WIN_MaxLinesPerSecond':'MaxLinesPerSecond',
    'VAR_Zabbix40AG_WIN_Timeout':'Timeout',
    'VAR_Zabbix40AG_WIN_UnsafeUserParameters':'UnsafeUserParameters'
    }
zabbix_conf_list_dict={
    'VAR_Zabbix40AG_WIN_Alias':'Alias',
    'VAR_Zabbix40AG_WIN_Include':'Include',
    'VAR_Zabbix40AG_WIN_UserParameter':'UserParameter',
    'VAR_Zabbix40AG_WIN_PerfCounter':'PerfCounter'
    }

# For parameter in zabbix-agentd.conf
if os.path.isfile(zab_conf_win_path):
    with open(zab_conf_win_path) as file_object:
        zab_conf_lines = file_object.readlines()
    for line in zab_conf_lines:
        line = line.strip()
        for temp in zabbix_conf_dict.keys():
            functionname(temp,zabbix_conf_dict[temp],line)
        for var in zabbix_conf_list_dict.keys():
            functionname_list(var,zabbix_conf_list_dict[var],line)
        for int_var in zabbix_conf_int_dict.keys():
            functionname_int(int_var,zabbix_conf_int_dict[int_var],line)

result['VAR_Zabbix40AG_WIN_conf'] = 'zabbix_agentd.win.conf'
result['VAR_Zabbix40AG_WIN_Hostname'] = '{{ ansible_hostname }}'
print(json.dumps(result))
