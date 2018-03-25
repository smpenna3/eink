# Screen Size (176, 264) 

import epd2in7
import Image
import ImageFont
import ImageDraw
from text import *
import logging

# Grab logger
logger = logging.getLogger('mainlog')

# Global Variables
xend = 176
yend = 264

axisoffset = 25
axisend = 10
xzero = xend-axisoffset
yzero = yend-axisoffset
xmax = axisend
ymax = axisend

'''
The axes function will add the axes lines and titles to those axes
INPUTS:
    imageObject: the object image to draw on
    drawObject: the draw object to draw on
    axis1: text title of x axis
    axis2: text title of y axis
'''
def axes(imageObject, drawObject, axis1, axis2):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 10)
    drawObject.line((axisend, yend-axisoffset, xend-axisoffset, yend-axisoffset), fill=0) # Y-axis
    drawObject.line((xend-axisoffset, yend-axisoffset, xend-axisoffset, axisend), fill=0) # X-axis
    centerText(drawObject, axis2, 10, 10+(xend-axisoffset-10)/2, yend-(5)) # Y-label
    rotatedText(imageObject, axis1, 90, 10, xend-5, 10+(yend-axisoffset-10)/2)


'''
The title function will add a title to the top of the screen
INPUTS:
    imageObject: the object image to draw on
    string: text of the graph title
'''
def title(imageObject, string):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
    width = font.getsize(string)[0]
    rotatedText(imageObject, string, 90, 12, 6, yend/2)


'''

'''
def majorAxesDelimiters():
	pass


'''
The scatter function will plot the data in scatter format given two arrays
INPUTS:
	drawObject: the object to draw on
	size: the size of the points
	xdata: an array with the x-coordinates
	ydata: an array with the y-coordinates
'''
def scatter(drawObject, size, xdata, ydata):
	if(len(xdata) != len(ydata)):
		logger.error("ERROR: Data axis length mismatch")
		return 5

	else:
		# Find the length of the x and y axes on the graph
		xlength = xzero-axisend
		ylength = yzero-axisend
		logger.debug('X-axis length (pixels): ' + str(xlength))
		logger.debug('Y-axis length (pixels): ' + str(ylength))

		# Find the range of the x and y data
		dataxlength = max(xdata)-min(xdata)+10
		dataylength = max(ydata)-min(ydata)+10
		logger.debug('X-data range: ' + str(dataxlength))
		logger.debug('Y-data range: ' + str(dataylength))

		# Find how much of the xdata can fit on the xaxis (y length)
		yscale = float(ylength)/float(dataxlength)
		# Find how much of the ydata can fit on the yaxis (x length)
		xscale = float(xlength)/float(dataylength)


		# Find the offset for x and y
		xoffset = min(ydata)
		if(xoffset < max(ydata)/10):
			xoffset = 0
		yoffset = min(xdata)
		if(yoffset < max(xdata)/10):
			yoffset = 0

		logger.debug('X-offset: ' + str(xoffset))
		logger.debug('Y-offset: ' + str(yoffset))		

		logger.debug('X-scale factor: ' + str(xscale))
		logger.debug('Y-scale factor: ' + str(yscale))

		for i in range(0, len(xdata)):
			centerRectangle(drawObject, size, xzero-((ydata[i]-xoffset)*xscale), yzero-((xdata[i]-yoffset)*yscale))





