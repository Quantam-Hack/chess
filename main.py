
import pygame
import random

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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
quantum_mode = False
quantum_moves = []
quantum_piece = None
quantum_positions = []

quantum_board = {}  # {(r, c): [(piece, color), ...]} for superposed states


def get_square_from_pos(x, y):
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def highlight_moves(win, moves):
    for move in moves:
        pygame.draw.rect(win, GREEN, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def get_possible_moves(piece, row, col):
    moves = []
    color = piece[0]
    opponent = 'b' if color == 'w' else 'w'

    if piece[1] == 'p':
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] == "":
            moves.append((row + direction, col))
        if row == start_row and board[row + direction][col] == "" and board[row + 2 * direction][col] == "":
            moves.append((row + 2 * direction, col))
        for dc in [-1, 1]:
            nr, nc = row + direction, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board[nr][nc] != "" and board[nr][nc][0] == opponent:
                    moves.append((nr, nc))

    elif piece[1] == 'r':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == "":
                        moves.append((r, c))
                    elif board[r][c][0] == opponent:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

    elif piece[1] == 'b':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == "":
                        moves.append((r, c))
                    elif board[r][c][0] == opponent:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

    elif piece[1] == 'q':
        moves.extend(get_possible_moves(color + 'r', row, col))
        moves.extend(get_possible_moves(color + 'b', row, col))

    elif piece[1] == 'n':
        deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "" or board[r][c][0] == opponent:
                    moves.append((r, c))

    elif piece[1] == 'k':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "" or board[r][c][0] == opponent:
                    moves.append((r, c))

    return moves

# (The beginning remains unchanged up to draw_board...)

def draw_instructions(win):
    font = pygame.font.SysFont("Arial", 28, bold=True)
    instructions = [
        "Press ENTER to start playing",
        "Press Q to enter quantum mode",
        "In quantum mode, click two possible moves",
        "Press M to collapse to one location"
    ]
    
    total_height = len(instructions) * 40
    start_y = (HEIGHT - total_height) // 2  # Center vertically

    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))  # ⬛ Black text
        text_rect = text.get_rect(center=(WIDTH // 2, start_y + i * 40))  # Center horizontally
        win.blit(text, text_rect)


def draw_board(win, board, show_instructions=False):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if (row, col) in quantum_board:
                for piece in quantum_board[(row, col)]:
                    ghost_surface = PIECE_IMAGES[piece].copy()
                    ghost_surface.set_alpha(128)  # 👻 Transparent piece
                    win.blit(ghost_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif board[row][col] != "":
                win.blit(PIECE_IMAGES[board[row][col]], (col * SQUARE_SIZE, row * SQUARE_SIZE))

            if selected_pos == (row, col):
                pygame.draw.rect(win, SELECTED_BORDER_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    if show_instructions:
        draw_instructions(win)

    if quantum_mode:  # 🔮 Show quantum banner
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render("Quantum Mode Active", True, (0, 0, 255))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))

    

def is_in_check(color):
    king_pos = None
    opponent_color = 'b' if color == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            if board[r][c] == color + 'k':
                king_pos = (r, c)
                break
        if king_pos:
            break

    for r in range(8):
        for c in range(8):
            if board[r][c] != '' and board[r][c][0] == opponent_color:
                moves = get_possible_moves(board[r][c], r, c)
                if king_pos in moves:
                    return True
    return False

def has_any_moves(color):
    for r in range(8):
        for c in range(8):
            if board[r][c] != '' and board[r][c][0] == color:
                moves = get_possible_moves(board[r][c], r, c)
                for move in moves:
                    # Try the move
                    saved = board[move[0]][move[1]]
                    board[move[0]][move[1]] = board[r][c]
                    board[r][c] = ''
                    in_check = is_in_check(color)
                    board[r][c] = board[move[0]][move[1]]
                    board[move[0]][move[1]] = saved
                    if not in_check:
                        return True
    return False

def show_message(win, text):
    font = pygame.font.SysFont("Arial", 40, bold=True)
    surface = font.render(text, True, (255, 0, 0))
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(surface, rect)
    pygame.display.update()
    pygame.time.wait(3000)

def main():
    global selected_piece, selected_pos, turn, quantum_mode, quantum_moves, quantum_piece, quantum_positions
    run = True
    clock = pygame.time.Clock()
    load_images()
    game_started = False

    while run:
        clock.tick(60)
        draw_board(WIN, board, show_instructions=not game_started)
        if game_started and selected_piece:
            moves = get_possible_moves(selected_piece, selected_pos[0], selected_pos[1])
            highlight_moves(WIN, moves)

        if game_started:
            # 🛡 Check if a king has been removed from the board
            white_king_exists = any(board[r][c] == 'wk' for r in range(8) for c in range(8))
            black_king_exists = any(board[r][c] == 'bk' for r in range(8) for c in range(8))

            if not white_king_exists:
                show_message(WIN, "Black Wins!")
                pygame.time.wait(3000)
                run = False
                continue
            elif not black_king_exists:
                show_message(WIN, "White Wins!")
                pygame.time.wait(3000)
                run = False
                continue

            # ♟ Classic check/checkmate logic
            if is_in_check('w'):
                if not has_any_moves('w'):
                    show_message(WIN, "Black Wins!")
                    pygame.time.wait(3000)
                    run = False
                elif selected_piece is None:
                    show_message(WIN, "White King in Check!")
            elif is_in_check('b'):
                if not has_any_moves('b'):
                    show_message(WIN, "White Wins!")
                    pygame.time.wait(3000)
                    run = False
                elif selected_piece is None:
                    show_message(WIN, "Black King in Check!")



        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_RETURN:
                    game_started = True
                elif event.key == pygame.K_q:
                    quantum_mode = not quantum_mode
                    if not quantum_mode:
                        quantum_moves = []
                        quantum_piece = None
                        quantum_positions = []
                        selected_piece = None
                        selected_pos = None
                elif event.key == pygame.K_m and quantum_piece and len(quantum_positions) == 2:
                    chosen = random.choice(quantum_positions)
                    board[chosen[0]][chosen[1]] = quantum_piece
                    for pos in quantum_positions:
                        if pos != chosen:
                            board[pos[0]][pos[1]] = ""
                        if pos in quantum_board:
                            del quantum_board[pos]
                    quantum_piece = None
                    quantum_positions = []
                    selected_piece = None
                    quantum_mode = False
                    turn = 'black' if turn == 'white' else 'white'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    continue

                x, y = event.pos
                row, col = get_square_from_pos(x, y)

                if quantum_mode:
                    if not quantum_piece:
                        if board[row][col] != "" and ((turn == 'white' and board[row][col][0] == 'w') or (turn == 'black' and board[row][col][0] == 'b')):
                            quantum_piece = board[row][col]
                            selected_pos = (row, col)
                            selected_piece = board[row][col]

                            valid_moves = get_possible_moves(quantum_piece, selected_pos[0], selected_pos[1])
                            if len(valid_moves) == 1:
                                only_pos = valid_moves[0]
                                board[selected_pos[0]][selected_pos[1]] = ""
                                board[only_pos[0]][only_pos[1]] = quantum_piece
                                quantum_piece = None
                                quantum_positions = []
                                selected_piece = None
                                selected_pos = None
                                quantum_mode = False
                                turn = 'black' if turn == 'white' else 'white'
                    else:
                        valid_moves = get_possible_moves(quantum_piece, selected_pos[0], selected_pos[1])
                        if (row, col) not in quantum_positions and (row, col) in valid_moves:
                            quantum_positions.append((row, col))
                            board[row][col] = quantum_piece
                            quantum_board[(row, col)] = [quantum_piece]
                            if len(quantum_positions) == 2:
                                board[selected_pos[0]][selected_pos[1]] = ""
                                selected_piece = None
                                selected_pos = None
                else:
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

    pygame.quit()

if __name__ == "__main__":
    main()
