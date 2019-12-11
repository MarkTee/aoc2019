from subprocess import Popen, PIPE

def send_signal(robot, signal):
    """Sends a signal to the painting robot.
    0: if the robot is over a black panel
    1: if the robot is over a white panel
    """
    signal = str(signal) + '\n'
    robot.stdin.write(signal.encode())
    robot.stdin.flush()

def get_signal(robot):
    """Receives a signal from the painting robot.
    First, a value indicating the colour that the robot will paint the panel
    that it's currently over.
    0: black
    1: white

    Second, a value indicating the direction the robot will turn.
    0: turn left 90 degrees
    1: turn right 90 degrees
    """
    to_paint_colour = robot.stdout.readline().decode().rstrip()
    turn_direction = robot.stdout.readline().decode().rstrip()

    return to_paint_colour, turn_direction

def run_painting_robot(program_filename):
    """Run the painting robot, sending and receiving calls as necessary.
    Through this process, collect data in order to laern more about the
    dimensions of the hull, the starting position of the robot, and the final
    colours of the hull.
    """
    # create process to run the robot program
    robot = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program_filename),
                  shell=True,
                  stdin=PIPE,
                  stdout=PIPE)

    x = 0
    y = 0

    # keep track of the dimensions of the hull
    uppermost = 0
    rightmost = 0
    bottommost = 0
    leftmost = 0

    colours = {(0, 0): '1'} # start on a white panel
    velocity = [0, 1]       # (x, y) unit vector

    # interface with the robot until its program terminates
    while robot.poll() is None:
        # get the colour of the current panel
        if (x, y) not in colours:
            current_colour = '0' # all panels start out black
        else:
            current_colour = colours[(x, y)]

        # communicate with the robot and see what it intends to do
        send_signal(robot, current_colour)
        to_paint_colour, turn_direction = get_signal(robot)
        colours[(x, y)] = to_paint_colour

        # handle turn
        # currently moving vertically
        if velocity[0] == 0:
            if turn_direction == '0':
                velocity[0] = -velocity[1]
            elif turn_direction == '1':
                velocity[0] = velocity[1]
            velocity[1] = 0

        # currently moving horizontally
        elif velocity[1] == 0:
            if turn_direction == '0':
                velocity[1] = velocity[0]
            elif turn_direction == '1':
                velocity[1] = -velocity[0]
            velocity[0] = 0

        # move forward one space after turning
        x += velocity[0]
        y += velocity[1]

        if x < leftmost:
            leftmost = x
        elif x > rightmost:
            rightmost = x
        elif y > uppermost:
            uppermost = y
        elif y < bottommost:
            bottommost = y

    # don't paint the panel that the robot ended on
    colours[(x, y)] = current_colour

    # calculate dimensions of the hull and the robot's starting position
    width = rightmost - leftmost + 1
    height = uppermost - bottommost + 1
    starting_position = (-leftmost, uppermost)

    # return the data we collected regarding the colour of different panels,
    # the the dimensions of the hull's area, and the robot's starting position
    return colours, width, height, starting_position

def paint_hull(colours, width, height, starting_position):
    """After the robot has done its job, print the painted hull to the terminal."""
    starting_x = starting_position[0]
    starting_y = starting_position[1]

    grid = [['0' for col in range(width)] for row in range(height)]

    for cell, colour in colours.items():
        cell_x = cell[0]
        cell_y = cell[1]

        if cell_y >= 0:
            cell_y -= starting_y
        elif cell_y < 0:
            cell_y = -cell_y + starting_y

        if cell_x >= 0:
            cell_x -= starting_x
        elif cell_y < 0:
            cell_x = -cell_x + starting_x

        grid[cell_y][cell_x] = colour

    for row in grid:
        for col in row:
            # print white pixel
            if col == '0':
                print(u"\u2588", end='')
            # print black pixel
            else:
                print(u"\u2591", end='')
        print()

def main():
    program_filename = '../IntcodePrograms/11.in'
    paint_hull(*run_painting_robot(program_filename))

if __name__ == '__main__':
    main()
