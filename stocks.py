from eink import eink
import logging

import datetime

# Setup logging
logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
logger.addHandler(stream)

# Initialize the display
eink = eink()

# Define dates
start = datetime.datetime(2018, 1, 1)
end = datetime.date.today()

# Grab the data
