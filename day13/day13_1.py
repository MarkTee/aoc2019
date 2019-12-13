from subprocess import Popen, PIPE

def get_game_output(cabinet):
    """Gets the next output signal from the arcade cabinet.

    Output signals are of the form:
        x - tile's distance from the left
        y - tile's distance from the top
        tile_id - the type of tile
    """
    x = int(cabinet.stdout.readline().decode().rstrip())
    y = int(cabinet.stdout.readline().decode().rstrip())
    tile_id = int(cabinet.stdout.readline().decode().rstrip())
    return x, y, tile_id

def draw_game(grid, max_x, max_y):
    """Prints the contents of the game's grid to the terminal."""
    tiles = {0: u"\u2591",
             1: u"\u2588",
             2: 'x',
             3: '-',
             4: 'o'}
    block_count = 0 # keep track of the number of blocks being drawn
    # draw rows
    for y in range(max_y):
        # draw columns
        for x in range(max_x):
            tile = grid[(x, y)]
            print(tiles[tile], end='')
            if tile == 2:
                block_count += 1
        print()
    return block_count

def run_game(program_filename):
    """Run the game. The final grid will be printed to the terminal."""
    cabinet = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program_filename),
                    shell=True,
                    stdin=PIPE,
                    stdout=PIPE)
    grid = {}
    max_x = 0
    max_y = 0
    while True:
        try:
            # check if the game has sent any more output
            x, y, tile_id = get_game_output(cabinet)
        except ValueError:
            break

        # keep track of the dimensions of the grid
        max_x = max(x + 1, max_x)
        max_y = max(y, max_y)

        grid[(x, y)] = tile_id

    # print the final state of the game to the terminal
    block_count = draw_game(grid, max_x, max_y)
    print(block_count)

def main():
    program_filename = '../IntcodePrograms/13.in'
    run_game(program_filename)

if __name__ == '__main__':
    main()
