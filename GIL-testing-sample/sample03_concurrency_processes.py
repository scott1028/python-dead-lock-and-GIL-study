# coding: utf-8
#! /usr/bin/python

# Mutiprocess is the fastest one!!!

from multiprocessing import Process
from threading import _get_ident
import time


TOTAL = 100000000

def my_counter(begin=0, end=TOTAL):
    def run():
        print(_get_ident(), begin, end)
        i = 0
        for _ in range(begin, end):
            i = i + 1
        return True
    return run

def main():
    process_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Process(target=my_counter(*[TOTAL * tid, TOTAL * (tid + 1)]))
        t.start()
        process_array[tid] = t
    for i in range(2):
        process_array[i].join()
    end_time = time.time()
    print("Two Process executor total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
