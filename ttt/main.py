#!/bin/env python3

# Make sure the src folder is in path
import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from ttt.game import Game


def main():
    """This function is where everything comes together. Therefore, it should:
            
            - Ask the user to provide two names for the players.
            - Ask the user for a stats file name. If none is given, use the default value "stats.json"
            - Create a Game object with the given arguments. Remember that this might raise ValueErrors
              if the given names are empty. Handle those by asking the user for new names or prevent them
              in the first place by not allowing empty inputs.
            - Run the make_move method until a TimeoutError is raised and the game is over
            - Handle the TimeoutError and print its message into the console
            - End the game by using sys.exit(0)

    Please don't forget to handle all errors and to only end the program using sys.exit(0)
    """
    player1_name = input("Enter the name for Player 1: ")
    while not player1_name:
        print("Name cannot be empty.")
        player1_name = input("Enter the name for Player 1: ")

    player2_name = input("Enter the name for Player 2: ")
    while not player2_name:
        print("Name cannot be empty.")
        player2_name = input("Enter the name for Player 2: ")

    stats_file = input("Enter the stats file name (default: stats.json): ")
    if not stats_file:
        stats_file = "stats.json"

    try:
        game = Game(player1_name, player2_name, stats_file)
    except ValueError as e:
        print(e)
        main()

    try:
        while True:
            game.make_move()
    except TimeoutError as e:
        print(e)
        sys.exit(0)


if __name__ == "__main__":
    main()
