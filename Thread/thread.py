import threading
import time
from random import seed, randrange


class GoatWorker(threading.Thread):
    shared_data = 0

    def run(self):
        my_data = threading.local()
        my_data.seed = seed()
        my_data.r = randrange(1, 10)
        for y in range(10):
            self.shared_data += 1
            print("{} : {} : {} my choice is {}. Up is {}. Shared data is {}".
                  format(threading.active_count(), time.ctime(time.time()),
                         threading.current_thread(), my_data.r, y, self.shared_data))
            time.sleep(my_data.r)
        print("!!!!!! {} is ended.....".format(threading.current_thread()))


if __name__ == "__main__":
    print("Hi")
    for x in range(5):
        t = GoatWorker()
        t.start()
    for z in range(10):
        print("main function is working...")
        time.sleep(1)
