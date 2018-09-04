# coding: utf-8
#! /usr/bin/python

# Ref: https://docs.python.org/3/library/timeit.html

from threading import Thread, _get_ident
import time
import timeit
import os


CODE = 'for n in range(200 * 50000): n += 1'
DELAY = 3

def tSleep(code=CODE):
    exec(code)

def my_counter(code=CODE, delay=None):
    def run():
        print(_get_ident(), CODE)
        tSleep(CODE)
    if delay != None:
        # time.sleep 不佔用 CPU 資源可以 delay 此 Thread 去 Acquire GIL, 即另一個 Thread 可以完全使用 CPU 資源
        # 即接下來每一個 sys.getcheckinterval() 都是由其餘的 Thread 獲得!
        # 
        # ( 每一個 PyThread, 每 checkinterval code frame 將競爭一次 GIL 才能做事情 )
        # 所以如果非 IO 或 Time Sleep 等待就會持續競爭導致 Python MultiThread 效能變差
        # 
        # Note: 將 getcheckinterval 調大可以讓 GIL 次數減少增加效能！
        return lambda: time.sleep(delay)
    return run

def main1(delay=None):
    print 'GIL Alternate Multi Thread'
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter(CODE, delay))
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("Two Thread executor total time: {}".format(end_time - start_time))
    return end_time - start_time

def main2(delay=None):
    print 'Consecutive Single Thread'
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter(CODE, delay))
        t.start()
        t.join()
    end_time = time.time()
    print("One Thread executor twice total time: {}".format(end_time - start_time))    
    return end_time - start_time

if __name__ == '__main__':
    raw_input('This pid is %s. You can type `strace -p %s` to trace system call!!' % (os.getpid(), os.getpid()))
    print '[TestCase - Python Base Code Block Busy]'
    print timeit.timeit(CODE, number=1)  # estimate time for special python code
    t1 = main1()
    print
    t2 = main2()
    assert t1 > t2
    print 'Pure Python Code Busy Block can not swith GIL!! so multi thread become slower!'
    
    print

    print '[TestCase - System Call Base Code Block Busy]'
    t1 = main1(DELAY)
    print
    t2 = main2(DELAY)
    assert t2 > t1
    print 'Use time.sleep to save time when GIL switched'
