import time
import queue
import threading


def cpu_work(i):
    work_rate = pow(2, 26)
    print("{} : Work {} rate is {}".format(threading.current_thread(), i, work_rate))
    for z in range(work_rate):
        i += 1
    return i


def cpu_worker(external_queue):
    while True:
        item = external_queue.get()
        if item is None:
            break
        cpu_work(item)
        external_queue.task_done()


def perform_work_by_threads_(number_of_threads, works_as_list):
    print("Threads are ", number_of_threads)
    q = queue.Queue()
    for work in works_as_list:
        q.put(work)
    threads = []
    for x in range(number_of_threads):
        t = threading.Thread(target=cpu_worker, args=(q,))
        threads.append(t)
        t.start()
    q.join()
    for x in range(number_of_threads):
        q.put(None)
    for t in threads:
        t.join()


if __name__ == "__main__":
    works = [0, 1, 2, 3, 4, 5]
    # print("Main thread working...")
    # t_zero = time.time()
    # for w in works:
    #     t0 = time.time()
    #     ret = cpu_work(w)
    #     # print("Work {} with return {} spent {} secs.".format(w, ret, time.time() - t0))
    # print("Total Work spent {} secs.".format(time.time() - t_zero))

    threads_n = [4, 5, 6]
    for tn in threads_n:
        t0 = time.time()
        perform_work_by_threads_(tn, works)
        print("Total Work with threads spent {} secs.".format(time.time() - t0))

    print("Bye Bye!!!")
