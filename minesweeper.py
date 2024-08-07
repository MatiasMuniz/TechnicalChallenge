#!/usr/bin/env python3
# Python 3.12.4
from typing import List

def create_sanitize_board(board: List[List[int]]) -> List[List[int]]:
    """
    Convert 1s to 9s in the board.

    Args:
        board (List[List[int]]): 2D list with 0s and 1s.

    Raises:
        ValueError: If input is invalid.

    Returns:
        List[List[int]]: 2D list with 1s replaced by 9s.
    """
    if not all(isinstance(row, list) for row in board) or not all(cell in (0, 1) for row in board for cell in row):
        raise ValueError("The board must be a 2D list with cells 0 or 1.")
    
    return [[9 if cell == 1 else cell for cell in row] for row in board]

def count_mines(board: List[List[int]], i: int, j: int) -> int:
    """
    Count mines around cell (i, j).

    Args:
        board (List[List[int]]): 2D list with 0s and 9s.
        i (int): Row index.
        j (int): Column index.

    Raises:
        IndexError: If indices are out of bounds.

    Returns:
        int: Number of adjacent mines.
    """
    rows, columns = len(board), len(board[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    if not (0 <= i < rows and 0 <= j < columns):
        raise IndexError("Cell index out of bounds.")

    return sum(board[i + di][j + dj] == 9
               for di, dj in directions
               if 0 <= i + di < rows and 0 <= j + dj < columns)

def create_counted_board(sanitized_board: List[List[int]]) -> List[List[int]]:
    """
    Create a board with the count of adjacent mines.

    Args:
        sanitized_board (List[List[int]]): 2D list with 0s and 9s.

    Raises:
        ValueError: If board is invalid.

    Returns:
        List[List[int]]: 2D list with mine counts.
    """
    if not all(isinstance(row, list) for row in sanitized_board) or \
       not all(len(row) == len(sanitized_board[0]) for row in sanitized_board):
        raise ValueError("The sanitized board must be a 2D list with consistent row lengths.")
    
    return [[9 if cell == 9 else count_mines(sanitized_board, i, j)
             for j, cell in enumerate(row)]
            for i, row in enumerate(sanitized_board)]

def main() -> int:
    """Main function to run the Minesweeper logic."""
    try:
        board = [[0, 1, 0, 0],[0, 0, 1, 0],[0, 1, 0, 1],[1, 1, 0, 0]]
    
        sanitized_board = create_sanitize_board(board)
        counted_board = create_counted_board(sanitized_board)
    
        print(*counted_board, sep="\n")
    
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
