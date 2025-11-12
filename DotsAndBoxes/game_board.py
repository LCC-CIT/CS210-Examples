# game_board.py
# Game board logic and state management for Dots and Boxes.
# Manages the game state, moves, box completion, and scoring.

from typing import Set, Tuple, List, Optional


class GameBoard:
    """
    Represents the game board for Dots and Boxes.
    
    The board is a grid of dots. Players draw lines between adjacent dots.
    When a player completes a box (square), they score a point and get another turn.
    The game ends when all boxes are completed.
    
    Attributes:
        rows (int): Number of rows of dots
        cols (int): Number of columns of dots
        horizontal_lines (Set[Tuple[int, int]]): Set of horizontal line coordinates (row, col)
        vertical_lines (Set[Tuple[int, int]]): Set of vertical line coordinates (row, col)
        boxes (dict): Dictionary mapping box coordinates to player number (1 or 2)
        current_player (int): Current player (1 or 2)
        scores (dict): Dictionary mapping player number to score
    """
    
    def __init__(self, rows: int = 3, cols: int = 3):
        """
        Initialize a new game board.
        
        Args:
            rows (int): Number of rows of dots (default: 3)
            cols (int): Number of columns of dots (default: 3)
        """
        self.rows = rows
        self.cols = cols
        # Horizontal lines: (row, col) where col is the left dot column
        self.horizontal_lines: Set[Tuple[int, int]] = set()
        # Vertical lines: (row, col) where row is the top dot row
        self.vertical_lines: Set[Tuple[int, int]] = set()
        # Boxes: (row, col) -> player number, where (row, col) is top-left corner
        self.boxes: dict = {}
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
    
    def make_move(self, move_type: str, row: int, col: int) -> bool:
        """
        Make a move on the board.
        
        Args:
            move_type (str): 'h' for horizontal line, 'v' for vertical line
            row (int): Row coordinate
            col (int): Column coordinate
            
        Returns:
            bool: True if move was valid and made, False otherwise
        """
        if not self.is_valid_move(move_type, row, col):
            return False
        
        # Add the line
        if move_type == 'h':
            self.horizontal_lines.add((row, col))
        else:  # move_type == 'v'
            self.vertical_lines.add((row, col))
        
        # Check for completed boxes
        boxes_completed = self._check_and_mark_boxes(move_type, row, col)
        
        # If no boxes were completed, switch players
        if boxes_completed == 0:
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
        
        # Update scores
        self.scores[self.current_player] += boxes_completed
        
        return True
    
    def is_valid_move(self, move_type: str, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        Args:
            move_type (str): 'h' for horizontal line, 'v' for vertical line
            row (int): Row coordinate
            col (int): Column coordinate
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        if move_type == 'h':
            # Horizontal line: valid if 0 <= row < rows and 0 <= col < cols-1
            if row < 0 or row >= self.rows:
                return False
            if col < 0 or col >= self.cols - 1:
                return False
            return (row, col) not in self.horizontal_lines
        elif move_type == 'v':
            # Vertical line: valid if 0 <= row < rows-1 and 0 <= col < cols
            if row < 0 or row >= self.rows - 1:
                return False
            if col < 0 or col >= self.cols:
                return False
            return (row, col) not in self.vertical_lines
        else:
            return False
    
    def _check_and_mark_boxes(self, move_type: str, row: int, col: int) -> int:
        """
        Check for boxes completed by the most recent move and mark them.
        
        Args:
            move_type (str): 'h' for horizontal line, 'v' for vertical line
            row (int): Row coordinate of the line
            col (int): Column coordinate of the line
            
        Returns:
            int: Number of boxes completed by this move
        """
        boxes_completed = 0
        
        if move_type == 'h':
            # Check box above the horizontal line
            if row > 0:
                if self._is_box_complete(row - 1, col):
                    if (row - 1, col) not in self.boxes:
                        self.boxes[(row - 1, col)] = self.current_player
                        boxes_completed += 1
            
            # Check box below the horizontal line
            if row < self.rows - 1:
                if self._is_box_complete(row, col):
                    if (row, col) not in self.boxes:
                        self.boxes[(row, col)] = self.current_player
                        boxes_completed += 1
        
        else:  # move_type == 'v'
            # Check box to the left of the vertical line
            if col > 0:
                if self._is_box_complete(row, col - 1):
                    if (row, col - 1) not in self.boxes:
                        self.boxes[(row, col - 1)] = self.current_player
                        boxes_completed += 1
            
            # Check box to the right of the vertical line
            if col < self.cols - 1:
                if self._is_box_complete(row, col):
                    if (row, col) not in self.boxes:
                        self.boxes[(row, col)] = self.current_player
                        boxes_completed += 1
        
        return boxes_completed
    
    def _is_box_complete(self, box_row: int, box_col: int) -> bool:
        """
        Check if a box is complete (all four sides are drawn).
        
        Args:
            box_row (int): Row of the box (top-left corner row)
            box_col (int): Column of the box (top-left corner column)
            
        Returns:
            bool: True if box is complete, False otherwise
        """
        # Check top horizontal line
        if (box_row, box_col) not in self.horizontal_lines:
            return False
        
        # Check bottom horizontal line
        if (box_row + 1, box_col) not in self.horizontal_lines:
            return False
        
        # Check left vertical line
        if (box_row, box_col) not in self.vertical_lines:
            return False
        
        # Check right vertical line
        if (box_row, box_col + 1) not in self.vertical_lines:
            return False
        
        return True
    
    def get_score(self, player: int) -> int:
        """
        Get the score for a player.
        
        Args:
            player (int): Player number (1 or 2)
            
        Returns:
            int: Player's score
        """
        return self.scores.get(player, 0)
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over (all boxes are completed).
        
        Returns:
            bool: True if game is over, False otherwise
        """
        total_boxes = (self.rows - 1) * (self.cols - 1)
        return len(self.boxes) >= total_boxes
    
    def get_available_moves(self) -> List[Tuple[str, int, int]]:
        """
        Get a list of all available moves.
        
        Returns:
            List[Tuple[str, int, int]]: List of (move_type, row, col) tuples
        """
        moves = []
        
        # Horizontal moves
        for row in range(self.rows):
            for col in range(self.cols - 1):
                if (row, col) not in self.horizontal_lines:
                    moves.append(('h', row, col))
        
        # Vertical moves
        for row in range(self.rows - 1):
            for col in range(self.cols):
                if (row, col) not in self.vertical_lines:
                    moves.append(('v', row, col))
        
        return moves
    
    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game (if game is over).
        
        Returns:
            Optional[int]: Player number (1 or 2) if there's a winner, None if tie or game not over
        """
        if not self.is_game_over():
            return None
        
        if self.scores[1] > self.scores[2]:
            return 1
        elif self.scores[2] > self.scores[1]:
            return 2
        else:
            return None  # Tie

