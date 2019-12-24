import random
from matplotlib import pyplot
import numpy

def create_random_list(num):
    x = list()
    for i in range(num):
        x.append(random.randrange(0, 500))
    return x


def fifo(now, x):
    y = list()
    for i in range(len(x)):
        if (i is 0):
            y.append(abs(x[i] - now))
        else:
            y.append(abs(x[i] - x[i - 1]))

    # print("FIFO调度算法：")
    # print("下列请求序列等待访问磁盘：")
    # print(x)
    # print("从", str(now), "出发")
    # for i in range(len(x)):
    #     print(str(x[i]), str(y[i]))
    # print("平均寻道长度：", str(avg(y)))
    return avg(y)


def sstf(now, x):
    y = x.copy()
    next = list()
    move = list()
    index, min = near(now, y)
    next.append(y[index])
    move.append(min)
    y.pop(index)
    for i in range(len(y)):
        if (i is 0):
            continue
        index, min = near(next[i - 1], y)
        next.append(y[index])
        move.append(min)
        y.pop(index)
    # print("SSTF调度算法：")
    # print("下列请求序列等待访问磁盘：")
    # print("从", str(now), "出发")
    # for i in range(len(next)):
    #     print(next[i], move[i])
    # print("平均寻道长度：", str(avg(move)))
    return avg(move)


def scan(now, x, direction):
    above = list()
    below = list()
    equ = list()
    next = list()
    move = list()
    for i in range(len(x)):
        if (x[i] < now):
            below.append(x[i])
        elif (x[i] > now):
            above.append(x[i])
        else:
            equ.append(x[i])
    below.sort(reverse=True)
    above.sort()
    for i in range(len(equ)):
        next.append(now)
        move.append(0)
    if (direction is 'up'):
        for i in range(len(above)):
            next.append(above[i])
            if (i is 0):
                move.append(abs(now - above[i]))
            else:
                move.append(abs(next[i] - next[i - 1]))
        for i in range(len(below)):
            next.append(below[i])
            move.append(abs(next[i + len(above)] - next[i + len(above) - 1]))
    elif (direction is 'down'):
        for i in range(len(below)):
            next.append(below[i])
            if (i is 0):
                move.append(abs(now - below[i]))
            else:
                move.append(abs(next[i] - next[i - 1]))
        for i in range(len(above)):
            next.append(above[i])
            move.append(abs(next[i + len(below)] - next[i + len(below) - 1]))
    sum = 0
    for i in range(len(move)):
        sum += move[i]
    # print("SCAN调度算法：")
    # print("下列请求序列等待访问磁盘：")
    # print("从", str(now), "出发")
    # for i in range(len(next)):
    #     print(next[i], move[i])
    # print("平均寻道长度：", sum / len(x))
    return sum / len(x)


def cscan(now, x, direction):
    above = list()
    below = list()
    equ = list()
    next = list()
    move = list()
    for i in range(len(x)):
        if (x[i] < now):
            below.append(x[i])
        elif (x[i] > now):
            above.append(x[i])
        else:
            equ.append(x[i])
    for i in range(len(equ)):
        next.append(now)
        move.append(0)
    if (direction is 'up'):
        below.sort()
        above.sort()
        for i in range(len(above)):
            next.append(above[i])
            if (i is 0):
                move.append(abs(now - above[i]))
            else:
                move.append(abs(next[i] - next[i - 1]))
        for i in range(len(below)):
            next.append(below[i])
            move.append(abs(next[i + len(above)] - next[i + len(above) - 1]))
    elif (direction is 'down'):
        below.sort(reverse=True)
        above.sort(reverse=True)
        for i in range(len(below)):
            next.append(below[i])
            if (i is 0):
                move.append(abs(now - below[i]))
            else:
                move.append(abs(next[i] - next[i - 1]))
        for i in range(len(above)):
            next.append(above[i])
            move.append(abs(next[i + len(below)] - next[i + len(below) - 1]))
    # print("CSCAN调度算法：")
    # print("下列请求序列等待访问磁盘：")
    # print("从", str(now), "出发")
    # for i in range(len(next)):
    #     print(next[i], move[i])
    sum = 0
    for i in range(len(move)):
        sum += move[i]
    # print("平均寻道长度：", sum / len(x))
    return sum / len(x)


def avg(y):
    sum = 0
    for i in range(len(y)):
        sum += y[i]
    return sum / len(y)


def near(x, list):
    min = abs(x - list[0])
    index = 0
    for i in range(len(list)):
        if (min > abs(list[i] - x)):
            min = abs(list[i] - x)
            index = i
    return index, min


a = list()
b = list()
c1 = list()
c2 = list()
d1 = list()
d2 = list()
for i in range(1000):
    x = create_random_list(50)
    # a.append(fifo(400, x))
    b.append(sstf(500, x))
    c1.append(scan(500, x, 'down'))
    # c2.append(scan(50, x, 'down'))
    d1.append(cscan(500, x, 'down'))
    # d2.append(cscan(50, x, 'down'))
# print(avg(a), avg(b), avg(c1), avg(c2), avg(d1), avg(d2))
x = numpy.arange(0,1000)
# pyplot.plot(x,a,color='deeppink',label='fifo')
pyplot.plot(x,b,color='darkblue',label='sstf',alpha=0.5)
pyplot.plot(x,c1,color='black',label='scan',alpha=0.3)
pyplot.plot(x,d1,color='green',label='cscan',alpha=0.4)
pyplot.legend(loc=2)
pyplot.title("T=500 M=50 StartAt500")
pyplot.savefig("001.png")
pyplot.show()
