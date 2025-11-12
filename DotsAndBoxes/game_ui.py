# game_ui.py
# Console UI and display functions for Dots and Boxes.
# Handles board display, input validation, and user interaction.

from game_board import GameBoard
from typing import Tuple, Optional


def display_board(board: GameBoard) -> None:
    """
    Display the game board in the console.
    
    Args:
        board (GameBoard): The game board to display
    """
    print("\n" + "=" * 50)
    
    # Display column numbers at the top (for horizontal line coordinates)
    print("   ", end="")
    for col in range(board.cols - 1):
        print(f"  {col}  ", end="")
    print()
    
    # Display each row of dots and boxes
    for row in range(board.rows):
        # First line: dots and horizontal lines
        print(f"{row} ", end="")
        for col in range(board.cols):
            print("·", end="")
            if col < board.cols - 1:
                if (row, col) in board.horizontal_lines:
                    print("---", end="")
                else:
                    print("   ", end="")
        print()
        
        # Second line: vertical lines and box contents
        if row < board.rows - 1:
            print("   ", end="")
            for col in range(board.cols):
                # Vertical line or space
                if (row, col) in board.vertical_lines:
                    print("|", end="")
                else:
                    print(" ", end="")
                
                # Box content or space (only between columns, not after the last column)
                if col < board.cols - 1:
                    box_key = (row, col)
                    if box_key in board.boxes:
                        owner = board.boxes[box_key]
                        print(f" {owner} ", end="")
                    else:
                        print("   ", end="")
            print()
    
    print("=" * 50 + "\n")


def display_scores(board: GameBoard) -> None:
    """
    Display the current scores.
    
    Args:
        board (GameBoard): The game board
    """
    print(f"Player 1 Score: {board.get_score(1)}")
    print(f"Player 2 Score: {board.get_score(2)}")
    print(f"Current Player: Player {board.current_player}\n")


def display_game_over(board: GameBoard) -> None:
    """
    Display the game over message and winner.
    
    Args:
        board (GameBoard): The game board
    """
    print("\n" + "=" * 50)
    print("GAME OVER!")
    print("=" * 50)
    print(f"Player 1 Score: {board.get_score(1)}")
    print(f"Player 2 Score: {board.get_score(2)}")
    
    winner = board.get_winner()
    if winner:
        print(f"Player {winner} Wins!")
    else:
        print("It's a tie!")
    print("=" * 50 + "\n")


def display_welcome() -> None:
    """
    Display the welcome message and game instructions.
    """
    print("=" * 50)
    print("Welcome to Dots and Boxes!")
    print("=" * 50)
    print("\nGame Rules:")
    print("- Players take turns drawing lines between adjacent dots")
    print("- Horizontal lines: connect dots in the same row")
    print("- Vertical lines: connect dots in the same column")
    print("- When you complete a box (square), you score a point and get another turn")
    print("- The player with the most boxes at the end wins!")
    print("\nMaking a Move:")
    print("- Enter 'h' for horizontal line or 'v' for vertical line")
    print("- Then enter the row and column coordinates")
    print("- Example: 'h 0 0' draws a horizontal line at row 0, column 0")
    print("- Coordinates are 0-indexed (start from 0)")
    print("\n" + "=" * 50 + "\n")


def get_player_move(board: GameBoard) -> Optional[Tuple[str, int, int]]:
    """
    Get a move from the player with validation.
    
    Args:
        board (GameBoard): The game board
        
    Returns:
        Optional[Tuple[str, int, int]]: (move_type, row, col) if valid, None if invalid/quit
    """
    while True:
        try:
            move_input = input(
                f"Player {board.current_player}, enter your move (h/v row col) or 'q' to quit: "
            ).strip().lower()
            
            if move_input == 'q':
                return None
            
            parts = move_input.split()
            if len(parts) != 3:
                print("Invalid input. Please enter: h/v row col")
                continue
            
            move_type = parts[0]
            if move_type not in ['h', 'v']:
                print("Move type must be 'h' (horizontal) or 'v' (vertical)")
                continue
            
            row = int(parts[1])
            col = int(parts[2])
            
            if not board.is_valid_move(move_type, row, col):
                print("Invalid move. That line is already drawn or coordinates are out of bounds.")
                continue
            
            return (move_type, row, col)
        
        except ValueError:
            print("Invalid input. Please enter numbers for row and column.")
        except KeyboardInterrupt:
            print("\nGame interrupted. Goodbye!")
            return None
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def display_available_moves(board: GameBoard) -> None:
    """
    Display available moves (optional helper function).
    
    Args:
        board (GameBoard): The game board
    """
    moves = board.get_available_moves()
    if moves:
        print(f"Available moves ({len(moves)} remaining):")
        # Show first few moves as examples
        for move in moves[:5]:
            print(f"  {move[0]} {move[1]} {move[2]}")
        if len(moves) > 5:
            print(f"  ... and {len(moves) - 5} more")
    else:
        print("No moves available.")

