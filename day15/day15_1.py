from collections import defaultdict, deque
from subprocess import Popen, PIPE

def shortest_path_to_oxygen(G, oxygen_location):
    visited = set()
    queue = deque([(0, 0)])
    distances = {(0, 0): 0}

    # perform BFS and track distances until we reach the oxygen system
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            parent_distance = distances[node]

            for child in G[node]:
                if child not in visited:
                    queue.append(child)
                    if child == oxygen_location:
                        return parent_distance + 1
                    distances[child] = parent_distance + 1

def send_move(droid, move):
    """Send a movement command to the droid.
    1: north
    2: south
    3: west
    4: east
    """
    move = str(move) + '\n'
    droid.stdin.write(move.encode())
    droid.stdin.flush()

def get_status_code(droid):
    """Get the latest status code from the droid.
    0: the droid hit a wall
    1: the droid has moved one step in the requested direction
    2: the droid has moved one step in the requested direction, and has located
       the oxygen system
    """
    status_code = int(droid.stdout.readline().decode().rstrip())
    return status_code


def run_droid(program):
    """Continuously run the droid program until all cells in the grid have been
    visited.
    """
    droid = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program),
                  shell=True,
                  stdin=PIPE,
                  stdout=PIPE)
    x = y = 0
    graph = defaultdict(list)
    MOVES = {1: (0, 1),  # north
             2: (0, -1), # south
             3: (-1, 0), # west
             4: (1, 0)}  # east
    stack = [] # holds backtracking directions

    # tracks whether a given cell has tried to visit cells to the:
    # North, South, West, East
    tried_directions = defaultdict(lambda:[False, False, False, False])

    while droid.poll() is None:
        # try to get the next unexplored direction
        try:
            next_direction = tried_directions[(x, y)].index(False) + 1
        # if all surrounding cells have been visited
        except ValueError:
            # if all cells in the grid have been visited
            if not stack:
                droid.kill()
                break
            # move back in the opposite direction of the latest movement command
            backtrack_direction = stack.pop()
            x = x + MOVES[backtrack_direction][0]
            y = y + MOVES[backtrack_direction][1]
            send_move(droid, backtrack_direction)
            get_status_code(droid) # ignore status code (which will always be a 1)
            continue

        # try to move in the next unexplored direction
        tried_directions[(x, y)][next_direction - 1] = True
        send_move(droid, next_direction)
        next_x = x + MOVES[next_direction][0]
        next_y = y + MOVES[next_direction][1]

        status_code = get_status_code(droid)
        if status_code == 0:
            # if the droid wasn't able to move, try the next direction
            continue
        elif status_code == 2:
            # if the oxygen system has been located, save its location
            oxygen_location = (next_x, next_y)

        # build graph
        graph[(x, y)].append((next_x, next_y))
        graph[(next_x, next_y)].append((x, y))

        x = next_x
        y = next_y

        # add backtrack direction to stack
        if next_direction == 1:
            backtrack = 2
        elif next_direction == 2:
            backtrack = 1
        elif next_direction == 3:
            backtrack = 4
        elif next_direction == 4:
            backtrack = 3
        tried_directions[(x, y)][backtrack - 1] = True
        stack.append(backtrack)

    return graph, oxygen_location

def main():
    program = '../IntcodePrograms/15.in'
    graph, oxygen_location = run_droid(program)
    shortest_path = shortest_path_to_oxygen(graph, oxygen_location)
    print(shortest_path)

if __name__ == '__main__':
    main()
