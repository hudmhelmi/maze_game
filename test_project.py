import pytest
from project import (
    Maze,
    Player,
    Direction,
    InvalidMoveError,
    is_valid_move,
    check_win,
    move,
    state,
)


def test_check_win():
    maze = Maze()
    assert not check_win(maze, [0, 0])
    assert check_win(maze, [maze.height - 1, maze.width - 1])


def test_is_valid_move():
    maze = Maze()
    assert is_valid_move([0, 0], maze)
    assert not is_valid_move([-1, 0], maze)


def test_move():
    maze = Maze()
    player = Player()
    with pytest.raises(InvalidMoveError):
        move(player, Direction.LEFT, maze)


def test_state():
    maze = Maze()
    player = Player()
    player.position = [0, 0]
    assert "P" in state(maze.state, player.position)


if __name__ == "__main__":
    pytest.main()
