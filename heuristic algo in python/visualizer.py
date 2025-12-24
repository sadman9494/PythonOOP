"""
Streamlit Visualizer Module
Interactive web-based visualization of search algorithm execution.

Visualization Elements:
- Grid display with start, goal, obstacles
- Frontier expansion animation
- Visited states highlighting
- Optimal path rendering
- Real-time metrics dashboard
"""

import streamlit as st
import numpy as np
import pandas as pd
from typing import Dict, List, Set, Tuple, Optional
import plotly.graph_objects as go
from search_algorithms import (
    BreadthFirstSearch, DepthFirstSearch, 
    UniformCostSearch, AStarSearch
)
from grid_environment import GridEnvironment


# Page configuration
st.set_page_config(
    page_title="Search Algorithms Visualizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .algorithm-title {
        color: #1f77d4;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-header {
        color: #2c3e50;
        font-size: 20px;
        font-weight: bold;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


class GridVisualizer:
    """Handles grid visualization with Plotly."""
    
    def __init__(self, grid_env: GridEnvironment):
        self.grid_env = grid_env
        self.width = grid_env.width
        self.height = grid_env.height
    
    def create_base_grid(self) -> go.Figure:
        """Create base grid figure with obstacles."""
        # Create grid array (0 = empty, 1 = obstacle, 2 = start, 3 = goal)
        grid = np.zeros((self.height, self.width))
        
        # Mark obstacles
        for obs in self.grid_env.obstacles:
            grid[obs[1], obs[0]] = 1
        
        # Mark start and goal
        grid[self.grid_env.start[1], self.grid_env.start[0]] = 2
        grid[self.grid_env.goal[1], self.grid_env.goal[0]] = 3
        
        fig = go.Figure()
        
        # Add grid cells as rectangles
        fig.add_trace(go.Heatmap(
            z=grid,
            colorscale=[[0, 'white'], [1, 'black'], [0.5, 'lightblue'], [1, 'red']],
            showscale=False,
            hovertemplate='(%{x}, %{y})<extra></extra>'
        ))
        
        return fig
    
    def visualize_search_state(self, frontier: List[Tuple[int, int]], 
                              visited: Set[Tuple[int, int]],
                              path: List[Tuple[int, int]]) -> go.Figure:
        """
        Create visualization with frontier, visited, and path highlighted.
        
        Color coding:
        - White: Empty cells
        - Dark gray: Obstacles
        - Light blue: Start position
        - Red: Goal position
        - Yellow: Frontier (nodes eligible for expansion)
        - Green: Visited (already expanded)
        - Blue: Optimal path
        """
        grid = np.zeros((self.height, self.width, 3))  # RGB
        
        # White background for empty cells
        grid[:, :] = [255, 255, 255]
        
        # Black for obstacles
        for obs in self.grid_env.obstacles:
            x, y = obs
            grid[y, x] = [0, 0, 0]
        
        # Green for visited nodes (already expanded)
        for vis in visited:
            x, y = vis
            if grid[y, x, 0] != 0:  # Not an obstacle
                grid[y, x] = [144, 238, 144]
        
        # Yellow for frontier nodes (eligible for expansion)
        for front in frontier:
            x, y = front
            if grid[y, x, 0] != 0 or np.array_equal(grid[y, x], [144, 238, 144]):
                grid[y, x] = [255, 255, 0]
        
        # Blue for optimal path
        for path_cell in path:
            x, y = path_cell
            if (x, y) != self.grid_env.start and (x, y) != self.grid_env.goal:
                grid[y, x] = [0, 0, 255]
        
        # Light blue for start
        start_x, start_y = self.grid_env.start
        grid[start_y, start_x] = [173, 216, 230]
        
        # Red for goal
        goal_x, goal_y = self.grid_env.goal
        grid[goal_y, goal_x] = [255, 0, 0]
        
        # Normalize to [0, 255]
        grid = grid.astype(np.uint8)
        
        fig = go.Figure(data=go.Image(z=grid))
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            xaxis={'showticklabels': True},
            yaxis={'showticklabels': True}
        )
        
        return fig


def run_search_algorithm(algorithm_name: str, grid_env: GridEnvironment) -> Dict:
    """
    Execute selected search algorithm and return results.
    
    Args:
        algorithm_name: Name of algorithm (BFS, DFS, UCS, A*)
        grid_env: Grid environment instance
    
    Returns:
        Dictionary with algorithm results and metrics
    """
    algorithms = {
        'BFS': BreadthFirstSearch,
        'DFS': DepthFirstSearch,
        'Uniform Cost Search': UniformCostSearch,
        "A* Search": AStarSearch
    }
    
    algorithm_class = algorithms[algorithm_name]
    algorithm = algorithm_class(
        grid_env.start,
        grid_env.goal,
        (grid_env.width, grid_env.height),
        grid_env.obstacles
    )
    
    found = algorithm.search()
    
    return {
        'found': found,
        'path': algorithm.path,
        'path_length': len(algorithm.path) - 1 if algorithm.path else 0,
        'total_cost': algorithm.total_cost,
        'expanded_nodes': algorithm.expanded_nodes,
        'frontier_history': algorithm.frontier_history,
        'visited_history': algorithm.visited_history
    }


def main():
    """Main Streamlit application."""
    
    # Title
    st.markdown("<h1>🔍 Search Algorithms Visualizer</h1>", unsafe_allow_html=True)
    st.markdown("Compare uninformed and informed search strategies for pathfinding in grid environments")
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### Configuration")
        
        # Grid parameters
        col1, col2 = st.columns(2)
        with col1:
            grid_width = st.slider("Grid Width", 10, 50, 20, step=5)
        with col2:
            grid_height = st.slider("Grid Height", 10, 50, 20, step=5)
        
        obstacle_density = st.slider("Obstacle Density", 0.0, 0.4, 0.2, step=0.05)
        
        # Grid presets
        grid_preset = st.selectbox(
            "Grid Preset",
            ["Random", "Sparse", "Dense", "Predefined Maze"]
        )
        
        st.markdown("---")
        st.markdown("### Algorithm Selection")
        algorithm = st.selectbox(
            "Choose Algorithm",
            ["BFS", "DFS", "Uniform Cost Search", "A* Search"]
        )
        
        st.markdown("---")
        st.markdown("### Seed for Reproducibility")
        seed = st.number_input("Random Seed", value=42, min_value=0, step=1)
    
    # Initialize grid environment
    import random
    random.seed(seed)
    np.random.seed(seed)
    
    try:
        if grid_preset == "Random":
            grid = GridEnvironment(grid_width, grid_height, (1, 1), 
                                 (grid_width-2, grid_height-2), 
                                 obstacle_probability=obstacle_density)
        elif grid_preset == "Sparse":
            grid = GridEnvironment.create_sparse_grid(grid_width, grid_height, 0.1)
        elif grid_preset == "Dense":
            grid = GridEnvironment.create_sparse_grid(grid_width, grid_height, 0.3)
        else:  # Predefined Maze
            grid = GridEnvironment.create_predefined_maze(grid_width, grid_height)
    except ValueError as e:
        st.error(f"Grid configuration error: {e}")
        return
    
    # Display grid information
    st.markdown("<div class='section-header'>Grid Environment</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    grid_info = grid.get_grid_info()
    
    with col1:
        st.metric("Grid Size", f"{grid_info['dimensions'][0]}×{grid_info['dimensions'][1]}")
    with col2:
        st.metric("Obstacles", grid_info['obstacles'])
    with col3:
        st.metric("Obstacle Density", f"{grid_info['obstacle_density']:.1%}")
    with col4:
        st.metric("Free Cells", grid_info['free_cells'])
    
    # Run search algorithm
    with st.spinner(f"Running {algorithm}..."):
        results = run_search_algorithm(algorithm, grid)
    
    # Visualize search
    st.markdown("<div class='section-header'>Search Visualization</div>", unsafe_allow_html=True)
    
    visualizer = GridVisualizer(grid)
    
    if results['found']:
        # Get final states
        final_frontier = results['frontier_history'][-1] if results['frontier_history'] else []
        final_visited = set(results['visited_history'][-1]) if results['visited_history'] else set()
        
        fig = visualizer.visualize_search_state(
            final_frontier, 
            final_visited, 
            results['path']
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No path found between start and goal!")
    
    # Display metrics
    st.markdown("<div class='section-header'>Search Metrics</div>", unsafe_allow_html=True)
    
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric("Status", "✅ Found" if results['found'] else "❌ Not Found")
    
    with metric_cols[1]:
        st.metric("Path Length", results['path_length'])
    
    with metric_cols[2]:
        st.metric("Path Cost", int(results['total_cost']))
    
    with metric_cols[3]:
        st.metric("Nodes Expanded", results['expanded_nodes'])
    
    # Algorithm information
    st.markdown("<div class='section-header'>Algorithm Information</div>", unsafe_allow_html=True)
    
    algorithm_info = {
        'BFS': {
            'description': 'Breadth-First Search explores nodes level by level using a FIFO queue.',
            'properties': [
                '✓ Complete: Always finds solution if exists',
                '✓ Optimal: Yes, for unweighted graphs',
                '✗ Space: O(b^d) - can be prohibitive',
                '⟳ Time: O(b^d)'
            ],
            'use_case': 'Unweighted shortest paths, maze solving'
        },
        'DFS': {
            'description': 'Depth-First Search explores as far as possible before backtracking using a LIFO stack.',
            'properties': [
                '✗ Complete: Only with visited set and no cycles',
                '✗ Optimal: No, may find suboptimal paths',
                '✓ Space: O(bm) - memory efficient',
                '⟳ Time: O(b^m)'
            ],
            'use_case': 'Memory-constrained scenarios, topological sorting'
        },
        'Uniform Cost Search': {
            'description': 'Expands nodes in order of path cost from start (g-value).',
            'properties': [
                '✓ Complete: Always finds solution',
                '✓ Optimal: Yes, always finds minimum-cost path',
                '✗ Space: O(b^(1+floor(C*/ε)))',
                '⟳ Time: O(b^(1+floor(C*/ε)))'
            ],
            'use_case': 'Weighted graphs, when no heuristic available'
        },
        "A* Search": {
            'description': 'Combines actual cost g(n) with heuristic estimate h(n): f(n) = g(n) + h(n).',
            'properties': [
                '✓ Complete: Always finds solution',
                '✓ Optimal: Yes (with admissible heuristic)',
                '✓ Space: Much better than uninformed with good heuristic',
                '⟳ Time: Far fewer nodes than uninformed search'
            ],
            'use_case': 'Optimal pathfinding with heuristics (standard in games, navigation)'
        }
    }
    
    info = algorithm_info[algorithm]
    
    st.write(f"**{info['description']}**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Properties:**")
        for prop in info['properties']:
            st.write(prop)
    
    with col2:
        st.markdown("**Use Case:**")
        st.write(info['use_case'])
    
    # Detailed comparison table
    st.markdown("<div class='section-header'>Algorithm Comparison</div>", unsafe_allow_html=True)
    
    comparison_data = {
        'Algorithm': ['BFS', 'DFS', 'UCS', 'A*'],
        'Complete': ['✓', '✓*', '✓', '✓'],
        'Optimal': ['✓**', '✗', '✓', '✓***'],
        'Time': ['O(b^d)', 'O(b^m)', 'O(b^(1+⌊C*/ε⌋))', 'Better'],
        'Space': ['O(b^d)', 'O(bm)', 'O(b^(1+⌊C*/ε⌋))', 'Better'],
        'Type': ['Uninformed', 'Uninformed', 'Informed', 'Informed']
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Notes:**
    - *DFS: Complete only with visited set and no infinite paths
    - **BFS: Optimal only for uniform edge costs
    - ***A*: Optimal only if heuristic is admissible (never overestimates)
    - d = depth, b = branching factor, m = max depth, C* = optimal cost
    """)
    
    # Learning outcomes
    st.markdown("<div class='section-header'>Learning Outcomes</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Key Concepts to Understand
    
    **State Space:**
    - Every grid cell is a unique state
    - Start state: Initial position
    - Goal state: Target position
    - State transitions: Movement to adjacent cells
    
    **Search Frontier:**
    - Open list: Nodes eligible for expansion
    - Closed list (visited): Already explored nodes
    - Expansion: Generating successor states
    
    **Heuristics (A*):**
    - Admissible: Never overestimates (h(n) ≤ h*(n))
    - Consistent: h(n) ≤ cost(n→n') + h(n')
    - Manhattan distance: |Δx| + |Δy| (perfect for grid + 4-connectivity)
    
    **Optimality vs Efficiency:**
    - BFS/UCS: Guaranteed optimal, but slow on large spaces
    - A*: Optimal + practical (dramatically faster with good heuristic)
    - DFS: Fast but no quality guarantee
    """)
    
    # Heuristic explanation for A*
    if algorithm == "A* Search":
        st.markdown("<div class='section-header'>A* Heuristic: Manhattan Distance</div>", unsafe_allow_html=True)
        
        st.latex(r"h(x, y) = |x_{goal} - x| + |y_{goal} - y|")
        
        st.markdown("""
        **Why Manhattan Distance is Admissible:**
        
        The Manhattan distance provides a lower bound on actual movement cost because:
        1. You must move |Δx| steps horizontally and |Δy| steps vertically
        2. Minimum moves possible = |Δx| + |Δy|
        3. Actual path may require more moves (around obstacles)
        4. Therefore: h(n) ≤ h*(n) ✓ (never overestimates)
        
        **Impact on Search:**
        - Without heuristic (UCS): Expands nodes in all directions
        - With heuristic (A*): Focuses on promising directions
        - Good heuristic = exponential speedup in practice
        """)


if __name__ == "__main__":
    main()
