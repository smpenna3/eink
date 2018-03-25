from eink import eink
from mbta import mbta
import logging

# Setup logging
logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
logger.addHandler(stream)

# Setup mbta object with desired station
mbta = mbta(stop='Charles')
#mbta.nearStations()

# Find the arrivals to the specified station
a =mbta.arrivalToDelta(mbta.predictionsFromStop())

# Display the times on the e-paper screen
mbta.timesToDisplay(a)
