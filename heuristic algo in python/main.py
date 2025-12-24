"""
Main Entry Point
Runs the Streamlit web application for search algorithm visualization.

Usage:
    streamlit run main.py
"""

import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualizer import main

if __name__ == "__main__":
    main()
