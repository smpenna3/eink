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

string = " A few words of advice for anyone who finds themselves in the same situation I once did.  Do not delete your parents.  They might nag and bicker and drive you nuts, and you might think you're better off without them -- the temptation to erase them might linger on your finger each day like a bad itch, but don't scratch it. Once they're gone, you won't be able to retrieve them from the recycling bin. It doesn't work like that. And trust me, that nagging, bickering and everything else you couldn't stand just the other day, well, suddenly you'll miss it. You'll long for it more than anything else in the world.  Or maybe you won't.  Try archiving the bad memories. You can check them occasionally, sure. But put the good memories some place real obvious, like your desktop. You'll catch yourself smiling more often than you'd think.  Do not overdo copy and paste. Pizza is great one day, and yes, it's still great the next... Hell, I could enjoy it every day for an entire month. But the time will come when you're so sick of cheese and that same crusty base, that you'll actually want a salad. Trust me on that. And no, salad everyday doesn't work either. Variation isn't just the spice of life, it is life. So don't sit there playing games all day everyday. Go for a walk once in a while.  Create a shortcut here or there. I do it myself from time to time. But sometimes, please, take the long route -- even if it means getting lost occasionally. You might think that it sounds like a waste of time, but that's the thing about getting lost: it takes you somewhere new, and that's rarely a waste of anything.  Don't undo. Make mistakes. You learn best from them. So don't regret them too much, and don't try to undo them.  Send to a friend. Anything that's bothering you. That's what they're there for. A burden shared may not be a burden halved, but it helps. Send something that you're proud of to your best friend. Share it now. Go on, I'll wait. They will want to hear about it, because if they're your friend, they'll be happy for you. They'll want you to succeed. Don't zip it all up -- there's only so much storage space inside you.  Open a window occasionally. That one should go without saying.  Sort. I don't care how you sort -- name, date, whatever -- just sort. Organise your room, your school work, your social calendar. Stress can sweep you away when what seems like a thousand problems lurk on your mind's horizon; they will come in close at 3am, when you're desperate to sleep, spinning like a tempest of knives. So write them all down. All the things on your mind. They won't seem as many or as bad when you can hold them on a single sheet of paper.  Don't delete your parents. Yes, I know I've already said it, but it's worth saying another time. Don't delete your parents.  You'll miss them."

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
