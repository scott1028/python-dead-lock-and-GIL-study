# coding: utf-8
#! /usr/bin/python

# Basically, Due to GIL multithread without any IO operator is slower than single thread.
# 
# Multithread 再存在 IO 等待的時候才會有明顯的加速效果, 
# 如果是 Always busy thread 不如用 MultiProcess!!

from threading import Thread, _get_ident
import time


TOTAL = 5

def my_counter(delay=TOTAL):
    def run():
        print(_get_ident(), TOTAL)
        time.sleep(TOTAL)
    return run

def main():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter(TOTAL))
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("Two Thread executor total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
