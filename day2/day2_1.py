def run_program(program):
    """Run intcode program and return its state after halting"""
    pc = 0 # program counter

    # run program until halt instruction is reached
    while True:
        opcode = program[pc]

        # halt instruction
        if opcode == 99:
            break

        # parse inputs and output register
        operand1_reg = program[pc + 1]
        operand1 = program[operand1_reg]

        operand2_reg = program[pc + 2]
        operand2 = program[operand2_reg]

        output_reg = program[pc + 3]

        # add instruction
        if opcode == 1:
            program[output_reg] = operand1 + operand2

        # multiply instruction
        elif opcode == 2:
            program[output_reg] = operand1 * operand2

        # advance program counter
        pc += 4

    return program

def main():
    # get input program
    with open('2.in') as f:
        program = list(map(int, f.readline().split(',')))

    # replace position 1 with the value 12 and position 2 with the value 2
    # (as described in the instructions)
    program[1] = 12
    program[2] = 2

    # run program and get state after halting
    print(run_program(program)[0])

if __name__ == '__main__':
    main()
