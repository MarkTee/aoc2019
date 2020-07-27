def fft(signal):
    """Execute Flawed Frequency Transmission algorithm, as described in the
    problem statement.
    """
    offset = int(signal[:7])

    # anything before the offset can be safely ignored
    output = list(map(int, list(signal[offset:])))
    
    # work backwards, so that the problem is simplified to a series of sums
    output.reverse() 
    for i in range(100):
        for j in range(1, len(output)):
            output[j] = (output[j-1] + output[j]) % 10
    output.reverse()

    return ''.join(str(i) for i in output[:8])

def main():
    with open('16.in') as f:
        input_signal = f.readline().strip() * 10000
    print(fft(input_signal))

def test():
    assert fft('03036732577212944063491565474664' *  10000) == '84462026'
    assert fft('02935109699940807407585447034323' *  10000) == '78725270'
    assert fft('03081770884921959731165446850517' *  10000) == '53553731'

if __name__ == '__main__':
    #test()
    main()
