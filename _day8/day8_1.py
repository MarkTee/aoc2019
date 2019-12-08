from collections import Counter

def main():
    # get image
    with open('8.in') as f:
        image = f.readline().rstrip()

    # separate image into layers
    layer_size = 25 * 6
    layers = [image[i:i + layer_size] for i in range(0, len(image), layer_size)]

    # determine which layer has the fewest 0 digits
    fewest_zeros = float('inf')
    fewest_zeros_layer = None
    for i, layer in enumerate(layers):
        zero_count = layer.count('0')
        if zero_count < fewest_zeros:
            fewest_zeros = zero_count
            fewest_zeros_layer = i

    # count occurence of each digit
    c = Counter(layers[fewest_zeros_layer])
    # print number of 1 digits multiplied by the number of 2 digits
    print(c['1'] * c['2'])

if __name__ == '__main__':
    main()
