import re
import heapq
from itertools import combinations

def assess_node_viability(nodes, empty_node_pos):
    num_viable = 0
    unviable_nodes = set()
    for node1_pos, node2_pos in combinations(nodes, 2):
        (used1, avail1), (used2, avail2) = nodes[node1_pos], nodes[node2_pos]
        if (used1 > 0 and used1 <= avail2) or (used2 > 0 and used2 <= avail1):
            if node1_pos != empty_node_pos and node2_pos != empty_node_pos:
                raise Exception("The empty node must be part of each viable pair.")
            num_viable += 1
        elif node1_pos == empty_node_pos:
            unviable_nodes.add(node2_pos)
        elif node2_pos == empty_node_pos:
            unviable_nodes.add(node1_pos)
    return num_viable, unviable_nodes

def print_grid(max_x, max_y, empty_node_pos, unviable_nodes):
    for y in range(0, max_y + 1):
        row = ""
        for x in range(0, max_x + 1):
            if (x, y) == (0, 0):
                row += "(.)"
            elif (x, y) == empty_node_pos:
                row += " _ "
            elif (x, y) == (max_x, 0):
                row += " G "
            elif (x, y) in unviable_nodes:
                row += " # "
            else:
                row += " . "
        print(row)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(unviable_nodes, end_pos, initial_target_node_pos, initial_empty_node_pos, max_x, max_y):
    frontier = PriorityQueue()
    start = (initial_empty_node_pos, initial_target_node_pos)
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    final_end_state = None

    while not frontier.empty():
        current = frontier.get()
        (empty_node_pos, target_node_pos) = current

        if target_node_pos == end_pos:
            final_end_state = current
            break

        for delta_x, delta_y in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            cur_x, cur_y = empty_node_pos
            new_x, new_y = cur_x + delta_x, cur_y + delta_y
            if (not ((0 <= new_x <= max_x) and (0 <= new_y <= max_y))) or (new_x, new_y) in unviable_nodes:
                continue

            new_empty_node_pos = (new_x, new_y)
            new_target_node_pos = target_node_pos
            if (new_empty_node_pos == new_target_node_pos):
                new_target_node_pos = empty_node_pos
            next = (new_empty_node_pos, new_target_node_pos)
            new_cost = cost_so_far[current] + 1

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(new_target_node_pos, end_pos) + heuristic(new_target_node_pos, new_empty_node_pos)
                frontier.put(next, priority)
                came_from[next] = current

    return cost_so_far[final_end_state]


lines = open("data.txt").read().split("\n")
max_x, max_y = -1, -1
nodes = {}
empty_node_pos = None

min_size = float('inf')
for line in lines:
    if line.startswith("/dev/grid/node"):
        x, y, size, used, avail, use_percentage = map(int, re.findall("([\d]+)", line))
        min_size = min(min_size, size)
        nodes[(x, y)] = (used, avail)
        if used == 0 and empty_node_pos != None:
            raise Exception("Only one empty node allowed.")
        if used == 0:
            empty_node_pos = (x, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

num_viable, unviable_nodes = assess_node_viability(nodes, empty_node_pos)
max_used = max(nodes[(x, y)][0] for x in range(max_x + 1) for y in range(max_y + 1) if (x, y) not in unviable_nodes)
if max_used > min_size:
    raise Exception("The smallest node size must exceed the largest node usage for viable nodes.")

print(num_viable) #part 1 answer
print(a_star_search(unviable_nodes, (0, 0), (max_x, 0), empty_node_pos, max_x, max_y)) #part 2 answer
print_grid(max_x, max_y, empty_node_pos, unviable_nodes)