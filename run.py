#!/usr/bin/env python3
"""
SoloMiner Launcher
Quick launch script for the SoloMiner GUI application
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []

    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")

    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")

    if missing:
        print("❌ Missing dependencies detected!")
        print(f"   Missing: {', '.join(missing)}")
        print("\n   Please run the installer first:")
        print("   python install.py")
        print("\n   Or install manually:")
        print(f"   pip install {' '.join(missing)}")
        return False

    return True


def main():
    """Launch SoloMiner application"""
    print("""
    ╔══════════════════════════════════════╗
    ║       ₿  SoloMiner Launcher  ₿       ║
    ╚══════════════════════════════════════╝
    """)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    print("    ✅ Dependencies verified")
    print("    🚀 Launching SoloMiner GUI...\n")

    # Import and run
    try:
        from solominer.gui.main_window import SoloMinerApp

        app = SoloMinerApp()
        app.run()

    except Exception as e:
        print(f"\n❌ Error launching SoloMiner: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure all dependencies are installed: python install.py")
        print("  2. Check that you're running Python 3.8+")
        print("  3. On Linux, ensure tkinter is installed: sudo apt install python3-tk")
        sys.exit(1)


if __name__ == "__main__":
    main()
