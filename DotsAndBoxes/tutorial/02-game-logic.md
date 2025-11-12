# Game Logic: How Dots and Boxes Works

## Game State Representation

The game state is managed by the `GameBoard` class in `game_board.py`. The board represents:

- **Grid of Dots**: A 2D grid of dots (e.g., 3x3 dots)
- **Horizontal Lines**: Lines drawn between dots in the same row
- **Vertical Lines**: Lines drawn between dots in the same column
- **Completed Boxes**: Boxes that have all four sides drawn, along with which player owns them
- **Scores**: Points for each player
- **Current Player**: Which player's turn it is

## Data Structures

### Horizontal Lines
Stored as a set of tuples: `(row, col)` where:
- `row`: The row of the dot on the left
- `col`: The column of the left dot (0 to cols-2)

Example: `(0, 0)` represents a horizontal line connecting dots at (0,0) and (0,1)

### Vertical Lines
Stored as a set of tuples: `(row, col)` where:
- `row`: The row of the top dot (0 to rows-2)
- `col`: The column of the dot

Example: `(0, 0)` represents a vertical line connecting dots at (0,0) and (1,0)

### Completed Boxes
Stored as a dictionary: `{(row, col): player}` where:
- `(row, col)`: The top-left corner of the box (coordinates of the top-left dot)
- `player`: The player number (1 or 2) who owns the box

Example: `{(0, 0): 1}` means Player 1 owns the box in the top-left corner

## Move Validation

Before a move can be made, the game checks:

1. **Move Type**: Must be 'h' (horizontal) or 'v' (vertical)
2. **Coordinates**: Must be within valid bounds:
   - Horizontal: `0 <= row < rows` and `0 <= col < cols-1`
   - Vertical: `0 <= row < rows-1` and `0 <= col < cols`
3. **Line Not Already Drawn**: The line must not already exist in the respective set

### Example Validation

```python
# Valid horizontal move on 3x3 grid
move_type = 'h'
row = 0
col = 0
# Valid: connects dots at (0,0) and (0,1)

# Invalid horizontal move
move_type = 'h'
row = 0
col = 2
# Invalid: col must be < cols-1 (2 < 2 is False)

# Valid vertical move
move_type = 'v'
row = 0
col = 0
# Valid: connects dots at (0,0) and (1,0)
```

## Box Completion Detection

When a line is drawn, the game checks if any boxes were completed. A box is complete when all four sides are drawn:

1. **Top horizontal line**: `(box_row, box_col)` in `horizontal_lines`
2. **Bottom horizontal line**: `(box_row + 1, box_col)` in `horizontal_lines`
3. **Left vertical line**: `(box_row, box_col)` in `vertical_lines`
4. **Right vertical line**: `(box_row, box_col + 1)` in `vertical_lines`

### Checking Adjacent Boxes

When a horizontal line is drawn at `(row, col)`:
- Check box above: `(row - 1, col)` (if `row > 0`)
- Check box below: `(row, col)` (if `row < rows - 1`)

When a vertical line is drawn at `(row, col)`:
- Check box to the left: `(row, col - 1)` (if `col > 0`)
- Check box to the right: `(row, col)` (if `col < cols - 1`)

### Example Box Completion

```
Grid state:
·---·   ·
|   |   
·---·   ·

Horizontal line at (1,0) is drawn:
·---·   ·
|   |   
·---·---·

This completes the box at (0,0):
- Top: (0,0) ✓
- Bottom: (1,0) ✓
- Left: (0,0) ✓
- Right: (0,1) ✓

Box is marked as owned by current player.
```

## Turn Management

The game uses a simple turn management system:

1. **Normal Turn**: After a move, if no boxes were completed, switch to the other player
2. **Box Completed**: If one or more boxes were completed, the current player keeps their turn
3. **Multiple Boxes**: If multiple boxes are completed in one move, the player gets another turn (but this is rare in small grids)

### Implementation

```python
boxes_completed = self._check_and_mark_boxes(move_type, row, col)

# If no boxes were completed, switch players
if boxes_completed == 0:
    self.current_player = 3 - self.current_player  # Switch between 1 and 2
```

The expression `3 - self.current_player` switches between 1 and 2:
- If current player is 1: `3 - 1 = 2`
- If current player is 2: `3 - 2 = 1`

## Game Over Detection

The game ends when all boxes are completed. The total number of boxes is:

```python
total_boxes = (rows - 1) * (cols - 1)
```

For a 3x3 grid of dots: `(3 - 1) * (3 - 1) = 2 * 2 = 4 boxes`

The game checks if the number of completed boxes equals the total:

```python
def is_game_over(self) -> bool:
    total_boxes = (self.rows - 1) * (self.cols - 1)
    return len(self.boxes) >= total_boxes
```

## Winner Determination

After the game ends, the winner is determined by comparing scores:

```python
def get_winner(self) -> Optional[int]:
    if not self.is_game_over():
        return None
    
    if self.scores[1] > self.scores[2]:
        return 1
    elif self.scores[2] > self.scores[1]:
        return 2
    else:
        return None  # Tie
```

## Key Methods

### `make_move(move_type, row, col)`
1. Validates the move
2. Adds the line to the appropriate set
3. Checks for completed boxes
4. Updates scores
5. Manages turn switching

### `is_valid_move(move_type, row, col)`
Checks if a move is legal before making it

### `_check_and_mark_boxes(move_type, row, col)`
Checks adjacent boxes for completion and marks them if complete

### `_is_box_complete(box_row, box_col)`
Checks if all four sides of a box are drawn

### `get_available_moves()`
Returns a list of all legal moves remaining

## Design Patterns

The game logic uses several important design patterns:

1. **Separation of Concerns**: Game logic is completely separate from UI code
2. **Immutable State Updates**: State is updated through well-defined methods
3. **Validation Before Action**: Moves are validated before being applied
4. **Encapsulation**: Internal state is protected, accessed only through methods

This design makes it easy to:
- Test game logic independently
- Add AI players (they use the same `GameBoard` class)
- Swap out the UI (e.g., for a graphical interface)

## Next Steps

- **03-console-ui.md**: Learn how the console interface displays the board and handles input
- **04-ai-integration.md**: Learn how to integrate AI APIs (future tutorial)

