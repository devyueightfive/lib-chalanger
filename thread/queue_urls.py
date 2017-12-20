import urllib.request as request
import time

urls = ["lenta.ru", "stoloto.ru", "auto.ru",
        "tproger.ru", "pikabu.ru", "python.org"]


def some_work(url):
    name = url
    print(name)
    try:
        response = request.urlopen(r"http://" + url)
    except Exception as e:
        print("{} Error: {}".format(name,e))
        return

    file = "./output." + name
    f_out = open(file, "wb")
    f_out.write(response.read())
    f_out.close()


def sequence_of_works():
    for url in urls:
        some_work(url)


if __name__ == "__main__":
    t0 = time.time()
    print("{}: Sequence works ... ".format(
        time.ctime(t0)))
    sequence_of_works()
    print("{}: Sequence finished by {} secs.".format(
        time.ctime(t0), time.time() - t0))
    print("Bye Bye!!!")
