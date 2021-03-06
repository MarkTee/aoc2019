def module_fuel(mass):
    """Calculate the fuel needed for the mass of each module."""
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + module_fuel(fuel)

def main():
    total_fuel = 0
    # Calculate fuel for all modules
    with open('1.in') as f:
        for line in f:
            module_mass = int(line)
            total_fuel += module_fuel(module_mass)
    print(total_fuel)

def test():
    assert module_fuel(14) == 2
    assert module_fuel(1969) == 966
    assert module_fuel(100756) == 50346

if __name__ == '__main__':
    # test()
    main()
