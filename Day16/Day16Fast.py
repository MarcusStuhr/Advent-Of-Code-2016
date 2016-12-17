"""
TODO: Code cleanup
"""

input_code = "00101000101111010"

def flip_bits(a):
    return ''.join('1' if x == '0' else '0' for x in a)

def reverse_and_flip_bits(a):
    return flip_bits(a)[::-1]

def largest_pow_2_dividing(n):
    return n & (~n + 1)

def get_inverse_dragon_bitcount_parity(n):
    return ((n - bin(n ^ (n >> 1)).count('1')) >> 1) & 1

def construct_counts_raw_bitstring(a):
    counts = [0]*(len(a) + 1)
    for i in range(1, len(a) + 1):
        counts[i] = counts[i-1] + (a[i - 1] == '1')
    return counts

def cumulative_bitcount_parity_expanded(pos, len_a, counts_a, counts_b):
    if pos < 0: return 0
    m = pos // (2 * len_a + 2)
    index_chunk_start = m * (2 * len_a + 2)
    offset_within_chunk = pos - index_chunk_start
    dragon_index_so_far = 2 * m - 1 + (offset_within_chunk >= len_a) + (offset_within_chunk == 2 * len_a + 2 - 1)
    parity_a = counts_a[min(len_a, offset_within_chunk + 1)] & 1
    parity_b = counts_b[min(len_a, max(0, offset_within_chunk - len_a))] & 1
    return (len_a * m + parity_a + parity_b + get_inverse_dragon_bitcount_parity(dragon_index_so_far + 1)) & 1

def get_checksum(a, disk_capacity):
    counts_a, counts_b = construct_counts_raw_bitstring(a), construct_counts_raw_bitstring(reverse_and_flip_bits(a))
    x = largest_pow_2_dividing(disk_capacity)
    checksum = ""
    for k in range(disk_capacity // x):
        count_right = cumulative_bitcount_parity_expanded((k + 1) * x - 1, len(a), counts_a, counts_b)
        count_left = cumulative_bitcount_parity_expanded(k * x - 1, len(a), counts_a, counts_b)
        checksum += str(int((count_right - count_left) & 1 == 0))
    return checksum if disk_capacity & 1 == 0 else flip_bits(checksum)

print(get_checksum(input_code, 272))
print(get_checksum(input_code, 35651584))