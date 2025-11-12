# Console UI: Displaying the Game

## Overview

The console user interface (`game_ui.py`) handles all aspects of displaying the game and getting input from players. It is completely separate from the game logic, making it easy to swap out for a different UI (e.g., a graphical interface) without changing the game logic.

## Displaying the Board

The `display_board()` function renders the game board using ASCII art. The board shows:

- **Dots** (·): The intersections where lines can be drawn
- **Horizontal Lines** (---): Lines connecting dots in the same row
- **Vertical Lines** (|): Lines connecting dots in the same column
- **Box Contents**: Player numbers (1 or 2) in completed boxes
- **Coordinates**: Row numbers on the left, column numbers at the top

### Example Board Display

```
==================================================
     0    1  
0 ·---·   ·
  |   |   
1 ·   ·   ·
     |     
2 ·   ·   ·
==================================================
```

This shows:
- A 3x3 grid of dots
- A horizontal line at (0,0) connecting the top two dots
- A vertical line at (0,0) connecting the left two dots
- An incomplete box at (0,0) (three sides drawn, one missing)

### Completed Box Display

```
==================================================
     0    1  
0 ·---·   ·
  | 1 |   
1 ·---·   ·
        
2 ·   ·   ·
==================================================
```

This shows:
- Player 1 owns the box at (0,0)
- The box is complete (all four sides drawn)

## Board Rendering Algorithm

The board is rendered in two passes:

1. **First Pass**: Display dots and horizontal lines
   - For each row, display dots and horizontal lines between them
   - Show row numbers on the left

2. **Second Pass**: Display vertical lines and box contents
   - Between rows, display vertical lines and box contents
   - Show column numbers at the top (for horizontal line coordinates)

### Implementation Details

```python
# Display column numbers
print("   ", end="")
for col in range(board.cols - 1):
    print(f"  {col}  ", end="")
print()

# Display each row
for row in range(board.rows):
    # Display dots and horizontal lines
    print(f"{row} ", end="")
    for col in range(board.cols):
        print("·", end="")
        if col < board.cols - 1:
            if (row, col) in board.horizontal_lines:
                print("---", end="")
            else:
                print("   ", end="")
    print()
    
    # Display vertical lines and box contents
    if row < board.rows - 1:
        print("   ", end="")
        for col in range(board.cols):
            if (row, col) in board.vertical_lines:
                print("|", end="")
            else:
                print(" ", end="")
            
            if col < board.cols - 1:
                box_key = (row, col)
                if box_key in board.boxes:
                    owner = board.boxes[box_key]
                    print(f" {owner} ", end="")
                else:
                    print("   ", end="")
        print()
```

## Displaying Scores

The `display_scores()` function shows:

- Current scores for both players
- Which player's turn it is

Example output:
```
Player 1 Score: 2
Player 2 Score: 1
Current Player: Player 1
```

## Getting Player Input

The `get_player_move()` function handles player input with validation:

1. **Prompt**: Asks the player to enter their move
2. **Parse**: Parses the input into move type, row, and column
3. **Validate**: Checks if the move is valid
4. **Return**: Returns the move as a tuple, or None if invalid/quit

### Input Format

Players enter moves in the format:
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

### Example Input

```
Player 1, enter your move (h/v row col) or 'q' to quit: h 0 0
```

This draws a horizontal line at row 0, column 0.

### Input Validation

The function validates:

1. **Format**: Input must have three parts (move type, row, col)
2. **Move Type**: Must be 'h' or 'v'
3. **Coordinates**: Must be integers
4. **Move Validity**: Move must be valid (within bounds, line not already drawn)
5. **Quit**: Player can enter 'q' to quit

### Error Handling

The function handles various errors:

- **Invalid Format**: "Invalid input. Please enter: h/v row col"
- **Invalid Move Type**: "Move type must be 'h' (horizontal) or 'v' (vertical)"
- **Invalid Coordinates**: "Invalid input. Please enter numbers for row and column."
- **Invalid Move**: "Invalid move. That line is already drawn or coordinates are out of bounds."
- **Keyboard Interrupt**: Handles Ctrl+C gracefully

## Welcome Message

The `display_welcome()` function shows:

- Game title
- Game rules
- Instructions for making moves
- Coordinate system explanation

This helps new players understand how to play.

## Game Over Display

The `display_game_over()` function shows:

- Game over message
- Final scores
- Winner (or tie)

Example output:
```
==================================================
GAME OVER!
==================================================
Player 1 Score: 3
Player 2 Score: 1
Player 1 Wins!
==================================================
```

## UI Design Principles

The UI follows several important design principles:

1. **Separation of Concerns**: UI code is separate from game logic
2. **Clear Communication**: Messages are clear and helpful
3. **Error Handling**: Invalid input is handled gracefully
4. **User Feedback**: Players always know the current game state
5. **Accessibility**: Simple text-based interface works on any system

## Making the UI Better

Potential improvements:

1. **Color**: Use ANSI color codes to highlight different elements
2. **Clear Screen**: Clear the screen between moves for a cleaner display
3. **Move History**: Show a history of recent moves
4. **Help Command**: Add a 'help' command to show instructions during the game
5. **Move Suggestions**: Show available moves when player is stuck

## Integration with Game Logic

The UI interacts with the game logic through the `GameBoard` class:

- **Reading State**: UI reads board state to display it
- **Making Moves**: UI gets moves from players and calls `board.make_move()`
- **Checking Status**: UI checks `board.is_game_over()` and `board.get_winner()`

The UI never modifies the game state directly - all changes go through the `GameBoard` methods.

## Next Steps

- **04-ai-integration.md**: Learn how to integrate AI APIs to create an AI opponent (future tutorial)

