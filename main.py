from eink import eink
import logging

# Setup logging
logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
logger.addHandler(stream)

# Initialize the display
eink = eink()

# Make some fake data and graph it
x = [0, 10, 20, 30, 40, 50, 60, 70]
y = [0, 05, 30, 05, 15, 40, 10, 50]

#eink.scatter(5, x, y, grid='full')
#eink.display()

#eink.linePlot(x, y, points=True, grid='horizontal')
#eink.display()

eink.barPlot(x, y, grid='horizontal')

# Add the axes with titles and the graph title
eink.axes('time (s)', 'temperature (F)')
eink.title('Temp vs Time')

# Draw to the display
eink.display()
