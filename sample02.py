#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, TimeoutError
import time
import os

def handler(x):
    print time.time()
    while True:
        print time.time()
        time.sleep(1)
    return x*x

if __name__ == '__main__':
    raw_input('[{0}] Press to start...'.format(os.getpid()))
    pool = Pool(processes=4)
    results = []
    for i in range(0, 1):
        res = pool.apply_async(handler, (10,))
        results.append(res)
    try:
        for obj in results:
            obj.get(timeout=11)  # test deal lock release
    except TimeoutError:
        print "We lacked patience and got a multiprocessing.TimeoutError"
