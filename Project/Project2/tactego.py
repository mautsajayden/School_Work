import random

EMPTY_CELL = " "

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
#   pieces_file (str) – name of the file containing blue and red piece setups
#   length (int) – number of rows in the game grid
#   width  (int) – number of columns in the game grid
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
                start_length, start_width, end_length, end_width = start_end_index(start, end, grid_table)
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

        # Execute the move / combat 
        isMove, red_flags, blue_flags, grid_table, winner = move_rules(False, start_value, end_value, current, red_flags, blue_flags,start_length, start_width, end_length, end_width, grid_table)

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

    # If loop exits naturally 
    if blue_flags == 0:
        display_grid(grid_table, length, width)
        print("R has won the game")
    elif red_flags == 0:
        display_grid(grid_table, length, width)
        print("B has won the game")

#----Get the file name with the pieces----
def filename_pieces(name_file):

    file_pieces = []
    blue_pieces = []
    red_pieces = []
    piece_power = []
    num_piece = []
    
    with open(name_file) as file:
        for f in file:
            file_pieces.append(f)
        
    for line in file_pieces:
        piece = line.split()
        piece_power.append(piece[0])
        num_piece.append(int(piece[1]))
    
    for i in range(len(num_piece)):
        for j in range(num_piece[i]):
            red_pieces.append('R' + piece_power[i])
            blue_pieces.append('B' + piece_power[i])
            
    random.shuffle(red_pieces) 
    random.shuffle(blue_pieces)
                    
    return blue_pieces , red_pieces

#----Create the board and the pieces, and place them onto the board randomly as specified here----
def make_grid(length, width, blue_pieces, red_pieces):

    #makes an empty 2D grid table 
    grid_table = []
    for j in range(length):
        row = []
        for j in range(width):
            row.append(EMPTY_CELL)
        grid_table.append(row)

    # place red pieces in top half
    index_R = 0
    R_flags = 0

    for i in range(length):
        for j in range(width):
            if index_R < len(red_pieces):
                grid_table[i][j] = red_pieces[index_R]
                if len(red_pieces[index_R]) >= 2 and red_pieces[index_R][1] == FLAG:
                    R_flags += 1
                index_R += 1

    #  place blue pieces in bottom half
    index_blue = 0
    B_flags = 0

    for i in range(length - 1, -1, -1):
        for j in range(width):
            if index_blue < len(blue_pieces):
                grid_table[i][j] = blue_pieces[index_blue]
                if len(blue_pieces[index_blue]) >= 2 and blue_pieces[index_blue][1] == FLAG:
                    B_flags += 1
                index_blue += 1

    return grid_table, R_flags, B_flags

#Draw the board
def display_grid(grid_table, length, width):
    # Print header indices
    print("    ", end="")
    for j in range(width):
        # match sample spacing a bit
        print(f"{j}", end="   ")
    print()
    for i in range(length):
        print(f"  {i}", end=" ")
        for j in range(width):
            cell = grid_table[i][j]
            # ensure empty cell prints as spaces
            if cell == EMPTY_CELL:
                print("   ", end=" ")
            else:
                print(f"{cell}", end=" ")
        print()

#Get the player's move.
def enter_moves(current):

    print("Current Turn is : ", current)
    start_pos = input("Select Piece to Move by Position >> ")
    move_pos = input("Select Position to move Piece >> ")

    return start_pos, move_pos

#re-look
def validate_position(start, end):

    pos = start.strip().split()
    if len(pos) != 2:
        print("Thers is no space between your cordinates")
        return False

    if not pos[0].isdigit() or not pos[1].isdigit():
        print("Thers is not a number between your cordinates")
        return False

    pos2 = end.strip().split()
    if len(pos2) != 2:
        print("Thers is no space between your cordinates")
        return False

    if not pos2[0].isdigit() or not pos2[1].isdigit():
        print("Thers is not a number between your cordinates")
        return False

    return True


def start_end_index(start, end, grid_table):
    
    s = start.split()
    e = end.split()
    return int(s[0]), int(s[1]), int(e[0]), int(e[1])


def start_end_value(start_length, start_width, end_length, end_width, grid_table):
    return grid_table[start_length][start_width], grid_table[end_length][end_width]


def alternate_turn(current):
    if current == RED_PIECE:
        return BLUE_PIECE
    return RED_PIECE


def validate_turn(start_val, current_player):
    # start_val must be a piece belonging to current_player and not a flag and not EMPTY
    if start_val == EMPTY_CELL:
        return F
    # flag cannot move
    if len(start_val) >= 2 and start_val[1] == FLAG:
        return F
    piece_owner = start_val[0]
    return piece_owner == current_player


def switch_position(grid_table, start_length, start_width, end_length, end_width):
    grid_table[end_length][end_width] = grid_table[start_length][start_width]
    grid_table[start_length][start_width] = EMPTY_CELL
    return grid_table


def move_rules(isMove, start_value, end_value, current, red_flag, blue_flag,start_length, start_width, end_length, end_width, grid_table):
    """
    Perform the move and apply combat rules (including extra-credit A/S/M).
    Returns tuple: (isMove, red_flag, blue_flag, grid_table, winner)
    winner is 'R' or 'B' or None.
    """
    winner = None

    # tokens after first character (color)
    start_symble = EMPTY_CELL
    if len(start_value) > 1:
        start_symble = start_value[1:]

    end_symbol = EMPTY_CELL
    if end_value != EMPTY_CELL and len(end_value) > 1:
        end_symbol = end_value[1:]

    # If moving into empty cell: simple move
    if end_value == EMPTY_CELL:
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return True, red_flag, blue_flag, grid_table, None

    # If moving into a flag -> capture flag
    if end_symbol == FLAG:
        # attacker current captures defender's flag
        if end_value[0] == RED_PIECE:
            # captured a red flag
            red_flag -= 1
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            if red_flag == 0:
                winner = BLUE_PIECE
        else:
            # captured a blue flag
            blue_flag -= 1
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            if blue_flag == 0:
                winner = RED_PIECE
        return True, red_flag, blue_flag, grid_table, winner

    # Now handle extra-credit pieces and mines/sapper/assassin interactions

    # If defender is a mine
    if end_symbol == MINE:
        # Sapper attacking mine: sapper disarms mine and moves into cell
        if start_symble == SAPPER:
            # mine removed, sapper moves into mine cell
            grid_table[end_length][end_width] = grid_table[start_length][start_width]
            grid_table[start_length][start_width] = EMPTY_CELL
            return True, red_flag, blue_flag, grid_table, None
        else:
            # any other attacker (including assassin) gets defeated; mine is removed afterwards
            grid_table[start_length][start_width] = EMPTY_CELL  # attacker removed
            grid_table[end_length][end_width] = EMPTY_CELL    # mine removed
            return True, red_flag, blue_flag, grid_table, None

    # If attacker is assassin
    if start_symble == ASSASSIN:
        # Assassin attacking any non-mine piece defeats it
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return True, red_flag, blue_flag, grid_table, None

    # If defender is assassin (attacker attacking an assassin): assassin loses if attacked
    if end_symbol == ASSASSIN:
        # attacker loses, defender (assassin) stays
        grid_table[start_length][start_width] = EMPTY_CELL
        return True, red_flag, blue_flag, grid_table, None

    # Sapper vs Sapper: attacker wins (treat as equal numeric -> attacker wins)
    if start_symble == SAPPER and end_symbol == SAPPER:
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return True, red_flag, blue_flag, grid_table, None

    # If either is Sapper (and not handled above)
    if start_symble == SAPPER and end_symbol != MINE:
        # sapper attacks non-mine non-sapper: sapper has strength 0 so loses against any numeric defender
        # but project text says "it will be defeated by any piece if it is attacked" (meaning when sapper is defender).
        # When sapper attacks a numeric piece, regular strength rules apply; sapper has strength 0 -> will lose unless defender also 0 or special
        # So treat sapper as strength 0
        try_parse_start = start_symble
        # start_strength = 0
        # determine defender numeric strength if any
        if end_symbol.isdigit():
            # sapper (0) vs numeric -> sapper loses
            grid_table[start_length][start_width] = EMPTY_CELL
            return True, red_flag, blue_flag, grid_table, None
        else:
            # defender is non-numeric (shouldn't occur here), fallback to switching
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
            return True, red_flag, blue_flag, grid_table, None

    # If defender is Sapper and attacker is numeric (not S)
    if end_symbol == SAPPER and start_symble.isdigit():
        # any piece attacking a sapper defeats it
        grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        return True, red_flag, blue_flag, grid_table, None

    # At this point both are numeric pieces (normal combat)
    if start_symble.isdigit() and end_symbol.isdigit():
        if int(start_symble) >= int(end_symbol):
            grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
        else:
            # attacker loses
            grid_table[start_length][start_width] = EMPTY_CELL
        return True, red_flag, blue_flag, grid_table, None

    # Catch-all fallback: perform a simple switch
    grid_table = switch_position(grid_table, start_length, start_width, end_length, end_width)
    return True, red_flag, blue_flag, grid_table, None

if __name__ == '__main__':
    random.seed(input('What is seed? '))
    tactego("small_game.pieces", 6, 4)
