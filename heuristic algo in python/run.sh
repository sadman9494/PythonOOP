#!/bin/bash
# Installation and Running Guide

# =====================================================
# INFORMED SEARCH ALGORITHMS VISUALIZER
# Complete Setup & Running Instructions
# =====================================================

echo "🔍 Informed Search Algorithms Visualizer"
echo "========================================"
echo ""

# CHECK Python Installation
echo "✓ Checking Python installation..."
python --version

if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "✓ Python is installed"
echo ""

# Create Virtual Environment
echo "📦 Creating virtual environment..."
python -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate Virtual Environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

echo "✓ Virtual environment activated"
echo ""

# Install Dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run Application
echo "🚀 Starting Streamlit application..."
echo ""
echo "📱 The application will open in your browser automatically"
echo "   If not, visit: http://localhost:8501"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

streamlit run main.py
