from collections import defaultdict, deque
from math import atan2

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

def find_best_station(filename):
    """Find the best location for a new station.
    (i.e. the station with the most distinct slopes to other asteroids)

    Return its coordinates and a dictionary mapping its normalized slopes to
    a list of other asteroids on that line.
    """
    asteroids = get_asteroids(filename) # find asteroid coordinates

    most_detected = 0
    # iterate over each asteroid
    for asteroid1 in asteroids:
        asteroid1_x = asteroid1[0]
        asteroid1_y = asteroid1[1]

        slopes = defaultdict(list)
        # get lines to other asteroids
        for asteroid2 in asteroids:
            # don't check against self
            if asteroid1 == asteroid2:
                continue

            """
            normalize rise over run for all asteroids to determine which
            asteroids block others (i.e. those lying on the same line)
            """
            y = asteroid2[1] - asteroid1_y # y2 - y1
            x = asteroid2[0] - asteroid1_x # x2 - x1

            if y == 0 or x == 0:
                fraction_gcd = max(abs(y), abs(x))
            else:
                fraction_gcd = gcd(abs(y), abs(x))

            reduced_y = y // fraction_gcd
            reduced_x = x // fraction_gcd

            slopes[reduced_y, reduced_x].append(asteroid2)

        # check if the current asteroid can detect more asteroids than the
        # previous best
        detected = len(slopes)
        if detected > most_detected:
            most_detected = detected

            best_station = asteroid1
            best_station_slopes = slopes

    return best_station, best_station_slopes

def find_vaporization_order(filename):
    # determine the best station location and obtain a dict mapping its
    # normalized slopes to all other asteroids
    best_station, best_station_slopes = find_best_station(filename)
    best_station_x = best_station[0]
    best_station_y = best_station[1]

    # sort slopes based on their angle between the x-axis and their unit vector
    sorted_slopes = sorted(best_station_slopes, key=lambda x:(-atan2(x[1], x[0])))

    # for each slope, sort all asteroids on that line based on distance to the
    # best station
    for slope in best_station_slopes:
        sorted_asteroids = deque(sorted(best_station_slopes[slope],
                                        key=lambda point:((point[0] - best_station_x)**2 +
                                                          (point[1] - best_station_y)**2)))
        best_station_slopes[slope] = sorted_asteroids

    vaporization_order = []
    # continuously vaporize asteroids until they've all been destroyed
    while sorted_slopes:
        empty_slopes = set()
        # rotate the laser clockwise
        for slope in sorted_slopes:
            # destroy the next asteroid on the current line
            next_asteroid = best_station_slopes[slope].popleft()
            vaporization_order.append(next_asteroid)

            # check if all asteroids on this line have been destroyed
            if not best_station_slopes[slope]:
                empty_slopes.add(slope)

        # remove any slopes that no longer have asteroids lying on their line
        sorted_slopes = list(set(sorted_slopes).difference(empty_slopes))

    return vaporization_order

def main():
    filename = '10.in'
    two_hundredth_vaporized = find_vaporization_order(filename)[199]
    print(two_hundredth_vaporized[0] * 100 + two_hundredth_vaporized[1])

def test():
    assert len(find_best_station('test1.in')[1]) == 8
    assert len(find_best_station('test2.in')[1]) == 33
    assert len(find_best_station('test3.in')[1]) == 35
    assert len(find_best_station('test4.in')[1]) == 41
    assert len(find_best_station('test5.in')[1]) == 210

    vaporization_order = find_vaporization_order('test5.in')
    assert len(vaporization_order) == 299
    assert vaporization_order[0] == (11, 12)
    assert vaporization_order[1] == (12, 1)
    assert vaporization_order[2] == (12, 2)
    assert vaporization_order[9] == (12, 8)
    assert vaporization_order[19] == (16, 0)
    assert vaporization_order[49] == (16, 9)
    assert vaporization_order[99] == (10, 16)
    assert vaporization_order[198] == (9, 6)
    assert vaporization_order[199] == (8, 2)
    assert vaporization_order[200] == (10, 9)
    assert vaporization_order[298] == (11, 1)

if __name__ == '__main__':
    # test()
    main()
