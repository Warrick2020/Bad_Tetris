import random
import os

# Tetris shapes
SHAPES = [
    [['.','.','.','.'],
     ['.','#','#','#'],
     ['.','.','.','.'],
     ['.','.','.','.']],
    
    [['.','.','.','.'],
     ['.','.','#','.'],
     ['.','#','#','#'],
     ['.','.','.','.']],
    
    [['.','.','.','.'],
     ['#','#','#','#'],
     ['.','.','.','.'],
     ['.','.','.','.']],
    
    [['.','#','.','.'],
     ['.','#','#','.'],
     ['.','.','#','.'],
     ['.','.','.','.']],
    
    [['.','.','#','.'],
     ['.','.','#','.'],
     ['.','#','#','.'],
     ['.','.','.','.']],
    
    [['.','.','#','.'],
     ['.','#','#','.'],
     ['.','#','.','.'],
     ['.','.','.','.']],
    
    [['.','#','#','.'],
     ['.','#','#','.'],
     ['.','.','.','.'],
     ['.','.','.','.']],
]

# Game settings
WIDTH = 10
HEIGHT = 20
HIGH_SCORE_FILE = "highscore.txt"

def create_board():
    """Create an empty game board."""
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_board(board, score, high_score):
    """Draw the game board with score and high score."""
    print('Score: ' + str(score).rjust(10) + '   ' + 'High Score: ' + str(high_score).rjust(10))
    for i, row in enumerate(board):
        print(' '.join(row).center(WIDTH * 2 + 10))
    print()

def generate_shape():
    """Generate a random Tetris shape."""
    return random.choice(SHAPES)

def place_shape(board, shape, x, y):
    """Place the shape on the board at the given position."""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == '#':
                board[y + row][x + col] = '#'

def check_collision(board, shape, x, y):
    """Check if the shape collides with the board or other shapes."""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == '#':
                if x + col < 0 or x + col >= WIDTH or y + row >= HEIGHT or board[y + row][x + col] == '#':
                    return True
    return False

def remove_complete_lines(board):
    """Remove any completed lines from the board."""
    lines_to_remove = []
    for row in range(HEIGHT):
        if '.' not in board[row]:
            lines_to_remove.append(row)
    for row in lines_to_remove:
        del board[row]
        board.insert(0, ['.'] * WIDTH)

def read_high_score():
    """Read the high score from the file."""
    if not os.path.isfile(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, 'r') as file:
        try:
            return int(file.read())
        except ValueError:
            return 0

def write_high_score(score):
    """Write the high score to the file."""
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

def play_tetris():
    """Play a game of Tetris."""
    print("Play NOW")
    input("Press Enter to start...")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    
    board = create_board()
    current_shape = generate_shape()
    x, y = WIDTH // 2 - len(current_shape[0]) // 2, 0
    score = 0
    high_score = read_high_score()
    
    while not check_collision(board, current_shape, x, y):
        board_copy = [row[:] for row in board]  # Create a copy of the board
        place_shape(board_copy, current_shape, x, y)
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        draw_board(board_copy, score, high_score)
        
        user_input = input("Use WASD or Space to move the shape: ")
        if user_input.lower() == 'w':
            rotated_shape = list(zip(*reversed(current_shape)))
            if not check_collision(board, rotated_shape, x, y):
                current_shape = rotated_shape
            y += 1  # Automatically move down after each rotation
        elif user_input.lower() == 'a':
            if not check_collision(board, current_shape, x - 1, y):
                x -= 1
            y += 1  # Automatically move down after each left movement
        elif user_input.lower() == 'd':
            if not check_collision(board, current_shape, x + 1, y):
                x += 1
            y += 1  # Automatically move down after each right movement
        elif user_input.lower() == 's':
            if not check_collision(board, current_shape, x, y + 1):
                y += 1
        elif user_input.lower() == ' ':
            while not check_collision(board, current_shape, x, y + 1):
                y += 1
        
        if check_collision(board, current_shape, x, y + 1):
            place_shape(board, current_shape, x, y)
            remove_complete_lines(board)
            score += 1
            if score > high_score:
                high_score = score
                write_high_score(high_score)
            current_shape = generate_shape()
            x, y = WIDTH // 2 - len(current_shape[0]) // 2, 0
    
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    draw_board(board, score, high_score)
    input("Press Enter to quit...")

# Start the game
play_tetris()
