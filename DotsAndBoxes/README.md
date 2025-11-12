# Dots and Boxes Game

## Purpose

This program demonstrates a console-based implementation of the classic Dots and Boxes game. Initially designed as a two-player game, it will later be enhanced with AI opponent capabilities to serve as a tutorial on integrating AI into applications using APIs like OpenAI or Google Gemini.

## Description

Dots and Boxes is a pencil-and-paper game for two players. Players take turns drawing lines between adjacent dots on a grid. When a player completes a box (square) by drawing its fourth side, they score a point and get another turn. The player with the most boxes at the end of the game wins.

This implementation demonstrates:

- Object-oriented game design with separation of concerns
- Game state management and validation
- Console-based user interface
- Move validation and box completion detection
- Score tracking and game termination

## Program Structure

### Main Components

#### 1. dots_and_boxes.py (Main Program)

The entry point for the application. This file provides the main game loop that:

- Initializes the game board
- Displays the current game state
- Gets player input
- Processes moves
- Determines when the game is over
- Displays the winner

#### 2. game_board.py

Contains the `GameBoard` class that manages all game logic:

- **Game State**: Tracks horizontal lines, vertical lines, completed boxes, and scores
- **Move Validation**: Checks if moves are valid before applying them
- **Box Completion**: Detects when boxes are completed and assigns ownership
- **Score Tracking**: Maintains scores for both players
- **Game Over Detection**: Determines when all boxes are completed

Key methods:
- `make_move()`: Makes a move and checks for box completion
- `is_valid_move()`: Validates if a move is legal
- `is_game_over()`: Checks if the game has ended
- `get_score()`: Returns a player's score
- `get_winner()`: Returns the winner (or None for a tie)

#### 3. game_ui.py

Handles all console display and user input:

- **Board Display**: Renders the game board with dots, lines, and completed boxes
- **Score Display**: Shows current scores and whose turn it is
- **Input Handling**: Gets and validates player moves
- **Messages**: Displays welcome message, instructions, and game over message

Key functions:
- `display_board()`: Renders the game board in ASCII art
- `display_scores()`: Shows current scores
- `get_player_move()`: Gets and validates player input
- `display_welcome()`: Shows game instructions
- `display_game_over()`: Shows final scores and winner

### File Dependencies

```
dots_and_boxes.py
    ↓ imports from
game_ui.py
    ↓ imports from
game_board.py
```

## How to Play

### Running the Game

```bash
python dots_and_boxes.py
```

### Game Rules

1. The game is played on a grid of dots (default: 3x3 dots, creating 2x2 boxes)
2. Players take turns drawing lines between adjacent dots
3. Lines can be horizontal (between dots in the same row) or vertical (between dots in the same column)
4. When a player completes a box (draws its fourth side), they:
   - Score one point
   - Get another turn (do not switch players)
5. The game ends when all boxes are completed
6. The player with the most boxes wins (or it's a tie if scores are equal)

### Making a Move

When prompted, enter your move in the format:
```
h row col
```
or
```
v row col
```

Where:
- `h` = horizontal line
- `v` = vertical line
- `row` = row coordinate (0-indexed)
- `col` = column coordinate (0-indexed)

**Example**: `h 0 0` draws a horizontal line at row 0, column 0 (connecting the dots at (0,0) and (0,1))

### Coordinate System

- Coordinates are 0-indexed (start from 0)
- For a 3x3 grid:
  - Rows: 0, 1, 2
  - Columns: 0, 1, 2 (for horizontal lines)
  - Columns: 0, 1 (for vertical lines, since there are fewer vertical line positions)

## Current Features

- Two-player game mode (players take turns on the same console)
- 3x3 grid (2x2 boxes) - configurable in code
- Move validation
- Automatic box completion detection
- Score tracking
- Turn management (player gets another turn when completing a box)
- Game over detection
- Winner determination

## Future Features

### AI Opponent Integration

The game will be enhanced to support playing against an AI opponent using:

- **OpenAI API**: Integration with GPT models for intelligent move selection
- **Google Gemini API**: Alternative AI integration option
- **Tutorial Documentation**: Step-by-step guide on integrating AI APIs into the game

The `tutorial/` folder contains documentation on:

1. Game Overview - Understanding the game mechanics
2. Game Logic - How the game state is managed
3. Console UI - How the user interface works
4. AI Integration - How to integrate AI APIs (to be added)

## Technical Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Code Structure

The code follows object-oriented principles with clear separation of concerns:

- **Game Logic** (`game_board.py`): Pure game state management, no UI code
- **User Interface** (`game_ui.py`): Display and input handling, no game logic
- **Main Program** (`dots_and_boxes.py`): Orchestrates the game loop

This modular design makes it easy to:
- Test game logic independently
- Swap out the UI (e.g., for a graphical interface)
- Add AI opponents (they can use the same `GameBoard` class)

## Tutorial

See the `tutorial/` folder for detailed documentation on:

- **01-game-overview.md**: What is Dots and Boxes, basic rules, project goals
- **02-game-logic.md**: How the game state is represented, move validation, box completion logic
- **03-console-ui.md**: How the console interface works, displaying the board, handling input
- **04-ai-integration.md**: How to integrate AI APIs (placeholder for future)

## Educational Use

This project is designed for educational purposes to demonstrate:

- Game development fundamentals
- Object-oriented programming
- Separation of concerns in software design
- API integration (future)
- AI integration patterns (future)

## Authors

Initial implementation for CS210: Intro to AI Programming

## License

This code is available under the MIT License.

Educational use only.

