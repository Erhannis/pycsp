import threading as t
import multiprocessing as m
import time

def F():
    for i in range(5):
        print "Alive"
        time.sleep(1)


def X(t1):
    t1[0]= t.Thread(target=F)
    t1[0].daemon = False
    t1[0].start()

    t1[0].join()

x0 = [None]
x1 = m.Process(target=X, args=(x0,))
x1.start()
x1.join()
