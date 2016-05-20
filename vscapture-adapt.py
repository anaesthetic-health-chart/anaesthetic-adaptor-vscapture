#!/usr/bin/env python

import httplib, urllib
import time
import os.path
import requests
import sys
import time
import urlparse
import json
import requests

'''
The following is the CSV columns we receive from VSCapture
00 Date
01 Time
02 Heart Rate(/min)
03 Systolic BP(mmHg) - Systolic (Sys) Blood Pressure (BP)
04 Diastolic BP(mmHg) - Diastolic (Dia) BP
05 Mean BP(mmHg)
06 SpO2(%)
07 ETCO2(mmHg) - End Tidal (ET) C02
08 CO2 FI
09 ETO2(mmHg) - End Tidal (ET) C02
10 AA ET - Anaesthetic.Agent (AA) ET
11 AA FI - AA Fraction Inspired (FI)
12 AA MAC SUM - minimum aviolo concentration
13 AA
14 O2 FI
15 N2O FI
16 N2O ET
17 RR - Respiratory Rate (RR)
18 T1 temperature
19 T2
20 P1 HR - (Normally Invasive [P1]) Heart Rate (HR)
21 P1 Sys - P1 Sys BP
22 P1 Dia - P1 Dia BP
23 P1 Mean
24 P2 HR (Central Venous Pressure [P2]) HR
25 P2 Sys
26 P2 Dia
27 P2Mean
28 PPeak - Peak Airway Pressure (PPeak)
29 PPlat - Plateau Pressure (PPlat)
30 TV Exp - Expiratory (Exp) Tidal Volume (TV)
31 TV Insp - Inspiratory (Insp) TV
32 Peep Positive End Expiratory Pressure (Peep)
33 MV Exp minute volume
34 Compliance
35 RR
36 ST II(mm) ecg stuff
37 ST V5(mm)
38 ST aVL(mm)
39 SE state entropy (brain)
40 RE response entropy
41 ENTROPY BSR
42 BIS bispectral index (BWM)
43 BIS BSR
44 BIS EMG
45 BIS SQI
46 **Python mapping of datetime
'''

'''
This is where we map the data from the VSCapture CSV to the data models in
the web app
'''
dataMaps = {
  'Observation': {
    'uri': '/api/v0.1/observation/',
    'map': {
      'bp_systolic': 3,
      'bp_diastolic': 4,
      'pulse': 2,
      'resp_rate': 17,
      'sp02': 6,
      'temperature': 18,
      'datetime': 46
    }
  },
  'Gases': {
    'uri': '/api/v0.1/gases/',
    'map': {
      'inspired_carbon_dioxide': 8,
      'expired_carbon_dioxide': 7,
      'inspired_oxygen': 14,
      'expired_oxygen': 9,
      'datetime': 46
    }
  },
  'Ventilators': {
    'uri': '/api/v0.1/ventilators/',
    'map': {
      'peak_airway_pressure': 28,
      'peep_airway_pressure': 32,
      'rate': 17,
      'datetime': 46
    }
  }
}

if len(sys.argv) != 3:
  print "Usage: %s <VSCAPTURE_CSV> <HEALTH_CHART_BASE_URL>"
  print "  <VSCAPTURE_CSV> The CSV file being written to by VSCapture"
  print "  <HEALTH_CHART_BASE_URL> Base URL of the health chart to send the data to"
  sys.exit(1)

filename = sys.argv[1]
baseUrl = sys.argv[2]

# Check file exists and open file
if not os.path.isfile(filename):
  print "Couldn't find CSV to read"
  sys.exit(2)

print "Opening file %s" % filename
fp = open(filename, 'r')

# Should at least the first three lines that container a file header
fp.readline()
fp.readline()
fp.readline()
#Find the size of the file and move to the end
#st_results = os.stat(filename)
#st_size = st_results[6]
#fp.seek(st_size)

while 1:
  where = fp.tell()
  line = fp.readline()
  if not line:
    time.sleep(1)
    fp.seek(where)
  else:
    #print line, # already has newline

    parts = line.split(',')

    # Create properly formatted datetime string
    #parts[46] = '%s %s' % (time.strftime('%Y-%m-%d', time.strptime(parts[0], '%d/%m/%Y')), parts[1])
    parts[46] = '%s %s' % (parts[0], parts[1])

    # Start running maps and POSTs
    for m in dataMaps:
      #print 'Building %s map' % m
      data = {
        'episode_id': 1
      }
      for d in dataMaps[m]['map']:
        if parts[dataMaps[m]['map'][d]] != '-':
          #print '%s: %s' % (d, parts[dataMaps[m]['map'][d]])
          data[d] = parts[dataMaps[m]['map'][d]]

      #print 'data is:'
      #print data

      #print 'Making url from %s and %s' % (baseUrl, dataMaps[m]['uri'])
      url = urlparse.urljoin(baseUrl, dataMaps[m]['uri'])
      print url
      urlBits = urlparse.urlparse(url)

      params = urllib.urlencode({'number': 12524, 'type': 'issue', 'action': 'show'})
      headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
      }

      print 'sending ' + json.dumps(data, separators=(',',':'))

      response = requests.post(url, data=json.dumps(data, separators=(',',':')), headers=headers)
      print response.status, response.reason
