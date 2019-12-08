def wire_path(wire):
    """Return a set containing all (x, y) coordinates occupied by the wire."""
    x = y = 0
    path = set()

    # traverse each segment of the wire to determine its path
    for segment in wire:
        direction = segment[0]
        magnitude = int(segment[1:])

        # follow the segment to its end, storing any coordinates it occupies
        if direction == 'R':
            for col in range(x + 1, x + magnitude + 1):
                path.add((col, y))
            x += magnitude

        elif direction == 'D':
            for row in range(y - 1, y - magnitude - 1, -1):
                path.add((x, row))
            y -= magnitude

        elif direction == 'L':
            for col in range(x - 1, x - magnitude - 1, -1):
                path.add((col, y))
            x -= magnitude

        elif direction == 'U':
            for row in range(y + 1, y + magnitude + 1):
                path.add((x, row))
            y += magnitude

    return path

def closest_intersection_distance(wire1, wire2):
    """Calculate the Manhattan distance from the central port (0, 0) to the
    closest intersection point between two wires.
    """
    # determine the coordinates occupied by each wire
    wire1_path = wire_path(wire1)
    wire2_path = wire_path(wire2)

    # find intersection points
    intersections = wire1_path & wire2_path

    # find the closest intersection point
    closest_distance = float('inf')
    for point in intersections:
        # calculate Manhattan distance for given point
        distance = abs(point[0]) + abs(point[1])
        if distance < closest_distance:
            closest_distance = distance
    return closest_distance

def main():
    # get wire descriptions
    with open('3.in') as f:
        wire1 = f.readline().split(',')
        wire2 = f.readline().split(',')

    print(closest_intersection_distance(wire1, wire2))

def test():
    wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
    wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
    assert(closest_intersection_distance(wire1, wire2) == 159)

    wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
    wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
    assert(closest_intersection_distance(wire1, wire2) == 135)

if __name__ == '__main__':
    # test()
    main()
