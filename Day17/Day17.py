import re
from hashlib import md5
from collections import deque

code = "qtetzkpl"

def get_moves(code, dirs):
    moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    cur_hash = md5((code + dirs).encode()).hexdigest()[:4]
    return [(move, moves[move]) for index, move in enumerate("UDLR") if cur_hash[index] in "bcdef"]

def bfs(code, start, end):
    grid_max_row, grid_max_col = end
    q = deque()
    q.append((start, ""))
    shortest_dirs = ""
    longest_dirs = ""
    while q:
        pos, dirs = q.popleft()
        if pos == end:
            if shortest_dirs == "":
                shortest_dirs = dirs
            if len(dirs) > len(longest_dirs):
                longest_dirs = dirs
            continue
        for move, (delta_r, delta_c) in get_moves(code, dirs):
            old_r, old_c = pos
            new_r, new_c = (old_r + delta_r, old_c + delta_c)
            new_pos = (new_r, new_c)
            new_dirs = dirs + move
            if 0 <= new_r <= grid_max_row and 0 <= new_c <= grid_max_col:
                q.append((new_pos, new_dirs))
    return shortest_dirs, longest_dirs

shortest_dirs, longest_dirs = bfs(code, (0, 0), (3, 3))
print(shortest_dirs)
print(len(longest_dirs))