from itertools import chain

def print_decoded_image(image, col_length, row_length):
    # separate image into layers
    layer_size = col_length * row_length
    layers = [image[i:i + layer_size] for i in range(0, len(image), layer_size)]
    # flatten layers
    flattened_image = [''.join(pixel) for pixel in zip(*layers)]
    # remove zeros from the flattened image (i.e. ignore transparency)
    opaque_image = [pixel.replace('2', '') for pixel in flattened_image]
    # only examine the topmost visible pixel in each location
    decoded_image = [pixel[0] for pixel in opaque_image]

    # print the decoded image to the terminal
    for row in range(row_length):
        for col in range(col_length):
            # print white pixel
            if decoded_image[(row * col_length) + col] == '0':
                print(u"\u2591", end='')
            # print black pixel
            else:
                print(u"\u2588", end='')
        print()

def main():
    # get image
    with open('8.in') as f:
        image = f.readline().rstrip()

    print_decoded_image(image, 25, 6)

def test():
    image = '0222112222120000'
    print_decoded_image(image, 2, 2)

if __name__ == '__main__':
    # test()
    main()
