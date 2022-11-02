import time


def timer(sec):
    while sec:
        minute, second = divmod(sec, 60)
        time_format = '{:02d}:{:02d}'.format(minute, second)
        print("\r" + time_format , end='')
        time.sleep(1)
        sec -= 1


