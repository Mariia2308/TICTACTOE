class Player:
    """This class is meant to abstract the concept of a player.
    The information about a player that is relevant in the context of our
    implementation of the game TicTacToe is the following:
    
        - The player's name (so that we can keep track of high scores later)
        - The player's marker, X or O, so that we know which marker to place
          on the board when a player made a move
    """

    def __init__(self, name, marker):
        """This method is run whenever we create a new instance of the Player class,
        i.e., whenever we create a new Player object. It takes two parameters, name and
        marker.

        Since we'd like to be able to use the values of these parameters outside
        the __init__ function, we have to create new class variables using the
        'self' variable, which, for each instance of the class, always references
        that specific instance. If you are unsure of what to do, please refer to the
        lecture notes.

        Args:
            name (str): The name of the player
            marker (str): The marker of the player (X or O)

        Goal:
            Create two class variables, self._name and self._marker, and set their values
            to the arguments passed to this function.
        """
        self.name = name
        self.marker = marker

    def __str__(self):
        """This method handles the player's string representation. To be precise,
        the return value of this method is what will come out when a player object
        is casted/transformed to a string. Come up with something that would ideally
        represent a player as a string and set them apart from other players.

        Returns:
            str: The string representation of a player
        """
        return f"Player {self.name} with marker {self.marker}"

    @property
    def name(self):
        """This is the getter method of the player name. It should return the value
        of the hidden variable self._name.

        Returns:
            self._name (str): The value of the hidden variable self._name
        """
        return self._name

    @name.setter
    def name(self, value):
        """This is the setter method of the player name. When you try to change the value of
        self.name, this method is run instead. So, doing something like

        self.name = "Alice"

        would actually run this method, i.e.,

        self.name = "Alice"

        Therefore, in order to store the value that is being passed to this method, we want to
        create a new class variable called self._name. The underscore (_) in front of the variable
        name signals to the programmer that this variable is not to be directly accessed.

        The advantage here is that we can perform sanity checks on the value before actually modifying
        the hidden variable self._name. For example, we don't want people to be able to set an empty
        string as the name. If they try anyways, we raise a ValueError, saying that the name must not
        be empty.

        Args:
            value (str): The new value for self._name (must not be empty)

        Raises:
            ValueError, when value is an empty string
        """
        if not value:
            raise ValueError("Name must not be empty")
        self._name = value

    @property
    def marker(self):
        """This is the getter method for the player's marker. Much like the getter for the name,
        this method should merely return the value of self._marker (the hidden variable that contains
        the actual value of the player marker)
        
        Returns:
            self._marker (str): The player marker (X or O)
        """
        return self._marker

    @marker.setter
    def marker(self, value):
        """This is the setter method for the player's marker. It should do the same thing as the
        setter method for the player, except of course that it should store the new value in the
        hidden variable self._marker.

        Also, we'd like to be a bit more strict with the values one should be able to set. Specifically,
        this method should implement the following:
        
            - The new value must be either be "X" or "O". The case (upper case/lower case) should NOT matter
              here, so either one of "X", "O", "x" and "o" should be accepted, everything else should raise
              a ValueError.
            - The value that is stored in self._marker in the end should be upper case, so if the user provides
              a lower case "x" or "o", it should be transformed to upper case prior to storing.

        Args:
            value (str): The new player marker to be stored, must be either "X", "O", "x" or "o"

        Raises:
            ValueError, if a non-valid marker was passed
        """
        value_upper = value.upper()
        if value_upper not in ['X', 'O']:
            raise ValueError("Invalid marker. Must be 'X' or 'O'.")
        self._marker = value_upper
