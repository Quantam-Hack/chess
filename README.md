# chess

1. Constants & Variables:

    Board size (WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE).

    Piece images loaded into PIECE_IMAGES dictionary.

    Colors defined for UI elements (e.g., white, gray, green for move highlights).

2. Game Variables:

    selected_piece, selected_pos: Track selected piece and its position.

    turn: Indicates whose turn it is ('white' or 'black').

    quantum_mode: A boolean that activates quantum mode.

    quantum_moves, quantum_positions: Track quantum moves and superposition states.

3. Helper Functions:

    get_square_from_pos(x, y): Converts mouse clicks to board positions.

    highlight_moves(win, moves): Highlights valid move squares.

    get_possible_moves(piece, row, col): Calculates valid moves for each piece type.

4. Drawing Functions:

    draw_instructions(win): Displays game instructions.

    draw_board(win, board): Draws the chessboard and pieces on the screen.

5. Game Logic:

    is_in_check(color): Checks if the king of a color is in check.

    has_any_moves(color): Checks if the player has valid moves left.

    show_message(win, text): Displays messages like "Check" or "Game Over."

6. Quantum Mode:

    A piece can exist in multiple positions (superposition).

    Players select two valid positions, and the piece collapses to one position.

    Activated by pressing "Q" and collapsed by pressing "M."

7. Main Game Loop (main()):

    Initializes the game, loads images, and handles user interactions (clicks, keypresses).

    Moves pieces, checks for check/checkmate, and toggles quantum mode.

Conclusion:
The game is a standard chess implementation enhanced with a quantum mechanic, allowing pieces to occupy multiple squares at once and collapse into one. It uses Pygame for graphical rendering and user input handling, with the added complexity of quantum moves to make the gameplay more strategic.

--------------------------------------------------------------------------------------------------------------
1. Mahathi (Frontend and Graphics Handling)
    Role: Mahathi was responsible for the graphical user interface (UI) and how the chessboard and pieces are displayed.

    Responsibilities:

    Rendering the Chessboard and Pieces:

    Created functions like draw_board(win, board) to render the chessboard and all pieces on the screen.

    Managed the loading and displaying of piece images from PIECE_IMAGES.

    Highlighting Valid Moves:

    Implemented the highlight_moves(win, moves) function to highlight possible valid moves for a selected piece.

    Handling User Input (Mouse and Key Presses):

    Implemented event handlers for mouse clicks (to select and move pieces).

    Set up keyboard event handling to toggle quantum mode with the "Q" key and collapse superposition with the "M" key.

2. Reshma (Game Logic and Chess Rules)
    Role: Reshma worked on the core game logic, which involves implementing chess rules, calculating valid moves, and handling game states like check and checkmate.

    Responsibilities:

    Piece Movement and Validity:

    Developed the get_possible_moves(piece, row, col) function to calculate valid moves for each piece type (king, queen, rook, etc.).

    Ensured that the rules of movement for different pieces (e.g., rook, bishop) were correctly followed.

    Check and Checkmate Logic:

    Implemented the functions is_in_check(color) to check if the player's king is under threat.

    Wrote has_any_moves(color) to determine if the player has any valid moves left.

    Game State Management:

    Managed the turn order (white/black) and checked for game-ending conditions like checkmate or stalemate.

3. Sahasara (Quantum Mode and Superposition)
    Role: Sahasara handled the implementation of quantum mode, which allows a piece to exist in multiple positions at once (superposition) and then collapse into a single square when selected.

    Responsibilities:

    Implementing Quantum Mechanics:

    Designed and implemented the quantum_moves and quantum_positions to track the superposition states of pieces.

    Created logic to allow a piece to exist in multiple squares, giving the player the ability to select two positions in quantum mode.

    Managed the collapse of superposition when the player selects one of the positions, updating the board accordingly.

    Quantum Mode Activation:

    Implemented the toggling of quantum mode via the "Q" key and collapse using the "M" key.

    Ensured that the quantum feature interacted correctly with the standard chess game rules, including movement and game state transitions.

Final Notes:
    Mahathi was primarily in charge of the visual aspects and UI components, including drawing the board and handling player input.

    Reshma focused on the core logic of the game, ensuring the chess rules and game states like check and checkmate were accurately implemented.

    Sahasara worked on the innovative quantum mode, adding the quantum mechanics element and ensuring it interacted smoothly with the rest of the game.

    This division of labor allowed each person to focus on a key aspect of the game while ensuring the final product was both functional and engaging.



