# Game Overview: Dots and Boxes

## What is Dots and Boxes?

Dots and Boxes is a classic pencil-and-paper game for two players. The game is played on a grid of dots, and players take turns drawing lines between adjacent dots to form boxes. The player who completes a box scores a point and gets another turn. The game ends when all boxes are completed, and the player with the most boxes wins.

## Basic Rules

1. **Setup**: Start with a grid of dots (e.g., 3x3 dots creates a 2x2 grid of boxes)

2. **Taking Turns**: Players alternate turns (unless a player completes a box, in which case they get another turn)

3. **Drawing Lines**: On each turn, a player draws one line between two adjacent dots:
   - **Horizontal lines**: Connect dots in the same row
   - **Vertical lines**: Connect dots in the same column

4. **Completing Boxes**: When a player draws the fourth side of a box (completing a square), they:
   - Score one point
   - Get another turn immediately (do not switch players)

5. **Winning**: The game ends when all boxes are completed. The player with the most boxes wins. If both players have the same number of boxes, it's a tie.

## Example Game

Here's a simple example on a 2x2 grid (3x3 dots):

```
Initial State:
·   ·   ·
        
·   ·   ·
        
·   ·   ·

After Player 1 draws horizontal line at (0,0):
·---·   ·
        
·   ·   ·
        
·   ·   ·

After Player 2 draws vertical line at (0,0):
·---·   ·
|       
·   ·   ·
        
·   ·   ·

After Player 1 draws horizontal line at (1,0) and vertical line at (0,1):
·---·   ·
|   |   
·---·   ·
        
·   ·   ·

After Player 2 draws the bottom horizontal line at (1,0):
·---·   ·
| 1 |   
·---·   ·
        
·   ·   ·
```

Player 1 completes the first box and scores a point, then gets another turn.

## Project Goals

This project serves multiple educational purposes:

1. **Game Development Fundamentals**: Demonstrates how to structure a game with clear separation between game logic and user interface

2. **Object-Oriented Programming**: Shows how to use classes and methods to manage game state

3. **Console Application Development**: Provides experience building interactive console applications

4. **AI Integration Tutorial**: Will serve as a foundation for learning how to integrate AI APIs (OpenAI, Gemini) into applications

5. **API Integration Patterns**: Will demonstrate how to call external APIs, handle responses, and integrate AI decision-making into game logic

## Game Structure

The game is organized into three main components:

- **Game Board** (`game_board.py`): Manages the game state, validates moves, detects box completion, and tracks scores
- **User Interface** (`game_ui.py`): Handles display and user input
- **Main Program** (`dots_and_boxes.py`): Orchestrates the game loop

This modular design makes it easy to:
- Test game logic independently
- Swap out the UI (e.g., for a graphical interface)
- Add AI opponents (they can use the same `GameBoard` class)

## Next Steps

- **02-game-logic.md**: Learn how the game state is represented and managed
- **03-console-ui.md**: Understand how the console interface works
- **04-ai-integration.md**: Learn how to integrate AI APIs (future tutorial)

