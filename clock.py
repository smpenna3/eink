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
        current_time = dt.strftime(dt.now(), "%H:%M")
        self.eink.rotatedText(current_time, 90, 20, self.eink.xend/2, 20/2+10/2, fill=0)
        self.eink.display()
        time.sleep(5)


clock = clock()
