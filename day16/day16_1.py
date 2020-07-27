def fft(signal, phase):
    """Execute Flawed Frequency Transmission algorithm, as described in the
    problem statement.
    """
    signal_length = len(signal)
    base_pattern = [0, 1, 0, -1]

    # execute the given number of phases of the algorithm
    for phase_i in range(phase):
        output_signal = []
        output_i = 1

        # calculate each digit of the output list for the given phase
        while output_i < signal_length + 1:
            pattern = [digit for digit in base_pattern for i in range(output_i)]
            digit_list = []

            # iterate over the signal's digits to calculate the ith output signal digit
            for digit_i in range(signal_length):
                digit = int(signal[digit_i]) * pattern[(digit_i + 1) % len(pattern)] # offset pattern by 1
                digit_list.append(digit)

            output_digit = abs(sum(digit_list)) % 10 # only keep the ones digit
            output_signal.append(output_digit)

            output_i += 1

        signal = output_signal

    output_signal_int = ''.join(str(digit) for digit in output_signal)
    return output_signal_int

def main():
    with open('16.in') as f:
        input_signal = f.readline().strip()
    print(fft(input_signal, phase=100)[:8])

def test():
    input_signal = '12345678'
    assert fft(input_signal, phase=1) == '48226158'
    assert fft(input_signal, phase=2) == '34040438'
    assert fft(input_signal, phase=3) == '03415518'
    assert fft(input_signal, phase=4) == '01029498'

    assert fft('80871224585914546619083218645595', phase=100)[:8] == '24176176'
    assert fft('19617804207202209144916044189917', phase=100)[:8] == '73745418'
    assert fft('69317163492948606335995924319873', phase=100)[:8] == '52432133'

if __name__ == '__main__':
    #test()
    main()
