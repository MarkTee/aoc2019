from subprocess import Popen, PIPE

def send_signal(robot, signal):
    signal = str(signal) + '\n'
    robot.stdin.write(signal.encode())
    robot.stdin.flush()

def get_signal(robot):
    to_paint_colour = robot.stdout.readline().decode().rstrip()
    turn_direction = robot.stdout.readline().decode().rstrip()

    return to_paint_colour, turn_direction

def main():
    program_filename = '../IntcodePrograms/11.in'
    # create process to run the robot program
    robot = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program_filename),
                  shell=True,
                  stdin=PIPE,
                  stdout=PIPE)
    x = 0
    y = 0
    colours = dict()
    painted_panels = set()
    velocity = [0, 1] # (x, y)

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

        # if the robot plans to paint the panel a different colour, keep track of it
        if current_colour != to_paint_colour:
            painted_panels.add((x, y))
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

    # print the number of panels that the robot painted at least once
    print(len(painted_panels))

if __name__ == '__main__':
    main()
