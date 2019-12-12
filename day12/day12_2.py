def gcd(a, b):
    """Calculate the greatest common divisor for two numbers."""
    if (a < b):
        return gcd(b, a)
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the least common multiple for two numbers."""
    return a * b / gcd(a, b)

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

    return moons

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

def find_periods(moons):
    """Finds the period for each of the 3 axes."""
    states = [set(), set(), set()] # all previous states
    found = [False, False, False]  # whether the x, y, z period has been found

    i = 0
    # run simulation until all 3 periods are determined
    while not all(found):
        moons = step(moons, 1)

        x_state = tuple()
        y_state = tuple()
        z_state = tuple()

        # iterate over each moon and separately calculate the state of each axis
        for moon in moons.values():
            if not found[0]:
                x = (moon[0][0], moon[1][0])
                x_state += x

            if not found[1]:
                y = (moon[0][1], moon[1][1])
                y_state += y

            if not found[2]:
                z = (moon[0][2], moon[1][2])
                z_state += z

        # for each axis, check if the current state has been seen before
        if not found[0]:
            if x_state in states[0]:
                found[0] = True
                x_period = i
            states[0].add(x_state)

        if not found[1]:
            if y_state in states[1]:
                found[1] = True
                y_period = i
            states[1].add(y_state)

        if not found[2]:
            if z_state in states[2]:
                found[2] = True
                z_period = i
            states[2].add(z_state)

        i += 1

    return x_period, y_period, z_period

def find_first_repeats(moons):
    """Finds the first step where the state exactly matches a previous state.
    Since the 3 axes don't have any effect on each other, this will be equal to
    the least common multiple between the 3 axes' periods.
    """
    x_period, y_period, z_period = find_periods(moons)
    first_repeat = lcm(lcm(x_period, y_period), z_period)
    assert first_repeat.is_integer() # make sure nothing went wrong
    return int(first_repeat)


def main():
    filename = '12.in'
    moons = scan_moons(filename)
    print(find_first_repeats(moons))

def test():
    filename = 'test1.in'
    moons = scan_moons(filename)
    # step(moons, 10, debug=False)
    # assert calculate_total_energy(moons) == 179
    assert find_first_repeats(moons) == 2772

    filename = 'test2.in'
    moons = scan_moons(filename)
    # step(moons, 100, debug=False)
    # assert calculate_total_energy(moons) == 1940
    assert find_first_repeats(moons) == 4686774924

if __name__ == '__main__':
    # test()
    main()
