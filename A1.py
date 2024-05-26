import random

def is_single_letter(input_str):
    # to ensure the input is a letter.
    return isinstance(input_str, str) and len(input_str) == 1 and input_str.isalpha()

def init():
    line = input('Enter the four letters used for left, right, up, and down move (e.g., l r u d) > ')
    try:
        left, right, up, down = map(str, line.strip().split())  # Split the input and map to strings
        left, right, up, down = left.lower(), right.lower(), up.lower(), down.lower()  # Convert to lowercase
        if(left==right or left==up or left==down or right==up or right==down or up == down):    
            print('Repeated input!',end=' ');    
            return init()   
        if is_single_letter(left) and is_single_letter(right) and is_single_letter(up) and is_single_letter(down):
            return left, right, up, down
        else:
            print('Invalid input!',end=' ')
            return init()
    except:
        print("Invalid input!",end=' ')
        return init()

def create_board():
    # Continuously generate a solvable 3x3 puzzle until one is created
    while True:
        numbers = list(range(1, 9)) + [None]
        random.shuffle(numbers)
        if is_solvable(numbers):
            return [numbers[n:n+3] for n in range(0, 9, 3)]

def is_solvable(numbers):
    # Check if the generated puzzle is solvable using the inversion count
    inversions = 0
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            if numbers[i] is not None and numbers[j] is not None and numbers[i] > numbers[j]:
                inversions += 1

    # If the board is edven-sized, adjust inversions based on the row number of the empty space
    if len(numbers) % 2 == 0:
        row_empty = numbers.index(None) // 3
        inversions += row_empty

    # Puzzle is solvable if the total inversions count is even
    return inversions % 2 == 0

def print_board(board):
    # Display the current state of the board
    for row in board:
        print(' '.join([' ' if i is None else str(i) for i in row]))

def get_valid_moves(board, left, right, up, down):
    # Determine valid moves based on the empty space position
    valid_moves = []
    for i, row in enumerate(board):
        if None in row:
            j = row.index(None)
            break
    if i > 0: valid_moves.append(down)
    if i < 2: valid_moves.append(up)
    if j > 0: valid_moves.append(right)
    if j < 2: valid_moves.append(left)
    return valid_moves

def get_move(valid_moves,left, right, up, down):
    # Prompt the user for a move and validate it
    move_prompts = {left: "left", right: "right", up: "up", down: "down"}
    move_prompt = ", ".join([f"{move_prompts[move]}-{move}" for move in valid_moves])
    while True:
        try:
            player_move = input(f'Enter your move ({move_prompt})> ').lower()
            if player_move in valid_moves:
                return player_move
            else:
                # print(f'Invalid move! Please enter left-{left}, right-{right}, up-{up}, or down-{down} > ')
                print(f'Invalid move!',end=' ')
                print_board(board)
                get_move(valid_moves,left, right, up, down)
        except:
            continue

def make_move(board, player_move, left, right, up, down):
    # Update the board based on the player's move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                break
        if board[i][j] is None:
            break

    if player_move == left and j < 2:
        board[i][j], board[i][j+1] = board[i][j+1], board[i][j]
    elif player_move == right and j > 0:
        board[i][j], board[i][j-1] = board[i][j-1], board[i][j]
    elif player_move == up and i < 2:
        board[i][j], board[i+1][j] = board[i+1][j], board[i][j]
    elif player_move == down and i > 0:
        board[i][j], board[i-1][j] = board[i-1][j], board[i][j]

def is_solved(board):
    # Check if the board is in the solved state
    return board == [[1, 2, 3], [4, 5, 6], [7, 8, None]]

def replay_game():
    choice = input('Enter "n" for another game, or "q" to end the game > ').strip().lower()
    if (choice=='n'):
        play_game()
    elif (choice=='q'):
        exit()
    else:
        print("Invalid input!",end=' ')
        replay_game()
        
def play_game():
    # Main function to play the game
    
    board = create_board()
    moves = 0
    while True:
        print_board(board)
        valid_moves = get_valid_moves(board, left, right, up, down)
        player_move = get_move(valid_moves, left, right, up, down)
        make_move(board, player_move, left, right, up, down)
        moves += 1
        if is_solved(board):
            print(f'Congratulations! You solved the puzzle in {moves} moves!')
            replay_game()
                    
        

if __name__ == '__main__':
    left, right, up, down = init()
    play_game()
