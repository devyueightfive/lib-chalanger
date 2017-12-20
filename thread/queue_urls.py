import urllib.request as request
import time
import queue
import threading

urls = ["lenta.ru", "stoloto.ru", "auto.ru",
        "tproger.ru", "pikabu.ru", "python.org"]
max_threads = 2


def some_work(url):
    name = url
    # print("Found work ", name)
    try:
        response = request.urlopen(r"http://" + url)
    except Exception as e:
        print("{}: {}".format(name, e))
        return

    file = "./output/" + name + ".txt"
    f_out = open(file, "wb")
    f_out.write(response.read())
    f_out.close()


def sequence_of_works():
    for url in urls:
        some_work(url)


class GoatWorker(threading.Thread):
    def __init__(self, q):
        super().__init__()
        self.queue = q

    def run(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            # print("{} found {}".format(threading.current_thread(), item))
            some_work(item)
            self.queue.task_done()


def work_by_threads(number_of_threads):
    print("Threads are ", number_of_threads)
    threads = []
    lq = queue.Queue()
    for u in urls:
        lq.put(u)
    for i in range(number_of_threads):
        t = GoatWorker(lq)
        threads.append(t)
        t.start()
    # print("Main thread. Waiting...")
    lq.join()
    for t in threads:
        lq.put(None)
    for t in threads:
        t.join()


if __name__ == "__main__":
    t0 = time.time()
    print("{}: Sequence works ... ".format(
        time.ctime(t0)))
    sequence_of_works()
    print("{}: Sequence finished by {} secs.".format(
        time.ctime(t0), time.time() - t0))
    print("\n" * 3)
    time.sleep(3)

    workers = [2, 3, 4]

    for worker in workers:
        t0 = time.time()
        work_by_threads(worker)
        print("{}: Threads finished by {} secs.".format(
            time.ctime(t0), time.time() - t0))
        print("\n" * 3)
        time.sleep(3)

    print("Bye Bye!!!")
