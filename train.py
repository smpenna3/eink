import requests, urllib
import json
import os
from eink import eink
import datetime
import argparse
import pandas as pd
from mbta import mbta
import logging

# Setup logging
logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
logger.addHandler(stream)

url = 'https://api-v3.mbta.com/'


#test = json.loads(test.read().decode())

#print(json.dumps(test, indent=4, sort_keys=True))

#for key in test['data']:
#	print key

#print(test['data'][0])
#print(json.dumps(test['data'][0], indent=4, sort_keys=True))

'''
sched = urllib.urlopen(url+'predictions?filter[stop]=70015')
schedjson = json.loads(sched.read().decode())
print(json.dumps(schedjson, indent=4, sort_keys=True))
'''

'''
sched = urllib.urlopen(url+'predictions?filter[route]=Red')
schedjson = json.loads(sched.read().decode())
print(json.dumps(schedjson, indent=4, sort_keys=True))
'''

'''
stop = urllib.urlopen(url+'stops/70071')
schedjson = json.loads(stop.read().decode())
print(json.dumps(schedjson, indent=4, sort_keys=True))
'''

mbta = mbta(stop='Harvard')
#mbta.nearStations()

#print(mbta.predictionsFromLine('Red'))

a = [['Rapid Transit', 'Northbound', 0, 26], ['Rapid Transit', 'Southbound', 2, 33],['Rapid Transit', 'Northbound', 0, 26],['Rapid Transit', 'Northbound', 0, 26]]
#print(mbta.arrivalToDelta(mbta.predictionsFromStop()))
mbta.timesToDisplay(a)
