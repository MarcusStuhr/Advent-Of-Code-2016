from math import log

"""
TODO: Code cleanup
"""

input_code = "00101000101111010"

def reverse_and_flip_bits(a):
    return ''.join('1' if x == '0' else '0' for x in a[::-1])

def exponent_pow_2(n):
    return int(log(n & (-n), 2))

def get_inverse_dragon_bitcount_parity(n):
    if n < 0 : return 0
    return ((n - bin(n ^ (n >> 1)).count('1')) >> 1) & 1

def cumulative_bitcount_parity(pos, L, a, b):
    if pos < 0: return 0
    m = pos // (2 * L + 2)
    index_chunk_start = m * (2 * L + 2)
    parity_ab_up_to_m = L * m % 2
    offset_within_chunk = pos - index_chunk_start
    dragon_index_so_far = 2 * m - 1
    parityA = a.count('1') % 2
    parityB = 0
    if 0 <= offset_within_chunk < L:
        parityA = a[:offset_within_chunk + 1].count('1') % 2
    if offset_within_chunk >= L:
        dragon_index_so_far += 1
    if offset_within_chunk == 2 * L + 2 - 1:
        dragon_index_so_far += 1
    if L < offset_within_chunk:
        parityB = b[:offset_within_chunk - L].count('1') % 2
    return (parity_ab_up_to_m + parityA + parityB + get_inverse_dragon_bitcount_parity(dragon_index_so_far + 1)) % 2

def get_checksum(a, disk_capacity):
    b = reverse_and_flip_bits(a)
    L = len(a)
    x = exponent_pow_2(disk_capacity)
    checksum = ""
    for k in range(disk_capacity//2**x):
        count_right = cumulative_bitcount_parity((k + 1) * (2 ** x) - 1, L, a, b)
        count_left = cumulative_bitcount_parity(k * (2 ** x) - 1, L, a, b)
        checksum += str(int(count_right - count_left % 2 == 0))
    return checksum

print(get_checksum(input_code, 272))
print(get_checksum(input_code, 35651584))