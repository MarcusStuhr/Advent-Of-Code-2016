from math import log
from collections import deque
from time import clock

NUM_ELVES = 3014603

def josephus(n):
    return int(bin(n)[3:] + '1', 2)

def josephus_across(n):
    t = 3**int(log(n, 3))
    return n if n == t else max(n - t, 2*n - 3*t)

def josephus_slow(n):
    d = deque(range(1, n + 1))
    while len(d) > 1:
        d.rotate(-1)
        d.popleft()
    return d[0]

def josephus_across_slow(n):
    left_deque = deque(range(1, n//2 + 1))
    right_deque = deque(range(n//2 + 1, n + 1))
    while len(left_deque) + len(right_deque) > 1:
        right_deque.popleft()
        right_deque.append(left_deque.popleft())
        if len(left_deque) == len(right_deque) - 2:
            left_deque.append(right_deque.popleft())
    return right_deque[0]

t = clock()
print(josephus_slow(NUM_ELVES))
print(josephus_across_slow(NUM_ELVES))
print("Slow versions done in {} s".format(clock() - t))

t = clock()
print(josephus(NUM_ELVES))
print(josephus_across(NUM_ELVES))
print("Fast versions done in {} s".format(clock() - t))
