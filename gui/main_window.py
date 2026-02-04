"""
Main application window integrating all visualization components.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import threading
import time

from .btc_block_view import BTCBlockView
from .tree_of_life import TreeOfLifeView
from .spinning_wheels import SpinningWheelsView
from .algorithm_panel import AlgorithmPanel

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from btc.block import BTCBlock
from btc.algorithm import SHA256Algorithm, MiningAlgorithm


class BlockheadApp(tk.Tk):
    """
    Main application window for Blockhead - BTC Block Rotation GUI.

    Integrates:
    - Rotating 3D BTC Block visualization
    - Tree of Life with algorithm flow
    - Spinning wheels within wheels
    - Algorithm step display panel
    """

    def __init__(self):
        super().__init__()

        self.title("BLOCKHEAD - BTC Block Rotation Visualizer")
        self.configure(bg='#050508')

        # Set window size and position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = min(1400, screen_width - 100)
        window_height = min(800, screen_height - 100)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Prevent resizing below minimum
        self.minsize(1000, 600)

        # Initialize BTC components
        self.current_block: Optional[BTCBlock] = None
        self.sha256_algo = SHA256Algorithm()
        self.mining_algo: Optional[MiningAlgorithm] = None

        # Create UI
        self._create_menu()
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Initialize with genesis block
        self._load_genesis_block()

        # Bind cleanup
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self, bg='#1a1a2a', fg='white')

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2a', fg='white')
        file_menu.add_command(label="New Block", command=self._new_block)
        file_menu.add_command(label="Load Genesis", command=self._load_genesis_block)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        menubar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2a', fg='white')
        view_menu.add_command(label="Toggle Animations", command=self._toggle_animations)
        view_menu.add_command(label="Reset View", command=self._reset_view)
        menubar.add_cascade(label="View", menu=view_menu)

        # Mining menu
        mining_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2a', fg='white')
        mining_menu.add_command(label="Start Mining", command=self._start_mining)
        mining_menu.add_command(label="Stop Mining", command=self._stop_mining)
        mining_menu.add_separator()
        mining_menu.add_command(label="Set Difficulty...", command=self._set_difficulty)
        menubar.add_cascade(label="Mining", menu=mining_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2a', fg='white')
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _create_header(self):
        """Create the header section."""
        header_frame = tk.Frame(self, bg='#0a0a15', height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="⬡ BLOCKHEAD ⬡",
            font=('Arial', 24, 'bold'),
            fg='#00ffcc',
            bg='#0a0a15'
        )
        title_label.pack(side=tk.LEFT, padx=20)

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Bitcoin Block Rotation Visualizer",
            font=('Arial', 12),
            fg='#888899',
            bg='#0a0a15'
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)

        # Block info (right side)
        self.block_info_frame = tk.Frame(header_frame, bg='#0a0a15')
        self.block_info_frame.pack(side=tk.RIGHT, padx=20)

        self.block_hash_label = tk.Label(
            self.block_info_frame,
            text="Block: Loading...",
            font=('Courier', 10),
            fg='#ffcc00',
            bg='#0a0a15'
        )
        self.block_hash_label.pack()

    def _create_main_content(self):
        """Create the main content area with all visualizations."""
        # Main container
        main_frame = tk.Frame(self, bg='#050508')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel - Algorithm display
        left_panel = tk.Frame(main_frame, bg='#0a0a15', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)

        self.algorithm_panel = AlgorithmPanel(left_panel)
        self.algorithm_panel.pack(fill=tk.BOTH, expand=True)
        self.algorithm_panel.set_mining_callback(self._on_block_found)

        # Center area - Visualizations
        center_frame = tk.Frame(main_frame, bg='#050508')
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top row - Block and Tree of Life
        top_row = tk.Frame(center_frame, bg='#050508')
        top_row.pack(fill=tk.BOTH, expand=True)

        # BTC Block visualization
        block_frame = tk.LabelFrame(
            top_row,
            text="3D Block View",
            font=('Arial', 10),
            fg='#00ccff',
            bg='#0a0a15',
            relief=tk.RIDGE
        )
        block_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.block_view = BTCBlockView(block_frame, width=380, height=380)
        self.block_view.pack(padx=5, pady=5)

        # Tree of Life visualization
        tree_frame = tk.LabelFrame(
            top_row,
            text="Tree of Life - Algorithm Flow",
            font=('Arial', 10),
            fg='#00ffaa',
            bg='#0a0a15',
            relief=tk.RIDGE
        )
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.tree_view = TreeOfLifeView(tree_frame, width=380, height=380)
        self.tree_view.pack(padx=5, pady=5)

        # Right panel - Spinning Wheels
        right_panel = tk.LabelFrame(
            main_frame,
            text="Wheels Within Wheels",
            font=('Arial', 10),
            fg='#ffaa00',
            bg='#0a0a15',
            relief=tk.RIDGE,
            width=420
        )
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)

        self.wheels_view = SpinningWheelsView(right_panel, width=400, height=400)
        self.wheels_view.pack(padx=5, pady=5)

        # Wheel controls
        wheel_controls = tk.Frame(right_panel, bg='#0a0a15')
        wheel_controls.pack(fill=tk.X, padx=10, pady=5)

        speed_label = tk.Label(
            wheel_controls,
            text="Wheel Speed:",
            font=('Arial', 9),
            fg='#888888',
            bg='#0a0a15'
        )
        speed_label.pack(side=tk.LEFT)

        self.speed_scale = ttk.Scale(
            wheel_controls,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            command=self._on_speed_change
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        status_frame = tk.Frame(self, bg='#0a0a15', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 9),
            fg='#888888',
            bg='#0a0a15',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Animation status
        self.anim_status = tk.Label(
            status_frame,
            text="🔴 Animations: ON",
            font=('Arial', 9),
            fg='#00ff00',
            bg='#0a0a15'
        )
        self.anim_status.pack(side=tk.RIGHT, padx=10)

    def _load_genesis_block(self):
        """Load the Bitcoin genesis block."""
        self.current_block = BTCBlock.create_genesis()
        self._update_visualizations()
        self.status_label.config(text="Loaded: Bitcoin Genesis Block (Block #0)")

    def _new_block(self):
        """Create a new random block."""
        import random
        import hashlib
        import time

        # Generate random data
        prev_hash = hashlib.sha256(str(random.random()).encode()).hexdigest()
        merkle = hashlib.sha256(str(random.random()).encode()).hexdigest()

        self.current_block = BTCBlock(
            version=1,
            prev_block_hash=prev_hash,
            merkle_root=merkle,
            timestamp=int(time.time()),
            bits=0x1d00ffff,
            nonce=random.randint(0, 2**32)
        )

        self._update_visualizations()
        self.status_label.config(text="Created new block")

    def _update_visualizations(self):
        """Update all visualizations with current block data."""
        if not self.current_block:
            return

        block_hash = self.current_block.block_hash
        block_data = self.current_block.to_dict()

        # Update block view
        self.block_view.set_block(block_hash, block_data)

        # Update tree view
        self.tree_view.set_block_data(block_hash)

        # Update wheels view
        wheel_speeds = self.current_block.get_wheel_speeds()
        self.wheels_view.set_block_data(block_hash, wheel_speeds)

        # Update header
        short_hash = block_hash[:24] + "..." if block_hash else "---"
        self.block_hash_label.config(text=f"Block: {short_hash}")

        # Update algorithm panel
        self.algorithm_panel.update_hash(block_hash, self.current_block.nonce)

    def _toggle_animations(self):
        """Toggle all animations on/off."""
        # Get current state from block view
        is_animating = self.block_view.is_animating

        if is_animating:
            self.block_view.stop_animation()
            self.tree_view.stop_animation()
            self.wheels_view.stop_animation()
            self.anim_status.config(text="⚫ Animations: OFF", fg='#ff0000')
        else:
            self.block_view.start_animation()
            self.tree_view.start_animation()
            self.wheels_view.start_animation()
            self.anim_status.config(text="🔴 Animations: ON", fg='#00ff00')

    def _reset_view(self):
        """Reset all views to default state."""
        self.block_view.set_rotation(0, 0, 0)
        self.block_view.set_speeds(0.02, 0.015, 0.01)
        self.tree_view.set_algorithm_step(0)
        self.speed_scale.set(1.0)
        self.status_label.config(text="View reset")

    def _start_mining(self):
        """Start the mining simulation."""
        self.algorithm_panel._toggle_mining()
        if self.algorithm_panel.is_mining:
            self.status_label.config(text="Mining simulation started...")

    def _stop_mining(self):
        """Stop the mining simulation."""
        if self.algorithm_panel.is_mining:
            self.algorithm_panel._toggle_mining()
            self.status_label.config(text="Mining stopped")

    def _set_difficulty(self):
        """Open difficulty setting dialog."""
        dialog = tk.Toplevel(self)
        dialog.title("Set Mining Difficulty")
        dialog.geometry("300x150")
        dialog.configure(bg='#0a0a15')
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Number of leading zeros required:",
            font=('Arial', 10),
            fg='white',
            bg='#0a0a15'
        ).pack(pady=20)

        diff_var = tk.IntVar(value=4)
        diff_scale = ttk.Scale(
            dialog,
            from_=1,
            to=8,
            variable=diff_var,
            orient=tk.HORIZONTAL
        )
        diff_scale.pack(fill=tk.X, padx=20)

        diff_label = tk.Label(
            dialog,
            text="4",
            font=('Arial', 14, 'bold'),
            fg='#00ff00',
            bg='#0a0a15'
        )
        diff_label.pack()

        def update_label(val):
            diff_label.config(text=str(int(float(val))))

        diff_scale.configure(command=update_label)

        def apply():
            self.algorithm_panel.set_difficulty(diff_var.get())
            dialog.destroy()

        tk.Button(
            dialog,
            text="Apply",
            command=apply,
            bg='#228822',
            fg='white'
        ).pack(pady=10)

    def _on_block_found(self, hash_result: str, nonce: int):
        """Callback when mining finds a valid block."""
        self.status_label.config(
            text=f"BLOCK FOUND! Nonce: {nonce}",
        )

        # Update current block with found hash
        if self.current_block:
            self.current_block.nonce = nonce
            self.current_block.block_hash = hash_result
            self._update_visualizations()

        # Pulse effect on wheels
        for i in range(8):
            self.after(i * 100, lambda idx=i: self.wheels_view.pulse_wheel(idx))

    def _on_speed_change(self, value):
        """Handle wheel speed slider change."""
        speed = float(value)
        base_speeds = [0.02 - i * 0.002 for i in range(8)]
        adjusted_speeds = [s * speed for s in base_speeds]
        self.wheels_view.set_wheel_speeds(adjusted_speeds)

    def _show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Blockhead",
            "BLOCKHEAD\n"
            "BTC Block Rotation Visualizer\n\n"
            "Version 1.0\n\n"
            "A mystical visualization of Bitcoin's\n"
            "SHA-256 mining algorithm through:\n"
            "• Rotating 3D Block\n"
            "• Tree of Life\n"
            "• Wheels within Wheels\n\n"
            "© 2026 Zero2oneZ\n"
            "MIT License"
        )

    def _on_close(self):
        """Clean up and close the application."""
        # Stop all animations
        self.block_view.stop_animation()
        self.tree_view.stop_animation()
        self.wheels_view.stop_animation()

        # Stop mining if running
        if self.algorithm_panel.is_mining:
            self.algorithm_panel.is_mining = False

        self.destroy()


def main():
    """Entry point for the application."""
    app = BlockheadApp()
    app.mainloop()


if __name__ == "__main__":
    main()
