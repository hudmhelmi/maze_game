# This code uses the random module from the Python standard library.
# For more information on the random module, refer to the Python documentation:
# https://docs.python.org/3/library/random.html

# This code uses the enum module from the Python standard library.
# For more information on the enum module, refer to the Python documentation:
# https://docs.python.org/3/library/enum.html

# This code uses the copy module from the Python standard library.
# For more information on the copy module, refer to the Python documentation:
# https://docs.python.org/3/library/copy.html

import random
from enum import Enum
from copy import deepcopy

MAZE_WIDTH = 10
MAZE_HEIGHT = 10


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class InvalidMoveError(Exception):
    """
    Custom exception class for invalid player moves.
    """

    pass


class Maze:
    def __init__(self) -> None:
        """
        Initialize the Maze object and generate the maze.
        """
        self.maze = self.generate()

    def generate(self):
        """
        Generate a random maze with a start (S) and end (E) point.

        Returns:
            list: A 2D list representing the maze.
        """
        maze = [["#" for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        maze[0][0] = "S"

        position = [0, 0]
        while position != [MAZE_HEIGHT - 1, MAZE_WIDTH - 1]:
            if position[0] == MAZE_HEIGHT - 1:
                direction = Direction.RIGHT
            elif position[1] == MAZE_WIDTH - 1:
                direction = Direction.DOWN
            else:
                direction = random.choice([Direction.RIGHT, Direction.DOWN])
            if direction == Direction.RIGHT:
                maze[position[0]][position[1] + 1] = " "
                position[1] += 1
            elif direction == Direction.DOWN:
                maze[position[0] + 1][position[1]] = " "
                position[0] += 1

        maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = "E"

        return maze

    def state(self, position):
        """
        Get the current state of the maze with the player's position.

        Args:
            position (list): The player's position [row, col].

        Returns:
            str: A string representation of the maze with the player's position marked as 'P'.
        """
        maze_copy = deepcopy(self.maze)
        maze_copy[position[0]][position[1]] = "P"
        return "\n".join([" ".join(row) for row in maze_copy])

    def win(self, position):
        """
        Check if the player has reached the end of the maze.

        Args:
            position (list): The player's position [row, col].

        Returns:
            bool: True if the player has won (reached the end), False otherwise.
        """
        return position == [MAZE_HEIGHT - 1, MAZE_WIDTH - 1]


class Player:
    def __init__(self) -> None:
        """
        Initialize the Player object with the starting position.
        """
        self._position = [0, 0]

    def _is_valid_move(self, new_position, maze: Maze):
        """
        Check if a move to the new position is valid within the maze.

        Args:
            new_position (list): The new position [row, col].
            maze (Maze): The Maze object representing the game maze.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row, col = new_position
        return (
            0 <= row < MAZE_HEIGHT
            and 0 <= col < MAZE_WIDTH
            and maze.maze[row][col] != "#"
        )

    def move(self, direction: Direction, maze: Maze):
        """
        Move the player in a specified direction within the maze.

        Args:
            direction (Direction): The direction to move.
            maze (Maze): The Maze object representing the game maze.

        Raises:
            InvalidMoveError: If the move is invalid, an exception is raised.
        """
        new_position = self._position.copy()

        if direction == Direction.UP:
            new_position[0] -= 1
        elif direction == Direction.DOWN:
            new_position[0] += 1
        elif direction == Direction.LEFT:
            new_position[1] -= 1
        elif direction == Direction.RIGHT:
            new_position[1] += 1

        if self._is_valid_move(new_position, maze):
            self._position = new_position
        else:
            raise InvalidMoveError("You can't move there! Press any key to continue.")

    @property
    def position(self):
        """
        Get the current position of the player.

        Returns:
            list: The player's position [row, col].
        """
        return self._position

    @position.setter
    def position(self, value):
        """
        Set the position of the player.

        Args:
            value (list): The new position [row, col].
        """
        self._position = value
