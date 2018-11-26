# eink
### Library to use the Waveshare 2.7" e-paper HAT for Raspberry Pi
This library allows you to create graphs and plots, display text on the screen, and draw shapes among other things.  A few libraries from Waveshare are included for the communication with the e-ink screen, and PIL is also required (see below).  There are a few demo files, `main.py` and `train.py`.

### Required Libraries
- PIL (*sudo apt-get install python-imaging*)

### Files
- *epd2in7* Library provided by Waveshare to interface with the eink display.  Required in the same folder as the eink class since it is a required dependecy used to draw the frame buffer.
- *epdif* The second library provided by Waveshare, also needs to be in the same folder as the eink class.
- *eink* A class which holds all of the custom methods to interface with the eink screen.  Each is detailed in the file with a comment directly under describing what the function does and what inputs are needed for it.  The various functions can write text to the screen in different justifications, draw boxes using center or corner coordinates, and also do the graphing and story page utilities.
- *mbta* A class which adds to the eink class with the information for the MBTA API.  This class uses the eink class to draw on the display.  The MBTA data is pulled from the real-time API using urlopen requests to an address.  An API key should be used to manage requests from the server.  
- *main* A program to test the graphing utilities of the eink class.  Shows many of the available functions to the user including the scatter plot, line graph, and bar graph.  Shows grid options such as full, horizontal and none.  Also shows how to label the axes and title the graph.
- *train* An example of the mbta class, grabbing data for an upcoming train at a given station.  Will pull the timing data and write to the display.
- *stringTest* An example of the story utility.  A string is pasted into this program to feed the screen, which is then divided up into lines and pages and placed on the screen.  The buttons are used to change the pages.
- *stops* A dictionary holding the station names and IDs for some popular MBTA stations.