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

selected_piece = None
selected_pos = None
turn = 'white'

def get_square_from_pos(x, y):
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def highlight_moves(win, moves):
    for move in moves:
        pygame.draw.rect(win, (0, 255, 0), (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def get_possible_moves(piece, row, col):
    moves = []

    if piece == "wp":
        if row > 0 and board[row - 1][col] == "":
            moves.append((row - 1, col))
        if row == 6 and board[row - 2][col] == "" and board[row - 1][col] == "":
            moves.append((row - 2, col))
        if row > 0 and col > 0 and board[row - 1][col - 1] != "" and board[row - 1][col - 1][0] == 'b':
            moves.append((row - 1, col - 1))
        if row > 0 and col < 7 and board[row - 1][col + 1] != "" and board[row - 1][col + 1][0] == 'b':
            moves.append((row - 1, col + 1))

    elif piece == "bp":
        if row < 7 and board[row + 1][col] == "":
            moves.append((row + 1, col))
        if row == 1 and board[row + 2][col] == "" and board[row + 1][col] == "":
            moves.append((row + 2, col))
        if row < 7 and col > 0 and board[row + 1][col - 1] != "" and board[row + 1][col - 1][0] == 'w':
            moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and board[row + 1][col + 1] != "" and board[row + 1][col + 1][0] == 'w':
            moves.append((row + 1, col + 1))

    elif piece in ["wr", "br"]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board[r][c] == "":
                        moves.append((r, c))
                    elif board[r][c][0] != piece[0]:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

    elif piece in ["wb", "bb"]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board[r][c] == "":
                        moves.append((r, c))
                    elif board[r][c][0] != piece[0]:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

    elif piece in ["wq", "bq"]:
        moves.extend(get_possible_moves(piece[0] + "r", row, col))
        moves.extend(get_possible_moves(piece[0] + "b", row, col))

    elif piece in ["wn", "bn"]:
        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] == "" or board[r][c][0] != piece[0]:
                    moves.append((r, c))

    elif piece in ["wk", "bk"]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] == "" or board[r][c][0] != piece[0]:
                    moves.append((r, c))

    return moves

def draw_board(win, board):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[row][col]
            if piece != "":
                win.blit(PIECE_IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

            if selected_pos == (row, col):
                pygame.draw.rect(win, SELECTED_BORDER_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def find_king(color):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece == f"{color[0]}k":
                return r, c
    return None

def is_king_in_check(color):
    king_pos = find_king(color)
    if not king_pos:
        return False
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece != "" and piece[0] != color[0]:
                moves = get_possible_moves(piece, r, c)
                if king_pos in moves:
                    return True
    return False

def has_legal_moves(color):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece != "" and piece[0] == color[0]:
                moves = get_possible_moves(piece, r, c)
                for move in moves:
                    orig_piece = board[move[0]][move[1]]
                    board[move[0]][move[1]] = piece
                    board[r][c] = ""
                    in_check = is_king_in_check(color)
                    board[r][c] = piece
                    board[move[0]][move[1]] = orig_piece
                    if not in_check:
                        return True
    return False

def draw_end_message(text):
    font = pygame.font.SysFont(None, 64)
    msg_surface = font.render(text, True, (255, 0, 0))
    rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(msg_surface, rect)
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global selected_piece, selected_pos, turn
    run = True
    clock = pygame.time.Clock()
    load_images()

    while run:
        clock.tick(60)
        draw_board(WIN, board)

        if selected_piece:
            moves = get_possible_moves(selected_piece, selected_pos[0], selected_pos[1])
            highlight_moves(WIN, moves)

        # Display "Check!" if king is under threat
        if is_king_in_check(turn):
            font = pygame.font.SysFont(None, 48)
            check_surface = font.render("Check!", True, (255, 0, 0))
            WIN.blit(check_surface, (WIDTH // 2 - 60, HEIGHT - 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = get_square_from_pos(x, y)

                if selected_piece is None:
                    piece = board[row][col]
                    if piece != "" and ((turn == 'white' and piece[0] == 'w') or (turn == 'black' and piece[0] == 'b')):
                        selected_piece = piece
                        selected_pos = (row, col)
                else:
                    moves = get_possible_moves(selected_piece, selected_pos[0], selected_pos[1])
                    if (row, col) in moves:
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = ""
                        turn = 'black' if turn == 'white' else 'white'
                    selected_piece = None

        # Victory check
        all_pieces = [p for row_ in board for p in row_]
        if "wk" not in all_pieces:
            draw_end_message("Black wins!")
            run = False
        elif "bk" not in all_pieces:
            draw_end_message("White wins!")
            run = False

        # Checkmate
        if is_king_in_check(turn):
            if not has_legal_moves(turn):
                winner = 'White' if turn == 'black' else 'Black'
                draw_end_message(f"Checkmate! {winner} wins!")
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()

