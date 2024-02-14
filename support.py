import time


# a while loop that keeps executing a function for a period of time
def timed_loop(seconds, func):
    start = time.time()
    while(time.time() - start < seconds):
        func()
