#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, TimeoutError
import time
import os
import urllib2
import signal
import subprocess


if __name__ == '__main__':
    print 'Test to request deadLock HTTP dummyServer...'
    # pro = subprocess.Popen('python dummy_server.py', stdout=subprocess.PIPE, 
    pro = subprocess.Popen('yarn lift', stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
    time.sleep(1)
    print 'Lauched dummy-server...'
    pool = Pool(processes=4)
    results = []
    for i in range(0, 1):
        print 'Start to get!!'
        res = pool.apply_async(urllib2.urlopen, [
            'http://127.0.0.1:8088?deadLock=true'
        ])
        results.append(res)
    try:
        for obj in results:
            print 'Before start!'
            obj.get(timeout=3)  # test deal lock release
            print 'After requested!'
    except TimeoutError:
        print "We lacked patience and got a multiprocessing.TimeoutError"
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    except:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
        raise Exception('Other error, you should get a TimeoutError in this testcase!')
