from collections import Counter

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")
LINE_LEN = len(lines[0])
counters = [Counter(line[i] for line in lines) for i in range(LINE_LEN)]
print(''.join(c.most_common()[0][0] for c in counters)) #part 1 answer
print(''.join(c.most_common()[-1][0] for c in counters)) #part 2 answer