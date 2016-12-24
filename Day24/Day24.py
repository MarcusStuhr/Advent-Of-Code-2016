from heapq import heappush, heappop

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heappush(self.elements, (priority, item))

    def get(self):
        return heappop(self.elements)[1]


def heuristic(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start_node, end_node, a_star_memo={}):
    memo_key = (start_node, end_node)
    if memo_key in a_star_memo:
        return a_star_memo[memo_key]

    frontier = PriorityQueue()
    frontier.put(start_node, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    while not frontier.empty():
        current = frontier.get()
        (r, c) = current
        if current == end_node:
            a_star_memo[memo_key] = cost_so_far[current]
            return a_star_memo[memo_key]
        for delta_r, delta_c in ((-1,0),(1,0),(0,-1),(0,1)):
            new_r, new_c = r + delta_r, c + delta_c
            if graph[new_r][new_c] != '#':
                next_state = (new_r, new_c)
                new_cost = cost_so_far[current] + 1
                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + heuristic(next_state, end_node)
                    frontier.put(next_state, priority)
                    came_from[next_state] = current

    a_star_memo[memo_key] = float('inf')
    return a_star_memo[memo_key]


def min_cost_circuit(graph, target_cells, start_node, already_visited, home_node=None, visit_memo={}):
    memo_key = (start_node, already_visited, home_node)
    if already_visited == (1 << len(target_cells)) - 1:
        if home_node != None:
            return a_star_search(graph, start_node, home_node)
        else:
            return 0
    if memo_key in visit_memo:
        return visit_memo[memo_key]

    min_cost = float('inf')
    for index, next_node in enumerate(target_cells.values()):
        if (already_visited & (1 << index)) == 0:
            min_cost_next = min_cost_circuit(graph, target_cells, next_node, already_visited | (1 << index), home_node)
            min_cost = min(min_cost, min_cost_next + a_star_search(graph, start_node, next_node))
    visit_memo[memo_key] = min_cost

    return visit_memo[memo_key]


DATA_FILENAME = "data.txt"
graph = open(DATA_FILENAME).read().split("\n")

target_cells = {}
for r in range(len(graph)):
    for c in range(len(graph[0])):
        if graph[r][c].isdigit():
            target_cells[int(graph[r][c])] = (r, c)

print(min_cost_circuit(graph, target_cells, target_cells[0], 1)) #part 1 answer
print(min_cost_circuit(graph, target_cells, target_cells[0], 1, target_cells[0])) #part 2 answer