import datetime
import time

start_time = datetime.datetime.now()
print start_time

def runTimer(_start):
    start = _start
    while True:
        now = datetime.datetime.now()
        delta = now-start
        print delta
        time.sleep(10)

runTimer(start_time)