import threading

threads = []
n = 0


def foo():
    global n
    n += 1


if __name__ == "__main__":
    for i in range(100):
        t = threading.Thread(target=foo)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(n)
