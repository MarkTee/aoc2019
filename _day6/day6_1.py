from collections import defaultdict, deque

def count_total_orbits(G, s):
    """Count the total number of orbits (both direct and indirect) for a graph
    representation of an orbit map.
    """
    visited = set()
    d = deque([s])
    orbits = {'COM': 0}

    # perform bfs
    while d:
        node = d.popleft()
        if node not in visited:
            visited.add(node)
            parent_orbits = orbits[node]

            for child in G[node]:
                if child not in visited:
                    d.append(child)
                    orbits[child] = parent_orbits + 1 # indirect orbits + direct

    return sum(orbits.values())

def create_graph(orbit_map):
    """Creates an adjacency list representation of a graph of an orbit map."""
    graph = defaultdict(set)
    for line in orbit_map:
        parent, child = line.split(')')
        graph[parent].add(child)
    return graph

def main():
    orbit_map = []
    with open('6.in') as f:
        for line in f:
            orbit_map.append(line.rstrip())

    graph = create_graph(orbit_map)
    orbits = count_total_orbits(graph, 'COM')
    print(orbits)

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
                   'K)L']
    graph = create_graph(orbit_map)
    orbits = count_total_orbits(graph, 'COM')
    assert orbits == 42

if __name__ == '__main__':
    # test()
    main()
