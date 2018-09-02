#! /usr/bin/python


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
        t.join()
    end_time = time.time()
    print("Two Consecutive Single Thread executor total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
