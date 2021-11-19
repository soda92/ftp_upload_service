import model_rw
import datetime
import threading
import logging
import sys
import time
import model_upload
from model_timer import check_time

logging.basicConfig(level=logging.INFO, filename="log.txt",
                    format='%(asctime)s %(levelname)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


# 锁
lock = threading.Lock()

config = ""


def do_upload():
    global lock, config
    if lock.acquire(False):
        logging.info("starting..")
        cost = model_upload.upload_using_config(config=config)
        logging.info(f"finished, time elasped: {cost:.2f} sec")
        lock.release()
    else:
        logging.warning("trying to start but task still running")


check_period = datetime.timedelta(seconds=30)

if __name__ == "__main__":
    if not model_rw.exists():
        logging.info("creating example config")
        model_rw.create_example()
        sys.exit(0)

    config = model_rw.read_conf()

    while True:
        now = datetime.datetime.now()
        if(check_time(config=config, time=now, check_period=check_period)):
            t = threading.Thread(target=do_upload, daemon=True)
            t.start()

        time.sleep(check_period.seconds)
