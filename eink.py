# Screen Size (176, 264) 

import epd2in7
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import logging
import math
import sys

# Grab logger
logger = logging.getLogger('mainlog')

class eink:
    def __init__(self):
        '''
        Initializes a new object with the relevant parameters
        '''
        # Setup the image canvas and the display driver
        self.image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.epd = epd2in7.EPD()
        self.epd.init()
        
        # Define constants
        self.axisend = 5
        self.axisoffset = 20
        self.yaxisoffset = 25
        self.xend = 176
        self.yend = 264
        self.xzero = self.xend-self.axisoffset
        self.yzero = self.yend-self.yaxisoffset
        self.ymax = self.axisend
        self.xmax = self.axisend
        self.axisthickness = 2
        self.roundToBase = [5, 5]
        self.page = 0
        self.maxPages = 100    
    
        # Define flags
        self.dataPlotted = False


    def display(self):
        '''
        Updates the display
        '''
        self.epd.display_frame(self.epd.get_frame_buffer(self.image))

    
    def fontGrab(self, fontSize):
        '''
        Returns a font object of the given fontSize
        INPUTS:
            fontSize: the size of the font to return
        '''
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fontSize)        


    def rightText(self, string, fontSize, x, y):
        '''
        Draws text to the canvas, justified right
        INPUTS:
            string: string to print
            fontSize: size of font to print
            x: right x-coordinate
            y: center y-coordinate
        '''
        self.font_tmp = self.fontGrab(fontSize)
        self.width_tmp = self.font_tmp.getsize(string)[0]
        self.draw.text((x-self.width_tmp-1, y-(fontSize/2)), string, font=self.font_tmp, fill=0)


    def leftText(self, string, fontSize, x, y):
        '''
        Draws text to the canvas, justified left
        INPUTS:
            string: string to print
            fontSize: size of font to print
            x: left x-coordinate
            y: center y-coordinate
        '''
        self.font_tmp = self.fontGrab(fontSize)
        self.draw.text((x, y-(fontSize/2)), string, font=self.font_tmp, fill=0)


    def rotatedText(self, string, angle, fontSize, x, y, fill=255):
        '''
        Draws text to the canvas, rotated to a specified angle
        INPUTS:
            string: string to write to the canvas
            angle: angle to rotate the string at
            fontSize: size of font to use
            x: center x-coordinate
            y: center y-coordinate
        '''
        self.font_tmp = self.fontGrab(fontSize)
        self.fill_tmp = fill
        if(fill == 0):
            self.fill_tmp2 = 255
        else:
            self.fill_tmp2 = 0
        self.im_tmp = Image.new('1', (self.font_tmp.getsize(string)[0], fontSize), self.fill_tmp)
        self.draw_tmp = ImageDraw.Draw(self.im_tmp)
        self.draw_tmp.text((0, 0), string, font=self.font_tmp, fill=self.fill_tmp2)
        self.rotated_tmp = self.im_tmp.rotate(angle, expand=1)
        self.width_tmp, self.height_tmp = self.rotated_tmp.size
        self.image.paste(self.rotated_tmp, (int(x-(self.width_tmp/2)), int(y-(self.height_tmp/2))))


    def centerSquare(self, size, x, y):
        '''
        Draws a sqare in the given location based on center coordinates
        INPUTS:
            size: side length of the rectangle to draw in pixels
            x: center x-coordinate
            y: center y-coordinate
        '''
        self.draw.rectangle((x-(size/2), y+(size/2), x+(size/2), y-(size/2)), fill=0)


    def centerRectangle(self, xlength, ylength, x, y):
        '''
        Draws a rectangle around given center location
        INPUTS:
            xlength: half length of x direction
            ylength: half length of y direction
            x: center x-coordinate
            y: center y-coordinate
        '''
        self.draw.rectangle((x-xlength, y-ylength, x+xlength, y+ylength), fill=0)


    def axes(self, axis1, axis2):
        '''
        Draws and labels the axes on the graph
        INPUTS:
            axis1: title for the x-axis
            axis2: title for the y-axis
        '''

        # Data needs to have been plotted first
        if(self.dataPlotted):
            font = self.fontGrab(10)
            self.draw.rectangle((self.xend-self.axisoffset-self.axisthickness, self.axisend, self.xend-self.axisoffset, self.yend-self.yaxisoffset), fill=0) # X-axis line
            self.draw.rectangle((self.axisend, self.yend-self.yaxisoffset-self.axisthickness, self.xend-self.axisoffset, self.yend-self.yaxisoffset), fill=0) # Y-axis line

            self.rotatedText(axis2, 180, 10, 10+(self.xend-self.axisoffset-10)/2, self.yend-(5)) # Y-label
            self.rotatedText(axis1, 90, 10, self.xend-5, 10+(self.yend-self.axisoffset-10)/2) # X-label
        else:
            logger.error("ERROR: Data not plotted, axes")
            sys.exit()


    def title(self, string):
        '''
        Adds a title to the graph
        INPUTS:
            string: title of the graph
        '''

        if(self.dataPlotted):
            self.font_tmp = self.fontGrab(13)
            self.width_tmp = self.font_tmp.getsize(string)[0]
            self.rotatedText(string, 90, 12, 6, self.yend/2)
        else:
            logger.error("ERROR: Data not plotted, title")
            sys.exit()


    def roundTo(self, x, base, up=False, down=False):
        '''
        Function to round to a certain base
        INPUTS:
            x: the value to round
            base: the closest base to round to
            up: boolean to say if it rounds to nearest or rounds up (default Nearest)
            ex. round 3 up to the nearest 10 roundUp(3, 10, up=True)
        RETURN:
            returns the rounded value
        '''
    
        if(up):
            return math.ceil(float(x)/float(base))*base
        elif(down):
            return math.floor(float(x)/float(base))*base
        else:
            return round(float(x)/float(base))*base
    

    def graphSetup(self, xdata, ydata):
        '''
        Finds the parameters necessary to graph
        INPUTS:
            xdata: list of the x-coordinates (must be same length as ydata)
            ydata: list of the y-coordinates (must be same length as xdata)
        '''
        
        # Check if the x list and y list are the same length
        if(len(xdata) != len(ydata)):
            logger.error("ERROR: Data length mismatch")
            sys.exit()
    
        # Find the length of the x and y axes on the graph
        self.xlength = self.xzero-self.axisend
        self.ylength = self.yzero-self.axisend
        logger.debug('X-axis length (pixels): ' + str(self.xlength))
        logger.debug('Y-axis length (pixels): ' + str(self.ylength))

        # Find the range of the x and y data
        self.dataxlength = max(xdata)-min(xdata)+10
        self.dataylength = max(ydata)-min(ydata)+10
        logger.debug('X-data range: ' + str(self.dataxlength))
        logger.debug('Y-data range: ' + str(self.dataylength))

        # Find how much of the xdata can fit on the xaxis (y length)
        self.yscale = float(self.ylength)/float(self.dataxlength)
        # Find how much of the ydata can fit on the yaxis (x length)
        self.xscale = float(self.xlength)/float(self.dataylength)


        # Find the offset for x and y
        self.xoffset = min(ydata)
        if(self.xoffset < max(ydata)/10):
            self.xoffset = 0
        self.yoffset = min(xdata)
        if(self.yoffset < max(xdata)/10):
            self.yoffset = 0
    
        # Log found data
        logger.debug('X-offset: ' + str(self.xoffset))
        logger.debug('Y-offset: ' + str(self.yoffset))        
        logger.debug('X-scale factor: ' + str(self.xscale))
        logger.debug('Y-scale factor: ' + str(self.yscale))

        self.markers(xdata, ydata)


    def scatter(self, size, xdata, ydata, grid='off', markers=True):
        '''
        Displays the points given in a scatterplot
        INPUTS:
            size: size of the points to plot (side length in pixels)
            xdata: list of the x-coordinates (must be same length as ydata)
            ydata: list of the y-coordinates (must be same length as xdata)
            grid: boolean to say if grid is horizontal ('horizontal') or both ('full')  (default off)
            markers: boolean to say if the markers are placed (default placed)
        '''
        
        # Setup graphing parameters
        if(markers):
            self.graphSetup(xdata, ydata)
    
        # For each point in the dataset, create a rectangle to show the point
        for i in range(0, len(xdata)):
            self.centerSquare(size, self.xzero-((ydata[i]-self.xoffset)*self.xscale), self.yzero-((xdata[i]-self.yoffset)*self.yscale))

        if(markers):
            self.majorDelimiters(xdata, ydata, grid)


    def markers(self, xdata, ydata):
        '''
            Finds the major axis delimiters
            INPUTS:
                xdata: list of x coordinate data (same length as ydata)
                ydata: list of y coordinate data (same length as xdata)
        '''
        if(len(str(int(max(ydata)))) > 3):
            self.roundToBase[1] = 100
        elif(len(str(int(max(ydata)))) > 2):
            self.roundToBase[1] = 10
        if(len(str(int(max(xdata)))) > 3):
            self.roundToBase[0] = 100
        elif(len(str(int(max(xdata)))) > 2):
            self.roundToBase[0] = 10

        # Find the data per marker
        self.dataperX = self.roundTo(((max(xdata) - min(xdata))/8), self.roundToBase[0], up=True)
        self.dataperY = self.roundTo(((max(ydata) - min(ydata))/6), self.roundToBase[1], up=True)
        logger.debug('Data per mark X-axis: ' + str(self.dataperX))
        logger.debug('Data per mark Y-axis: ' + str(self.dataperY))
        
        # Find the marker points
        self.xmarkers = [] 
        self.ymarkers = []

        for i in range(0, 8):
            self.xmarkers.append(self.roundTo(min(xdata), self.roundToBase[0])+(i*self.dataperX))
        for i in range(0, 5):
            self.ymarkers.append(self.roundTo(min(ydata), self.roundToBase[1])+(i*self.dataperY))
            
        logger.debug('X Markers: ' + str(self.xmarkers))
        logger.debug('Y Markers: ' + str(self.ymarkers))

        self.dataPlotted = True

        if(len(str(int(max(self.ymarkers)))) > 2):
            self.yaxisoffset = 30
            self.yzero = self.yend-self.yaxisoffset
        elif(len(str(int(max(self.ymarkers)))) > 3):
            self.yaxisoffset = 35
            self.yzero = self.yend-self.axisoffset
    

    def linePlot(self, xdata, ydata, points=False, grid='off'):
        '''
        Displays the points given in a line graph
        INPUTS:
            xdata: list of the x-coordinates (must be same length as ydata)
            ydata: list of the y-coordinates (must be same length as xdata)
            grid: boolean to say if grid is horizontal ('horizontal') or both ('full')  (default off)
        '''
        # Setup graphing parameters
        self.graphSetup(xdata, ydata)
    
        # If points are needed place those on image
        if(points):
            self.scatter(2, xdata, ydata, markers=False)
        
        # Plot the lines between each point
        for i in range(0, len(xdata)-1):
            self.firstX_tmp = self.xzero-((ydata[i]-self.xoffset)*self.xscale)
            self.firstY_tmp = self.yzero-((xdata[i]-self.yoffset)*self.yscale)
            self.secondX_tmp = self.xzero-((ydata[i+1]-self.xoffset)*self.xscale)
            self.secondY_tmp = self.yzero-((xdata[i+1]-self.yoffset)*self.yscale)
            self.draw.line((self.firstX_tmp, self.firstY_tmp, self.secondX_tmp, self.secondY_tmp), fill=0)    

        self.majorDelimiters(xdata, ydata, grid)


    def barPlot(self, xdata, ydata, space=10, grid='off'):
        '''
        Displays the points given in a bar graph
        INPUTS:
            xdata: list of the x values (must be same length as y values)
            ydata: list of the y values (must be same length as x values)
            space: number of pixels to leave between bars (default 10)
            grid: boolean to say if grid is horizontal ('horizontal') or both ('full')  (default off)
        '''
        # Setup graphing parameters
        self.graphSetup(xdata, ydata)
        
        # Get bar graph specific parameters
        if(len(xdata) > self.xlength/2):
            logger.warning("WARNING: Too many data points for given resolution")

        #find the bar width
        if(space < 0):
            logger.warning("WARNING: Spacing is less than 0")
            space = 0

        self.barWidth = (self.ylength/len(xdata))-space
        if(self.barWidth < 2):
            self.barWidth = 2
            logger.error("ERROR: spacing too large")

        logger.debug('Bar width: ' + str(self.barWidth))

        # Plot the bars
        for i in range(0, len(xdata)):
            self.x1_tmp = self.xzero-((ydata[i]-self.xoffset)*self.xscale)
            self.y1_tmp = self.yzero-((xdata[i]-self.yoffset)*self.yscale)+(self.barWidth/2)
            self.x2_tmp = self.xzero
            self.y2_tmp = self.yzero-((xdata[i]-self.yoffset)*self.yscale)-(self.barWidth/2)
            self.draw.rectangle((self.x1_tmp, self.y1_tmp, self.x2_tmp, self.y2_tmp), fill=0)
        
        self.majorDelimiters(xdata, ydata, grid)


    def majorDelimiters(self, xdata, ydata, grid=False):
        '''
        Displays the axis markings. Called by internal functions
        INPUTS:
            xdata: list of the x-coordinates
            ydata: list of the y-coordinates
            grid: boolean if the grid is displayed or not
        '''
        # Put the text labels
        for i in range(0, len(self.xmarkers)):
            self.rotatedText(str(int(self.xmarkers[i])), 90, 8, self.xend-14, self.yzero-int((int(self.xmarkers[i])-self.yoffset)*self.yscale))

        for i in range(0, len(self.ymarkers)):
            self.rotatedText(str(int(self.ymarkers[i])), 90, 8, self.xzero-int((int(self.ymarkers[i])-self.xoffset)*self.xscale), self.yend-18)

        # Draw the grid if required
        if(grid == 'full'):
            # Draw the vertical lines
            for i in range(0, len(self.xmarkers)):
                self.y_tmp = self.yzero-int((int(self.xmarkers[i])-self.yoffset)*self.yscale)
                self.draw.line((self.axisend, self.y_tmp, self.xend-self.axisoffset, self.y_tmp), fill=0)
        if(grid == 'full' or grid == 'horizontal'):
            # Draw the horizontal lines
            for i in range(0, len(self.ymarkers)):
                self.x_tmp = self.xzero-int((int(self.ymarkers[i])-self.xoffset)*self.xscale)
                self.draw.line((self.x_tmp, self.yend-self.yaxisoffset, self.x_tmp, self.axisend), fill=0)

    def stringToPages(self, string, fontSize):
        '''
        Displays the string on the screen, wraps text where necessary
        INPUTS:
            string: string to display
        '''
        # Grab a font
        self.font_tmp = self.fontGrab(fontSize)
        self.stringFontSize = fontSize

        # Split the string into an array of words
        self.splitString = string.split()
        #logger.debug('Starting string: ' + str(self.splitString))

        # Array to hold pagewise data
        self.pageHold = []
        self.pageBuffer_tmp = []
        self.pageIndex = 0
        self.page = 0
        self.pageHeight = 238
        self.maxLines = self.roundTo(self.pageHeight/(fontSize+2), 1, down=True)
        logger.debug('Maxlines: ' + str(self.maxLines))

        # Array to hold linewise data
        self.hold_tmp = []
        index = 0
        self.string_tmp = ''

        # Fill the linewise data array
        for word in self.splitString:
            if(self.font_tmp.getsize(self.string_tmp + word + ' ')[0] < 176):
                self.string_tmp = self.string_tmp + word + ' ' 
            else:
                self.hold_tmp.append(self.string_tmp)
                self.string_tmp = word + ' '
    
        self.hold_tmp.append(self.string_tmp)

        #logger.debug('hold: ' + str(self.hold_tmp))

        # Fill the pagewise data array
        for line in self.hold_tmp:
            if(self.pageIndex < self.maxLines):
                self.pageBuffer_tmp.append(line)
            else:
                self.pageHold.append(self.pageBuffer_tmp)
                self.pageBuffer_tmp = []
                self.pageIndex = -1
            self.pageIndex = self.pageIndex + 1
        self.pageHold.append(self.pageBuffer_tmp)
    
        #logger.debug('pages: ' + str(self.pageHold))
        
        # Save total number of pages
        self.maxPages = len(self.pageHold)
        logger.debug('Max pages: ' + str(self.maxPages))

    def pagesToDisplay(self):
        '''
        Displays the pages on to the screen and displays the UI at bottom
        '''
        # Start with clean canvas    
        self.image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)
        self.draw = ImageDraw.Draw(self.image)        
        
        # Grab font
        self.font_tmp = self.fontGrab(self.stringFontSize)

        # Print to the display
        i = 0
        for line in self.pageHold[self.page]:
            self.draw.text((0, i*(self.stringFontSize+2)), line, font=self.font_tmp, fill=0)
            i = i+1

        # Grab a font
        self.fontUI_tmp = self.fontGrab(10)

        # Draw the options at the bottom        
        self.draw.text((0, self.yend-11), 'Page ' + str(self.page+1) + ' of ' + str(self.maxPages), font=self.fontUI_tmp, fill=0)

        self.display()


    def buttonPress(self, button):
        '''
        Will perform an action depending on the button pressed.
        INPUTS:
            button: the number of the button that was pressed
        ACTIONS:
            1: Moves back a page
            2: Currently unused
            3: Currently unused
            4: Moves forward a page
        '''
        self.startPage = self.page
        # Change page number depending on button press
        if(button == 1):
            self.page = self.page - 1        
        elif(button == 2):
            pass
        elif(button == 3):
            pass
        elif(button == 4):
            self.page = self.page + 1
        else:
            logger.error("ERROR: Button not valid: " + str(button))

        # Check that page is in valid range
        if(self.page < 0):
            self.page = 0
        if(self.page >= self.maxPages):
            self.page = self.maxPages-1

        logger.debug('Current page: ' + str(self.page+1))        

        # Display the new page
        if(self.startPage != self.page):
            self.pagesToDisplay()
