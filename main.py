#!/usr/bin/env python3
"""
BLOCKHEAD - BTC Block Rotation GUI

A mystical visualization of Bitcoin's SHA-256 mining algorithm featuring:
- Rotating 3D Block visualization
- Tree of Life sacred geometry with algorithm flow
- Wheels within Wheels (Ezekiel's vision) with SHA-256 constants
- Step-by-step algorithm display and mining simulation

Usage:
    python main.py

Requirements:
    - Python 3.8+
    - tkinter (usually included with Python)
    - pillow (optional, for enhanced graphics)
    - numpy (optional, for calculations)

Author: Zero2oneZ
License: MIT
"""

import sys
import os

# Ensure proper path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Check if required dependencies are available."""
    missing = []

    # tkinter is required
    try:
        import tkinter
    except ImportError:
        print("ERROR: tkinter is required but not installed.")
        print("On Ubuntu/Debian: sudo apt-get install python3-tk")
        print("On Fedora: sudo dnf install python3-tkinter")
        print("On macOS: tkinter should be included with Python")
        sys.exit(1)

    # Optional dependencies
    try:
        from PIL import Image
    except ImportError:
        print("Note: pillow not installed. Some features may be limited.")
        print("Install with: pip install pillow")

    try:
        import numpy
    except ImportError:
        print("Note: numpy not installed. Some features may be limited.")
        print("Install with: pip install numpy")


def main():
    """Main entry point."""
    print("=" * 50)
    print("  BLOCKHEAD - BTC Block Rotation Visualizer")
    print("=" * 50)
    print()

    # Check dependencies
    check_dependencies()

    print("Starting application...")
    print()

    # Import and run the application
    try:
        from gui.main_window import BlockheadApp

        app = BlockheadApp()
        app.mainloop()

    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
