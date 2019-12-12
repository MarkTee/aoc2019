def scan_moons(filename):
    """Parses an input file and extracts the coordinates of each moon.
    Returns two dicts, which map the i-th moon to its (x, y, z) coordinates,
    and its initial velocity (which is always 0 on all 3 axes), respectively.
    """
    moon_positions = dict()
    moon_velocities = dict()
    # iterate over the input file, which contains one moon per line
    with open(filename) as f:
        for i, line in enumerate(f):
            moon = line.rstrip().split()

            # extract the (x, y, z) coordinates for the current moon
            x = int(moon[0][moon[0].index('=') + 1:-1])
            y = int(moon[1][moon[1].index('=') + 1:-1])
            z = int(moon[2][moon[2].index('=') + 1:-1])

            moon_positions[i] = (x, y, z)
            moon_velocities[i] = (0, 0, 0)
    return moon_positions, moon_velocities

def apply_gravity(moon_positions, moon_velocities):
    """Applies gravity (as described in the problem statement)."""
    pass

def apply_velocity(moon_positions, moon_velocities):
    """Adds the velocity of each moon to its own position."""
    pass

def main():
    filename = '12.in'
    moon_positions, moon_velocities = scan_moons(filename)

def test():
    filename = 'test1.in'
    moon_positions, moon_velocities = scan_moons(filename)

if __name__ == '__main__':
    test()
    # main()
