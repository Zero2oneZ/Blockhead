"""
BTC Block 3D rotation visualization using Canvas.

Displays a rotating cube representation of a Bitcoin block with
hash data mapped to visual properties.
"""

import tkinter as tk
from tkinter import Canvas
import math
from typing import List, Tuple, Optional
import colorsys


class BTCBlockView(Canvas):
    """
    A Canvas widget that displays a rotating 3D cube representation
    of a Bitcoin block.
    """

    def __init__(self, parent, width: int = 400, height: int = 400, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg='#0a0a0a', highlightthickness=0, **kwargs)

        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2

        # Rotation angles (in radians)
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

        # Rotation speeds (radians per frame)
        self.speed_x = 0.02
        self.speed_y = 0.015
        self.speed_z = 0.01

        # Block properties
        self.block_size = 100
        self.block_hash: Optional[str] = None
        self.block_data: dict = {}

        # Colors derived from hash
        self.face_colors = ['#ff6b35', '#f7c59f', '#2ec4b6',
                            '#011627', '#e71d36', '#ff9f1c']

        # Cube vertices (unit cube centered at origin)
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]

        # Cube faces (indices into vertices, in order for face drawing)
        self.faces = [
            [0, 1, 2, 3],  # Back
            [4, 5, 6, 7],  # Front
            [0, 1, 5, 4],  # Bottom
            [2, 3, 7, 6],  # Top
            [0, 3, 7, 4],  # Left
            [1, 2, 6, 5],  # Right
        ]

        # Edges for wireframe
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
        ]

        # Animation state
        self.is_animating = True
        self.animation_id = None

        # Hash display
        self.hash_chars: List[str] = []

        # Start animation
        self.animate()

    def set_block(self, block_hash: str, block_data: dict = None):
        """
        Set the block data to visualize.

        Args:
            block_hash: The block's hash string
            block_data: Optional dictionary of block properties
        """
        self.block_hash = block_hash
        self.block_data = block_data or {}
        self.hash_chars = list(block_hash) if block_hash else []

        # Derive colors from hash
        if block_hash:
            self._update_colors_from_hash(block_hash)

        # Update rotation speeds from block data
        if block_data:
            self._update_speeds_from_data(block_data)

    def _update_colors_from_hash(self, hash_str: str):
        """Derive face colors from the hash string."""
        self.face_colors = []

        for i in range(6):
            # Take segments of the hash for each face
            segment = hash_str[i * 10:(i + 1) * 10] if len(hash_str) >= (i + 1) * 10 else hash_str
            if segment:
                # Convert segment to color
                value = int(segment[:6], 16) if len(segment) >= 6 else 0
                hue = (value % 360) / 360.0
                sat = 0.7 + (value % 30) / 100.0
                val = 0.6 + (value % 40) / 100.0
                rgb = colorsys.hsv_to_rgb(hue, min(sat, 1.0), min(val, 1.0))
                color = '#{:02x}{:02x}{:02x}'.format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                )
                self.face_colors.append(color)
            else:
                self.face_colors.append('#444444')

    def _update_speeds_from_data(self, data: dict):
        """Update rotation speeds based on block data."""
        if 'nonce' in data:
            nonce = data['nonce']
            self.speed_x = 0.01 + (nonce % 100) / 5000.0
            self.speed_y = 0.015 + (nonce % 50) / 3000.0

        if 'timestamp' in data:
            ts = data['timestamp']
            self.speed_z = 0.005 + (ts % 100) / 8000.0

    def rotate_point(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Apply 3D rotation to a point."""
        # Rotate around X axis
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x

        # Rotate around Y axis
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        x1 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y

        # Rotate around Z axis
        cos_z, sin_z = math.cos(self.angle_z), math.sin(self.angle_z)
        x2 = x1 * cos_z - y1 * sin_z
        y2 = x1 * sin_z + y1 * cos_z

        return x2, y2, z2

    def project(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """Project 3D point to 2D screen coordinates."""
        # Simple perspective projection
        scale = 200 / (z + 4)  # Perspective factor
        screen_x = int(self.center_x + x * scale * self.block_size / 100)
        screen_y = int(self.center_y - y * scale * self.block_size / 100)
        return screen_x, screen_y

    def get_face_depth(self, face_indices: List[int]) -> float:
        """Calculate average Z depth of a face for sorting."""
        total_z = 0
        for idx in face_indices:
            v = self.vertices[idx]
            _, _, z = self.rotate_point(v[0], v[1], v[2])
            total_z += z
        return total_z / len(face_indices)

    def draw(self):
        """Draw the rotating cube."""
        self.delete('all')

        # Draw background gradient effect
        for i in range(20):
            shade = int(10 + i * 2)
            color = f'#{shade:02x}{shade:02x}{int(shade * 1.2):02x}'
            self.create_oval(
                self.center_x - 180 + i * 5,
                self.center_y - 180 + i * 5,
                self.center_x + 180 - i * 5,
                self.center_y + 180 - i * 5,
                fill=color, outline=''
            )

        # Calculate rotated and projected vertices
        projected = []
        depths = []
        for v in self.vertices:
            rx, ry, rz = self.rotate_point(v[0], v[1], v[2])
            px, py = self.project(rx, ry, rz)
            projected.append((px, py))
            depths.append(rz)

        # Sort faces by depth (painter's algorithm)
        face_depths = []
        for i, face in enumerate(self.faces):
            depth = self.get_face_depth(face)
            face_depths.append((depth, i, face))
        face_depths.sort(reverse=True)  # Draw far faces first

        # Draw faces
        for depth, i, face in face_depths:
            points = [projected[idx] for idx in face]
            color = self.face_colors[i] if i < len(self.face_colors) else '#444444'

            # Calculate face brightness based on orientation
            brightness = 0.5 + depth * 0.25
            brightness = max(0.3, min(1.0, brightness))

            # Adjust color brightness
            r = int(int(color[1:3], 16) * brightness)
            g = int(int(color[3:5], 16) * brightness)
            b = int(int(color[5:7], 16) * brightness)
            adjusted_color = f'#{r:02x}{g:02x}{b:02x}'

            self.create_polygon(
                points,
                fill=adjusted_color,
                outline='#ffffff',
                width=2
            )

            # Draw hash character on face if available
            if self.hash_chars and i < len(self.hash_chars):
                # Calculate face center
                cx = sum(p[0] for p in points) // len(points)
                cy = sum(p[1] for p in points) // len(points)

                # Only draw if face is facing forward
                if depth < 0.5:
                    char = self.hash_chars[i * 4:(i + 1) * 4]
                    char_str = ''.join(char) if char else ''
                    self.create_text(
                        cx, cy,
                        text=char_str,
                        fill='white',
                        font=('Courier', 10, 'bold')
                    )

        # Draw edges with glow effect
        for edge in self.edges:
            p1 = projected[edge[0]]
            p2 = projected[edge[1]]

            # Glow effect
            self.create_line(
                p1[0], p1[1], p2[0], p2[1],
                fill='#00ffff',
                width=3,
                stipple='gray50'
            )
            self.create_line(
                p1[0], p1[1], p2[0], p2[1],
                fill='#ffffff',
                width=1
            )

        # Draw block info
        self._draw_info()

    def _draw_info(self):
        """Draw block information overlay."""
        # Title
        self.create_text(
            self.center_x, 25,
            text="BTC BLOCK",
            fill='#00ffff',
            font=('Courier', 14, 'bold')
        )

        # Hash preview
        if self.block_hash:
            short_hash = self.block_hash[:16] + "..."
            self.create_text(
                self.center_x, self.height - 40,
                text=short_hash,
                fill='#88ff88',
                font=('Courier', 9)
            )

        # Nonce if available
        if self.block_data and 'nonce' in self.block_data:
            nonce_text = f"Nonce: {self.block_data['nonce']}"
            self.create_text(
                self.center_x, self.height - 20,
                text=nonce_text,
                fill='#ffff88',
                font=('Courier', 9)
            )

    def animate(self):
        """Animation loop."""
        if self.is_animating:
            # Update rotation angles
            self.angle_x += self.speed_x
            self.angle_y += self.speed_y
            self.angle_z += self.speed_z

            # Keep angles in range
            self.angle_x %= 2 * math.pi
            self.angle_y %= 2 * math.pi
            self.angle_z %= 2 * math.pi

            # Redraw
            self.draw()

            # Schedule next frame
            self.animation_id = self.after(33, self.animate)  # ~30 FPS

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

    def set_rotation(self, x: float, y: float, z: float):
        """Set rotation angles directly."""
        self.angle_x = x
        self.angle_y = y
        self.angle_z = z
        if not self.is_animating:
            self.draw()

    def set_speeds(self, x: float, y: float, z: float):
        """Set rotation speeds."""
        self.speed_x = x
        self.speed_y = y
        self.speed_z = z
