from collections import defaultdict, deque
from math import ceil

def parse_input_file(filename):
    """Parse the input file to obtain chemical reaction data."""
    reactions = defaultdict(list)
    with open(filename) as f:
        for line in f.readlines():
            precursors, produced = line.split(' => ')

            # parse precursors' quantities and names
            precursors = precursors.strip().split(', ')
            precursors = [i.split() for i in precursors]
            precursors = [{'precursor_name': i[1], 'n_needed': int(i[0])} for i in precursors]

            # parse produced
            produced_quantity, produced_name = produced.strip().split()

            # map produced to precursors
            reactions[produced_name] = {'n_produced': int(produced_quantity), 'precursors': precursors}
    return reactions

def get_fuel_cost(reactions, n):
    """Calculate the number of ore needed to produce n units of fuel."""
    ore_cost = 0
    have = defaultdict(int)       # leftover chemicals from other reactions
    needed = deque([['FUEL', n]]) # a queue holding chemicals that need to be produced

    while needed:
        chemical_name, n_needed = needed.popleft()

        if chemical_name == 'ORE':
            # if the chemical only needs ore
            ore_cost += n_needed
        elif n_needed <= have[chemical_name]:
            # if there are already enough leftover chemicals to satisfy need
            have[chemical_name] -= n_needed
        else:
            reaction = reactions[chemical_name]

            n_needed = n_needed - have[chemical_name]  # deficit that must be filled
            n_produced = reaction['n_produced']        # quantity of chemical produced in each reaction
            n_reactions = ceil(n_needed / n_produced)  # number of reactions needed to fill deficit

            for precursor in reaction['precursors']:
                # track number of precursors needed for each reaction
                needed.append([precursor['precursor_name'],
                               precursor['n_needed'] * n_reactions])

            # keep track of excess chemicals not used for the current reaction
            leftovers = (n_reactions * n_produced) - n_needed
            have[chemical_name] = leftovers

    return ore_cost

def max_fuel_production(reactions, max_ore=1000000000000):
    """Determine the maximum amount of FUEL that can be produced for a given
    amount of ore.
    """
    lower = 1
    upper = max_ore

    while lower <= upper:
        middle = (lower + upper) // 2 # check if middle units of fuel can be produced
        fuel_cost = get_fuel_cost(reactions, middle)

        if fuel_cost == 1000000000000 or (upper - lower) == 1:
            return middle
        elif fuel_cost < 1000000000000:
                lower = middle
        elif fuel_cost > 1000000000000:
                upper = middle
    return middle

def main():
    print(max_fuel_production(parse_input_file('14.in')))

def test():
    assert get_fuel_cost(parse_input_file('test1.in'), 1) == 31
    assert get_fuel_cost(parse_input_file('test2.in'), 1) == 165
    assert get_fuel_cost(parse_input_file('test3.in'), 1) == 13312
    assert get_fuel_cost(parse_input_file('test4.in'), 1) == 180697
    assert get_fuel_cost(parse_input_file('test5.in'), 1) == 2210736

    assert max_fuel_production(parse_input_file('test3.in')) == 82892753
    assert max_fuel_production(parse_input_file('test4.in')) == 5586022
    assert max_fuel_production(parse_input_file('test5.in')) == 460664

if __name__ == '__main__':
    # test()
    main()
