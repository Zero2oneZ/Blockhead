"""
Tree of Life (Kabbalah) visualization with Bitcoin algorithm mapping.

The Tree of Life consists of 10 Sephirot (nodes) connected by 22 paths,
mapped to Bitcoin's SHA-256 algorithm components.
"""

import tkinter as tk
from tkinter import Canvas
import math
from typing import List, Tuple, Optional
import colorsys


class TreeOfLifeView(Canvas):
    """
    Canvas widget displaying the Kabbalistic Tree of Life with
    Bitcoin algorithm data flowing through it.
    """

    # Sephirot names and their meanings
    SEPHIROT = [
        ("Kether", "Crown", "Block Header"),
        ("Chokmah", "Wisdom", "SHA-256 Round 1"),
        ("Binah", "Understanding", "SHA-256 Round 2"),
        ("Chesed", "Mercy", "Message Schedule"),
        ("Geburah", "Severity", "Compression"),
        ("Tiphareth", "Beauty", "Working Variables"),
        ("Netzach", "Victory", "Hash Update"),
        ("Hod", "Splendor", "Nonce Iteration"),
        ("Yesod", "Foundation", "Double Hash"),
        ("Malkuth", "Kingdom", "Block Hash"),
    ]

    # Tree connections (22 paths)
    PATHS = [
        (0, 1), (0, 2), (1, 2),  # Supernal triad
        (1, 3), (1, 4), (2, 3), (2, 4),  # Upper paths
        (3, 4), (3, 5), (4, 5),  # Middle paths
        (3, 6), (4, 7), (5, 6), (5, 7), (5, 8),  # Lower upper
        (6, 7), (6, 8), (7, 8),  # Lower paths
        (6, 9), (7, 9), (8, 9),  # To Malkuth
    ]

    def __init__(self, parent, width: int = 400, height: int = 500, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg='#050510', highlightthickness=0, **kwargs)

        self.width = width
        self.height = height

        # Node positions (normalized 0-1, will be scaled)
        self.node_positions = [
            (0.5, 0.08),   # Kether - top center
            (0.75, 0.18),  # Chokmah - right upper
            (0.25, 0.18),  # Binah - left upper
            (0.75, 0.38),  # Chesed - right middle-upper
            (0.25, 0.38),  # Geburah - left middle-upper
            (0.5, 0.48),   # Tiphareth - center
            (0.75, 0.65),  # Netzach - right lower
            (0.25, 0.65),  # Hod - left lower
            (0.5, 0.78),   # Yesod - center lower
            (0.5, 0.92),   # Malkuth - bottom center
        ]

        # Scale positions to canvas
        self.scaled_positions = [
            (int(x * width), int(y * height))
            for x, y in self.node_positions
        ]

        # Animation state
        self.is_animating = True
        self.animation_id = None
        self.pulse_phase = 0.0
        self.flow_phase = 0.0

        # Data flow visualization
        self.active_paths: List[int] = []
        self.active_nodes: List[int] = []
        self.node_values: List[str] = [''] * 10

        # Colors
        self.node_colors = [
            '#ffffff',  # Kether - white
            '#888888',  # Chokmah - gray
            '#000000',  # Binah - black
            '#0000ff',  # Chesed - blue
            '#ff0000',  # Geburah - red
            '#ffff00',  # Tiphareth - yellow
            '#00ff00',  # Netzach - green
            '#ff8800',  # Hod - orange
            '#ff00ff',  # Yesod - purple
            '#8b4513',  # Malkuth - brown/earth
        ]

        # Hash data for visualization
        self.block_hash: Optional[str] = None
        self.algorithm_step = 0

        # Start animation
        self.animate()

    def set_block_data(self, block_hash: str, algorithm_data: dict = None):
        """Set block data to visualize through the tree."""
        self.block_hash = block_hash

        if block_hash:
            # Distribute hash segments to nodes
            seg_len = len(block_hash) // 10
            for i in range(10):
                start = i * seg_len
                end = start + seg_len
                self.node_values[i] = block_hash[start:end][:4]

        if algorithm_data:
            self.algorithm_step = algorithm_data.get('step', 0)

    def set_active_flow(self, path_indices: List[int], node_indices: List[int]):
        """Set which paths and nodes are actively showing data flow."""
        self.active_paths = path_indices
        self.active_nodes = node_indices

    def draw_path(self, start_idx: int, end_idx: int, path_idx: int):
        """Draw a connecting path between two nodes."""
        x1, y1 = self.scaled_positions[start_idx]
        x2, y2 = self.scaled_positions[end_idx]

        # Calculate if path is active
        is_active = path_idx in self.active_paths

        # Base path color
        base_color = '#1a1a3a' if not is_active else '#4444aa'

        # Glow effect for active paths
        if is_active:
            glow_intensity = 0.5 + 0.5 * math.sin(self.flow_phase + path_idx * 0.3)
            glow_width = int(6 + glow_intensity * 4)

            # Outer glow
            self.create_line(
                x1, y1, x2, y2,
                fill='#0044ff',
                width=glow_width,
                stipple='gray50'
            )

        # Main path line
        self.create_line(
            x1, y1, x2, y2,
            fill=base_color if not is_active else '#6688ff',
            width=2 if not is_active else 3
        )

        # Flow particles on active paths
        if is_active:
            self._draw_flow_particles(x1, y1, x2, y2, path_idx)

    def _draw_flow_particles(self, x1: int, y1: int, x2: int, y2: int, path_idx: int):
        """Draw animated particles flowing along a path."""
        num_particles = 3
        for i in range(num_particles):
            # Calculate particle position along path
            t = ((self.flow_phase / (2 * math.pi) + i / num_particles + path_idx * 0.1) % 1.0)
            px = x1 + (x2 - x1) * t
            py = y1 + (y2 - y1) * t

            # Particle size varies with phase
            size = 3 + 2 * math.sin(self.flow_phase * 2 + i)

            # Draw particle
            self.create_oval(
                px - size, py - size, px + size, py + size,
                fill='#00ffff',
                outline='#ffffff'
            )

    def draw_node(self, idx: int):
        """Draw a Sephirah node."""
        x, y = self.scaled_positions[idx]
        name, meaning, btc_component = self.SEPHIROT[idx]

        # Check if node is active
        is_active = idx in self.active_nodes

        # Pulse effect
        pulse = 0.5 + 0.5 * math.sin(self.pulse_phase + idx * 0.5)
        base_radius = 25
        radius = int(base_radius + (5 if is_active else 2) * pulse)

        # Get node color
        color = self.node_colors[idx]

        # Outer glow for active nodes
        if is_active:
            glow_radius = radius + 15
            self.create_oval(
                x - glow_radius, y - glow_radius,
                x + glow_radius, y + glow_radius,
                fill='',
                outline=color,
                width=3,
                stipple='gray25'
            )

        # Main node circle
        self.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline='#ffffff' if is_active else '#666666',
            width=2
        )

        # Inner circle
        inner_radius = radius - 8
        if inner_radius > 5:
            self.create_oval(
                x - inner_radius, y - inner_radius,
                x + inner_radius, y + inner_radius,
                fill='',
                outline='#ffffff',
                width=1,
                stipple='gray50'
            )

        # Node value (hash segment)
        if self.node_values[idx]:
            # Determine text color based on node color brightness
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            text_color = '#000000' if brightness > 128 else '#ffffff'

            self.create_text(
                x, y,
                text=self.node_values[idx],
                fill=text_color,
                font=('Courier', 8, 'bold')
            )

        # Node label
        label_y = y + radius + 12
        self.create_text(
            x, label_y,
            text=name,
            fill='#aaaaaa',
            font=('Arial', 8)
        )

        # BTC component label for active nodes
        if is_active:
            btc_y = label_y + 12
            self.create_text(
                x, btc_y,
                text=btc_component,
                fill='#00ff88',
                font=('Arial', 7, 'italic')
            )

    def draw(self):
        """Draw the complete Tree of Life."""
        self.delete('all')

        # Draw background effect
        self._draw_background()

        # Draw all paths first (behind nodes)
        for i, (start, end) in enumerate(self.PATHS):
            self.draw_path(start, end, i)

        # Draw all nodes
        for i in range(len(self.SEPHIROT)):
            self.draw_node(i)

        # Draw title
        self.create_text(
            self.width // 2, 15,
            text="TREE OF LIFE",
            fill='#00ffcc',
            font=('Arial', 12, 'bold')
        )

        # Draw algorithm step indicator
        if self.algorithm_step > 0:
            self.create_text(
                self.width // 2, self.height - 15,
                text=f"Algorithm Step: {self.algorithm_step}/8",
                fill='#888888',
                font=('Arial', 9)
            )

    def _draw_background(self):
        """Draw mystical background effect."""
        # Central light pillar
        for i in range(10):
            alpha = 0.05 + i * 0.01
            width = 60 - i * 5
            shade = int(20 + i * 3)
            color = f'#{shade:02x}{shade:02x}{int(shade * 1.5):02x}'

            self.create_rectangle(
                self.width // 2 - width, 0,
                self.width // 2 + width, self.height,
                fill=color,
                outline=''
            )

        # Side pillars (Severity and Mercy)
        for side in [-1, 1]:
            x_center = self.width // 4 if side == -1 else 3 * self.width // 4
            for i in range(5):
                width = 40 - i * 7
                shade = int(15 + i * 2)
                color = f'#{shade:02x}{shade:02x}{shade:02x}'

                self.create_rectangle(
                    x_center - width, 0,
                    x_center + width, self.height,
                    fill=color,
                    outline=''
                )

    def animate(self):
        """Animation loop."""
        if self.is_animating:
            # Update animation phases
            self.pulse_phase += 0.1
            self.flow_phase += 0.15

            # Keep phases in range
            self.pulse_phase %= 2 * math.pi
            self.flow_phase %= 2 * math.pi

            # Auto-activate nodes in sequence based on algorithm step
            self._update_active_elements()

            # Redraw
            self.draw()

            # Schedule next frame
            self.animation_id = self.after(50, self.animate)  # ~20 FPS

    def _update_active_elements(self):
        """Update which elements are active based on animation state."""
        # Cycle through nodes
        cycle_time = 3.0  # seconds per complete cycle
        cycle_position = (self.pulse_phase / (2 * math.pi)) * 10

        # Active nodes are around the current position
        active_node = int(cycle_position) % 10
        self.active_nodes = [active_node, (active_node + 1) % 10]

        # Find paths connected to active nodes
        self.active_paths = []
        for i, (start, end) in enumerate(self.PATHS):
            if start in self.active_nodes or end in self.active_nodes:
                self.active_paths.append(i)

    def start_animation(self):
        """Start the animation."""
        if not self.is_animating:
            self.is_animating = True
            self.animate()

    def stop_animation(self):
        """Stop the animation."""
        self.is_animating = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None

    def set_algorithm_step(self, step: int):
        """Set the current algorithm step for visualization."""
        self.algorithm_step = step

        # Map step to active nodes
        step_to_nodes = {
            1: [0],        # Block header -> Kether
            2: [0, 1, 2],  # Parse -> Supernal triad
            3: [1, 2, 3, 4],  # Initialize
            4: [3, 4, 5],  # Message schedule
            5: [4, 5],     # Compression
            6: [5, 6, 7],  # Working vars
            7: [6, 7, 8],  # Hash update
            8: [8, 9],     # Final hash
        }

        self.active_nodes = step_to_nodes.get(step, [])
