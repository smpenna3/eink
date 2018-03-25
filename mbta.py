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
        '''
        Initializes an mbta object with latitude, longitude, and/or station name
        (latitude and longitude aren't implemented correctly)
        INPUTS:
            latitude: latitude of desired location
            longitude: longitude of desired location
            stop: name of the stop to work with
        '''
		self.url = 'https://api-v3.mbta.com'
		self.latitude = latitude
		self.longitude = longitude
		self.stopName = stop
		self.stopID = stops[self.stopName]

	
	def jsonLoad(self, item):
        '''
        Returns the decoded json object
        INPUTS:
            item: response from urlopen call
        '''
		return json.loads(item.read().decode())


	def stopName(self, stopID):
        '''
        Returns the name of the stop from the stopID
        INPUTS:
            stopID: the ID of the stop to be found
        '''
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
        '''
        Finds and returns all arrivals for a specified line in an array with stop name and time
        INPUTS:
            line: the line to return arrival data for
        '''
        # Check that the line is a string, if not then change to string
		if(not isinstance(line, basestring)):
			logger.warning("Warning: line argument isn't string")
            line = str(line)

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
        '''
        Get and return the description of a line, such as Rapid Transit or Bus Line
        INPUTS:
            route: the ID of the route to analyze
        '''
        # Check that the route is a string, if not then change to string
		if(not isinstance(route, basestring)):
			logger.warning("Warning: route argument isn't string")
            route = str(route)
		try:
			self.response_tmp = urllib.urlopen(self.url+'/routes/'+route)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			return self.json_tmp['data']['attributes']['description']
		
		except:
			logger.error("ERROR: Could not find route " + str(route))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())


	def arrivalToDelta(self, item):
        '''
        Changes all of the arrival times to delta time from present in array
        INPUTS:
            item: array with arrival times formatted: ['route_type', 'direction', 'arrival_time']
        '''
		self.return_tmp = []
		for arrival in item:
			self.seconds_tmp = (datetime.datetime.strptime(arrival[2], '%Y-%m-%dT%H:%M:%S-04:00')-datetime.datetime.now()).seconds
			self.return_tmp.append([arrival[0], arrival[1], self.seconds_tmp/60, self.seconds_tmp%60])
		return self.return_tmp
		

	def getDirection(self, direction_id, route):
        '''
        Returns the direction of the given route
        INPUTS:
            direction_id: The ID of the direction, gotten from the predictions and corresponds to the direction
            route: The route to find the direction of
        '''
		try:
			self.response_tmp = urllib.urlopen(self.url+'/routes/'+route)
			self.json_tmp = self.jsonLoad(self.response_tmp)
			return self.json_tmp['data']['attributes']['direction_names'][direction_id]
		
		except:
			logger.error("ERROR: Could not find direction id " + str(direction_id) + ' for route ' + str(route))
			logger.error("Response: " + str(self.json_tmp))
			logger.error(traceback.print_exc())

            
	def timesToDisplay(self, item):
        '''
        Displays the predicted times on the epaper display with the station as a header
        INPUT:
            item: the array holding the times, formatted: ['route_type', 'direction', 'minutes', 'seconds']
        '''
        # Initilaize the E-ink screen
		self.eink = eink()
		self.title_fontSize = 16 # Set the title font size
		self.listing_fontSize = 12 # Set the time listing font size
		self.spacingTop = 20 # Set the spacing for the title
		self.interSpacing = 10 # Set the spacing between the listings
        
        # Draw a rectangle around the title
		self.eink.draw.rectangle((0, 0, self.eink.xend, self.title_fontSize+self.spacingTop), fill=0)
        # Write the title at the top center
		self.eink.rotatedText(self.stopName, 0, self.title_fontSize, self.eink.xend/2, self.title_fontSize/2+self.spacingTop/2, fill=0)
        
        # Determine the max number of list items to write
        # If the length of the predicted times is greater than 6, cap at 6 times
        # If the length is not greater than six, set as the length of available times
		if(6 > len(item)):
			self.max_tmp = len(item)
		else:
			self.max_tmp = 6

		# Draw the direction of the train (southbound/westbound/eastbound/northbound)
        # and the lines between each listing
		for i in range(0, self.max_tmp):
			self.eink.leftText(item[i][1], self.listing_fontSize, 1, self.title_fontSize+self.spacingTop+8+self.interSpacing+((self.listing_fontSize+self.interSpacing)*i))
			self.eink.draw.line((0, (self.title_fontSize+self.listing_fontSize+self.spacingTop+3+self.interSpacing)+((self.listing_fontSize+self.interSpacing)*i), self.eink.xend, (self.title_fontSize+self.listing_fontSize+self.spacingTop+self.interSpacing+3)+((self.listing_fontSize+self.interSpacing)*i)), fill=0)

		# Draw the time until the train, as a string concatenated from the minutes and seconds in the array
		for i in range(0, self.max_tmp):
			if(len(str(item[i][3])) == 1):
				item[i][3] = '0' + str(item[i][3])
			self.str_tmp = str(item[i][2]) + ':' + str(item[i][3])
			self.eink.rightText(self.str_tmp, self.listing_fontSize, self.eink.xend, self.title_fontSize+self.spacingTop+8+self.interSpacing+((self.listing_fontSize+self.interSpacing)*i))

        # Display the times on the e-paper display
		self.eink.display()
	
    
	def predictionsFromStop(self, stopID=''):
        '''
        Returns an array with the upcoming departures for a stop
        INPUTS:
            stopID: the ID of the stop to get the departing trains from
        '''
        # Check that the stopID is a string, if not make it a string
		if(not isinstance(stopID, basestring)):
			stopID = str(stopID)
		if(stopID == ''):
            # If the user doesn't provide the stopID, use the one in the object
			stopID = self.stopID
		else:
            # If the user does provide the name, find the stopID from it
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
			logger.error('Response: ' + str(self.json_tmp))
			logger.error(traceback.print_exc())


	def nearStations(self, radius=0.0000025):
        '''
        Returns the stations near the given coordinates
        INPUTS:
            radius: radius at which to look for stations
            
        THIS FUNCTION DOESN'T WORK
        '''
		if(self.latitude != 0 and self.longitude != 0):
			self.response_tmp = urllib.urlopen(self.url+'/stops?filter[latitude]='+str(self.latitude)+'?filter[longitude]='+str(self.longitude)+'?filter[radius]='+str(radius))
			self.json_tmp = self.jsonLoad(self.response_tmp)
			print(json.dumps(self.json_tmp, indent=4))




