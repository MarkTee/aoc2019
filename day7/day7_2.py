import sys
from io import StringIO
from itertools import permutations

class IntCodeComputer():

    def __init__(self, program):
        self.program = program
        self.current_opcode = None
        self.pc = 0 # program counter
        self.jump_table = {1: self.op_1,
                           2: self.op_2,
                           3: self.op_3,
                           4: self.op_4,
                           5: self.op_5,
                           6: self.op_6,
                           7: self.op_7,
                           8: self.op_8}



    def run_program(self):
        """Run intcode program and return its state after halting"""
        while True:
            self.current_opcode = self.program[self.pc]

            # halt instruction
            if self.current_opcode == 99:
                break

            # only look at the 2 rightmost digits of the opcode to determine
            # the proper operation to perform
            operation = self.jump_table[self.current_opcode % 100]()

        return self.program

    def get_parameters(self, n):
        """Returns the next n parameters following the current opcode."""
        # pad opcode with zeros to determine parameter modes easier
        opcode = str(self.current_opcode).zfill(2 + n)

        # get parameter modes in order by moving backwards across the string
        parameters = []
        for i in range(1, n + 1):
            mode = opcode[-2 - i]

            # position mode
            if mode == '0':
                parameter_register = self.program[self.pc + i]
                parameter = self.program[parameter_register]

            # immediate mode
            elif mode == '1':
                parameter = self.program[self.pc + i]

            parameters.append(parameter)

        return parameters


    #############################
    ########## Opcodes ##########
    #############################

    def op_1(self):
        """Addition Operation"""
        addend1, addend2 = self.get_parameters(2)
        output_register = self.program[self.pc + 3]
        self.program[output_register] = addend1 + addend2
        self.pc += 4

    def op_2(self):
        """Multiplication Operation"""
        multiplicand1, multiplicand2  = self.get_parameters(2)
        output_register = self.program[self.pc + 3]
        self.program[output_register] = multiplicand1 * multiplicand2
        self.pc += 4

    def op_3(self):
        """Input Operation"""
        save_to_register = self.program[self.pc + 1]
        self.program[save_to_register] = int(input())
        self.pc += 2

    def op_4(self):
        """Output Operation"""
        output = self.get_parameters(1)[0]
        print(output)
        self.pc += 2

    def op_5(self):
        """Jump-if-True Operation"""
        parameter1, jump_destination = self.get_parameters(2)
        if parameter1 != 0:
            self.pc = jump_destination
        else:
            self.pc += 3

    def op_6(self):
        """Jump-if-False Operation"""
        parameter1, jump_destination = self.get_parameters(2)
        if parameter1 == 0:
            self.pc = jump_destination
        else:
            self.pc += 3

    def op_7(self):
        """Less Than Operation"""
        parameter1, parameter2 = self.get_parameters(2)
        output_register = self.program[self.pc + 3]

        if parameter1 < parameter2:
            self.program[output_register] = 1
        else:
            self.program[output_register] = 0

        self.pc += 4

    def op_8(self):
        """Equals Operation"""
        parameter1, parameter2 = self.get_parameters(2)
        output_register = self.program[self.pc + 3]

        if parameter1 == parameter2:
            self.program[output_register] = 1
        else:
            self.program[output_register] = 0

        self.pc += 4

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
    computer = IntCodeComputer([1,0,0,0,99])
    assert computer.run_program() == [2,0,0,0,99]

    computer = IntCodeComputer([2,3,0,3,99])
    assert computer.run_program() == [2,3,0,6,99]

    computer = IntCodeComputer([2,4,4,5,99,0])
    assert computer.run_program() == [2,4,4,5,99,9801]

    computer = IntCodeComputer([1,1,1,4,99,5,6,0,99])
    assert computer.run_program() == [30,1,1,4,2,5,6,0,99]

    computer = IntCodeComputer([1002,4,3,4,33])
    assert computer.run_program() == [1002,4,3,4,99]

    exit()

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
    test()
    # main()
