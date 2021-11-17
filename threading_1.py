import time
import threading
import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# 锁
l = threading.Lock()


def hello():
    global l
    if l.acquire(False):
        logging.info("hello, world")
        time.sleep(6)
        logging.info("End")
        l.release()


check_period = datetime.timedelta(seconds=1)

if __name__ == "__main__":
    now = datetime.datetime.now()
    # 开始和结束
    # start = datetime.datetime(year=now.year, month=now.month,
    #                           day=now.day, hour=16, minute=23)
    # end = datetime.datetime(year=now.year, month=now.month,
    #                         day=now.day, hour=16, minute=25)

    start = now
    end = now + datetime.timedelta(minutes=1)

    total = end-start
    # 执行间隔
    delta = datetime.timedelta(seconds=5)
    times = total//delta

    runs = []
    for i in range(times):
        runs.append(delta*i+start)

    def time_in_runs(t):
        for i in runs:
            if i <= t < i+check_period:
                return True
        return False

    while True:
        now = datetime.datetime.now()
        if(time_in_runs(now)):
            t = threading.Thread(target=hello, daemon=True)
            t.start()

        time.sleep(check_period.seconds)
