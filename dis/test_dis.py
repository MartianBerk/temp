import dis

m = 0
n = 0


def bar():
    global m
    m += 1


def foo():
    global n
    n += 1
    bar()


dis.dis(foo)
