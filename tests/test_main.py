from ttt.main import main

import pytest
from unittest import mock
import os

import random
import string
import json


counter = 0

STATSFILE_NAME = "pytest_stats.json"

# Some patterns with which player 1 or player 2 wins
winning_patterns_1 = [[1, 2, 4, 5, 7, 8], [5, 2, 1, 3, 9], [3, 1, 5, 2, 7], 
                      [4, 1, 5, 2, 6]]
winning_patterns_2 = [[1, 3, 2, 6, 4, 9], [2, 1, 3, 5, 6, 9], [1, 3, 2, 5, 4, 7],
                      [4, 1, 5, 2, 7, 3]]

random.shuffle(winning_patterns_1)
random.shuffle(winning_patterns_2)

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


def play_pattern(name1, name2, stats, pattern):
    """Function that plays one round of TicTacToe given a pattern and player names"""
    
    side_effect = [name1, name2, stats]
    for move in pattern:
        side_effect.append(str(move))

    mocked_input = mock.Mock(side_effect=side_effect)
    with mock.patch("builtins.input", mocked_input):
        main()

def test_main_plays_games(statsfile):
    """Test that checks whether the main function plays multiple games"""
    number_of_player_1_wins = random.randint(1, 4)
    number_of_player_2_wins = random.randint(1, 4)

    name1 = generate_name()
    name2 = generate_name()

    # Play a random number of wins for both players
    for i in range(number_of_player_1_wins):
        pattern = winning_patterns_1[i]
        # Check whether the game is ended with sys.exit(0)
        with pytest.raises(SystemExit):
            play_pattern(name1, name2, statsfile, pattern)

    for i in range(number_of_player_2_wins):
        pattern = winning_patterns_2[i]
        # Check whether the game is ended with sys.exit(0)
        with pytest.raises(SystemExit):
            play_pattern(name1, name2, statsfile, pattern)

    # Check whether the correct scores were added to the stats file
    assert os.path.isfile(statsfile), f"Statsfile was {statsfile} was not created"
    with open(statsfile, "r") as file:
        scores = json.loads(file.read())
        assert scores[name1] == number_of_player_1_wins
        assert scores[name2] == number_of_player_2_wins

def test_main_uses_default_statsfile_name():
    """Test that checks whether the main function uses the default stats file name
    of stats.json
    """
    # Chose any name and winning pattern
    name1 = "Alice"
    name2 = "Bob"
    pattern = winning_patterns_1[0]

    # Make sure to remove stats.json if it exists
    if os.path.isfile("stats.json"):
        os.remove("stats.json")

    with pytest.raises(SystemExit):
        # Pass an empty statsfile name to see whether the default one is used
        play_pattern(name1, name2, "", pattern)

    assert os.path.isfile("stats.json"), "Default statsfile name stats.json was not used"
    os.remove("stats.json")
