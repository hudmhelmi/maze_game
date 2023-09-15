# This code uses the copy module from the Python standard library.
# For more information on the copy module, refer to the Python documentation:
# https://docs.python.org/3/library/copy.html

# This code uses the curses module from the Python standard library.
# For more information on curses, refer to the Python documentation:
# https://docs.python.org/3/howto/curses.html

# This code uses the enum module from the Python standard library.
# For more information on the enum module, refer to the Python documentation:
# https://docs.python.org/3/library/enum.html

# This code uses the random module from the Python standard library.
# For more information on the random module, refer to the Python documentation:
# https://docs.python.org/3/library/random.html


import curses
import random
from enum import Enum
from copy import deepcopy


class Direction(Enum):
    """Enumeration of directions for movement."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class InvalidMoveError(Exception):
    """Custom exception class for invalid player moves."""

    def __init__(self, message="You can't move there! Press any key to continue."):
        super().__init__(message)


class Maze:
    """Represents the maze game environment."""

    MAZE_WIDTH = 10
    MAZE_HEIGHT = 10

    def __init__(self) -> None:
        """
        Initialize the Maze object.

        This constructor initializes the Maze object with the default maze dimensions.
        """
        self.width = self.MAZE_WIDTH
        self.height = self.MAZE_HEIGHT
        self.state = self.generate(self.width, self.height)

    def generate(self, width, height):
        """
        Generate a random maze with a start (S) and end (E) point.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.

        Returns:
            list: A 2D list representing the maze.
        """
        maze = [["#" for _ in range(width)] for _ in range(height)]
        maze[0][0] = "S"

        position = [0, 0]
        while position != [height - 1, width - 1]:
            if position[0] == height - 1:
                direction = Direction.RIGHT
            elif position[1] == width - 1:
                direction = Direction.DOWN
            else:
                direction = random.choice([Direction.RIGHT, Direction.DOWN])
            if direction == Direction.RIGHT:
                maze[position[0]][position[1] + 1] = " "
                position[1] += 1
            elif direction == Direction.DOWN:
                maze[position[0] + 1][position[1]] = " "
                position[0] += 1

        maze[height - 1][width - 1] = "E"

        return maze


class Player:
    """Represents the player in the maze game."""

    def __init__(self) -> None:
        """
        Initialize the Player object with the starting position.

        This constructor initializes the Player object with the default starting position.
        """
        self.position = [0, 0]


def main(stdscr):
    stdscr, maze, player = game_setup()

    while True:
        try:
            stdscr.clear()
            stdscr.addstr(0, 0, state(maze.state, player.position))
            stdscr.addstr(12, 0, "Use the arrow keys to move. Press q to quit.")
            stdscr.refresh()

            key = stdscr.getkey()

            player_input(stdscr, player, key, maze)

            if check_win(maze, player.position):
                break

        except InvalidMoveError as e:
            stdscr.clear()
            stdscr.addstr(0, 0, state(maze.state, player.position))
            stdscr.addstr(12, 0, str(e))
            stdscr.getch()

    win_screen(stdscr)

    quit(stdscr)


def check_win(maze, position):
    """
    Check if the player has reached the end of the maze.

    Args:
        maze (Maze): The Maze object representing the game maze.
        position (list): The player's position [row, col].

    Returns:
        bool: True if the player has won (reached the end), False otherwise.
    """
    return position == [maze.height - 1, maze.width - 1]


def game_setup():
    """
    Set up the game environment and return the curses window, maze, and player objects.

    Returns:
        tuple: A tuple containing the curses window (stdscr), maze, and player objects.
    """
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    maze = Maze()
    player = Player()
    return stdscr, maze, player


def is_valid_move(new_position, maze):
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
        0 <= row < maze.height and 0 <= col < maze.width and maze.state[row][col] != "#"
    )


def move(player, direction, maze):
    """
    Move the player in a specified direction within the maze.

    Args:
        player (Player): The Player object representing the player's position.
        direction (Direction): The direction to move.
        maze (Maze): The Maze object representing the game maze.

    Raises:
        InvalidMoveError: If the move is invalid, an exception is raised.
    """
    new_position = player.position.copy()

    if direction == Direction.UP:
        new_position[0] -= 1
    elif direction == Direction.DOWN:
        new_position[0] += 1
    elif direction == Direction.LEFT:
        new_position[1] -= 1
    elif direction == Direction.RIGHT:
        new_position[1] += 1

    if is_valid_move(new_position, maze):
        player.position = new_position
    else:
        raise InvalidMoveError


def player_input(stdscr, player, key, maze):
    """
    Handle player input for movement and quitting the game.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
        player (Player): The Player object representing the player's position.
        key (str): The key press input from the user.
        maze (Maze): The Maze object representing the game maze.

    Returns:
        None: This function modifies the player's position within the maze.
    """
    if key == "KEY_UP":
        return move(player, Direction.UP, maze)
    elif key == "KEY_DOWN":
        return move(player, Direction.DOWN, maze)
    elif key == "KEY_LEFT":
        return move(player, Direction.LEFT, maze)
    elif key == "KEY_RIGHT":
        return move(player, Direction.RIGHT, maze)
    elif key == "q":
        quit(stdscr)


def quit(stdscr):
    """
    Quit the game and reset terminal settings.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def state(maze, position):
    """
    Get the current state of the maze with the player's position.

    Args:
        maze (Maze): The Maze object representing the game maze.
        position (list): The player's position [row, col].

    Returns:
        str: A string representation of the maze with the player's position marked as 'P'.
    """
    maze_copy = deepcopy(maze)
    maze_copy[position[0]][position[1]] = "P"
    return "\n".join([" ".join(row) for row in maze_copy])


def win_screen(stdscr):
    """
    Display a win message and close the game.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(0, 0, f"You win! Closing in {i}...")
        stdscr.refresh()
        curses.napms(1000)


if __name__ == "__main__":
    curses.wrapper(main)
