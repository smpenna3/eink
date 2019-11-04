from eink import eink
from datetime import datetime as dt
import time

## Scheduler setup
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(timezone="America/New_York", \
								coalescing=True, misfire_grace_time=20)

class clock:
    def __init__(self):
        self.eink = eink()

        self.update_time()

        
    def update_time(self):
        time = dt.stftime(dt.now(), "%H:%M")

        self.eink.rotatedText(time, 90, 20, self.eink.xend/2, self.title_fontSize/2+self.spacingTop/2, fill=0)
		