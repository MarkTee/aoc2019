def wire_path(wire):
    """Return a set containing all (x, y) coordinates occupied by the wire."""
    x = y = 0
    path = dict()
    steps = 0

    # traverse each segment of the wire to determine its path
    for segment in wire:
        direction = segment[0]
        magnitude = int(segment[1:])

        # follow the segment to its end, storing any coordinates it occupies
        if direction == 'R':
            for col in range(x + 1, x + magnitude + 1):
                steps += 1
                path[(col, y)] = steps
            x += magnitude

        elif direction == 'D':
            for row in range(y - 1, y - magnitude - 1, -1):
                steps += 1
                path[(x, row)] = steps
            y -= magnitude

        elif direction == 'L':
            for col in range(x - 1, x - magnitude - 1, -1):
                steps += 1
                path[(col, y)] = steps
            x -= magnitude

        elif direction == 'U':
            for row in range(y + 1, y + magnitude + 1):
                steps += 1
                path[(x, row)] = steps
            y += magnitude

    return path

def fewest_combined_steps(wire1, wire2):
    """Calculate the fewest combined steps that two wires must take to reach an
    intersection point.
    """
    # determine the coordinates occupied by each wire
    wire1_path = wire_path(wire1)
    wire2_path = wire_path(wire2)

    # find intersection points
    intersections = wire1_path.keys() & wire2_path.keys()

    # determine the fewest combined steps
    fewest_steps = float('inf')
    for point in intersections:
        steps = wire1_path[point] + wire2_path[point]
        if steps < fewest_steps:
            fewest_steps = steps
    return fewest_steps

def main():
    # get wire descriptions
    with open('3.in') as f:
        wire1 = f.readline().split(',')
        wire2 = f.readline().split(',')

    print(fewest_combined_steps(wire1, wire2))

def test():
    wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
    wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
    assert(fewest_combined_steps(wire1, wire2) == 610)

    wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
    wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
    assert(fewest_combined_steps(wire1, wire2) == 410)

if __name__ == '__main__':
    test()
    main()
