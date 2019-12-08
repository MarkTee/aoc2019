def module_fuel(mass):
    """Calculate the fuel needed for the mass of each module."""
    return (mass // 3) - 2

def main():
    total_fuel = 0
    # Calculate fuel for all modules
    with open('1.in') as f:
        for line in f:
            module_mass = int(line)
            total_fuel += module_fuel(module_mass)
    print(total_fuel)

def test():
    assert module_fuel(12) == 2
    assert module_fuel(14) == 2
    assert module_fuel(1969) == 654
    assert module_fuel(100756) == 33583

if __name__ == '__main__':
    # test()
    main()
