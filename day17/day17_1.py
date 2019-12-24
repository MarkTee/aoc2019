from subprocess import Popen, PIPE

def get_alignment_parameters_sum(program):
    """Calculates the sum of the alignment paraemters for the scaffold
    intersections, as described in the problem statement.
    """
    robot = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program),
                  shell=True,
                  stdin=PIPE,
                  stdout=PIPE)

    robot_signal = robot.communicate()
    robot_signal = robot_signal[0].decode().strip(',').split('\n')[:-1]

    # convert robot signal to a grid representation
    grid = []
    line = []
    row = 0
    col = 0
    scaffolding = set()
    for char in robot_signal:
        if char == '35':
            line.append('#')
            scaffolding.add((row, col))
        elif char == '46':
            line.append('.')

        col += 1

        # start a new row
        if char == '10':
            grid.append(line)
            line = []
            row += 1
            col = 0

    # find scaffold intersections
    intersections = set()
    for scaffold in scaffolding:
        x = scaffold[0]
        y = scaffold[1]

        if (x+1, y) in scaffolding and (x-1, y) in scaffolding and \
           (x, y+1) in scaffolding and (x, y-1) in scaffolding:
           intersections.add(scaffold)

    # sum the alignment parameter of each  intersection
    alignment_parameters_sum = 0
    for intersect in intersections:
        alignment_parameters_sum += intersect[0] * intersect[1]

    return alignment_parameters_sum


def main():
    program = '../IntcodePrograms/17.in'
    print(get_alignment_parameters_sum(program))

if __name__ == '__main__':
    main()
