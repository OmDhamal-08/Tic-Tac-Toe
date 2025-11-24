import numpy as np
import random

POSITION_MAP = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    9: (2, 2),
}


def new_board():
    """Return a fresh 3x3 board."""
    return np.zeros((3, 3), dtype=object)


def format_board(board):
    """Return a string rendering of the current board state."""
    rows = []
    for i, row in enumerate(board):
        rows.append(" | ".join(str(cell) if cell and cell != "0" else " " for cell in row))
        if i < 2:
            rows.append("---+---+---")
    return "\n".join(rows)


def position_to_coords(position):
    return POSITION_MAP.get(position)


def place_symbol(board, position, symbol):
    """Place a symbol using the numeric keypad style positions."""
    coords = position_to_coords(position)
    if coords is None:
        raise ValueError("Invalid board position.")
    row, col = coords
    if board[row, col] != 0:
        raise ValueError("Position already occupied.")
    board[row, col] = symbol
    return row, col


def set_symbol(board, row, col, symbol):
    if board[row, col] != 0:
        raise ValueError("Position already occupied.")
    board[row, col] = symbol


def available_cells(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row, col] == 0]


def available_positions(board):
    return [pos for pos, coords in POSITION_MAP.items() if board[coords] == 0]


def random_move(board):
    cells = available_cells(board)
    if not cells:
        return None
    return random.choice(cells)


def check_winner(board):
    lines = []
    lines.extend(board)  # rows
    lines.extend(board.T)  # columns
    lines.append(np.array([board[i, i] for i in range(3)]))
    lines.append(np.array([board[i, 2 - i] for i in range(3)]))

    for line in lines:
        if line[0] != 0 and line[0] == line[1] == line[2]:
            return line[0]
    return None


def board_full(board):
    return all(cell != 0 for row in board for cell in row)

