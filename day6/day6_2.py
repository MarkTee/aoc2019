from collections import defaultdict, deque

def count_orbital_transfers(G, you, san):
    """Counts the total number of orbital transfers needed to navigate from the
    object YOU are orbiting to the object SAN is orbiting.
    """
    d = deque([you])
    distances = {you: 0}
    distance = 0

    # perform bfs
    while d:
        node = d.popleft()
        distance = distances[node] + 1
        for child in G[node]:
            if child not in distances:
                # if we encounter the object that SAN is orbiting, return its distance
                if child == san:
                    return distance

                distances[child] = distance
                d.append(child)

def create_graph(orbit_map):
    """Creates an adjacency list representation of a graph of an orbit map.
    Also returns the objects that YOU and SAN are orbiting.
    """
    graph = defaultdict(set)
    you = None
    san = None

    for line in orbit_map:
        parent, child = line.split(')')

        # check if the objects that YOU or SAN are orbiting are mentioned
        if child == 'YOU':
            you = parent
            continue
        elif child == 'SAN':
            san = parent
            continue

        graph[parent].add(child)
        graph[child].add(parent)

    # ensure YOU and SAN are actually present in the orbit_map
    assert you is not None
    assert san is not None

    return graph, you, san

def main():
    orbit_map = []
    with open('6.in') as f:
        for line in f:
            orbit_map.append(line.rstrip())

    graph, you, san = create_graph(orbit_map)
    transfers = count_orbital_transfers(graph, you, san)
    print(transfers)

def test():
    orbit_map = ['COM)B',
                   'B)C',
                   'C)D',
                   'D)E',
                   'E)F',
                   'B)G',
                   'G)H',
                   'D)I',
                   'E)J',
                   'J)K',
                   'K)L',
                   'K)YOU',
                   'I)SAN']
    graph, you, san = create_graph(orbit_map)
    transfers = count_orbital_transfers(graph, you, san)
    assert transfers == 4

if __name__ == '__main__':
    # test()
    main()
