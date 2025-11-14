import random

def tactego(pieces_file, length, width):
    
    blue_pieces , red_pieces = filename_pieces(pieces_file)
    
    grid_table = make_grid(length,width,blue_pieces,red_pieces)
    
    move(grid_table,length,width)

def filename_pieces(name_file):
    
    file_pieces = [ ]
    blue_pieces, red_pieces = [ ],[ ]
    
    with open(name_file) as file:
        for f in file :
            file_pieces.append(f)
        
    piece_power = [ ]
    num_piece = []
    
    for i in file_pieces :
        piece =  i.split()
        piece_power.append(piece[0])
        num_piece.append((int(piece[1])))
    
    for i in range(len(num_piece)):
        for j in range(num_piece[i]):
            red_pieces.append('R' + piece_power[i])
            blue_pieces.append('B' + piece_power[i])
            
    random.shuffle(red_pieces) 
    random.shuffle(blue_pieces)
                    
    return blue_pieces , red_pieces


def make_grid(length,width,blue_pieces,red_pieces):
         
    grid_table = []
    
    for i in range(length):
        grid_row = []
        for j in range(width):
            grid_row.append(" ")
        grid_table.append(grid_row)
    
    n = b = 0
    
    for i in range(length):
        for j in range(width):
            if( i == 0 or i == 1 ):
                if n < len(red_pieces):
                    grid_table[i][j] = red_pieces[n]
                    n += 1
    
    for i in range(length - 1, -1, -1):  
        for j in range(width):
            if( i == length-1 or i == length-2 ):
                if b < len(blue_pieces):
                    grid_table[i][j] = blue_pieces[b]
                    b += 1
        
    return grid_table
    
def move(grid_table, length, width):
    
    n = 0
    player_turns = []
    
    for i in range(4):
        
        display_grid(grid_table, length, width)
        
        prev_pos = input("Select Piece to Move by Position >> ")
        nex_pos  = input("Select Position to move Piece >> ")
        
        nex_length, nex_width, prev_length, prev_width = prev_nex_pos(prev_pos, nex_pos)
        
        starter = grid_table[prev_length][prev_width]
        
        # n and player_turns returned updated
        n, player_turns = check_rules(grid_table, starter, 
                                      nex_length, nex_width, 
                                      prev_length, prev_width, 
                                      n, player_turns)


def display_grid(grid_table,length,width):
    for i in range(length):
        for j in range(width):
            print(grid_table[i][j], end=" ")
        print()


def prev_nex_pos(prev_pos, nex_pos):
    prev_pos = prev_pos.split()
    nex_pos  = nex_pos.split()
    return int(nex_pos[0]), int(nex_pos[1]), int(prev_pos[0]), int(prev_pos[1])


def check_rules(grid_table, current, nex_length, nex_width,
                prev_length, prev_width, n, player_turns):

    # invalid start square
    if (grid_table[prev_length][prev_width] == " " 
        or grid_table[nex_length][nex_width] in ["BF","RF"]):
        print("You must select a starting position with one of your pieces, not a flag.")

    starter = grid_table[prev_length][prev_width]
    nex_starter = grid_table[nex_length][nex_width]

    # --- TURN CHECK LOGIC (unchanged, just fixed) ---
    player_turns.append(current[0])  # R or B

    # check move distance
    isCheck_move = (abs(nex_length - prev_length) <= 1) and \
                   (abs(nex_width - prev_width) <= 1)

    if not isCheck_move:
        print("You moved more than 1 length size")

    # check own piece collision
    if starter[0] == nex_starter[0]:
        print("You moved to a position containing your own piece")

    # perform swap
    grid_table[prev_length][prev_width], grid_table[nex_length][nex_width] = \
        grid_table[nex_length][nex_width], grid_table[prev_length][prev_width]

    # combat check
    if starter[0] != nex_starter[0] and nex_starter != " ":
        print("Its now combat time")

    # update turn index
    n += 1

    # --- DOUBLE PLAY CHECK ---
    if n == 2:
        if player_turns[0] == player_turns[1]:
            print("Someone has played 2 times")
        # reset for next cycle
        player_turns.clear()
        n = 0

    return n, player_turns

        

def combat_rules():
    n=0
    

    
    
if __name__ == '__main__':
    
   random.seed(input('What is seed? '))
   
   #file_name = input('What is the filename for the pieces? ')
   #length = int(input('What is the length? '))
   #width = int(input('What is the width? '))
   #tactego(file_name, length, width)
   
   tactego("Project/Project2/small_game.pieces", 6, 4)