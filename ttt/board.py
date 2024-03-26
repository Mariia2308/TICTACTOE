import numpy as np

# Helper functions

def position_to_coordinates(position):
    """Imagine you have a 3 by 3 numpy array and you introduce a numbering system to
    address each square in the array with a unique number like this:
     
     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9

    Now, you'd like this function to convert the position in the array, i.e. the number
    from 1 to 9, to a tuple of array coordinates (row, col), where, for example,
    position 1 corresponds to (0, 0), position 2 to (0, 1), and so on, until you
    reach position 9, which corresponds to (2, 2).

    For further information, please refer to the docstring of the Board class below.

    Args:
        position (int): The position on the board (see doctring of Board class)

    Returns:
        (row, col) (tuple): Tuple of integers, each ranging from 0 to 2, representing
                            the coordinates in the array corresponding to the 
                            given position.
    Example:
        >>> position_to_coordinates(5)
        <<< (1, 1)
    """
    row = (position - 1) // 3
    col = (position - 1) % 3
    return row, col

def diagonal(grid):
    """Function that returns the main diagonal of a given numpy array

    Args:
        grid (np.ndarray): Numpy array to get the diagonal of

    Returns:
        np.ndarray: The diagonal entries of grid as a 1d-numpy array
    """
    return np.diagonal(grid)

def antidiagonal(grid):
    """Function that returns the main antidiagonal of a given numpy array

    Args:
        grid (np.ndarray): Numpy array to get the antidiagonal of

    Returns:
        np.ndarray: The antidiagonal entries of grid as a 1d-numpy array
    """
    return np.flipud(grid).diagonal()

class Board:
    """This class represents the playing field of a TicTacToe game. Since the players will have
    to be able to place markers (X and O) on the field, we introduce a way of numbering each
    square in the 3 by 3 field:

     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9

     Therefore, we are now able to translate array-coordinates which are of the form (row, col)
     where (row, col) is a tuple of two integers, each ranging from 0 to 2, to a single integer
     that we will call 'position'. Please stick to this numbering convention throughout the whole
     exercise.
    """

    def __init__(self):
        """Initializes a new 3 by 3 board.
        
        Since all new TicTacToe boards are the same, this function does not take any
        arguments. Instead, it should initialize the following two class variables:

        self.grid (np.ndarray): An empty numpy array of dtype str with shape (3, 3). Later,
                                this will contain "X" and "O" markers.

                                Note: Setting the dtype to str creates a numpy array that
                                allows us to store single unicode characters in each cell,
                                which is exactly what we want here.

        self.last_move (int):   This stores the last position at which a marker was placed by
                                a player. The value goes from 1 to 9 and should be initialized
                                with value 0.
        """
        self.grid = np.empty((3, 3), dtype=str)
        self.last_move = 0

    def __str__(self):
        """The string representation of this class. Since all information about a Board object that 
        is of interest for the player is contained in self.grid, maybe it would be a good idea to
        have this function return a nice and readable string-representation of the array.

        Returns:
            A string representing the class
        """
        return str(self.grid)

    def is_valid(self, position):
        """Checks whether an attempted move is valid, i.e., whether:
            - The given position is an integer between 1 and 9
            - The selected position is not already occupied
        
        If the position is valid, do nothing. If it is not valid, raise a ValueError with the
        problem (value not in [1, 9]/position occupied) as the error message.

        Args:
            position (int): The position to be checked for validity

        Returns:
            Nothing, either passes without error or raises an error
        """
        if not (1 <= position <= 9):
            raise ValueError("Position must be an integer between 1 and 9.")
        row, col = position_to_coordinates(position)
        if self.grid[row, col] != "":
            raise ValueError("Position already occupied.")

    def place(self, position, marker):
        """Function that places a marker in a given position:
            - Check whether the given position is valid by running self.is_valid. Do not worry about
                handling exceptions; that will be done later on.
            - Place the given marker in the selected position in self.grid
            - Record the move by updating self.last_move to the given position

        Args:
            position (int): The position for the marker to be placed in
            marker (str): The marker (X or O) to be placed at the given position
        """
        row, col = position_to_coordinates(position)
        self.is_valid(position) 
        self.grid[row, col] = marker
        self.last_move = position

    def show_marker(self, marker):
        """Function that returns a 3 by 3 array of booleans, which is True at (i, j) if self.grid[i, j] == marker
        and False otherwise.
        
        Args:
            marker (str): The marker ("X" or "O") to be shown

        Returns:
            np.ndarray: A 3 by 3 numpy array of booleans which is True where self.grid is equal to marker

        Example:

            >>> self.grid = np.array([["X", "O", "O"], ["X", "X", "O"], ["O", "X", "O"]])
            >>> self.show_marker("X")
            <<< np.array([[True, False, False], [True, True, False], [False, True, False]])
        
        """
        return self.grid == marker

    def check_win(self):
        """Function that checks whether a win has occurred, meaning that a player has managed to fill an entire
        row, column, diagonal or antidiagonal with their marker. If a win has occurred, return True, else, return
        False.

        Hint: You don't need to check the entire board for a win. Use the position of the last move stored
              in self.last_move

        Returns:
            True, if a win has occurred, False otherwise.
        """
        row, col = position_to_coordinates(self.last_move)
        marker = self.grid[row, col]

        if all(self.grid[row, :] == marker):
            return True


        if all(self.grid[:, col] == marker):
            return True

        if row == col and all(np.diagonal(self.grid) == marker):
            return True

        if row + col == 2 and all(np.flipud(self.grid).diagonal() == marker):
            return True

        return False

    def check_full(self):
        """Function that checks whether the board is completely filled with markers. If it is,
        the function returns True. Otherwise, it returns False.
        
        Returns:
            True, if the board is full. False otherwise.
        """
        return not "" in self.grid
