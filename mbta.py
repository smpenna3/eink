import urllib
import json
from eink import eink
import datetime
import logging
import traceback
import sys
from stops import stops

# Grab logger
logger = logging.getLogger('mainlog')

class mbta(eink):
	def __init__(self, latitude=0, longitude=0, stop=''):
		self.url = 'https://api-v3.mbta.com'
		self.latitude = latitude
		self.longitude = longitude
		self.stopName = stop
		self.stopID = stops[self.stopName]

	
	def jsonLoad(self, item):
		return json.loads(item.read().decode())


	def stopName(self, stopID):
		if(not isinstance(stopID, basestring)):
			logger.error("ERROR: line argument isn't string")
		try:
			self.response_tmp = urllib.urlopen(self.url+'/stops/'+str(stopID))
			self.json_tmp = self.jsonLoad(self.response_tmp)
			return self.json_tmp['data']['attributes']['name']
		except:
			logger.error("ERROR: Could not find station with ID " + str(stopID))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())
			sys.exit()


	def predictionsFromLine(self, line):
		if(not isinstance(line, basestring)):
			logger.error("ERROR: line argument isn't string")

		try:
			self.response_tmp = urllib.urlopen(self.url+'/predictions?filter[route]='+line)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			self.return_tmp = []
			for item in self.json_tmp['data']:
				self.stopID_tmp = item['relationships']['stop']['data']['id']
				self.stopName_tmp = self.stopName(self.stopID_tmp)
				self.nextArrival = item['attributes']['arrival_time']
				self.return_tmp.append([self.stopName_tmp, self.nextArrival])
			
			return self.return_tmp
			

		except:
			logger.error("ERROR: Could not find schedule for line " + str(line))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())

	
	def getRouteDescription(self, route):
		try:
			self.response_tmp = urllib.urlopen(self.url+'/routes/'+route)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			return self.json_tmp['data']['attributes']['description']
		
		except:
			logger.error("ERROR: Could not find route " + str(route))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())


	def arrivalToDelta(self, item):
		self.return_tmp = []
		for arrival in item:
			self.seconds_tmp = (datetime.datetime.strptime(arrival[2], '%Y-%m-%dT%H:%M:%S-04:00')-datetime.datetime.now()).seconds
			self.return_tmp.append([arrival[0], arrival[1], self.seconds_tmp/60, self.seconds_tmp%60])
		return self.return_tmp
		

	def getDirection(self, direction_id, route):
		try:
			self.response_tmp = urllib.urlopen(self.url+'/routes/'+route)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			return self.json_tmp['data']['attributes']['direction_names'][direction_id]
		
		except:
			logger.error("ERROR: Could not find direction id " + str(direction_id) + ' for route ' + str(route))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())

	def timesToDisplay(self, item):
		self.eink = eink()
		self.title_fontSize = 16
		self.listing_fontSize = 12
		self.spacingTop = 20
		self.eink.rotatedText(self.stopName, 0, self.title_fontSize, self.eink.xend/2, self.title_fontSize/2+1)
		self.eink.lineDraw(0, self.title_fontSize+self.spacingTop, self.eink.xend, self.title_fontSize+self.spacingTop)
		if(6 > len(item)):
			self.max_tmp = len(item)
		else:
			self.max_tmp = 6

		# Draw the direction of the train
		for i in range(0, self.max_tmp):
			self.eink.leftText(item[i][1], self.listing_fontSize, 1, self.title_fontSize+self.spacingTop+8+((self.listing_fontSize+2)*i))
			self.eink.lineDraw(0, (self.title_fontSize+self.listing_fontSize+self.spacingTop+3)+((self.listing_fontSize+2)*i), self.eink.xend, (self.title_fontSize+self.listing_fontSize+self.spacingTop+3)+((self.listing_fontSize+2)*i))

		# Draw the time until the train
		for i in range(0, self.max_tmp):
			self.str_tmp = str(item[i][2]) + ':' + str(item[i][3])
			self.eink.rightText(self.str_tmp, self.listing_fontSize, self.eink.xend, self.title_fontSize+self.spacingTop+8+((self.listing_fontSize+2)*i))

		self.eink.display()
	
	def predictionsFromStop(self, stopID=''):
		if(not isinstance(stopID, basestring)):
			stopID = str(stopID)
		if(stopID == ''):
			stopID = self.stopID
		else:
			self.stopID = stopID
			for name, ID in stops:
				if ID == stopID:
					self.stopName = name
		try:
			self.response_tmp = urllib.urlopen(self.url+'/predictions?filter[stop]='+stopID)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			self.arrivals = []
			for item in self.json_tmp['data']:
				self.direction_tmp = self.getDirection(item['attributes']['direction_id'], item['relationships']['route']['data']['id'])
				self.time_tmp = item['attributes']['arrival_time']
				self.routeDescription_tmp = self.getRouteDescription(item['relationships']['route']['data']['id'])
				if(self.routeDescription_tmp == 'Rapid Transit'):
					self.arrivals.append([self.routeDescription_tmp, self.direction_tmp, self.time_tmp])
			return self.arrivals

		except:
			logger.error("ERROR: Could not find schedule for stop " + str(stopID))
			logger.error(traceback.print_exc())


	def nearStations(self, radius=0.0000025):
		if(self.latitude != 0 and self.longitude != 0):
			self.response_tmp = urllib.urlopen(self.url+'/stops?filter[latitude]='+str(self.latitude)+'?filter[longitude]='+str(self.longitude)+'?filter[radius]='+str(radius))
			self.json_tmp = self.jsonLoad(self.response_tmp)
			print(json.dumps(self.json_tmp, indent=4))




