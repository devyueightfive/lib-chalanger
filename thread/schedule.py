import sched
import random
import time
import threading

max_work_time = 1
max_works = 10


def do_work(name):
    print("{} performs ...".format(name))
    time.sleep(max_work_time)
    print("!!! {} completed.".format(name))


class TimeWorker(threading.Thread):
    def __init__(self, max_time):
        super().__init__()
        self.max_time = max_time

    def run(self):
        for z in range(self.max_time):
            print("{} sec".format(z))
            time.sleep(1)


if __name__ == "__main__":
    # create work list
    random.seed()
    delays = {}
    max_delay = 0
    for x in range(max_works):
        delays[x] = random.randrange(5)
        if max_delay < delays[x]:
            max_delay = delays[x]
    print("Random delays (name:delay) format: ", delays)
    print("Max delay is {}".format(max_delay))
    print("Work time is", max_work_time)
    import operator

    sort_dict = sorted(delays.items(), key=operator.itemgetter(1))
    print("Sorted delays (name:delay) format: ", dict(sort_dict))
    # create scheduler with delay_func == time.sleep
    s = sched.scheduler(time.time, time.sleep)
    for number, delay in delays.items():
        s.enter(delay, 1, do_work, argument=(number,))
    print("Scheduler queue: ", s.queue)

    # time_worker
    t = TimeWorker(max_delay + max_works * max_work_time)
    t.start()

    # block till schedule performs
    s.run()
    print("Scheduler completed. Thank you for your attention.")

    # block till time_worker complete
    t.join()
    print("Bye Bye!!!")
