MIN_IP = 0
MAX_IP = 2**32 - 1
lines = open("data.txt").read().split("\n")
ips = sorted(tuple(map(int, line.split('-'))) for line in lines if '-' in line)
ips.append((MAX_IP + 1, MAX_IP + 2))

count_allowed = 0
max_hi_ip_so_far = MIN_IP - 1
lowest_allowed = None

for lo_ip, hi_ip in ips:
    if lo_ip > max_hi_ip_so_far + 1:
        if lowest_allowed == None:
            lowest_allowed = max_hi_ip_so_far + 1
        count_allowed += lo_ip - max_hi_ip_so_far - 1
    max_hi_ip_so_far = max(max_hi_ip_so_far, hi_ip)

print(lowest_allowed)
print(count_allowed)
