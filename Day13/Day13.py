import heapq
from collections import defaultdict

FAVE_NUM = 1362
MAZE_SIZE = 40
WALL_CHAR = '#'
OPEN_CHAR = '.'
IMPOSSIBLE_COST = float('inf')

def f(x,y):
    return [OPEN_CHAR, WALL_CHAR][bin(x*x + 3*x + 2*x*y + y + y*y + FAVE_NUM)[2:].count('1') % 2]

def shortest_path(G, start, end):
    q = [(0, start, ())]
    visited = set()
    while q:
        (cost, v1, path) = heapq.heappop(q)
        if v1 not in visited:
            visited.add(v1)
            if v1 == end:
                return cost
            path = (v1, path)
            for (v2, cost2) in G[v1].items():
                if v2 not in visited:
                    heapq.heappush(q, (cost + cost2, v2, path))
    return IMPOSSIBLE_COST

edges = defaultdict(dict)
distinctCoordPairs = set()
M = [[f(x, y) for x in range(MAZE_SIZE)] for y in range(MAZE_SIZE)]

for x in range(MAZE_SIZE):
    for y in range(MAZE_SIZE):
        if x - 1 >= 0 and M[x - 1][y] == OPEN_CHAR:
            edges[(x, y)][(x - 1, y)] = 1
        if x + 1 < MAZE_SIZE and M[x + 1][y] == OPEN_CHAR:
            edges[(x, y)][(x + 1, y)] = 1
        if y - 1 >= 0 and M[x][y - 1] == OPEN_CHAR:
            edges[(x, y)][(x, y - 1)] = 1
        if y + 1 < MAZE_SIZE and M[x][y + 1] == OPEN_CHAR:
            edges[(x, y)][(x, y + 1)] = 1

for x in range(MAZE_SIZE):
    for y in range(MAZE_SIZE):
        d = shortest_path(edges, (1, 1), (x, y))
        if d <= 50:
            distinctCoordPairs.add((x, y))

print(shortest_path(edges, (1, 1), (39, 31))) #part 1 answer
print(len(distinctCoordPairs)) #part 2 answer