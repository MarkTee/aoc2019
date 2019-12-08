from itertools import chain

def main():
    # get image
    with open('8.in') as f:
        image = f.readline().rstrip()

    # separate image into layers
    layer_size = 25 * 6
    layers = [image[i:i + layer_size] for i in range(0, len(image), layer_size)]
    # flatten layers
    flattened_image = [''.join(pixel) for pixel in zip(*layers)]
    # remove zeros from the flattened image (i.e. ignore transparency)
    opaque_image = [pixel.replace('2', '') for pixel in flattened_image]
    # only examine the topmost visible pixel in each location
    decoded_image = [pixel[0] for pixel in opaque_image]

    # print the decoded image to the terminal
    for row in range(6):
        for col in range(25):
            # print black pixel
            if decoded_image[(row * 25) + col] == '0':
                print(u"\u2588", end='')
            # print white pixel
            else:
                print(u"\u2591", end='')
        print()

if __name__ == '__main__':
    main()
