import time
import multiprocessing as mp


def cpu_work(i):
    work_rate = pow(2, 26)
    print("{} : Work {} rate is {}".format(mp.current_process(), i, work_rate))
    for z in range(work_rate):
        i += 1
    return i


def cpu_worker(external_joinable_queue):
    while True:
        item = external_joinable_queue.get()
        if item is None:
            break
        cpu_work(item)
        external_joinable_queue.task_done()


def perform_work_by_processes(number_of_processes, works_as_list):
    print("Processes are ", number_of_processes)
    q = mp.JoinableQueue()
    for work in works_as_list:
        q.put(work)
    processes = []
    for x in range(number_of_processes):
        p = mp.Process(target=cpu_worker, args=(q,))
        processes.append(p)
        p.start()
    q.join()
    for x in range(number_of_processes):
        q.put(None)
    for t in processes:
        t.join()


if __name__ == "__main__":
    works = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    print("Main thread working...")
    t_zero = time.time()
    for w in works:
        t0 = time.time()
        ret = cpu_work(w)
        # print("Work {} with return {} spent {} secs.".format(w, ret, time.time() - t0))
    print("Total Work spent {} secs.".format(time.time() - t_zero))

    numbers_of_processes = [2, 3, 4, 5, 6]
    for n in numbers_of_processes:
        t0 = time.time()
        perform_work_by_processes(n, works)
        print("Total Work with processes spent {} secs.".format(time.time() - t0))

    print("Bye Bye!!!")
