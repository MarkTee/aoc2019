def module_fuel(mass):
    """Calculate the fuel needed for the mass of each module"""
    return (mass // 3) - 2

def main():
    total_fuel = 0
    # Calculate fuel for all modules
    while True:
        try:
            module_mass = int(input())
            total_fuel += module_fuel(module_mass)
        except EOFError:
            break
    print(total_fuel)

if __name__ == '__main__':
    main()
