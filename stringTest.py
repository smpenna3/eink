from eink import eink
import logging
import RPi.GPIO as gpio
import time

# Setup GPIO
gpio.setmode(gpio.BCM)
gpio.setup(5, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(13, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(19, gpio.IN, pull_up_down=gpio.PUD_UP)

# Setup logging
logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
logger.addHandler(stream)

eink = eink()

string = 'hello world this is a test of the string printing to the display to be able to do things.  Hi Devendra, how are you?  Still doing nothing I see. Good for you.  I need this string to be longer so I can test the overflow of the display and also see how many lines I can fit on here before it reaches the bottom where I want the interface controls to be.  I hope this small addition will get it onto another page so we can test that functionality.  I need this string to be way longer to get onto the third page since this is only one page and quite a lot of text.  I should find a way to pull text from some online source so that I can always have it on here.  Maybe it can cache it in some files, and the right and left middle buttons will switch between the files which are different stories.  It can be like that short story thing in the pru except on the epaper display.  I think this should reach a third page, and maybe even a fourth.'
eink.stringToPages(string, 10)
eink.pagesToDisplay()


while True:
	key1 = gpio.input(5)
	key2 = gpio.input(6)
	key3 = gpio.input(13)
	key4 = gpio.input(19)

	if(key1 == False):
		logger.info('Key 1 pressed')
		time.sleep(0.2)
		eink.buttonPress(1)
	if(key2 == False):
		logger.info('Key 2 pressed')
		time.sleep(0.2)
		eink.buttonPress(2)
	if(key3 == False):
		logger.info('Key 3 pressed')
		time.sleep(0.2)
		eink.buttonPress(3)
	if(key4 == False):
		logger.info('Key 4 pressed')
		time.sleep(0.2)
		eink.buttonPress(4)
