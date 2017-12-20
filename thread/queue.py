import random
import queue
import threading
import time


class GoodGoatWorker(threading.Thread):
    """
        Worker perform works from queue until get None work
    """

    def __init__(self, iq):
        super().__init__()
        self.queue = iq

    def run(self):
        print("{} starts ...".format(threading.current_thread()))
        while True:
            # block until get items
            item = self.queue.get(block=True)
            if item is None:
                print("!!!!! {}. Good bye!".format(
                    threading.current_thread(), item))
                break
            print("{}: {} found work = {}".format(
                threading.active_count(), threading.current_thread(), item))
            self.do_work(seconds=item)
            self.queue.task_done()
            # print("! {} completed work = {}".format(
            #       threading.current_thread(), item))

    @staticmethod
    def do_work(seconds):
        time.sleep(seconds)


def perform_work_by_threads(working, number_of_threads):
    print("The work is {}.".format(working))
    work_rate = 0
    for work in working:
        work_rate += work
    print("WorkRate equals {}.".format(work_rate))
    q = queue.Queue()
    # create threads
    print("Threads are {}".format(number_of_threads))
    threads = []
    for y in range(number_of_threads):
        t = GoodGoatWorker(q)
        t.start()
        threads.append(t)

    # fill queue
    for work in working:
        q.put(work)

    print("Main Thread. Queue size is {}".format(q.qsize()))
    print("Main Thread. Waiting threads... ")
    q.join()
    print("Main Thread. Thank you Threads!! Queue size is {}".format(
        q.qsize()))

    # fill queue with None items to end Threads
    for y in range(number_of_threads):
        q.put(None)

    # wait threads to complete
    for t in threads:
        t.join()

    print("Bye Bye!!! ")


if __name__ == "__main__":
    # create work list
    random.seed()
    works = []
    for x in range(5):
        works.append(random.randrange(10))
    # perform work
    workers = [2, 5, 10]
    for wrs in workers:
        t0 = time.time()
        perform_work_by_threads(works, wrs)
        print("Time work is {}.".format(time.time() - t0))
        time.sleep(1)
        print("\n\n\n")
