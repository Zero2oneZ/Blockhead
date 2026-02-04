"""
Helper utilities for SoloMiner
"""

from typing import List
import time


def format_hashrate(hashrate: float) -> str:
    """Format hashrate with appropriate unit"""
    if hashrate < 1000:
        return f"{hashrate:.2f} H/s"
    elif hashrate < 1_000_000:
        return f"{hashrate/1000:.2f} KH/s"
    elif hashrate < 1_000_000_000:
        return f"{hashrate/1_000_000:.2f} MH/s"
    elif hashrate < 1_000_000_000_000:
        return f"{hashrate/1_000_000_000:.2f} GH/s"
    else:
        return f"{hashrate/1_000_000_000_000:.2f} TH/s"


def format_time(seconds: float) -> str:
    """Format time duration"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"


def format_number(num: int) -> str:
    """Format large numbers with commas"""
    return f"{num:,}"


def generate_block_visual(hash_str: str, width: int = 32) -> List[str]:
    """Generate ASCII art visualization of a block hash"""
    lines = []

    # Top border
    lines.append("+" + "-" * (width + 2) + "+")
    lines.append("|" + " BLOCK ".center(width + 2) + "|")
    lines.append("+" + "-" * (width + 2) + "+")

    # Hash visualization
    for i in range(0, min(len(hash_str), 64), width):
        chunk = hash_str[i:i+width]
        lines.append("| " + chunk.ljust(width) + " |")

    # Bottom border
    lines.append("+" + "-" * (width + 2) + "+")

    return lines


def generate_mining_animation_frames() -> List[str]:
    """Generate frames for mining animation"""
    frames = [
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ░░░░░░░░░ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ▒▒░░░░░░░ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ▓▓▒▒░░░░░ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ██▓▓▒▒░░░ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ████▓▓▒▒░ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ ██████▓▓▒ ║
   ╚═══════════╝
        """,
        """
    ⛏️  Mining...
   ╔═══════════╗
   ║ █████████ ║
   ╚═══════════╝
        """,
    ]
    return frames


def get_bitcoin_logo_ascii() -> str:
    """Return ASCII art Bitcoin logo"""
    return """
      ████████████████
    ██              ██
  ██    ██████████    ██
  ██    ██      ██    ██
  ██    ██████████    ██
  ██    ██      ██    ██
  ██    ██████████    ██
    ██              ██
      ████████████████
           ██  ██
           ██  ██
    """


def get_hash_color_code(hash_str: str) -> str:
    """Get color code based on hash leading zeros"""
    zeros = len(hash_str) - len(hash_str.lstrip('0'))

    if zeros >= 8:
        return "gold"      # Excellent
    elif zeros >= 6:
        return "green"     # Great
    elif zeros >= 4:
        return "blue"      # Good
    elif zeros >= 2:
        return "cyan"      # Fair
    else:
        return "white"     # Normal


def calculate_difficulty_progress(current_zeros: int, target_zeros: int) -> float:
    """Calculate progress towards target difficulty"""
    if target_zeros == 0:
        return 100.0
    return min(100.0, (current_zeros / target_zeros) * 100)


def generate_stats_display(stats: dict) -> str:
    """Generate formatted stats display"""
    lines = [
        "╔════════════════════════════════════╗",
        "║         MINING STATISTICS          ║",
        "╠════════════════════════════════════╣",
    ]

    for key, value in stats.items():
        line = f"║ {key}: {str(value)[:20].rjust(20)} ║"
        lines.append(line)

    lines.append("╚════════════════════════════════════╝")

    return "\n".join(lines)
