#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import pymisp
import json
requests.packages.urllib3.disable_warnings()

url_pull = 'https://<misp_fqdn>/attributes/restSearch/json'
headers_pull = {'Authorization': '<misp_token>', 'Content-Type': 'application/json', 'Accept': 'application/json'}
data_pull = {"request": {"type": "ip-dst", "category": "Network activity", "last": "1d", "enforceWarnlinglist": "True"}}
url_push = 'https://<qradar_fqdn>/api/reference_data/sets/bulk_load/<reference_set_name>'
headers_push = {'SEC': '<token>', 'Content-Type': 'application/json', 'Version': '9.0', 'Accept': 'application/json'}

# Pull the list of attributes from a specific MISP instance
r = requests.post(url_pull, headers=headers_pull, json=data_pull, verify=False)
r.raise_for_status() #Raise exception on HTTP errors

print("Pull from MISP complete...extracting IOCs from JSON...")

j1=r.json()
j2 = j1['response']
j3 = j2['Attribute']

iocs = []
clean_iocs = []

for value in j3:
    iocs.append(value["value"])

for ioc in iocs:
    if '|' in ioc:
        continue
    elif '/' in ioc:
        continue
    clean_iocs.append(ioc)

print("IOCs clean...")
    
#Convert to JSON format
json.dumps(clean_iocs)
number_of_IOCs = str(len(clean_iocs))

print("IOCs extracted from JSON...pushing to QRadar...")

#Push list to QRadar
p = requests.post(url_push, headers=headers_push, json=clean_iocs, verify=False)
p.raise_for_status() #Raise exception on HTTP errors
print('Push complete, pushed ' + number_of_IOCs + ' IOCs to QRadar!')
