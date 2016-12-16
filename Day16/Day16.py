def get_checksum(disk):
    checksum = disk
    while True:
        checksum = ''.join(['0', '1'][checksum[i] == checksum[i + 1]] for i in range(0, len(checksum), 2))
        if len(checksum) % 2 == 1:
            return checksum

def fill_disk(state, disk_size):
    while len(state) < disk_size:
        state = state + '0' + ''.join(['0', '1'][x == '0'] for x in state[::-1])
    return state[:disk_size]

state = "00101000101111010"
print(get_checksum(fill_disk(state, 272))) #part 1 answer
print(get_checksum(fill_disk(state, 35651584))) #part 2 answer