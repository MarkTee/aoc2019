def scan_moons(filename):
    """Parses an input file and extracts the coordinates of each moon.

    Returns a dict mapping the i-th moon to a list containing its (x, y, z)
    coordinates and its velocity (which is initially 0 on all 3 axes).
    """
    moons = dict()
    # iterate over the input file, which contains one moon per line
    with open(filename) as f:
        for i, line in enumerate(f):
            moon = line.rstrip().split()

            # extract the (x, y, z) coordinates for the current moon
            x = int(moon[0][moon[0].index('=') + 1:-1])
            y = int(moon[1][moon[1].index('=') + 1:-1])
            z = int(moon[2][moon[2].index('=') + 1:-1])

            moons[i] = [[x, y, z], [0,0,0]]
    return moons

def apply_gravity(moons):
    """Applies gravity (as described in the problem statement)."""
    n_moons = len(moons) # number of moons

    # iterate over each moon
    for i in range(n_moons - 1):
        moon1_pos = moons[i][0]
        # iterate over each of the other moons
        for j in range(i + 1, n_moons):
            moon2_pos = moons[j][0]

            # iterate over (x, y, z) coordinate and update velocity as necessary
            for coord in range(3):
                if moon1_pos[coord] > moon2_pos[coord]:
                    moons[i][1][coord] -= 1
                    moons[j][1][coord] += 1
                elif moon1_pos[coord] < moon2_pos[coord]:
                    moons[i][1][coord] += 1
                    moons[j][1][coord] -= 1

def apply_velocity(moons):
    """Adds the velocity of each moon to its own position."""
    for moon in moons.values():
        for coord in range(3):
            moon[0][coord] += moon[1][coord]

def step(moons, n, debug=False):
    """Advances the simulation n steps."""
    if debug:
        print_debug(moons, 0)

    for i in range(n):
        apply_gravity(moons)
        apply_velocity(moons)

        if debug:
            print_debug(moons, i + 1)

def print_debug(moons, i):
    """Prints the current state of the simulation."""
    print("After {} steps:".format(i))
    for moon in moons:
        moon = moons[moon]
        print("pos=<x={:3d}, y={:3d}, z={:3d}>, ".format(moon[0][0],
                                                         moon[0][1],
                                                         moon[0][2]), end='')
        print("vel=<x={:3d}, y={:3d}, z={:3d}>".format(moon[1][0],
                                                       moon[1][1],
                                                       moon[1][2]))
    print()

def calculate_total_energy(moons):
    """Calculates total energy in the system."""
    total_system_energy = 0
    # calculate each moon's total energy
    for moon in moons.values():
        # sum of the absolute values of the moon's (x, y, z) coordinates
        potential_energy = sum(abs(n) for n in moon[0])
        # sum of the absolute values of the moon's (x, y, z) velocities
        kinetic_energy = sum(abs(n) for n in moon[1])

        total_moon_energy = potential_energy * kinetic_energy
        total_system_energy += total_moon_energy

    return total_system_energy

def main():
    filename = '12.in'
    moons = scan_moons(filename)
    step(moons, 1000, debug=False)
    print(calculate_total_energy(moons))

def test():
    filename = 'test1.in'
    moons = scan_moons(filename)
    step(moons, 10, debug=False)
    assert calculate_total_energy(moons) == 179

    filename = 'test2.in'
    moons = scan_moons(filename)
    step(moons, 100, debug=False)
    assert calculate_total_energy(moons) == 1940

if __name__ == '__main__':
    # test()
    main()
