def gcd(a, b):
    """Calculate the greatest common divisor for two numbers."""
    if (a < b):
        return gcd(b, a)
    while b != 0:
        a, b = b, a % b
    return a

def get_asteroids(filename):
    """Given a file containing a grid, extract the coordinate of all asteroids."""
    asteroids = set()

    with open(filename) as f:
        for row, line in enumerate(f):
            for col, cell in enumerate(line):
                if cell == '#':
                    asteroids.add((col, row))
    return asteroids

def get_most_detected(asteroids):
    """Determine the greatest number of asteroids that can be detected from an
    asteroid.
    """
    most_detected = 0
    # iterate over each asteroid
    for asteroid1 in asteroids:
        detected_angles = set()
        # check which asteroids can be detected form the current asteroid
        for asteroid2 in asteroids:
            # don't check against self
            if asteroid1 == asteroid2:
                continue

            # normalize rise over run for all asteroids to determine which
            # asteroids block others
            numerator   = asteroid1[1] - asteroid2[1] # y2 - y1
            denominator = asteroid1[0] - asteroid2[0] # x2 - x1

            if numerator == 0 or denominator == 0:
                fraction_gcd = max(abs(numerator), abs(denominator))
            else:
                fraction_gcd = gcd(abs(numerator), abs(denominator))

            numerator //= fraction_gcd
            denominator //= fraction_gcd

            detected_angles.add((numerator, denominator))

        # check if the current asteroid can detect more asteroids than the
        # previous best
        detected = len(detected_angles)
        if detected > most_detected:
            most_detected = detected

    return most_detected

def find_best_location(filename):
    """Determine how many asteroids can be detected from the best location for
    a new monitoring station.
    """
    asteroids = get_asteroids(filename)
    most_detected = get_most_detected(asteroids)
    return most_detected

def main():
    filename = '10.in'
    print(find_best_location(filename))

def test():
    assert find_best_location('test1.in') ==   8
    assert find_best_location('test2.in') == 33
    assert find_best_location('test3.in') == 35
    assert find_best_location('test4.in') == 41
    assert find_best_location('test5.in') == 210

if __name__ == '__main__':
    # test()
    main()
