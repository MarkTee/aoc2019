from collections import Counter

def decreasing(num):
    """Returns True if any adjacent digits in a number are in increasing order."""
    assert num >= 0 # only examine nonnegative numbers

    while num >= 10:
        last_digit = num % 10
        num //= 10
        if last_digit < num % 10:
            return True
    return False

def is_valid(num):
    """Returns True if a number satisfies the password criteria."""
    num_str = str(num)
    c = Counter(num_str)
    # numbers with decreasing digits are invalid
    if decreasing(num):
        return 0
    '''
    valid numbers must have at least two of the same digit; since at the point
    we know the number's digits are non-decreasing, then any repeated
    characters must also be adjacent to each other
    '''
    return 2 in c.values()

def main():
    lower = 367479
    upper = 893698

    valid_numbers = list(filter(is_valid, range(lower, upper + 1)))
    print(len(valid_numbers))

def test():
    assert decreasing(223450) == True
    assert decreasing(111111) == False
    assert decreasing(123789) == False
    assert decreasing(10) == True
    assert decreasing(0) == False
    assert decreasing(5) == False

if __name__ == '__main__':
    # test()
    main()
