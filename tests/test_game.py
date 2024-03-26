import pytest
from unittest import mock

from ttt.game import write_stats
from ttt.game import Game

from ttt.player import Player
from ttt.board import Board
from ttt.board import position_to_coordinates

import time
import os
import string
import random
import json

import numpy as np

counter = 0

STATSFILE_NAME = "pytest_stats.json"

# Helper functions
def generate_name():
    """Generates a random but unique name"""
    # Make sure we don't generate the same string multiple times during the tests
    global counter
    counter += 1
    return "".join(random.choice(string.ascii_lowercase) for i in range(7)) + str(counter)

def remove_statsfile():
    """Deletes statsfile if it exists"""
    if os.path.exists(STATSFILE_NAME):
        os.remove(STATSFILE_NAME)

@pytest.fixture
def statsfile():
    remove_statsfile()
    return STATSFILE_NAME

def test_write_stats_creates_file(statsfile):
    """Test that checks whether the write_stats function creates a new stats file"""
    
    # Generate trial stats file name and player name
    name = generate_name()
    print(f"weffihiewhfwewihfewfewiohfoiewhfoiewhfewhfiwhfhewifhewifhweifiewfiewfiew {statsfile} {type(statsfile)} ufdhgewufgweufwe")
    write_stats(statsfile, name)
    
    assert os.path.isfile(statsfile), f"Stats file {STATSFILE_NAME} was not created"

    with open(statsfile, "r") as file:
        scores = json.loads(file.read())
        assert len(scores) == 1, f"Score dictionary is not of length 1"
        assert scores[name] == 1, f"Score of 1 was not stored for player {name}"
    
def test_write_stats_updates_file(statsfile):
    """Test that checks whether an existing stats file is used and updated"""

    # Generate trial stats file name and player names
    name1, name2, name3 = [generate_name() for i in range(3)]
    random_score = random.randint(1, 100)

    # Write initial statsfile
    with open(statsfile, "w") as file:
        json_string = '{"' + name1 + '": 1, "' + name2 + '": ' + str(random_score) + '}'
        file.write(json_string)
    
    # Update statsfile
    write_stats(statsfile, name1)
    write_stats(statsfile, name2)
    write_stats(statsfile, name3)

    with open(statsfile, "r") as file:
        scores = json.loads(file.read())
        assert len(scores) == 3, "Length of scores is not 3"
        assert all([name in scores.keys() for name in [name1, name2, name3]]), "Not all names in score list"
        assert scores[name1] == 2, f"Score of {name1} was not updated"
        assert scores[name2] == random_score + 1, f"Score of {name2} was not updated"
        assert scores[name3] == 1, f"Score of {name3} was not inserted"

@pytest.fixture
def game(statsfile):
    """Returns a game object with random names"""
    name1, name2 = [generate_name() for i in range(2)]
    return Game(name1, name2, statsfile), name1, name2

def test_game_initializes(game, statsfile):
    """Test whether the game object initialized properly"""
    game, name1, name2 = game

    for attr in ["board", "player1", "player2", "statsfile", "_current"]:
        assert hasattr(game, attr), f"Game object does not have attribute {attr}"

    for attr, datatype in {game.board: Board, game.player1: Player, game.player2: Player,
                           game._current: Player}.items():
        assert isinstance(attr, datatype), f"{type(attr)} is not of type {datatype}"

    assert game._current == game.player1, "game._current does not initialize with value game.player1"
    assert game.player1.marker == "X", f"Marker of Player 1 is {game.player1.marker} (should be X)"
    assert game.player2.marker == "O", f"Marker of Player 2 is {game.player2.marker} (should be O)"

    assert game.player1.name == name1, f"Name of Player 1 is {game.player1.name} (should be {name1})"
    assert game.player2.name == name2, f"Name of Player 2 is {game.player2.name} (should be {name2})"

def test_handle_win_raises_timeout(game, statsfile):
    """Test whether the handle_win method raises a TimeoutError if a win has occurred"""
    game = game[0]
    
    # Force win
    game.board.check_win = mock.MagicMock(return_value=True)
    with pytest.raises(TimeoutError):
        game.handle_win()

    # Force no win
    game.board.check_win = mock.MagicMock(return_value=False)
    game.handle_win()

def test_handle_win_writes_statsfile(game, statsfile):
    """Test whether the handle_win method executes the write_stats function and
    successfully writes the winning player to the stats file
    """
    game = game[0]

    # Force win
    game.board.check_win = mock.MagicMock(return_value=True)
    try:
        game.handle_win()
    except TimeoutError:
        pass
    
    assert os.path.isfile(game.statsfile), "Statsfile was not created by handle_win"
    with open(game.statsfile, "r") as file:
        stats = json.loads(file.read())
        assert game.player1.name in stats.keys(), f"Winning player {game.player1.name} not in stats file"
        assert stats[game.player1.name] == 1, f"Score of winning player {game.player1.name} not in stats file"
   
def test_handle_draw_raises_timeout(game, statsfile):
    """Test whether the handle_draw method raises a TimeoutError when a draw has occurred"""
    game = game[0]

    # Force draw
    game.board.check_full = mock.MagicMock(return_value=True)
    with pytest.raises(TimeoutError):
        game.handle_draw()

    # Force no draw
    game.board.check_full = mock.MagicMock(return_value=False)
    game.handle_draw()

def test_make_move_asks_again(game, statsfile):
    """Test whether make_move rejects invalid spots and asks again for valid ones"""
    game = game[0]

    random_string = generate_name()

    mocked_input = mock.Mock(side_effect=[random_string, "0", "10", "1"])
    with mock.patch("builtins.input", mocked_input):
        game.make_move()

    assert mocked_input.call_count == 4, "The input function was not called 4 times after 3 invalid inputs"
    assert game.board.grid[0, 0] == "X", f"Marker was not placed at correct location\n{game.board}"
    assert np.sum(game.board.grid == "") == 8, f"Multiple markers were placed although only one should have been placed\n{game.board}"

def test_make_move_accepts_q(game, statsfile):
    """Test whether make_move accepts q and Q as input and raises TimeoutError"""
    game = game[0]
   
    with mock.patch("builtins.input", mock.Mock(side_effect=["q", "Q"])):
        with pytest.raises(TimeoutError):
            game.make_move()
        with pytest.raises(TimeoutError):
            game.make_move()


def test_make_move_places_markers(game, statsfile):
    """Test whether make_move places two markers and switches _current"""
    game = game[0]
    
    # Generate two random, non-equal positions
    positionX = random.randint(1, 9)
    positionO = ((positionX - 1) + random.randint(1, 8))%9 + 1

    mocked_input = mock.Mock(side_effect=[str(positionX), str(positionO)])
    
    with mock.patch("builtins.input", mocked_input):
        game.make_move()
        assert game._current == game.player2, "make_move did not switch _current to other player"
        game.make_move()
        assert game._current == game.player1, "make_move did switch _current to player 2 after first move but not back to player 1 after second move"

    assert game.board.grid[position_to_coordinates(positionX)] == "X"
    assert game.board.grid[position_to_coordinates(positionO)] == "O"

@pytest.fixture
def winning_board():
    """A board where only one marker remains until a player wins"""
    winning = Board()
    winning.grid = np.array([["X", "", ""], ["X", "", ""], ["", "", ""]])
    return winning

@pytest.fixture
def draw_board():
    """A board where only one marker remains until a draw happens"""
    draw = Board()
    draw.grid = np.array([["X", "X", "O"], ["O", "O", "X"], ["X", "O", ""]])
    return draw

def test_make_move_wins_game(game, winning_board, statsfile):
    """Tests whether make_move detects win"""
    game = game[0]

    game.board = winning_board
    
    with mock.patch("builtins.input", mock.Mock(side_effect=["7"])):
        with pytest.raises(TimeoutError):
            game.make_move()

def test_make_move_draws_game(game, draw_board, statsfile):
    """Tests whether make_move detects draw"""
    game = game[0]

    game.board = draw_board
    
    with mock.patch("builtins.input", mock.Mock(side_effect=["9"])):
        with pytest.raises(TimeoutError):
            game.make_move()



