# Maze Game
#### Video Demo:  https://youtu.be/IyOQWDACpAw
#### Description:

This is a simple maze game implemented in Python using the curses library. The objective of the game is to navigate through a randomly generated maze from the start ('S') to the end ('E') while avoiding obstacles ('#'). The player can use the arrow keys to move, and the game ends when the player reaches the end of the maze.

## Prerequisites

Before running the game, ensure that you have Python installed on your system. You'll also need the curses library, which is usually included with Python by default.

## How to Play

1. Clone this repository to your local machine or download the code.

2. Open your terminal and navigate to the directory containing the game files.

3. Run the game using the following command:

   ```bash
   python project.py
   ```

4. The game screen will appear, displaying the maze with the player's position marked as 'P'. You'll start at the 'S' (start) position.

5. Use the arrow keys (UP, DOWN, LEFT, RIGHT) to move the player through the maze. The goal is to reach the 'E' (end) position.

6. If you encounter an obstacle ('#') or try to move out of bounds, you'll receive an error message, and the game will continue.

7. Press 'q' at any time to quit the game.

8. If you successfully reach the 'E' position, you win the game! A win message will appear before the game closes.

## Code Structure

The code consists of the following components:

- `project.py`: The main Python script containing the game logic.

- `Direction`: An enumeration of directions for movement.

- `InvalidMoveError`: A custom exception class for handling invalid player moves.

- `Maze`: A class representing the maze game environment. It generates a random maze and keeps track of the game state.

- `Player`: A class representing the player in the maze game.

- `main`: The main game loop and logic for handling user input and displaying the game screen.

- Various helper functions for checking valid moves, updating player position, and displaying game messages.

## Acknowledgments

This maze game is a simple implementation designed for CS50P 2022's Final Project. It utilizes Python's curses library for handling terminal-based user interfaces. The game's core logic involves maze generation and navigation, providing an opportunity to explore concepts like data structures, game design, and user input handling.

Feel free to modify and expand upon this code to create more complex maze games or add additional features and challenges.