"""
Search Algorithms Module
Implements uninformed and informed search strategies for pathfinding in grid environments.

Classical AI Concepts:
- State space: Configuration of the agent's position in the grid
- Search frontier: Set of nodes eligible for expansion (open list)
- Visited set: States already explored (closed list)
- Optimality: Guarantee of finding lowest-cost path
- Completeness: Guarantee of finding solution if one exists
"""

from abc import ABC, abstractmethod
from collections import deque
import heapq
from typing import List, Tuple, Dict, Set, Optional
import math


class SearchNode:
    """
    Represents a node in the search tree.
    
    Attributes:
        state: (x, y) grid position
        parent: Parent node (for path reconstruction)
        g_cost: Actual cost from start to this node
        h_cost: Heuristic estimate to goal (0 for uninformed search)
        f_cost: g_cost + h_cost (for A*)
    """
    
    def __init__(self, state: Tuple[int, int], parent=None, g_cost: float = 0, h_cost: float = 0):
        self.state = state
        self.parent = parent
        self.g_cost = g_cost  # Actual cost from start
        self.h_cost = h_cost  # Heuristic estimate to goal
        self.f_cost = g_cost + h_cost  # Total estimated cost
    
    def __lt__(self, other):
        """Priority queue comparison: lower f_cost = higher priority."""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state
    
    def __hash__(self):
        return hash(self.state)


class SearchAlgorithm(ABC):
    """
    Abstract base class for search algorithms.
    Defines interface all search strategies must implement.
    """
    
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], 
                 grid_size: Tuple[int, int], obstacles: Set[Tuple[int, int]]):
        """
        Initialize search algorithm.
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            grid_size: (width, height) of grid
            obstacles: Set of impassable grid cells
        """
        self.start = start
        self.goal = goal
        self.grid_size = grid_size
        self.obstacles = obstacles
        
        # Metrics tracking
        self.expanded_nodes = 0
        self.frontier_history = []  # Track frontier at each step
        self.visited_history = []   # Track visited nodes at each step
        self.path = []
        self.total_cost = 0
    
    @abstractmethod
    def search(self) -> bool:
        """
        Execute search algorithm. Must be implemented by subclasses.
        
        Returns:
            True if path found, False otherwise
        """
        pass
    
    def reconstruct_path(self, node: SearchNode) -> List[Tuple[int, int]]:
        """
        Backtrack from goal node to start node following parent pointers.
        
        This is standard path reconstruction in graph search algorithms.
        Time complexity: O(path length)
        """
        path = []
        current = node
        while current is not None:
            path.append(current.state)
            current = current.parent
        return path[::-1]
    
    def is_valid(self, x: int, y: int) -> bool:
        """Check if position is within bounds and not an obstacle."""
        return (0 <= x < self.grid_size[0] and 
                0 <= y < self.grid_size[1] and 
                (x, y) not in self.obstacles)
    
    def get_neighbors(self, state: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get valid adjacent cells (4-connectivity: up, down, left, right).
        
        Note: 4-connectivity (no diagonals) is standard for Manhattan distance heuristic.
        """
        x, y = state
        neighbors = []
        # Order: right, down, left, up (for consistent exploration)
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors


class BreadthFirstSearch(SearchAlgorithm):
    """
    Breadth-First Search (BFS)
    
    Uninformed search strategy that explores all nodes at depth d before depth d+1.
    
    Properties:
    - COMPLETE: Always finds solution if one exists
    - OPTIMAL: Yes, if all edge costs are equal (unweighted graph)
    - Time: O(b^d) where b is branching factor, d is depth
    - Space: O(b^d) - worst case, entire frontier in memory
    - Use case: Unweighted shortest paths
    """
    
    def search(self) -> bool:
        """Execute BFS using FIFO queue."""
        frontier = deque()
        start_node = SearchNode(self.start, parent=None, g_cost=0)
        frontier.append(start_node)
        
        visited = {self.start}
        
        while frontier:
            # Record frontier state for visualization
            self.frontier_history.append([n.state for n in frontier])
            self.visited_history.append(list(visited))
            
            # Dequeue from front (FIFO behavior)
            node = frontier.popleft()
            self.expanded_nodes += 1
            
            if node.state == self.goal:
                self.path = self.reconstruct_path(node)
                self.total_cost = node.g_cost
                return True
            
            # Expand neighbors
            for neighbor_state in self.get_neighbors(node.state):
                if neighbor_state not in visited:
                    visited.add(neighbor_state)
                    # All edges have cost 1 in unweighted graph
                    neighbor_node = SearchNode(neighbor_state, parent=node, g_cost=node.g_cost + 1)
                    frontier.append(neighbor_node)
        
        return False


class DepthFirstSearch(SearchAlgorithm):
    """
    Depth-First Search (DFS)
    
    Uninformed search that explores as far as possible along each branch.
    
    Properties:
    - COMPLETE: No (can get stuck in cycles without visited set, finds solution with visited set)
    - OPTIMAL: No (may find longer paths)
    - Time: O(b^m) where m is maximum depth
    - Space: O(b*m) - only stores path from root
    - Use case: Memory-constrained scenarios, topological ordering
    """
    
    def search(self) -> bool:
        """Execute DFS using LIFO stack."""
        frontier = [SearchNode(self.start, parent=None, g_cost=0)]
        visited = {self.start}
        
        while frontier:
            # Record frontier state
            self.frontier_history.append([n.state for n in frontier])
            self.visited_history.append(list(visited))
            
            # Pop from end (LIFO/stack behavior)
            node = frontier.pop()
            self.expanded_nodes += 1
            
            if node.state == self.goal:
                self.path = self.reconstruct_path(node)
                self.total_cost = node.g_cost
                return True
            
            # Expand neighbors (reversed for consistent left-to-right exploration)
            neighbors = self.get_neighbors(node.state)
            for neighbor_state in reversed(neighbors):
                if neighbor_state not in visited:
                    visited.add(neighbor_state)
                    neighbor_node = SearchNode(neighbor_state, parent=node, g_cost=node.g_cost + 1)
                    frontier.append(neighbor_node)
        
        return False


class UniformCostSearch(SearchAlgorithm):
    """
    Uniform Cost Search (UCS)
    
    Informed search using actual path cost as heuristic (no estimate).
    Expands nodes in order of path cost from start.
    
    Properties:
    - COMPLETE: Yes
    - OPTIMAL: Yes (finds minimum-cost path)
    - Time: O(b^(1+floor(C*/e))) where C* is optimal cost
    - Space: O(b^(1+floor(C*/e)))
    - Use case: Weighted graphs where edge costs vary, no good heuristic available
    
    Connection to A*:
    - UCS is A* with h(n) = 0 (no heuristic guidance)
    - Priority: f(n) = g(n) + 0 = g(n)
    """
    
    def search(self) -> bool:
        """Execute UCS using priority queue ordered by path cost."""
        frontier = []
        start_node = SearchNode(self.start, parent=None, g_cost=0, h_cost=0)
        heapq.heappush(frontier, start_node)
        
        visited = set()
        
        while frontier:
            # Record frontier (convert heap to list for visualization)
            self.frontier_history.append([n.state for n in frontier])
            self.visited_history.append(list(visited))
            
            # Extract node with minimum path cost
            node = heapq.heappop(frontier)
            
            if node.state in visited:
                continue
            
            visited.add(node.state)
            self.expanded_nodes += 1
            
            if node.state == self.goal:
                self.path = self.reconstruct_path(node)
                self.total_cost = node.g_cost
                return True
            
            # Expand neighbors, all with cost 1 in grid navigation
            for neighbor_state in self.get_neighbors(node.state):
                if neighbor_state not in visited:
                    neighbor_node = SearchNode(
                        neighbor_state, 
                        parent=node, 
                        g_cost=node.g_cost + 1,
                        h_cost=0
                    )
                    heapq.heappush(frontier, neighbor_node)
        
        return False


class AStarSearch(SearchAlgorithm):
    """
    A* Search
    
    Informed search combining actual cost g(n) with heuristic estimate h(n).
    
    Core equation: f(n) = g(n) + h(n)
    where:
        g(n) = actual cost from start to n
        h(n) = heuristic estimate from n to goal
        f(n) = estimated total cost of path through n
    
    Properties:
    - COMPLETE: Yes
    - OPTIMAL: Yes (if h is admissible)
    - Time: O(b^d) with good heuristic (much faster than uninformed)
    - Space: O(b^d) - same worst case, better average
    
    Admissibility:
    - h(n) ≤ h*(n) for all n, where h* is true minimum cost to goal
    - Never overestimates actual cost
    - Guarantees optimality
    
    Heuristic Design (Manhattan Distance):
    - h(x,y) = |x_goal - x| + |y_goal - y|
    - Admissible because straight-line distance ≥ Manhattan distance
    - Consistent (monotonic): h(n) ≤ cost(n,n') + h(n')
    - Very effective for grid navigation with 4-connectivity
    """
    
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], 
                 grid_size: Tuple[int, int], obstacles: Set[Tuple[int, int]]):
        super().__init__(start, goal, grid_size, obstacles)
        self.goal = goal
    
    def heuristic(self, state: Tuple[int, int]) -> float:
        """
        Manhattan Distance Heuristic
        
        For grid with 4-connectivity (no diagonals), Manhattan distance is admissible.
        
        Mathematical property:
        - h(x,y) = |goal_x - x| + |goal_y - y|
        - Lower bound on actual cost because you must move |Δx| steps horizontally
          and |Δy| steps vertically, minimum |Δx| + |Δy| moves
        """
        x, y = state
        goal_x, goal_y = self.goal
        return abs(goal_x - x) + abs(goal_y - y)
    
    def search(self) -> bool:
        """Execute A* using priority queue ordered by f(n) = g(n) + h(n)."""
        frontier = []
        start_node = SearchNode(
            self.start, 
            parent=None, 
            g_cost=0, 
            h_cost=self.heuristic(self.start)
        )
        heapq.heappush(frontier, start_node)
        
        visited = set()
        g_score = {self.start: 0}
        
        while frontier:
            # Record frontier state
            self.frontier_history.append([n.state for n in frontier])
            self.visited_history.append(list(visited))
            
            # Extract node with minimum f(n)
            node = heapq.heappop(frontier)
            
            if node.state in visited:
                continue
            
            visited.add(node.state)
            self.expanded_nodes += 1
            
            if node.state == self.goal:
                self.path = self.reconstruct_path(node)
                self.total_cost = node.g_cost
                return True
            
            # Expand neighbors
            for neighbor_state in self.get_neighbors(node.state):
                if neighbor_state not in visited:
                    new_g_cost = node.g_cost + 1
                    
                    # Only add if we found better path or haven't seen it
                    if neighbor_state not in g_score or new_g_cost < g_score[neighbor_state]:
                        g_score[neighbor_state] = new_g_cost
                        h_cost = self.heuristic(neighbor_state)
                        neighbor_node = SearchNode(
                            neighbor_state,
                            parent=node,
                            g_cost=new_g_cost,
                            h_cost=h_cost
                        )
                        heapq.heappush(frontier, neighbor_node)
        
        return False
