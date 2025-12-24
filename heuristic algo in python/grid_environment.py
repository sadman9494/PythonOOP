"""
Grid Environment Module
Defines the 2D grid world where search algorithms operate.

Environment Concepts:
- Configuration space: All possible grid states
- Start state: Agent's initial position
- Goal state: Target location
- Actions: Movement to adjacent cells (up, down, left, right)
- Transition model: Movement rules and constraints
- Step cost: Uniform cost of 1 per move
"""

from typing import Set, Tuple, List
import random


class GridEnvironment:
    """
    2D grid world with obstacles, start position, and goal.
    
    Coordinate system:
    - Origin (0, 0) at top-left
    - x increases rightward
    - y increases downward
    """
    
    def __init__(self, width: int, height: int, start: Tuple[int, int], 
                 goal: Tuple[int, int], obstacle_probability: float = 0.2):
        """
        Initialize grid environment.
        
        Args:
            width: Grid width in cells
            height: Grid height in cells
            start: Starting position (x, y)
            goal: Goal position (x, y)
            obstacle_probability: Probability of each cell being obstacle [0, 1)
        
        Raises:
            ValueError: If start or goal is invalid or overlaps
        """
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.obstacles: Set[Tuple[int, int]] = set()
        
        # Validate positions
        self._validate_position(start, "start")
        self._validate_position(goal, "goal")
        
        if start == goal:
            raise ValueError("Start and goal cannot be the same position")
        
        # Generate obstacles randomly
        self._generate_obstacles(obstacle_probability)
    
    def _validate_position(self, pos: Tuple[int, int], name: str) -> None:
        """Check if position is valid grid coordinate."""
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"{name} position {pos} outside grid bounds")
    
    def _generate_obstacles(self, probability: float) -> None:
        """
        Randomly generate obstacles with given probability.
        
        Ensures start and goal positions are clear.
        Uses random.random() for Monte Carlo sampling of obstacle placement.
        """
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                # Skip start and goal
                if pos == self.start or pos == self.goal:
                    continue
                # Place obstacle with given probability
                if random.random() < probability:
                    self.obstacles.add(pos)
    
    def set_obstacles(self, obstacles: Set[Tuple[int, int]]) -> None:
        """
        Set obstacles manually (replaces randomly generated ones).
        Useful for deterministic testing scenarios.
        """
        # Filter out start and goal positions
        self.obstacles = {
            obs for obs in obstacles 
            if obs != self.start and obs != self.goal
        }
    
    def add_obstacle(self, pos: Tuple[int, int]) -> None:
        """Add single obstacle if not start or goal."""
        if pos != self.start and pos != self.goal:
            self.obstacles.add(pos)
    
    def remove_obstacle(self, pos: Tuple[int, int]) -> None:
        """Remove single obstacle."""
        self.obstacles.discard(pos)
    
    def is_valid_cell(self, x: int, y: int) -> bool:
        """Check if cell is passable (within bounds and not obstacle)."""
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                (x, y) not in self.obstacles)
    
    def get_grid_info(self) -> dict:
        """Get summary statistics about the grid."""
        total_cells = self.width * self.height
        obstacle_count = len(self.obstacles)
        free_cells = total_cells - obstacle_count
        
        return {
            'dimensions': (self.width, self.height),
            'total_cells': total_cells,
            'obstacles': obstacle_count,
            'free_cells': free_cells,
            'obstacle_density': obstacle_count / total_cells if total_cells > 0 else 0,
            'start': self.start,
            'goal': self.goal
        }
    
    @staticmethod
    def create_predefined_maze(width: int, height: int) -> 'GridEnvironment':
        """
        Create grid with predefined maze-like obstacle pattern.
        Useful for testing algorithm performance on structured environments.
        """
        # Simple checkerboard pattern with selective removal
        env = GridEnvironment(width, height, (1, 1), (width-2, height-2), obstacle_probability=0)
        
        # Create walls
        for y in range(height):
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    env.add_obstacle((x, y))
                elif (x + y) % 3 == 0 and (x, y) not in [(1, 1), (width-2, height-2)]:
                    env.add_obstacle((x, y))
        
        return env
    
    @staticmethod
    def create_sparse_grid(width: int, height: int, obstacle_density: float = 0.1) -> 'GridEnvironment':
        """Create grid with specified obstacle density."""
        env = GridEnvironment(width, height, (0, 0), (width-1, height-1), 
                             obstacle_probability=obstacle_density)
        return env
    
    def reset_obstacles(self, obstacle_probability: float) -> None:
        """Clear and regenerate obstacles."""
        self.obstacles.clear()
        self._generate_obstacles(obstacle_probability)
