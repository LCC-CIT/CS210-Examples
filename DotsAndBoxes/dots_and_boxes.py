# dots_and_boxes.py
# Main entry point for the Dots and Boxes game.
# Console-based two-player game where players take turns drawing lines to complete boxes.

from game_board import GameBoard
from game_ui import (
    display_board,
    display_scores,
    display_game_over,
    display_welcome,
    get_player_move
)


def main():
    """
    Main entry point for the Dots and Boxes game.
    
    This function runs the game loop, coordinating between the game board,
    UI display, and player input. The game continues until all boxes are
    completed, then displays the final scores and winner.
    """
    # Display welcome message and instructions
    display_welcome()
    
    # Initialize game board (3x3 dots = 2x2 boxes by default)
    board = GameBoard(rows=3, cols=3)
    
    # Main game loop
    while not board.is_game_over():
        # Display current game state
        display_board(board)
        display_scores(board)
        
        # Get player move
        move = get_player_move(board)
        
        # Handle quit
        if move is None:
            print("Game ended by player. Goodbye!")
            return
        
        # Make the move
        move_type, row, col = move
        success = board.make_move(move_type, row, col)
        
        if not success:
            print("Invalid move. Please try again.")
            continue
        
        # Check if player completed a box (they get another turn)
        # This is handled in make_move() which doesn't switch players if boxes were completed
        
        # Display message if box was completed
        if board.get_score(board.current_player) > 0:
            # Check if score increased (indicating a box was just completed)
            # Note: This is a simple check; in a more sophisticated implementation,
            # we could track this more precisely
            pass
    
    # Game over - display final state
    display_board(board)
    display_game_over(board)


if __name__ == "__main__":
    main()

