from hashlib import md5
from itertools import count
from collections import deque, defaultdict
import re

SALT = "yjdafjpo"

def get_hash(salt, index, num_keystretch_iterations):
    hash = md5(str(salt + str(index)).encode()).hexdigest()
    for stretch_index in range(num_keystretch_iterations):
        hash = md5(hash.encode()).hexdigest()
    return hash

def resolve_k_counts(counts, k, hash, index):
    for ch_key in "0123456789abcdef":
        counts[index][ch_key] = counts[index - 1][ch_key] + (ch_key * k in hash)

def find_index_one_time_pad_key(salt, target_pad_key_count, num_peek_ahead, num_reps_first, num_reps_second, num_keystretch_iterations = 0):
    pads_found = 0
    rolling_cache = deque([get_hash(salt, index, num_keystretch_iterations) for index in range(num_peek_ahead)])
    counts = defaultdict(lambda : defaultdict(int))
    for hash_index, hash in enumerate(rolling_cache):
        resolve_k_counts(counts, num_reps_second, hash, hash_index)
    for index in count(0):
        hash  = rolling_cache[0]
        peek_hash = get_hash(salt, index + num_peek_ahead, num_keystretch_iterations)
        rolling_cache.append(peek_hash)
        resolve_k_counts(counts, num_reps_second, peek_hash, index + num_peek_ahead)
        cur_rep = re.search(r"(\w){}".format("\\1" * (num_reps_first - 1)), hash)
        if cur_rep:
            ch_key = cur_rep.group()[0]
            if counts[index + num_peek_ahead][ch_key] > counts[index][ch_key]:
                pads_found += 1
                if (pads_found == target_pad_key_count):
                    return index
        del counts[index]
        rolling_cache.popleft()

target_pad_key_count = 64
num_peek_ahead = 1000
num_reps_first, num_reps_second = 3, 5
num_keystretch_iterations = 2016

print(find_index_one_time_pad_key(SALT, target_pad_key_count, num_peek_ahead, num_reps_first, num_reps_second))
print(find_index_one_time_pad_key(SALT, target_pad_key_count, num_peek_ahead, num_reps_first, num_reps_second, num_keystretch_iterations))
