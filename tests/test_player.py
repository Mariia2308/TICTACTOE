import pytest

from ttt.player import Player

import string
import random


@pytest.fixture
def random_player():
    """Method to generate a player with random name and random marker"""
    random_name_length = random.randint(1, 10)
    random_name = "".join(random.choice(string.ascii_lowercase) for i in range(random_name_length))
    random_marker = random.choice(["X", "O"])
    
    return Player(random_name, random_marker), random_name, random_marker

def test_init_succeeds(random_player):
    """Test that checks whether the __init__ function runs correctly
    """
    
    trial_player, random_name, random_marker = random_player

    assert hasattr(trial_player, "name")
    assert hasattr(trial_player, "marker")


def test_str(random_player):
    """Test that checks whether the __str__ method was implemented"""
    
    trial_player = random_player[0]
    
    memory_address = hex(id(trial_player))
    module = trial_player.__class__.__module__
    name = trial_player.__class__.__name__

    # This is the default string representation of an object if it has not been altered
    default_str = f"<{module}.{name} object at {memory_address}>"

    assert str(trial_player) != default_str

def test_name_getter_setter(random_player):
    """Test that checks whether the getter and setter for the player are implemented"""
    
    trial_player, random_name, random_marker = random_player
    
    assert hasattr(trial_player, "_name") # Check whether the hidden class variable exists
    assert trial_player._name == random_name
    assert trial_player.name == random_name

    trial_player.name = "Alice"
    assert trial_player.name == "Alice"
    assert trial_player._name == "Alice"

def test_name_setter_invalid_name(random_player):
    """Test that checks whether the name setter raises a ValueError when
    an empty name is provided
    """

    trial_player = random_player[0]
    try:
        trial_player.name = ""
        assert False, "Setting an empty name was allowed although it shouldn't be"
    except ValueError:
        assert True

def test_marker_getter_setter(random_player):
    """Test that checks whether the getter and setter for the marker are implemented"""

    trial_player, random_name, random_marker = random_player

    assert hasattr(trial_player, "_marker")
    assert trial_player.marker == random_marker
    assert trial_player._marker == random_marker

    new_marker = "X" if random_marker == "O" else "O"
    trial_player.marker = new_marker
    assert trial_player.marker == new_marker
    assert trial_player._marker == new_marker

def test_marker_setter_invalid_marker(random_player):
    """Test that checks whether the marker setter raises a ValueError when trying
    to set an invalid marker"""
    
    trial_player = random_player[0]

    # Empty string, space and all upper-/lowercase letters except x and o
    invalid_markers = [marker for marker in (["", " "] + [*string.ascii_letters]) if marker.lower() not in ["x", "o"]]
    
    # Add a random string with between 2 and 9 random characters
    invalid_markers += ["".join(random.choice(string.ascii_letters) for i in range(random.randint(2, 10)))]

    for marker in invalid_markers:
        try:
            trial_player.marker = marker
            assert False, f"Setting invalid marker {marker} was allowed by marker setter"
        except ValueError:
            assert True

