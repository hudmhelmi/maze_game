# This code uses the curses module from the Python standard library.
# For more information on curses, refer to the Python documentation:
# https://docs.python.org/3/howto/curses.html

import curses
from classes import Maze, Player, Direction, InvalidMoveError


def main(stdscr):
    """
    Main function for running the maze game.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    # Initialize curses and set up the game environment
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    maze = Maze()
    player = Player()
    allow_movement = True

    while True:
        try:
            # Clear the screen and display maze state
            stdscr.clear()
            stdscr.addstr(0, 0, maze.state(player.position))
            stdscr.addstr(12, 0, "Use the arrow keys to move. Press q to quit.")
            stdscr.refresh()

            allow_movement = True

            key = stdscr.getkey()

            if allow_movement:
                player_input(stdscr, player, key, maze)

                if maze.win(player.position):
                    break

        except InvalidMoveError as e:
            # Handle invalid moves and display error message
            allow_movement = False
            stdscr.clear()
            stdscr.addstr(0, 0, maze.state(player.position))
            stdscr.addstr(12, 0, str(e))
            stdscr.getch()

    win(stdscr)

    reset_terminal(stdscr)


def player_input(stdscr, player, key, maze):
    """
    Handle player input for movement and quitting the game.

    This function takes the player's input (a key press) and updates the player's
    position in the maze accordingly. It also provides an option to quit the game
    by pressing 'q'.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
        player (Player): The player object representing the player's position.
        key (str): The key press input from the user.
        maze (Maze): The maze object representing the game environment.

    Returns:
        None: This function modifies the player's position within the maze.
    """
    # Handle player movement and quitting
    if key == "KEY_UP":
        return player.move(Direction.UP, maze)
    elif key == "KEY_DOWN":
        return player.move(Direction.DOWN, maze)
    elif key == "KEY_LEFT":
        return player.move(Direction.LEFT, maze)
    elif key == "KEY_RIGHT":
        return player.move(Direction.RIGHT, maze)
    elif key == "q":
        quit(stdscr)


def reset_terminal(stdscr):
    """
    Reset the terminal settings and exit curses mode.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def win(stdscr):
    """
    Display a win message and close the game.

    This function displays a victory message on the curses window and initiates
    the game's closure by waiting for a few seconds before exiting the application.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(0, 0, f"You win! Closing in {i}...")
        stdscr.refresh()
        curses.napms(1000)


def quit(stdscr):
    """
    Quit the game and reset terminal settings.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    reset_terminal(stdscr)
    exit()


if __name__ == "__main__":
    # Wrap the main function in curses to handle initialization and cleanup
    curses.wrapper(main)
