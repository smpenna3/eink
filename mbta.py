import requests
import json
from eink import eink
import logging
import traceback
import sys
import math
from stops import stops
from datetime import datetime as dt
import pytz

timezone = pytz.timezone('US/Eastern')

directions = ['South', 'North']


class MBTATimeTracker(eink):
	def __init__(self, stopname, line):
		'''
		Initializes an mbta object with stop name
		INPUTS:
			stop: name of the stop to work with
		'''
		self.url = 'https://api-v3.mbta.com/'
		self.stopname = stopname
		self.line = line

	
	def mbta_request(self, arguments):
		''' Request data from the MBTA API '''
		response = requests.get(self.url + arguments)
		if(response.status_code != 200):
			raise Exception("Invalid API Call. Status Code " + str(response.status_code))
		
		return json.loads(response.text)['data']


	def stop_predictions(self):
		''' Get predictions for the stop '''
		# Returns a list of predictions
		predictions = self.mbta_request('predictions?filter[stop]='+str(self.stopname))

		return_predictions = []

		for prediction in predictions:
			# Each prediction is a dictionary
			direction = directions[prediction['attributes']['direction_id']]
			#direction = self.getDirection(prediction['attributes']['direction_id'], self.line)
			departure_time = prediction['attributes']['departure_time']

			minutes, seconds = self.get_minsec(departure_time)

			if(prediction['relationships']['route']['data']['id'] == self.line):
				return_predictions.append(['NA', direction, minutes, seconds])

		return return_predictions


	def get_minsec(self, time):
		''' Convert the departure timestamp into a minutes/seconds from now '''
		try:
			now = dt.now(timezone)
			departure = dt.strptime(time, '%Y-%m-%dT%H:%M:%S%z')

			difference = departure - now

			return math.floor(difference.seconds / 60), difference.seconds % 60
		except:
			return 0, 0

			
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
		self.eink.rotatedText(self.stopname, 0, self.title_fontSize, self.eink.xend/2, self.title_fontSize/2+self.spacingTop/2, fill=0)
		
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


	def getDirection(self, direction_id, route):
		'''
		Returns the direction of the given route
		INPUTS:
			direction_id: The ID of the direction, gotten from the predictions and corresponds to the direction
			route: The route to find the direction of
		'''
		try:
			response = self.mbta_request("routes/"+str(route))
			return response['attributes']['direction_names'][direction_id]
		
		except:
			print("ERROR: Could not find direction id " + str(direction_id) + ' for route ' + str(route))
			print(traceback.format_exc())


if(__name__ == '__main__'):
	m = MBTATimeTracker('place-rugg', 'Orange')
	a = m.stop_predictions()
	print(a)
	m.timesToDisplay(a)