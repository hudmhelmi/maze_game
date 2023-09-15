import curses
import pytest
from project import player_input, reset_terminal, win, quit
from classes import Maze, Player, Direction, InvalidMoveError


@pytest.fixture
def stdscr():
    """
    Pytest fixture to create a curses window object for testing.

    This fixture sets up the curses environment for testing, yields the curses window object,
    and ensures cleanup by restoring the terminal settings when the test is done.

    Yields:
        curses.window: The curses window object for testing.
    """
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()

    yield stdscr

    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def test_player_input(stdscr):
    """
    Test the player_input function for movement and quitting.

    This function tests the player_input function for different input keys, checking if the
    player's position is updated correctly for movement keys and if the game exits when 'q' is pressed.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """
    maze = Maze()
    player = Player()

    def test_function(stdscr):
        key = "KEY_UP"
        player_input(stdscr, player, key, maze)
        assert player.position == (0, 1)

        key = "KEY_DOWN"
        player_input(stdscr, player, key, maze)
        assert player.position == (1, 1)

        key = "KEY_LEFT"
        player_input(stdscr, player, key, maze)
        assert player.position == (1, 0)

        key = "KEY_RIGHT"
        player_input(stdscr, player, key, maze)
        assert player.position == (1, 1)

        key = "q"
        with pytest.raises(SystemExit):
            player_input(stdscr, player, key, maze)

    curses.wrapper(test_function)


def test_reset_terminal(stdscr):
    """
    Test the reset_terminal function for resetting terminal settings.

    This function tests if the reset_terminal function correctly resets terminal settings
    by checking if stdscr.keypad(True) and curses.echo() are set to their
    expected values after the function call.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """

    def test_function(stdscr):
        reset_terminal(stdscr)
        assert not stdscr.keypad(True)
        assert not curses.echo()

    curses.wrapper(test_function)


def test_win(stdscr):
    """
    Test the win function for program exit and message display.

    This function tests the win function by checking if it raises a SystemExit exception,
    and if the displayed text contains the expected win message.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """

    def test_function(stdscr):
        with pytest.raises(SystemExit):
            win(stdscr)

        displayed_text = stdscr.getstr(0, 0, 100).decode("utf-8")
        assert "You win!" in displayed_text
        assert "Closing in" in displayed_text

    curses.wrapper(test_function)


def test_quit(stdscr):
    """
    Test the quit function for program exit and terminal settings.

    This function tests the quit function by checking if it raises a SystemExit exception,
    if the terminal settings are reset as expected, and if the settings are restored to
    their initial values.

    Args:
        stdscr (curses.window): The curses window object representing the game screen.
    """

    def test_function(stdscr):
        initial_keypad = stdscr.keypad()
        initial_echo = curses.echo()

        with pytest.raises(SystemExit):
            quit(stdscr)

        assert not stdscr.keypad()
        assert not curses.echo()

        assert stdscr.keypad() == initial_keypad
        assert curses.echo() == initial_echo

    curses.wrapper(test_function)
