#!/usr/bin/env python3
"""
SoloMiner Installation Script
Installs all dependencies and sets up the environment
"""

import subprocess
import sys
import os
from pathlib import Path


def print_banner():
    """Print installation banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███████╗ ██████╗ ██╗      ██████╗ ███╗   ███╗██╗███╗   ██║
    ║   ██╔════╝██╔═══██╗██║     ██╔═══██╗████╗ ████║██║████╗  ██║
    ║   ███████╗██║   ██║██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║
    ║   ╚════██║██║   ██║██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║
    ║   ███████║╚██████╔╝███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
    ║   ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══║
    ║                                                           ║
    ║              Bitcoin Solo Mining GUI                       ║
    ║                    Installer                               ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Check Python version compatibility"""
    print("\n[1/5] Checking Python version...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"    ❌ Python 3.8+ required. Found: {version.major}.{version.minor}")
        return False

    print(f"    ✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_pip():
    """Check if pip is available"""
    print("\n[2/5] Checking pip installation...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            capture_output=True
        )
        print("    ✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("    ❌ pip not found. Please install pip first.")
        return False


def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n[3/5] Upgrading pip...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        print("    ✅ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    ⚠️ Could not upgrade pip: {e}")
        return True  # Continue anyway


def install_dependencies():
    """Install required dependencies"""
    print("\n[4/5] Installing dependencies...")

    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    requirements_file = script_dir / "requirements.txt"

    if not requirements_file.exists():
        print(f"    ❌ requirements.txt not found at {requirements_file}")
        return False

    dependencies = [
        ("customtkinter", "GUI Framework"),
        ("Pillow", "Image Processing"),
        ("requests", "HTTP Client"),
        ("rich", "Terminal Formatting"),
    ]

    print("\n    Installing packages:")
    for pkg, desc in dependencies:
        print(f"      📦 {pkg} - {desc}")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=False
        )
        print("\n    ✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n    ❌ Failed to install dependencies: {e}")
        return False


def verify_installation():
    """Verify that all required modules can be imported"""
    print("\n[5/5] Verifying installation...")

    required_modules = [
        "customtkinter",
        "PIL",
        "hashlib",
        "threading",
    ]

    all_ok = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"    ✅ {module}")
        except ImportError:
            print(f"    ❌ {module} - Failed to import")
            all_ok = False

    return all_ok


def create_launcher_script():
    """Create a convenient launcher script"""
    script_dir = Path(__file__).parent.absolute()

    # Create launcher for Unix/Linux/Mac
    launcher_unix = script_dir / "launch_solominer.sh"
    launcher_unix.write_text(f"""#!/bin/bash
cd "{script_dir}"
{sys.executable} -m solominer
""")
    launcher_unix.chmod(0o755)

    # Create launcher for Windows
    launcher_win = script_dir / "launch_solominer.bat"
    launcher_win.write_text(f"""@echo off
cd /d "{script_dir}"
"{sys.executable}" -m solominer
pause
""")

    print(f"\n    Created launchers:")
    print(f"      • Unix/Mac: {launcher_unix}")
    print(f"      • Windows:  {launcher_win}")


def main():
    """Main installation routine"""
    print_banner()

    print("\n" + "=" * 60)
    print("  Starting SoloMiner Installation")
    print("=" * 60)

    # Run installation steps
    steps = [
        ("Python Version Check", check_python_version),
        ("Pip Check", check_pip),
        ("Pip Upgrade", upgrade_pip),
        ("Dependencies", install_dependencies),
        ("Verification", verify_installation),
    ]

    for name, func in steps:
        if not func():
            print(f"\n❌ Installation failed at step: {name}")
            print("   Please fix the issue and try again.")
            sys.exit(1)

    # Create launchers
    create_launcher_script()

    # Success message
    print("\n" + "=" * 60)
    print("  ✅ Installation Complete!")
    print("=" * 60)

    print("""
    To launch SoloMiner, run one of the following:

        python -m solominer
        python run.py
        ./launch_solominer.sh  (Unix/Mac)
        launch_solominer.bat   (Windows)

    Enjoy mining! ⛏️ 💰
    """)


if __name__ == "__main__":
    main()
