# coding: utf-8
#! /usr/bin/python

# Basically, Due to GIL multithread without any IO operator is slower than single thread.
# 
# 两核心 Intel i5 Macbook上，两个程序用 python 2.7 解析执
# 行，理论上，在一个双核处理器上，t2应该比t1少用一半的时间，可是
# 实际上，t2居然比t1多用了一倍以上的时间，这是一种多么重的领悟。

from threading import Thread, _get_ident
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
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter(*[TOTAL * tid, TOTAL * (tid + 1)]))
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("Two Thread executor total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
