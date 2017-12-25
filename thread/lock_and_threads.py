import threading
import time
import queue


def remove_blanks(external_list):
    for x in external_list:
        if x == '':
            external_list.remove(x)
    return external_list


def worker(external_queue, file_path):
    # print("{} starts ...".format(threading.current_thread()))
    while True:
        item = external_queue.get()
        # print("{} found item".format(threading.current_thread()))
        if item is None:
            break
        f_out = open(file_path, "at")
        # print("{} opened file".format(threading.current_thread()))
        f_out.write(item + " ")
        # print("{} wrote in file".format(threading.current_thread()))
        f_out.close()
        external_queue.task_done()


def safe_worker(external_queue, file_path, external_lock):
    # print("{} starts ...".format(threading.current_thread()))
    while True:
        item = external_queue.get()
        # print("{} found item".format(threading.current_thread()))
        if item is None:
            break
        with external_lock:
            with open(file_path, "at") as f_out:
                # print("{} opened file".format(threading.current_thread()))
                f_out.write(item + " ")
                # print("{} wrote in file".format(threading.current_thread()))
            external_queue.task_done()


def perform_work_by_threads_with_no_lock(works_as_string, number_of_threads, file_path):
    works_as_list = works_as_string.split(sep=" ")
    print("Work rate is", len(works_as_list))
    print(sorted(works_as_list))
    q = queue.Queue()
    for work in works_as_list:
        q.put(work)
    threads = []
    for x in range(number_of_threads):
        t = threading.Thread(target=worker, args=(q, file_path,))
        threads.append(t)
        t.start()
    q.join()

    for x in range(number_of_threads):
        q.put(None)
    for t in threads:
        t.join()


def perform_work_by_threads_correctly(works_as_string, number_of_threads, file_path, external_lock):
    works_as_list = works_as_string.split(sep=" ")
    print("Work rate is", len(works_as_list))
    print(sorted(works_as_list))
    q = queue.Queue()
    for work in works_as_list:
        q.put(work)
    threads = []
    for x in range(number_of_threads):
        t = threading.Thread(target=safe_worker, args=(q, file_path, external_lock,))
        threads.append(t)
        t.start()
    q.join()

    for x in range(number_of_threads):
        q.put(None)
    for t in threads:
        t.join()


def check_file(file):
    print("Check:")
    with open(file, "r") as f_in:
        text = f_in.read()
        strings = text.split(sep=" ")
        strings = remove_blanks(strings)
        print("Strings in the file are ", len(strings))
        print(sorted(strings))


if __name__ == "__main__":
    locked_file = "./locked_file.output"
    number_of_workers = [2, 3, 5, 10, 20]
    works = "A primitive lock is a synchronization primitive " \
            "that is not owned by a particular thread when locked. " \
            "In Python, it is currently the lowest level synchronization " \
            "primitive available, implemented directly by the _thread " \
            "extension module."

    print("With no lock\n")
    for i in number_of_workers:
        # clean file
        with open(locked_file, "wt") as f:
            f.write("")
        print("Threads are ", i)
        t0 = time.time()
        perform_work_by_threads_with_no_lock(works, i, locked_file)
        print("Work time is {}".format(time.time() - t0))
        check_file(locked_file)
        print('\n')

    print("With Lock\n")
    my_lock = threading.Lock()

    for i in number_of_workers:
        # clean file
        with open(locked_file, "wt") as f:
            f.write("")
        print("Threads are ", i)
        t0 = time.time()
        perform_work_by_threads_correctly(works, i, locked_file, my_lock)
        print("Work time is {}".format(time.time() - t0))
        check_file(locked_file)
        print('\n')

    print("Bye Bye !!!")
