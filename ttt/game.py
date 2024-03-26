# Make sure the src folder is in path for cross-imports
import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import ttt.player
import ttt.board

from ttt.player import Player
from ttt.board import Board

import json

# Helper function

def write_stats(statsfile, player_name):
    """This helper function allows us to add 1 to the total number of wins of a player, which
    is stored in a file. The following arguments are given to this function:

    Args:
        statsfile (str): The name of the stats file
        player_name (str): The name of the player for which the total number of wins should be increased

    Therefore, there are two scenarios for this function:

        1. A stats file with the given name already exists. If so, read the contents of the file using the
           json library and, if the player is already in the stats file, increase their score by one. If not,
           add a new entry to the file using the player's name as a key and the score of 1 as a value.
        2. A stats file with the given name does not exist. If so, create a new one and add the given player
           to the file with a score of 1.

    WARNING: Please have a look at the example stats file in src/stats_example.json and exactly follow the
             pattern used to store data there. This basically reduces to loading a dictionary, adding/modifying
             an entry and storing it, all using the json library.
    """
    if os.path.exists(statsfile):
        with open(statsfile, 'r') as f:
            stats = json.load(f)
            if player_name in stats:
                stats[player_name] += 1
            else:
                stats[player_name] = 1
        with open(statsfile, 'w') as f:
            json.dump(stats, f)
    else:
        with open(statsfile, 'w') as f:
            stats = {player_name: 1}
            json.dump(stats, f)

class Game:
    """This class handles game logic for TicTacToe. It is responsible for:
        
        - Creating player objects
        - Creating a board object
        - Allowing players to make moves until a win or a draw has occurred
        - Writing to/reading from the stats file

    """

    def __init__(self, name1, name2, statsfile="stats.json"):
        """This method initializes a new Game object. It should initialize 
        the following class variables:

            self.board (Board): The board for the game of TicTacToe
            self.player1 (Player): The Player object for player 1, which has the marker "X"
            self.player2 (Player): The Player object for player 2, which has the marker "O"
            self.statsfile (str): The name of the statsfile as passed to this function
            self._current (Player): A placeholder for the player who is supposed to make the next move.
                                    Initialize it with self.player1

        Args:
            name1 (str): The name of player 1
            name2 (str): The name of player 2
            statsfile (str): The name of the stats file (default: stats.json)

        """
        self.board = Board()
        self.player1 = Player(name1, "X")
        self.player2 = Player(name2, "O")
        self.statsfile = statsfile
        self._current = self.player1

    def handle_win(self):
        """This method checks whether a win has occurred by running self.board.check_win
        If a win is detected, it does the following:

            1. Update the score of the winning player in the stats file by running the
               write_stats helper function with the player's name.
               
               Hint: The winning player is the player that made the current move, i.e.,
               the player stored in self._current

            2. Raise a TimeoutError with a message that indicates a win and that contains the
               winning player's name
        """
        if self.board.check_win():
            winner_name = self._current.name
            write_stats(self.statsfile, winner_name)
            raise TimeoutError(f"Player {winner_name} wins!")

    def handle_draw(self):
        """This method checks whether a draw has occurred by running self.board.check_full
        If a draw is detected (i.e. if the board is full), it raises a TimeoutError with a 
        message indicating that a draw has happened.
        """
        if self.board.check_full():
            raise TimeoutError("The game is a draw!")

    def make_move(self):
        """This method is responsible for making one move in TicTacToe. It should:
            
            1. Print the current board
            2. Ask the current player (stored in self._current) for a spot to place their marker in. If they
               give a "Q" or a "q", end the game by raising a TimeoutError with a message saying that the
               user ended the game. Otherwise, check whether they gave an integer. If not, notify them of
               their mistake and repeat this step until either "Q", "q" or an integer was given.
            3. Execute the self.board.place method with the current player's marker and the position chosen in step 2.
              
              WARNING: Since the self.board.place method runs the self.board.is_valid method (see the method's
              docstring), this step might raise a ValueError if the user provided an invalid spot (either not 
              between 1 and 9 or the spot is already taken). This should be handled by notifying the user of their 
              mistake and repeating steps 2. and 3. until the user provides a valid spot and, therefore, no ValueError 
              is raised anymore.
            
            4. Run the self.handle_win method to handle a possible win
            5. Run the self.handle_draw method to handle a possible draw
             6. Set the self._current player to the other player. For example, if self._current was self.player1,
               set it to self.player2 and vice versa.
        """
        print(self.board)
        spot = input(f"Player {self._current.name}, enter a spot to place your marker (1-9 or 'Q' to quit): ")
        
        if spot.upper() == "Q":
            raise TimeoutError("The game has ended. Player quit.")
        
        try:
            spot = int(spot)
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 9 or 'Q' to quit.")
            self.make_move()
            return
        
        try:
            self.board.place(spot, self._current.marker)
        except ValueError as e:
            print(e)
            self.make_move()
            return

        self.handle_win()
        self.handle_draw()
        self._current = self.player1 if self._current == self.player2 else self.player2