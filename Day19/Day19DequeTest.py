from collections import deque

NUM_ELVES = 3014603

#The "slow" implementations, O(n) time and memory

def josephus_slow(n):
    d = deque(range(1, n + 1))
    while len(d) > 1:
        d.rotate(-1)
        d.popleft()
    return d.pop()

def josephus_across_slow(n):
    d = deque(range(1, n + 1))
    d.rotate(-(n//2))
    while len(d) > 1:
        d.popleft()
        d.rotate(2*(n//2) - 1)
        n-=1
    return d.pop()

print(josephus_slow(NUM_ELVES))
print(josephus_across_slow(NUM_ELVES))