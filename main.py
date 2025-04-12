import pygame
print(pygame.__version__)



# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Load piece images
PIECE_IMAGES = {}

def load_images():
    pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
    for piece in pieces:
        try:
            image = pygame.image.load(f"{piece}.png")
            scale_factor = 3.8
            size = int(SQUARE_SIZE * scale_factor)
            PIECE_IMAGES[piece] = pygame.transform.scale(image, (size, size))
        except Exception as e:
            print(f"Failed to load {piece}.png: {e}")

# Colors
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)
SELECTED_BORDER_COLOR = (255, 0, 0)  # Red for selected pieces

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Chess")

board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

# Define a function to handle piece selection and movement
selected_piece = None
selected_pos = None
turn = 'white'  # White moves first

def get_square_from_pos(x, y):
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def highlight_moves(win, moves):
    for move in moves:
        pygame.draw.rect(win, (0, 255, 0), (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)


def get_possible_moves(piece, row, col):
    moves = []
    
    if piece == "wp":  # White pawn movement rules
        # Move one square forward if the square is empty
        if row > 0 and board[row - 1][col] == "":
            moves.append((row - 1, col))

        # Move two squares forward from the starting position if both squares are empty
        if row == 6 and board[row - 2][col] == "" and board[row - 1][col] == "":
            moves.append((row - 2, col))

        # Capture diagonally (to the left and right)
        if row > 0 and col > 0 and board[row - 1][col - 1] != "" and board[row - 1][col - 1][0] == 'b':
            moves.append((row - 1, col - 1))
        if row > 0 and col < 7 and board[row - 1][col + 1] != "" and board[row - 1][col + 1][0] == 'b':
            moves.append((row - 1, col + 1))

    elif piece == "bp":  # Black pawn movement rules
        # Move one square forward if the square is empty
        if row < 7 and board[row + 1][col] == "":
            moves.append((row + 1, col))

        # Move two squares forward from the starting position if both squares are empty
        if row == 1 and board[row + 2][col] == "" and board[row + 1][col] == "":
            moves.append((row + 2, col))

        # Capture diagonally (to the left and right)
        if row < 7 and col > 0 and board[row + 1][col - 1] != "" and board[row + 1][col - 1][0] == 'w':
            moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and board[row + 1][col + 1] != "" and board[row + 1][col + 1][0] == 'w':
            moves.append((row + 1, col + 1))

    elif piece == "wr" or piece == "br":  # Rook movement rules
        # Rooks move horizontally or vertically any number of squares
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            new_row, new_col = row, col
            while True:
                new_row += direction[0]
                new_col += direction[1]
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    if board[new_row][new_col] == "":
                        moves.append((new_row, new_col))
                    elif board[new_row][new_col][0] != piece[0]:  # Opponent's piece
                        moves.append((new_row, new_col))
                        break
                    else:
                        break  # Own piece, stop moving
                else:
                    break  # Out of bounds, stop moving

    elif piece == "wb" or piece == "bb":  # Bishop movement rules
        # Bishops move diagonally any number of squares
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            new_row, new_col = row, col
            while True:
                new_row += direction[0]
                new_col += direction[1]
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    if board[new_row][new_col] == "":
                        moves.append((new_row, new_col))
                    elif board[new_row][new_col][0] != piece[0]:  # Opponent's piece
                        moves.append((new_row, new_col))
                        break
                    else:
                        break  # Own piece, stop moving
                else:
                    break  # Out of bounds, stop moving

    elif piece == "wq" or piece == "bq":  # Queen movement rules (rook + bishop)
        # A queen can move like both a rook and a bishop
        moves.extend(get_possible_moves("wr", row, col))  # Rook-like moves
        moves.extend(get_possible_moves("wb", row, col))  # Bishop-like moves

    elif piece == "wn" or piece == "bn":  # Knight movement rules
        # Knights move in "L" shapes: two squares in one direction, one square perpendicular to that
        knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for direction in knight_moves:
            new_row, new_col = row + direction[0], col + direction[1]
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if board[new_row][new_col] == "" or board[new_row][new_col][0] != piece[0]:  # Empty or opponent's piece
                    moves.append((new_row, new_col))

    elif piece == "wk" or piece == "bk":  # King movement rules
        # The king can move one square in any direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if board[new_row][new_col] == "" or board[new_row][new_col][0] != piece[0]:  # Empty or opponent's piece
                    moves.append((new_row, new_col))

    return moves


def draw_board(win, board):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            # Draw checkerboard squares
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw piece if one exists at (row, col)
            piece = board[row][col]
            if piece != "":
                win.blit(PIECE_IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

            # Draw red border around selected piece
            if selected_pos == (row, col):
                pygame.draw.rect(win, SELECTED_BORDER_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def main():
    global selected_piece, selected_pos, turn
    run = True
    clock = pygame.time.Clock()
    load_images()

    while run:
        clock.tick(60)
        draw_board(WIN, board)

        if selected_piece:
            # Get possible moves for the selected piece
            moves = get_possible_moves(selected_piece, selected_pos[0], selected_pos[1])
            highlight_moves(WIN, moves)
            print(f"Selected piece: {selected_piece} at {selected_pos}")
            print(f"Possible moves: {moves}")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = get_square_from_pos(x, y)

                if selected_piece is None:
                    # Select a piece if clicked on
                    piece = board[row][col]
                    # Check if the piece belongs to the current player
                    if piece != "" and (turn == 'white' and piece[0] == 'w') or (turn == 'black' and piece[0] == 'b'):
                        selected_piece = piece
                        selected_pos = (row, col)
                        print(f"Piece selected: {selected_piece} at {selected_pos}")
                else:
                    # Move the selected piece if valid
                    moves = get_possible_moves(selected_piece, selected_pos[0], selected_pos[1])
                    if (row, col) in moves:
                        # Move the piece
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = ""
                        # Switch turn after the move
                        if turn == 'white':
                            turn = 'black'
                        else:
                            turn = 'white'
                        selected_piece = None  # Deselect piece
                        print(f"Piece moved to {row}, {col}")
                        print(f"Board state: {board}")
                        print(f"Turn: {turn}")  # Display current turn

    pygame.quit()

if __name__ == "__main__":
    main()