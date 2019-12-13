import os
from subprocess import Popen, PIPE

def send_game_input(cabinet, signal):
    """Send input to the cabinet (to control the jostick).

    Valid signals:
    -1 : move the paddle to the left
     0 : keep the paddle in its current position
     1 : move the paddle to the right.
    """
    signal = str(signal) + '\n'
    cabinet.stdin.write(signal.encode())
    cabinet.stdin.flush()

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

def draw_game(tile_coordinates, max_x, max_y):
    """Prints the contents of the game's grid to the terminal."""
    tiles = {0: u"\u2591",
             1: u"\u2588",
             2: 'x',
             3: '-',
             4: 'o'}

    # as described in the problem statement, this unique (x, y) value tracks
    # the player's current score
    score = 0
    if (-1, 0) in tile_coordinates:
        score = tile_coordinates[(-1, 0)]

    # assemble game grid
    grid = []
    # create rows
    for y in range(max_y):
        row = []
        # create columns
        for x in range(max_x):
            tile = tile_coordinates[(x, y)]
            row.append(tile)
        grid.append(row)

    # print game grid to the terminal
    for row in grid:
        for tile in row:
            print(tiles[tile], end='')
        print()
    print("Score: {}".format(score))

def run_game(program_filename):
    """Run the game. The final grid will be printed to the terminal."""
    cabinet = Popen('python3 ../IntcodePrograms/IntcodeComputer.py {}'.format(program_filename),
                    shell=True,
                    stdin=PIPE,
                    stdout=PIPE)
    tile_coordinates = {}
    max_x = 0
    max_y = 0
    paddle_position = 0
    ball_position = 0

    # run game until subprocess terminates
    while cabinet.poll() is None:
        # get game output (description of tiles)
        x, y, tile_id = get_game_output(cabinet)
        tile_coordinates[(x, y)] = tile_id

        # keep track of the dimensions of the game's grid
        max_x = max(x + 1, max_x)
        max_y = max(y, max_y)

        # always move paddle under the ball's current position
        if tile_id == 3:
            paddle_position = x
        elif tile_id == 4:
            ball_position = x

            if paddle_position == ball_position:
                send_game_input(cabinet, 0)
            elif paddle_position < ball_position:
                send_game_input(cabinet, 1)
            elif paddle_position > ball_position:
                send_game_input(cabinet, -1)

        # clear the terminal and print the game
        os.system('clear')
        draw_game(tile_coordinates, max_x, max_y)

def main():
    program_filename = '../IntcodePrograms/13.in'
    run_game(program_filename)

if __name__ == '__main__':
    main()
