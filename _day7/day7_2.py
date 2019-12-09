import sys
from itertools import permutations
from subprocess import Popen, PIPE

from IntcodeComputer import IntcodeComputer

def run_amplifiers(program_filename, phase_sequence, feedback_loop=False):
    amplifiers = []
    for phase_setting in phase_sequence:
        # create an IntcodeComputer object for each amplifier
        amplifier = Popen('python3 IntcodeComputer.py {}'.format(program_filename),
                          shell=True,
                          stdin=PIPE,
                          stdout=PIPE)
        amplifiers.append(amplifier)

        # pass phase setting as first input
        phase_setting = (str(phase_setting) + '\n')
        amplifier.stdin.write(phase_setting.encode())
        amplifier.stdin.flush()

    # continuously run feedback loop until one of the amplifiers terminates
    output_signal = b'0\n' # initial 0 signal for amplifier A
    last_valid_output = output_signal
    running = True
    while running:
        # process amplifiers left-to-right
        for amplifier in amplifiers:
            # pass the previous output signal as the next amplifier's input signal
            amplifier.stdin.write(output_signal)
            amplifier.stdin.flush()

            # save the current amplifier's output signal
            output_signal = amplifier.stdout.readline()

            # check if the current amplifier's process has terminated
            if amplifier.poll() is not None:
                running = False
                break

            # last non-empty output signal (i.e. from before amplifiers have terminated
            last_valid_output = output_signal.decode()

        if not feedback_loop:
            """
            If we're not using a feedback loop configuration, then each intcode
            computer only needs to run once.
            """
            break

    return int(last_valid_output)

def main():
    # get input program
    program_filename = 'programs/7.in'

    # generate all permutations of phase sequences
    phase_sequences = permutations(range(5, 10))
    largest_output_signal = float('-inf')

    # check the result of each phase sequence to determine which one produces
    # the largest output signal
    for phase_sequence in phase_sequences:
        output_signal = run_amplifiers(program_filename,
                                       phase_sequence,
                                       feedback_loop=True)

        if output_signal > largest_output_signal:
            largest_output_signal = output_signal

    print(largest_output_signal)

def test():
    # basic intcode operations tests
    computer = IntcodeComputer([1,0,0,0,99])
    assert computer.run_program() == [2,0,0,0,99]

    computer = IntcodeComputer([2,3,0,3,99])
    assert computer.run_program() == [2,3,0,6,99]

    computer = IntcodeComputer([2,4,4,5,99,0])
    assert computer.run_program() == [2,4,4,5,99,9801]

    computer = IntcodeComputer([1,1,1,4,99,5,6,0,99])
    assert computer.run_program() == [30,1,1,4,2,5,6,0,99]

    computer = IntcodeComputer([1002,4,3,4,33])
    assert computer.run_program() == [1002,4,3,4,99]

    # amplifier tests
    program_filename = 'programs/test1.in'
    phase_sequence = [4,3,2,1,0]
    assert run_amplifiers(program_filename, phase_sequence) == 43210

    program_filename = 'programs/test2.in'
    phase_sequence = [0,1,2,3,4]
    assert run_amplifiers(program_filename, phase_sequence) == 54321

    program_filename = 'programs/test3.in'
    phase_sequence = [1,0,4,3,2]
    assert run_amplifiers(program_filename, phase_sequence) == 65210

    # amplifier feedback loop tests
    program_filename = 'programs/test4.in'
    phase_sequence = [9,8,7,6,5]
    assert run_amplifiers(program_filename, phase_sequence, feedback_loop=True) == 139629729

    program_filename = 'programs/test5.in'
    phase_sequence = [9,7,8,5,6]
    assert run_amplifiers(program_filename, phase_sequence, feedback_loop=True) == 18216

if __name__ == '__main__':
    # test()
    main()
