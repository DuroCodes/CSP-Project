from utils import color, colors
from tabulate import tabulate


def create_board(rows: int, cols: int) -> list[list[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def fill_box(board: list[list[str]], row: int, col: int, char: str) -> bool:
    if board[row][col] == " ":
        board[row][col] = char
        return True
    return False


def check_winner(board: list[list[str]]) -> str:
    if check_win(board.copy(), color('X', colors.red)):
        return color('X', colors.red)

    if check_win(board.copy(), color('O', colors.blue)):
        return color('O', colors.blue)

    filled = 0
    rows, cols = len(board), len(board[0])

    for i in range(rows):
        for j in range(cols):
            if board[i][j] != ' ':
                filled += 1

    if filled == rows * cols:
        return 'T'

    return ' '


def check_win(board: list[list[str]], char: str) -> bool:
    rows = len(board)

    for i in range(rows):
        if all(board[i][j] == char for j in range(rows)) or all(board[j][i] == char for j in range(rows)):
            return True

    if all(board[i][i] == char for i in range(rows)) or all(board[i][2 - i] == char for i in range(rows)):
        return True

    return False


def transform_board(board: list[list[str]]) -> list[list[str]]:
    new_board = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                row.append(str(i * len(board) + j + 1))
            else:
                row.append(board[i][j])
        new_board.append(row)

    return new_board


def print_board(board: list[list[str]]):
    print(tabulate(transform_board(board), tablefmt="rounded_grid"))
