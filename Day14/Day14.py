from hashlib import md5
from itertools import count
from collections import deque, defaultdict
import re

SALT = "yjdafjpo"

def get_hash(salt, suffix_append, keystretch):
    """Computes a keystretched hash given an initial salt

    Args:
        salt: the initial string to be hashed
        suffix_append: integer to be appended (as string) to the salt
        keystretch: the number of keystretch iterations to be used
    """
    cur_hash = md5(str(salt + str(suffix_append)).encode()).hexdigest()
    for stretch_index in range(keystretch):
        cur_hash = md5(cur_hash.encode()).hexdigest()
    return cur_hash

def resolve_k_counts(counts, k, cur_hash, cur_index):
    """Updates the "counts" defaultdict with the cumulative counts of k-char
    streaks found up to the current index for all possible characters.

    Args:
        counts: the defaultdict containing the cumulative streak-counts
        k: the size of the streak (e.g. k = 4 can correspond to "aaaa", "3333", etc)
        cur_hash: the hash at cur_index which we want to check for k-streaks
        cur_index: the index of the hash, also the first key in the counts defaultdict
    """
    for ch_key in "0123456789abcdef":
        counts[cur_index][ch_key] = counts[cur_index - 1][ch_key] + (ch_key * k in cur_hash)

def find_index_one_time_pad_key(salt, pad_target = 64, peek_ahead = 1000, len_streak_1 = 3, len_streak_2 = 5, keystretch = 0):
    """Finds the index that corresponds to the target number of one-time-pad keys according to the AoC Day 14 description.

    Args:
        salt: the string to be hashed
        pad_target: the number of one-time-pad keys we wish to find
        peek_ahead: the number of future hashes we will check if we encounter a hash with a repetition of size len_streak_1
        len_streak_1: the size of a streak that will trigger the future-hash scan event
        len_streak_2: the size of the streak that must exist (using the trigger character) within the future hashes
        keystretch: the number of keystretch iterations to use during each hashing call
    """
    pads_found = 0
    #creates a rolling cache of hashes of size peek_ahead, allowing us to manage both ends quickly
    rolling_cache = deque([get_hash(salt, index, keystretch) for index in range(peek_ahead)])
    counts = defaultdict(lambda : defaultdict(int))

    #initialize the cumulative-count dict to keep track of how many times streaks have been seen over the cache
    for hash_index, cur_hash in enumerate(rolling_cache):
        resolve_k_counts(counts, len_streak_2, cur_hash, hash_index)

    for index in count(0):
        #the current hash is whatever is on the lower end of the cache
        cur_hash  = rolling_cache[0]
        #the peek hash is the final hash we would need to examine if cur_hash triggered a future-hash scan event
        peek_hash = get_hash(salt, index + peek_ahead, keystretch)
        rolling_cache.append(peek_hash)
        #update the counts dict with each new peek_hash we compute
        resolve_k_counts(counts, len_streak_2, peek_hash, index + peek_ahead)

        #searches for the first instance of a character repeating len_streak_1 times
        cur_rep = re.search(r"(\w){}".format("\\1" * (len_streak_1 - 1)), cur_hash)

        #if found, trigger the future-hash scan event
        if cur_rep:
            ch_key = cur_rep.group()[0]
            #if the cumulative counts of len_streak_2-streaks exceeds the count at the current index,
            #we found a one-time-pad key.
            if counts[index + peek_ahead][ch_key] > counts[index][ch_key]:
                pads_found += 1
                if (pads_found == pad_target):
                    return index

        del counts[index]
        rolling_cache.popleft()

print(find_index_one_time_pad_key(SALT))
print(find_index_one_time_pad_key(SALT, keystretch = 2016))
