from subprocess import Popen, PIPE

def send_char(robot, char):
    """Send an ascii char to the robot."""
    char = char + '\n'
    robot.stdin.write(char.encode())
    robot.stdin.flush()

def get_output(robot):
    """Get the robot's output."""
    output = robot.stdout.readline().decode().rstrip()
    return output

def run_robot(program):
    """Supply a series of instructions to the robot until it's completed its
    task. Then, get its output (i.e. how much dust the robot has collected)
    """
    robot = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program),
                  shell=True,
                  stdin=PIPE,
                  stdout=PIPE)
    
    # hand-calculated compressed path (and subroutines)
    # traverses the entire scaffolding
    main_routine ='A,B,A,B,C,B,A,C,B,C'
    a = 'L,12,L,8,R,10,R,10'
    b = 'L,6,L,4,L,12'
    c = 'R,10,L,8,L,4,R,10'
    
    # send all path info to the robot, represented by the ASCII values of 
    # each char
    for line in [main_routine, a, b, c]:
        for char in line:
            send_char(robot, str(ord(char))) # send move command
        send_char(robot, '10')               # send newline at end of routine
    send_char(robot, str(ord('n'))) # decline live video feed
    send_char(robot, '10')
    
    # get all output from robot; we can discard everything but the last line,
    # since the robot outputs the entire grid before outputting the dust value
    last_line = None
    while True:
        dust = get_output(robot)
        if dust == '':
            break
        last_line = dust
    return last_line

def main():
    program = '../IntcodePrograms/17-2.in'
    print(run_robot(program))

if __name__ == '__main__':
    main()
