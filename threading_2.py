from threading import Timer, Lock
from time import sleep

l = Lock()


def hello():
    global l
    if l.acquire(False):
        print("hello, world")
        sleep(6)
        print("End")
        l.release()


t = Timer(0, hello)
t.start()

t = Timer(5, hello)
t.start()
