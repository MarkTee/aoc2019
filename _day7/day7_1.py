import sys
from io import StringIO
from itertools import permutations

######################################
########## Helper Functions ##########
######################################

def get_parameters(program, pc, opcode, n):
    """Returns the next n parameters following the current opcode."""
    # pad opcode with zeros to determine parameter modes easier
    opcode = str(opcode).zfill(2 + n)

    # get parameter modes in order by moving backwards across the string
    parameters = []
    for i in range(1, n + 1):
        mode = opcode[-2 - i]

        # position mode
        if mode == '0':
            parameter_register = program[pc + i]
            parameter = program[parameter_register]

        # immediate mode
        elif mode == '1':
            parameter = program[pc + i]

        parameters.append(parameter)

    return parameters


#############################
########## Opcodes ##########
#############################

def op_1(program, pc, opcode):
    """Addition Operation"""
    addend1, addend2 = get_parameters(program, pc, opcode, 2)
    output_register = program[pc + 3]
    program[output_register] = addend1 + addend2
    return pc + 4

def op_2(program, pc, opcode):
    """Multiplication Operation"""
    multiplicand1, multiplicand2  = get_parameters(program, pc, opcode, 2)
    output_register = program[pc + 3]
    program[output_register] = multiplicand1 * multiplicand2
    return pc + 4

def op_3(program, pc, opcode):
    """Input Operation"""
    save_to_register = program[pc + 1]
    program[save_to_register] = int(input())
    return pc + 2

def op_4(program, pc, opcode):
    """Output Operation"""
    output = get_parameters(program, pc, opcode, 1)[0]
    print(output)
    return pc + 2

def op_5(program, pc, opcode):
    """Jump-if-True Operation"""
    parameter1, jump_destination = get_parameters(program, pc, opcode, 2)
    if parameter1 != 0:
        return jump_destination
    else:
        return pc + 3

def op_6(program, pc, opcode):
    """Jump-if-False Operation"""
    parameter1, jump_destination = get_parameters(program, pc, opcode, 2)
    if parameter1 == 0:
        return jump_destination
    else:
        return pc + 3

def op_7(program, pc, opcode):
    """Less Than Operation"""
    parameter1, parameter2 = get_parameters(program, pc, opcode, 2)
    output_register = program[pc + 3]

    if parameter1 < parameter2:
        program[output_register] = 1
    else:
        program[output_register] = 0

    return pc + 4

def op_8(program, pc, opcode):
    """Equals Operation"""
    parameter1, parameter2 = get_parameters(program, pc, opcode, 2)
    output_register = program[pc + 3]

    if parameter1 == parameter2:
        program[output_register] = 1
    else:
        program[output_register] = 0

    return pc + 4


#################################
########## Run Program ##########
#################################

def run_program(program):
    """Run intcode program and return its state after halting"""
    pc = 0 # program counter
    jump_table = {1: op_1,
                  2: op_2,
                  3: op_3,
                  4: op_4,
                  5: op_5,
                  6: op_6,
                  7: op_7,
                  8: op_8}

    # run program until halt instruction is reached
    while True:
        opcode = program[pc]

        # halt instruction
        if opcode == 99:
            break

        # only look at the 2 rightmost digits of the opcode to determine the
        # proper operation to perform
        operation = jump_table[opcode % 100]
        pc = operation(program, pc, opcode)

    return program

def run_amplifiers(program, phase_sequence):
    output_signal = None
    for i, setting in enumerate(phase_sequence):
        if output_signal is None:
            # if this is the first amplifier, provide an initial input signal
            sys.stdin = StringIO(str(setting) + '\n0')
        else:
            # provide phase setting for the current amplifier, as well as the
            # last amplifier's output signal
            sys.stdin = StringIO(str(setting) + '\n' + output_signal)

        # Monitor stdout to get the amplifier's output signal
        # Source for the following 6 lines: https://stackoverflow.com/q/5136611
        backup = sys.stdout                   # setup the environment
        sys.stdout = StringIO()               # capture output
        run_program(program)                  # run program with appropriate settings
        output_signal = sys.stdout.getvalue() # release output
        sys.stdout.close()                    # close the stream
        sys.stdout = backup                   # restore original stdout

        if i == len(phase_sequence) - 1:
            thruster_signal = output_signal
    return int(output_signal)

def main():
    # get input program
    with open('7.in') as f:
        program = list(map(int, f.readline().split(',')))

    # generate all permutations of phase sequences
    phase_sequences = permutations(range(5))
    largest_output_signal = float('-inf')
    # check the result of each phase sequence to determine which one produces
    # the largest output signal
    for phase_sequence in phase_sequences:
        output_signal = run_amplifiers(program, phase_sequence)

        if output_signal > largest_output_signal:
            largest_output_signal = output_signal

    print(largest_output_signal)

def test():
    assert run_program([1,0,0,0,99]) == [2,0,0,0,99]
    assert run_program([2,3,0,3,99]) == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
    assert run_program([1002,4,3,4,33]) == [1002,4,3,4,99]

    # run example amplifier programs
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_sequence = [4,3,2,1,0]
    assert run_amplifiers(program, phase_sequence) == 43210

    program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    phase_sequence = [0,1,2,3,4]
    assert run_amplifiers(program, phase_sequence) == 54321

    program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phase_sequence = [1,0,4,3,2]
    assert run_amplifiers(program, phase_sequence) == 65210

if __name__ == '__main__':
    # test()
    main()
