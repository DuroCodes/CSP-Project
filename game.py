from utils import prompt, color, Colors, clear_screen
from board import check_winner, create_board, fill_box, print_board
from typing import List, Optional, Tuple


def num_to_arr(num: int, rows: int) -> List[int]:
    i = (num - 1) // rows
    j = (num - 1) % rows
    return [i, j]


def arr_to_num(arr: List[int]) -> int:
    """
    Converts a 2D array to a 1D array

    Parameters:
        `arr (List[int])`: A 2D array representing the row and column

    Returns:
        `int`: The 1D array representation of the 2D array

    Example:
        `arr_to_num([1, 1]) -> 4`: Calculated as 1 * 3 + 1 + 1 = 4
    """
    return arr[0] * len(arr) + arr[1] + 1


def parse_player_move(board: List[List[str]], move: str) -> bool:
    """
    Parses the player's move and checks if it is valid

    Parameters:
        `board (List[List[str]])`: The current board
        `move (str)`: The player's move

    Returns:
        `bool`: True if the move is valid, False otherwise
    """
    try:
        int(move)
    except ValueError:
        return False

    move_arr = num_to_arr(int(move), len(board))

    return move.isdigit() and 1 <= int(move) <= 9 \
        and board[move_arr[0]][move_arr[1]] == " "


def ask_player_move(board: List[List[str]], player: str) -> List[int]:
    move = prompt(f"[*] Your Move {player} -> (1-9)?: ",
                  parser=lambda x: parse_player_move(board, x),
                  error_message="Invalid move, please try again."
                  )
    return num_to_arr(int(move), len(board))


def ask_player_char() -> str:
    char = prompt("[*] Choose your character (X/O): ",
                  parser=lambda x: x.lower() in ["x", "o"],
                  error_message="Invalid character, please try again."
                  )
    return [color("X", Colors.red), color("O", Colors.blue)][["x", "o"].index(char)]


def minimax(board: List[List[str]], maximizing: bool, depth: int, ai_char: str, human_char: str) -> int:
    """
    Minimax algorithm for the AI to determine the best move

    Parameters:
        `board (List[List[str]])`: The current board
        `maximizing (bool)`: True if the AI is maximizing, False otherwise
        `depth (int)`: The current depth of the tree
        `ai_char (str)`: The AI's character (X/O)
        `human_char (str)`: The human's character (X/O)

    Returns:
        `int`: The best score for the move
    """
    res = check_winner(board)
    rows, cols = len(board), len(board[0])

    if res != ' ':
        if res == 'T':
            return 0
        if res == human_char:
            return -100
        return 100

    if maximizing:
        best_score = -100
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == ' ':
                    board[i][j] = ai_char
                    score = minimax(board, False, depth +
                                    1, ai_char, human_char)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score - depth

    best_score = 100
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == ' ':
                board[i][j] = human_char
                score = minimax(board, True, depth + 1, ai_char, human_char)
                board[i][j] = ' '
                best_score = min(score, best_score)

    return best_score - depth


def best_move(
    board: List[List[str]], ai_char: str, human_char: str
) -> Optional[Tuple[int, int]]:
    """
    Determines the best move for the AI to make using the minimax algorithm

    Parameters:
        `board (List[List[str]])`: The current board
        `ai_char (str)`: The AI's character (X/O)
        `human_char (str)`: The human's character (X/O)

    Returns:
        `Optional[Tuple[int, int]]`: The best move for the AI to make ([row, col])
    """
    best_score = -100
    best_move = None
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                board[i][j] = ai_char
                score = minimax(board, False, 0, ai_char, human_char)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move


def play(rows: int, cols: int):
    board = create_board(rows, cols)
    clear_screen()
    print("[*] Welcome to Tic Tac Toe! [*]")

    chars = [color("X", Colors.red), color("O", Colors.blue)]

    human = ask_player_char()
    ai = chars[1 - chars.index(human)]
    filled = 0
    winner = ' '
    ai_last_turn = 0
    player_turn = human == color("X", Colors.red)

    while filled < rows * cols:
        if player_turn:
            clear_screen()
            print_board(board)
            print("[*] Waiting for your move..." if ai_last_turn ==
                  0 else f"[*] AI Move: {ai} -> {ai_last_turn}")
            human_move = ask_player_move(board, human)

            fill_box(board, human_move[0], human_move[1], human)
        else:
            ai_move = best_move(board, ai, human)

            if ai_move is None:
                break

            row, col = ai_move

            fill_box(board, row, col, ai)
            ai_last_turn = arr_to_num(list(ai_move))

        if check_winner(board) != ' ':
            winner = check_winner(board)
            break

        player_turn = not player_turn
        filled += 1

    clear_screen()

    if winner == human:
        print("[*] You won! [*]")
    elif winner == ai:
        print("[*] You lost! [*]")
    else:
        print("[*] Tie! [*]")

    return print_board(board)
