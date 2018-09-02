#! /usr/bin/python


from threading import Thread, _get_ident
import time


TOTAL=100000000

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
        t.join()
    end_time = time.time()
    print("Two Consecutive Single Thread executor total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
