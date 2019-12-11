from IntcodeComputer import IntcodeComputer

def main():
    """Identical to Day 9 - Part 1, except a different input is passed in."""

    # Test Programs
    # program_filename = '../IntcodePrograms/test6.in'
    # program_filename = '../IntcodePrograms/test7.in'
    # program_filename = '../IntcodePrograms/test8.in'

    program_filename = '../IntcodePrograms/9.in'

    with open(program_filename) as f:
        program = list(map(int, f.readline().split(',')))
    computer = IntcodeComputer(program)
    computer.run_program()

if __name__ == '__main__':
    main()
