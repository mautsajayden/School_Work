"""
    Come up with a name for the game
    nop-jump-mathetics game
    JMPs and HLTs
"""

import random

GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6


def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(['nop', f'add {random_points}', f'sub {random_points}', f'mul {random_points}', f'jmp {random_position}', 'hlt'], weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)

    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 1 + r][column_start + 1 + k] = c


def roll_dice():
    """
        Call this function once per turn.

        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)


#my code starts here 

"""
File: game_logic.py
Author: Jayden Mautsa
Date: October 24, 2025
Email: jmautsa1@umbc.edu
Project : 1 
Description: This program runs a dice-based instruction game.
"""

ADD = "add"
MUL = "mul"
SUB = "sub"
NO_OP = "nop"
JMP =  "jmp"
HLT = "hlt"

def ask_user():
    """
    :prompt: Asks the user to enter the board size and seed
<<<<<<< HEAD
    :return: the seed and size as integers to use for generating the map.
=======
    :return: the seed and size as integers to use for generating the map
>>>>>>> 2d97ead326870d3ffb8791f1c55c5e7f8f949e29
    """
    size_seed = input("Board Size and Seed: ")

    parts = size_seed.split()

    size = int(parts[0])

    seed = int(parts[1])

    return seed, size


def value(instr_word):
    """
    :param instr_word: a string that includes a number
    :return: the integer number taken from the string
    """
    #splits the word to get the integer 
    word = instr_word.split()

    num = int(word[1])
    
    return num


def jump_instruction(position, message, map_size, score, roll, game_map):
    """
    :param position: the current position of the player on the board
    :param message: the instruction that contains the jump command 
    :param map_size: the total number of squares on the board
    :param score: the players current score before jumping
    :param roll: the dice value from the current turn
    :param game_map: the list that holds all the boards instructions
    :return: the new position, score, roll, and finished status after the jump is done
    """

    # Jump to the new position
    position = value(message) 

    # Get instruction at the jump location
    next_message = game_map[position]  
    
    position, score, roll, finished = instructions(next_message, position, score, roll, map_size, game_map)

    return position, score, roll, finished


def control_position(position, map_size, roll):
    """
    :param position: the current position on the board before moving
    :param map_size: the total length of the board
    :param roll: the dice value used to move forward
    :return: the new position after moving. Wraps around if the move goes past the board size
    """
    #check if position is off bound 
    if (position + roll) >= map_size: position = (position + roll) % map_size

    else:position += roll

    return position

def instructions(message, position, score, roll, map_size, game_map):

    """"
    :param message: the instruction currently being executed
    :param position: the players position on the board before executing the instruction
    :param score: the players current score
    :param roll: the dice value used for this move
    :param map_size: the size of the map to control movement and wrapping
    :param game_map: the list that holds all board instructions
    :return: updated position, score, roll, and finished 
    """
    roll = roll_dice()

    #adds the score & the runs the positin 
    if ADD in message:

        score += value(message)

        position = control_position(position, map_size, roll)

    #sub the score & the runs the positin 
    elif SUB in message:

        score -= value(message)

        position = control_position(position, map_size, roll)

    #multiplies the score & the runs the positin 
    elif MUL in message:
        score *= value(message)

        position = control_position(position, map_size, roll)

    #nop just changes the position  
    elif (NO_OP in message):

        position = control_position(position, map_size, roll)

    #jumps to the next position 
    elif JMP in message:

        position, score, roll, finished = jump_instruction(position, message, map_size, score, roll, game_map)

        return position, score, roll, finished

    #stops game when posiotion on map is HLT
    elif HLT in message:
        print(f"Final Pos: {position} Final Score: {score}, Instruction {message}")
        yes_no = input("Would you like to play again Y or N: ").lower()
        if "y" in yes_no:
            main()
        else:
            return position, score, roll, True

    return position, score, roll, False

#displays the map
def display_grid(the_grid):
    """
<<<<<<< HEAD
    :param the_grid: the grid that was created using make_grid.
    :return: prints the full grid to the screen in a formatted layout.
=======
    :param the_grid: the grid that was created using make_grid
    :return: prints the full grid to the screen in a formatted layout
>>>>>>> 2d97ead326870d3ffb8791f1c55c5e7f8f949e29
    """
    
    for row in the_grid:
        print(''.join(row))

#plays the game
def play_game(game_map):
    """
<<<<<<< HEAD
    :param game_map: the list of instructions created by generate_random_map.
    :return: runs the main gameplay loop, handling dice rolls, moves, and commands until the game ends.
=======
    :param game_map: the list of instructions created by generate_random_map
    :return: runs the main gameplay loop, handling dice rolls, moves, and commands until the game ends
>>>>>>> 2d97ead326870d3ffb8791f1c55c5e7f8f949e29
    """
    seed_num, map_size = ask_user()
    random.seed(seed_num)

    game_map = generate_random_map(map_size, seed_num)

    the_grid = make_grid(map_size)
<<<<<<< HEAD
=======
    
>>>>>>> 2d97ead326870d3ffb8791f1c55c5e7f8f949e29
    for index in range(map_size):
        fill_grid_square(the_grid, map_size, index, game_map[index])

    display_grid(the_grid)

    position = 0
    score = 0
    roll = 0
    finished = False

    while not finished:
        command = game_map[position]
        position, score, roll, finished = instructions(command, position, score, roll, map_size, game_map)
        print("Pos:", position, "Score:", score, ", Instruction:", command, "Rolled:", roll)

    if not finished:
        print(f"Final Pos: {position} Final Score: {score}, Instruction {game_map[position]}")

def main():
    """
<<<<<<< HEAD
    :purpose: starts the JMPs and HLTs game and controls the overall program flow.
    :return: none.
    """

    message = []

    play_game(message)

if __name__ == "__main__":
    main()

=======
    :purpose: starts the JMPs and HLTs game and controls the overall program flow
    :return: none.
    """
    yes_no = "y"

    while yes_no == "y":
        
        message = []

        play_game(message)

        yes_no = input("Would you like to play again Y or N: ").lower()

    
if __name__ == "__main__":
    main()

>>>>>>> 2d97ead326870d3ffb8791f1c55c5e7f8f949e29
