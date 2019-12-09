import sys

class IntcodeComputer():
    """An implementation of the Intcode Computer described in Advent of Code 2019."""

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

def main():
    """When called from the command line and provided with an intcode program,
    create an IntcodeComputer object and run the given program.
    """
    program_filename = sys.argv[1] # path to the intcode program

    with open(program_filename) as f:
        program = list(map(int, f.readline().split(',')))

    # create IntcodeComputer object and run the provided program
    computer = IntcodeComputer(program)
    computer.run_program()

if __name__ == '__main__':
    main()
