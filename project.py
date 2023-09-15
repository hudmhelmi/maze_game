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
    curses.cbreak()
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
                # Handle player movement and quitting
                if key == "KEY_UP":
                    player.move(Direction.UP, maze)
                elif key == "KEY_DOWN":
                    player.move(Direction.DOWN, maze)
                elif key == "KEY_LEFT":
                    player.move(Direction.LEFT, maze)
                elif key == "KEY_RIGHT":
                    player.move(Direction.RIGHT, maze)
                elif key == "q":
                    quit(stdscr)

                if maze.win(player.position):
                    break

        except InvalidMoveError as e:
            # Handle invalid moves and display error message
            allow_movement = False
            stdscr.clear()
            stdscr.addstr(0, 0, maze.state(player.position))
            stdscr.addstr(12, 0, str(e))
            stdscr.getch()

    # Display a win message and close the game
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(0, 0, f"You win! Closing in {i}...")
        stdscr.refresh()
        curses.napms(1000)

    reset_terminal(stdscr)


def reset_terminal(stdscr):
    """
    Reset the terminal settings and exit curses mode.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


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
