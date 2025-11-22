import random

EMPTY_CELL = " "
NUM_2 = 2

ASSASSIN = 'A'
SAPPER = 'S'
MINE = 'M'

RED_PIECE = 'R'
BLUE_PIECE = 'B'
FLAG = 'F'

F = False
T = True

def tactego(pieces_file, length, width):
#-----------------------------------------------------------
# Function: tactego
# Parameters:
#   pieces_file  – name of the file containing blue and red piece setups
#   length  – number of rows in the game grid
#   width   – number of columns in the game grid
# Returns: None
# Description:
#   Main game function. Reads the pieces file, builds the game board,
#   places red and blue pieces, and starts the main game loop.
#-----------------------------------------------------------

    # the variables 
    start = EMPTY_CELL
    end = EMPTY_CELL
    start_value = EMPTY_CELL
    end_value = EMPTY_CELL
    start_length = 0
    start_width = 0
    end_length = 0
    end_width = 0

    #returns 2 list with blue and red pieces 
    blue_pieces, red_pieces = filename_pieces(pieces_file)

    #returns the number of flags and a updated grid with pieces 
    grid_table, blue_flags, red_flags = make_grid(length, width, blue_pieces, red_pieces)

    #start player 
    current = RED_PIECE

    # continue while both sides still have flags
    while blue_flags > 0 and red_flags > 0:

        #draws the grid
        display_grid(grid_table, length, width)

        # Get a valid move from the current player
        valid_move = F

        while not valid_move:

            #returns the playesrs moves 
            start, end = enter_moves(current)

            # Validates the rules for the entered positions by player
            if not validate_position(start, end):
                valid_move = F
            else:
                start_length, start_width, end_length, end_width = start_end_index(start, end)
                # checks if is inside board
                in_bounds = (0 <= start_length < length and 0 <= start_width < width and 0 <= end_length < length and 0 <= end_width < width)

                if not in_bounds:
                    print("One or both positions are out of bounds.")
                    valid_move = F
                else:
                    start_value, end_value = start_end_value(start_length, start_width, end_length, end_width, grid_table)
                    # validate that starting piece belongs to current and is not a flag and not empty
                    if not validate_turn(start_value, current):
                        print("You must select a starting position with one of your pieces, not a flag.")
                        valid_move = F
                    else:
                        # sees if move is at most one in each direction
                        if not (abs(end_length - start_length) <= 1 and abs(end_width - start_width) <= 1):
                            print("You can only move one square in any direction.")
                            valid_move = F
                        else:
                            # cannot move onto your own piece
                            if end_value != EMPTY_CELL and end_value[0] == current:
                                print("You cannot move onto your own piece.")
                                valid_move = F
                            else:
                                # disallow moving a mine 
                                starter = start_value[1:] if len(start_value) > 1 else ''
                                if starter == MINE:
                                    print("Cannot move a mine.")
                                    valid_move = F
                                else:
                                    valid_move = T

        # combat begins
        isMove, red_flags, blue_flags, grid_table, winner = combat_move_rules(False, start_value, end_value, current, red_flags, blue_flags,start_length, start_width, end_length, end_width, grid_table)

        # If winner found, announce and break out
        if winner == RED_PIECE:
            display_grid(grid_table, length, width)
            print("R has won the game")
            return 
        if winner == BLUE_PIECE:
            display_grid(grid_table, length, width)
            print("B has won the game")
            return 

        # Alternate turn
        current = alternate_turn(current)
 
#----Get the file name with the pieces----
def filename_pieces(name_file):
#-----------------------------------------------------------
# Function: filename_pieces
# Parameters:
#   name_file string – name of the file that contains pieces
#
# Returns:
#   blue_pieces list – list representing blue player's pieces
#   red_pieces list  – lisT  representing red player's pieces
#
# Description:
#   Opens and reads the pieces file. Extracts, validates, and stores all
#   piece types and positions for both red and blue sides.
#-----------------------------------------------------------
    file_pieces = []
    blue_pieces = []
    red_pieces = []
    piece_power = []
    num_piece = []
    
    #gets pieces from the file 
    with open(name_file) as file:
        for f in file:
            file_pieces.append(f)
    #gets the piece power and piece symbol 
    for line in file_pieces:
        piece = line.split()
        piece_power.append(piece[0])
        num_piece.append(int(piece[1]))
    
    #creates the pieces for R and B 
    for i in range(len(num_piece)):
        for j in range(num_piece[i]):
            red_pieces.append('R' + piece_power[i])
            blue_pieces.append('B' + piece_power[i])

    #shuffles the red then blue       
    random.shuffle(red_pieces) 
    random.shuffle(blue_pieces)
                    
    return blue_pieces , red_pieces

#----Create the board and the pieces, and place them onto the board randomly as specified here----
def make_grid(length, width, blue_pieces, red_pieces):
#-----------------------------------------------------------
# Function: make_grid
# Parameters:
#   length  – rows of the board
#   width   – columns of the board
#   blue_pieces  – list of blue pieces and locations
#   red_pieces   – list of red pieces and locations
# Returns:
#   grid_table (2D list)   grid with all pieces placed
#   red_flags   – number of red flags on the board
#   blue_flags – number of blue flags on the board
# Description:
#   Creates a 2D grid used for the Tactego board, fills it with EMPTY_CELL,
#   and places all red and blue pieces red up and blue bottom.
#-----------------------------------------------------------
    #makes an empty 2D grid table 
    grid_table = []
    for j in range(length):
        row = []
        for j in range(width):
            row.append(EMPTY_CELL)
        grid_table.append(row)

    # place red pieces in top 
    index_R = 0
    R_flags = 0

    for i in range(length):
        for j in range(width):
            if index_R < len(red_pieces):
                grid_table[i][j] = red_pieces[index_R]
                if len(red_pieces[index_R]) >= NUM_2 and red_pieces[index_R][1] == FLAG:
                    R_flags += 1
                index_R += 1

    #  place blue pieces in bottom 
    index_blue = 0
    B_flags = 0

    for i in range(length - 1, -1, -1):
        for j in range(width):
            if index_blue < len(blue_pieces):
                grid_table[i][j] = blue_pieces[index_blue]
                if len(blue_pieces[index_blue]) >= NUM_2 and blue_pieces[index_blue][1] == FLAG:
                    B_flags += 1
                index_blue += 1

    return grid_table, R_flags, B_flags

#Draw the board
def display_grid(grid_table, length, width):
#-----------------------------------------------------------
# Function: display_grid
# Parameters:
#   grid_table  – 2D list representing the current board
#   length  – number of rows in the grid
#   width   – number of columns in the grid
# Returns: nothing
#-------------------------------------------------------

    # Print header indices
    print("    ", end="")
    for j in range(width):
        print(f"{j}", end="   ")
    print()
    for i in range(length):
        print(f"  {i}", end=" ")
        for j in range(width):
            n = grid_table[i][j]
            if n == EMPTY_CELL:
                print("   ", end=" ")
            else:
                print(f"{n}", end=" ")
        print()

#Get the player's move.
def enter_moves(current):

#-----------------------------------------------------------
# Function: enter_moves
# Parameters:
#   current – the current player ('R' or 'B')
# Returns:
#   start_pos  – input string for the piece's starting position
#   move_pos   – input string for the desired ending position
# Description:
#   Prompts the current player to enter the coordinates of a piece
#   they want to move and where they want to move it. Does not validate.
#-----------------------------------------------------------

    print("Current Turn is : ", current)
    start_pos = input("Select Piece to Move by Position >> ")
    end_pos = input("Select Position to move Piece >> ")

    return start_pos, end_pos

def validate_position(start, end):
#-----------------------------------------------------------
# Function: validate_position
# Parameters:
#   start  – starting position input string
#   end    – ending position input string
# Returns:
#   True if both start and end positions are valid num coordinates
#   with exactly two values; otherwise False.
# Description:
#   Checks whether both coordinate strings are formatted correctly,
#   contain exactly two values, and both values are digits.
#-----------------------------------------------------------
    pos = start.strip().split()

    if len(pos) != NUM_2:
        print("Thers is no space between your cordinates")
        return F

    if not pos[0].isdigit() or not pos[1].isdigit():
        print("Thers is not a number between your cordinates")
        return F

    pos2 = end.strip().split()
    if len(pos2) != NUM_2:
        print("Thers is no space between your cordinates")
        return F

    if not pos2[0].isdigit() or not pos2[1].isdigit():
        print("Thers is not a number between your cordinates")
        return F

    return T


def start_end_index(start, end):
#-----------------------------------------------------------
# Function: start_end_index
# Parameters:
#   start  – starting coordinate 
#   end    – ending coordinate 
#   grid_table  – game board 
# Returns:
#   start_row (int), start_col (int), end_row (int), end_col (int)
# Description:
#   Converts start/end coordinate strings into integer indices
#   used for indexing into the grid.
#-----------------------------------------------------------
    s = start.split()
    e = end.split()

    return int(s[0]), int(s[1]), int(e[0]), int(e[1])


def start_end_value(start_length, start_width, end_length, end_width, grid_table):
#-----------------------------------------------------------
# Function: start_end_value
# Parameters:
#   start_length , start_width  starting cell coordinates
#   end_length   , end_width    ending cell coordinates
#   grid_table  – 2D board
# Returns:
#   start_value  – piece at the start location
#   end_value    – piece at the end location
# Description:
#   Retrieves the board values located at the chosen start
#   and end positions.
#-----------------------------------------------------------
    return grid_table[start_length][start_width], grid_table[end_length][end_width]


def alternate_turn(current):
#-----------------------------------------------------------
# Function: alternate_turn
# Parameters:
#   current  – current player symbol R or  B
# Returns: current 
# Description:
#   Switches the active player after a turn ends.
#-----------------------------------------------------------

    if current == RED_PIECE:
        return BLUE_PIECE
    
    return RED_PIECE


def validate_turn(start_val, current_player):
#-----------------------------------------------------------
# Function: validate_turn
# Parameters:
#   start_val  – piece selected by the player
#   current_player  – 'R' or 'B'
# Returns:
#   True if the piece belongs to the current player and is movable.
#   Returns F (False) if the piece is empty or a flag.
# Description:
#   Ensures the selected piece belongs to the current player,
#   is not an EMPTY_CELL, and is not a FLAG 
#-----------------------------------------------------------

    if start_val == EMPTY_CELL:
        return F
    # flag cannot move
    if len(start_val) >= 2 and start_val[1] == FLAG:
        return F
    
    piece_owner = start_val[0]

    return piece_owner == current_player


def switch_position(grid_table, start_length, start_width, end_length, end_width):
#-----------------------------------------------------------
# Function: switch_position
# Parameters:
#   grid_table  – game board
#   start_length  ,start_width  – old position
#   end_length, end_width    – new position
# Returns:
#   grid_table  – updated board
# Description:
#   Moves a piece from its start position to the end position
#   and replaces the start position with EMPTY_CELL.
#-----------------------------------------------------------
    grid_table[end_length][end_width] = grid_table[start_length][start_width]
    grid_table[start_length][start_width] = EMPTY_CELL

    return grid_table

def combat_move_rules(isMove, start_value, end_value, current, red_flag, blue_flag,start_length, start_width, end_length, end_width, grid_table):
#-----------------------------------------------------------
# Function: move_rules
# Parameters:
#   isMove  – indicates if movement was valid before combat
#   start_value  – attacking piece
#   end_value    – defending piece
#   current  – current player R or B
#   red_flag  – remaining red flags
#   blue_flag  – remaining blue flags
#   start_length , start_width – start coords
#   end_length   , end_width    – end coords
#   grid_table  – game grid
# Returns:
#
#   winner = R, B, or None
# Description:
#    movement and combat rules
#     - simple moves into empty cells high low power
#     - capturing flags
#     - mine/sapper 
#     - assassin rules
#     - sapper combat behavior
#     - numeric piece combat 
#-----------------------------------------------------------

    winner = None

    #  after first character 
    start_symble = EMPTY_CELL
    if len(start_value) > 1:
        start_symble = start_value[1:]

    end_symbol = EMPTY_CELL
    if end_value != EMPTY_CELL and len(end_value) > 1:
        end_symbol = end_value[1:]

    if end_value == EMPTY_CELL:
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return T, red_flag, blue_flag, grid_table, None

    #  attacking a  flag
    if end_symbol == FLAG:
        # attacker current defender's flag
        if end_value[0] == RED_PIECE:
            # attacking red flag
            red_flag -= 1
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            if red_flag == 0:
                winner = BLUE_PIECE
        else:
            # attacking a blue flag
            blue_flag -= 1
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            if blue_flag == 0:
                winner = RED_PIECE
        return T, red_flag, blue_flag, grid_table, winner

    #extra-credit pieces and mines/sapper/assassin 

    #  defender is a mine
    if end_symbol == MINE:
        # Sapper attacking mine: sapper disarms mine and moves into cell
        if start_symble == SAPPER:
            # mine removed
            grid_table[end_length][end_width] = grid_table[start_length][start_width]
            grid_table[start_length][start_width] = EMPTY_CELL
            return T, red_flag, blue_flag, grid_table, None
        else:
            # any other attacker gets defeated
            grid_table[start_length][start_width] = EMPTY_CELL  
            grid_table[end_length][end_width] = EMPTY_CELL   
            return T, red_flag, blue_flag, grid_table, None

    #  attacker is assassin
    if start_symble == ASSASSIN:
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return T, red_flag, blue_flag, grid_table, None

    # assassin vs assasin
    if end_symbol == ASSASSIN:
        grid_table[start_length][start_width] = EMPTY_CELL
        return T, red_flag, blue_flag, grid_table, None

    if start_symble == SAPPER and end_symbol == SAPPER:
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return T, red_flag, blue_flag, grid_table, None

    if start_symble == SAPPER and end_symbol != MINE:
       
        if end_symbol.isdigit():
            grid_table[start_length][start_width] = EMPTY_CELL
            return T, red_flag, blue_flag, grid_table, None
        else:
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            return T, red_flag, blue_flag, grid_table, None

    if end_symbol == SAPPER and start_symble.isdigit():
        # any piece attacking a sapper defeats it
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return T, red_flag, blue_flag, grid_table, None

    if start_symble.isdigit() and end_symbol.isdigit():
        if int(start_symble) >= int(end_symbol):
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        else:
            # attacker loses
            grid_table[start_length][start_width] = EMPTY_CELL
        return T, red_flag, blue_flag, grid_table, None

    grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
    return T, red_flag, blue_flag, grid_table, None

if __name__ == '__main__':

    isplay = 'yes'

    while  isplay.lower() == 'yes' :

        random.seed(input('What is seed? '))
        file_name = input('What is the filename for the pieces? ')
        length = int(input('What is the length? '))
        width = int(input('What is the width? '))
        tactego(file_name, length, width)
        print()
        print()
        isplay = input('Do you want to play again no or yes: ')
    
            
   
