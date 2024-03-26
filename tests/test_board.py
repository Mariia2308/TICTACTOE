#!/bin/env python3

import numpy as np
import pytest

from ttt import board
from ttt.board import Board

@pytest.fixture
def helper_board():
    return np.arange(1, 10).reshape((3, 3))

def test_position_to_coordinates(helper_board):
    """Tests helper function position_to_coordinates"""
    
    for position in range(1, 10):
        coordinates = board.position_to_coordinates(position)
        assert helper_board[coordinates] == position

def test_diagonal(helper_board):
    """Tests helper function diagonal"""
    random_board = np.random.random((3, 3))
    diagonal = board.diagonal(random_board)

    assert diagonal.ndim == 1
    assert diagonal.size == 3
    assert np.sum(diagonal) == np.trace(random_board)

def test_antidiagonal(helper_board):
    """Tests helper function antidiagonal"""
    random_board = np.random.random((3, 3))
    antidiagonal = board.antidiagonal(random_board)

    assert antidiagonal.ndim == 1
    assert antidiagonal.size == 3
    assert np.sum(antidiagonal) == np.trace(np.flip(random_board, axis=1))

@pytest.fixture
def empty_board():
    return Board()

@pytest.fixture
def full_board():
    b = Board()
    b.grid = np.random.choice(["X", "O"], size=(3, 3))
    return b

def test_init_board(empty_board):
    """Tests whether the init method initialized class variables correctly"""

    assert hasattr(empty_board, "grid")
    assert empty_board.grid.dtype == '<U1'
    assert empty_board.grid.shape == (3, 3)
    assert np.all(empty_board.grid == "")

    assert hasattr(empty_board, "last_move")
    assert empty_board.last_move == 0

def test_str(empty_board):
    """Tests whether the default string representation of the board class has
    been altered
    """

    module = empty_board.__class__.__module__
    name = empty_board.__class__.__name__

    assert str(empty_board) != f"<{module}.{name} object at {hex(id(empty_board))}>"

def test_is_valid_in_range(empty_board):
    """Tests the is_valid method for invalid positions outside allowed range"""

    trial_positions_invalid = [0, 10, np.random.randint(10, 100)*np.random.choice([-1, 1])]
    trial_positions_valid = range(1, 10)

    # Test invalid position
    for position in trial_positions_invalid:
        try:
            empty_board.is_valid(position)
            assert False, "Invalid position was marked as valid"
        except ValueError:
            continue # Invalid position was successfully detected

    # Test valid positions
    for position in trial_positions_valid:
        try:
            empty_board.is_valid(position)
        except ValueError:
            assert False, "Valid position was marked as invalid"

def test_is_valid_full_board(full_board):
    """Tests the is_valid method with a full board"""
    
    for position in range(1, 10):
        try:
            full_board.is_valid(position)
            assert False, f"Occupied position {position} was marked as valid"
        except ValueError:
            assert True

def test_place_detects_invalid_valid(empty_board, full_board):
    """Tests whether the place method runs the is_valid method"""
    
    trial_positions_invalid = [0, 10, np.random.randint(10, 100)*np.random.choice([-1, 1])]

    for position in trial_positions_invalid:
        try:
            empty_board.place(position, "X")
            assert False, "Invalid position undetected by place"
        except ValueError:
            assert True
    try:
        full_board.place(np.random.randint(1, 10), "X")
        assert False, "Place to occupied position was not forbidden"
    except ValueError:
        assert True

def test_place_places_markers(empty_board):
    """Tests whether the place method lets you place markers on the board"""

    trial_markers = np.random.choice(["X", "O"], size=9)

    for position in range(1, 10):
        empty_board.place(position, trial_markers[position-1])

    assert np.all(empty_board.grid.flatten() == trial_markers)

def test_place_updates_last_move(empty_board):
    """Tests whether the place method updates self.last_move"""

    position = np.random.randint(1, 10)
    empty_board.place(position, "X")

    assert empty_board.last_move == position

def test_show_marker(empty_board):
    """Tests the show_marker method"""

    # Determine random, non-identical positions for markers X and O
    positionX = np.random.randint(1, 10)
    positionO = ((positionX - 1) + np.random.randint(1, 9))%9 + 1
    
    empty_board.place(positionX, "X")
    empty_board.place(positionO, "O")

    markersX = empty_board.show_marker("X")
    markersO = empty_board.show_marker("O")

    # Check whether markersX and markersO are True at the right positions
    assert markersX.flatten()[positionX - 1]
    assert markersO.flatten()[positionO - 1]

    # Check whether they are only True at one position each
    assert np.sum(markersX) == 1
    assert np.sum(markersO) == 1

def test_check_full(empty_board, full_board):
    """Tests whether the check_full method detects a full board"""

    
    assert not empty_board.check_full(), "Full board was detected although board wasn't full"
    empty_board.grid[np.random.randint(0, 3), np.random.randint(0, 3)] = "X"
    assert not empty_board.check_full(), "Full board was detected although board wasn't full"

    
    assert full_board.check_full(), "Full board was not detected"

# Winning patterns

@pytest.fixture
def horizontal(empty_board):
    """Board with a horizontal win"""
    marker = np.random.choice(["X", "O"])
    # Choose random row position
    row_start = np.random.choice([1, 4, 7])
    
    for position in range(row_start, row_start + 3):
        empty_board.place(position, marker)

    return empty_board
    
@pytest.fixture
def vertical(empty_board):
    """Board with a vertical win"""
    marker = np.random.choice(["X", "O"])
    # Choose random column position
    column_start = np.random.choice([1, 2, 3])
    
    for position in range(column_start, column_start + 7, 3):
        empty_board.place(position, marker)

    return empty_board

@pytest.fixture
def diagonal(empty_board):
    """Board with diagonal win"""
    marker = np.random.choice(["X", "O"])
    diag = [1, 5, 9]

    for position in diag:
        empty_board.place(position, marker)
    return empty_board


@pytest.fixture
def antidiagonal(empty_board):
    """Board with antidiagonal win"""
    marker = np.random.choice(["X", "O"])
    antidiag = [3, 5, 7]

    for position in antidiag:
        empty_board.place(position, marker)
    return empty_board

def win_detected(board):
    """Helper function that asserts whether a win was detected"""
    assert board.check_win(), f"Win undetected: \n{board}"

def test_horizontal_win(horizontal):
    """Check if horizontal win is detected"""
    win_detected(horizontal)

def test_vertical_win(vertical):
    """Check if vertical win is detected"""
    win_detected(vertical)

def test_diagonal_win(diagonal):
    """Check if diagonal win is detected"""
    win_detected(diagonal)

def test_antidiagonal_win(antidiagonal):
    """Check if antidiagonal win is detected"""
    win_detected(antidiagonal)

def test_no_win(empty_board):
    """Check whether no win is detected"""
    empty_board.place(np.random.randint(1, 10), np.random.choice(["X", "O"]))
    assert not empty_board.check_win(), f"Win detected although there was no win\n{empty_board}"
    
