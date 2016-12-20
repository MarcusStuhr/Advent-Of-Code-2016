DATA_FILENAME = "data.txt"
MAX_IP = 2**32 - 1
ips = sorted([tuple(map(int, line.split('-'))) for line in open(DATA_FILENAME).read().split("\n")])
ips.append(tuple([MAX_IP + 1, MAX_IP + 2])) #dummy item for upper bounding

count_allowed = 0
prev_highest = -1
lowest_allowed = None

for lo_ip, hi_ip in ips:
    if lo_ip > prev_highest + 1:
        if lowest_allowed == None:
            lowest_allowed = lo_ip - 1
        count_allowed += lo_ip - prev_highest - 1
    prev_highest = max(prev_highest, hi_ip)

print(lowest_allowed if ips[0][0] == 0 else 0)
print(count_allowed)