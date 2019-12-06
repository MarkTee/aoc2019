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

    # try all noun and verb combinations to determine which ones cause the
    # program to produce the output 19690720 (as specified in the question)
    for noun in range(100):
        for verb in range(100):
            test_program = program.copy()
            test_program[1] = noun
            test_program[2] = verb

            if run_program(test_program)[0] == 19690720:
                print(100 * noun + verb)

if __name__ == '__main__':
    main()
