import threading
import time


class Goat(threading.Thread):
    def run(self):
        for x in range(2):
            print("Hello from {}".format(threading.current_thread()))
            time.sleep(5)


if __name__ == "__main__":
    print("Hi")
    for x in range(4):
        t = Goat()
        t.start()
