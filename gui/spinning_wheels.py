"""
Spinning Wheels within Wheels visualization.

Displays nested rotating wheels showing Bitcoin algorithm constants
and hash data, inspired by Ezekiel's vision.
"""

import tkinter as tk
from tkinter import Canvas
import math
from typing import List, Tuple, Optional


class SpinningWheelsView(Canvas):
    """
    Canvas widget displaying nested spinning wheels with
    Bitcoin algorithm data.
    """

    def __init__(self, parent, width: int = 450, height: int = 450, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg='#000005', highlightthickness=0, **kwargs)

        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2

        # Wheel configuration
        self.num_wheels = 8
        self.wheels = []
        self._init_wheels()

        # Animation state
        self.is_animating = True
        self.animation_id = None
        self.time = 0.0

        # SHA-256 constants for display
        self.sha256_k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        # Block hash for inner visualization
        self.block_hash: Optional[str] = None

        # Start animation
        self.animate()

    def _init_wheels(self):
        """Initialize wheel configurations."""
        max_radius = min(self.width, self.height) // 2 - 20

        for i in range(self.num_wheels):
            # Decreasing radius for nested wheels
            radius = max_radius - (i * (max_radius // (self.num_wheels + 1)))

            # Alternating rotation directions
            direction = 1 if i % 2 == 0 else -1

            # Speed varies by wheel
            base_speed = 0.02 - i * 0.002
            speed = base_speed * direction

            # Number of segments
            segments = 8 + (i * 2)

            # Colors
            hue = (i / self.num_wheels) * 0.7  # Range through spectrum

            wheel = {
                'radius': radius,
                'inner_radius': radius - 15 if radius > 30 else radius - 5,
                'angle': 0.0,
                'speed': speed,
                'segments': segments,
                'hue': hue,
                'constants': [],
            }

            # Assign SHA-256 constants to wheel
            constants_per_wheel = len(self.sha256_k) // self.num_wheels
            start_idx = i * constants_per_wheel
            wheel['constants'] = self.sha256_k[start_idx:start_idx + constants_per_wheel]

            self.wheels.append(wheel)

    def set_block_data(self, block_hash: str, wheel_speeds: List[float] = None):
        """Set block data for visualization."""
        self.block_hash = block_hash

        # Update wheel speeds if provided
        if wheel_speeds:
            for i, speed in enumerate(wheel_speeds[:self.num_wheels]):
                if i < len(self.wheels):
                    direction = 1 if i % 2 == 0 else -1
                    self.wheels[i]['speed'] = speed * 0.03 * direction

    def draw_wheel(self, wheel: dict, wheel_idx: int):
        """Draw a single wheel."""
        radius = wheel['radius']
        inner_radius = wheel['inner_radius']
        angle = wheel['angle']
        segments = wheel['segments']
        hue = wheel['hue']

        # Skip if wheel too small
        if radius < 10:
            return

        # Draw wheel segments
        segment_angle = 2 * math.pi / segments

        for i in range(segments):
            start_angle = angle + i * segment_angle
            end_angle = start_angle + segment_angle * 0.9  # Gap between segments

            # Alternate segment colors
            sat = 0.7 if i % 2 == 0 else 0.5
            val = 0.8 if i % 2 == 0 else 0.6

            # Convert HSV to hex color
            import colorsys
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )

            # Draw arc segment
            self._draw_arc_segment(radius, inner_radius, start_angle, end_angle, color)

            # Draw constant value on segment if space allows
            if radius > 60 and i < len(wheel['constants']):
                mid_angle = (start_angle + end_angle) / 2
                text_radius = (radius + inner_radius) / 2
                tx = self.center_x + text_radius * math.cos(mid_angle)
                ty = self.center_y + text_radius * math.sin(mid_angle)

                const_text = f"{wheel['constants'][i]:08x}"[:4]
                self.create_text(
                    tx, ty,
                    text=const_text,
                    fill='white',
                    font=('Courier', 7),
                    angle=-math.degrees(mid_angle)
                )

        # Draw rim circles
        self.create_oval(
            self.center_x - radius, self.center_y - radius,
            self.center_x + radius, self.center_y + radius,
            outline='#ffffff',
            width=1
        )
        self.create_oval(
            self.center_x - inner_radius, self.center_y - inner_radius,
            self.center_x + inner_radius, self.center_y + inner_radius,
            outline='#888888',
            width=1
        )

        # Draw spokes
        self._draw_spokes(radius, inner_radius, angle, segments)

    def _draw_arc_segment(self, outer_r: float, inner_r: float,
                          start_angle: float, end_angle: float, color: str):
        """Draw an arc segment (pie slice with inner cutout)."""
        # Create polygon points for the arc segment
        points = []
        num_arc_points = 12

        # Outer arc (counterclockwise)
        for i in range(num_arc_points + 1):
            t = start_angle + (end_angle - start_angle) * (i / num_arc_points)
            x = self.center_x + outer_r * math.cos(t)
            y = self.center_y + outer_r * math.sin(t)
            points.extend([x, y])

        # Inner arc (clockwise - reverse direction)
        for i in range(num_arc_points, -1, -1):
            t = start_angle + (end_angle - start_angle) * (i / num_arc_points)
            x = self.center_x + inner_r * math.cos(t)
            y = self.center_y + inner_r * math.sin(t)
            points.extend([x, y])

        if len(points) >= 6:
            self.create_polygon(points, fill=color, outline='#333333', width=1)

    def _draw_spokes(self, outer_r: float, inner_r: float, angle: float, segments: int):
        """Draw spoke lines on the wheel."""
        segment_angle = 2 * math.pi / segments

        for i in range(segments):
            spoke_angle = angle + i * segment_angle

            x1 = self.center_x + inner_r * math.cos(spoke_angle)
            y1 = self.center_y + inner_r * math.sin(spoke_angle)
            x2 = self.center_x + outer_r * math.cos(spoke_angle)
            y2 = self.center_y + outer_r * math.sin(spoke_angle)

            self.create_line(
                x1, y1, x2, y2,
                fill='#444466',
                width=1
            )

    def draw_center(self):
        """Draw the center of the wheel system with hash data."""
        # Innermost circle
        center_radius = 40

        # Glowing center
        for i in range(5):
            r = center_radius + (5 - i) * 3
            alpha = 0.2 + i * 0.1
            shade = int(100 + i * 30)
            color = f'#{shade:02x}{shade:02x}ff'

            self.create_oval(
                self.center_x - r, self.center_y - r,
                self.center_x + r, self.center_y + r,
                fill=color,
                outline=''
            )

        # Center disc
        self.create_oval(
            self.center_x - center_radius, self.center_y - center_radius,
            self.center_x + center_radius, self.center_y + center_radius,
            fill='#0a0a30',
            outline='#00ffff',
            width=2
        )

        # Rotating inner pattern
        pattern_radius = center_radius - 10
        num_points = 6
        points = []

        for i in range(num_points):
            angle = self.time * 2 + (i * 2 * math.pi / num_points)
            x = self.center_x + pattern_radius * math.cos(angle) * 0.7
            y = self.center_y + pattern_radius * math.sin(angle) * 0.7
            points.extend([x, y])

        if len(points) >= 6:
            self.create_polygon(points, fill='#000033', outline='#00ff88', width=1)

        # Hash preview in center
        if self.block_hash:
            short_hash = self.block_hash[:8]
            self.create_text(
                self.center_x, self.center_y,
                text=short_hash,
                fill='#00ffff',
                font=('Courier', 9, 'bold')
            )

    def draw_eyes(self):
        """Draw the 'eyes' around the wheels (Ezekiel reference)."""
        # Eyes are positioned around the outer wheel
        if not self.wheels:
            return

        outer_radius = self.wheels[0]['radius'] + 15
        num_eyes = 12
        eye_size = 8

        for i in range(num_eyes):
            angle = self.time * 0.5 + (i * 2 * math.pi / num_eyes)
            x = self.center_x + outer_radius * math.cos(angle)
            y = self.center_y + outer_radius * math.sin(angle)

            # Eye white
            self.create_oval(
                x - eye_size, y - eye_size * 0.6,
                x + eye_size, y + eye_size * 0.6,
                fill='white',
                outline='#666666'
            )

            # Pupil - looks toward center
            pupil_offset_x = -math.cos(angle) * 2
            pupil_offset_y = -math.sin(angle) * 2
            pupil_size = eye_size * 0.4

            self.create_oval(
                x + pupil_offset_x - pupil_size,
                y + pupil_offset_y - pupil_size,
                x + pupil_offset_x + pupil_size,
                y + pupil_offset_y + pupil_size,
                fill='#000000',
                outline=''
            )

    def draw(self):
        """Draw all wheels."""
        self.delete('all')

        # Draw background glow
        self._draw_background()

        # Draw eyes first (behind wheels)
        self.draw_eyes()

        # Draw wheels from outer to inner
        for i, wheel in enumerate(self.wheels):
            self.draw_wheel(wheel, i)

        # Draw center
        self.draw_center()

        # Draw title
        self.create_text(
            self.center_x, 15,
            text="WHEELS WITHIN WHEELS",
            fill='#00ffaa',
            font=('Arial', 11, 'bold')
        )

        # Draw info
        self.create_text(
            self.center_x, self.height - 15,
            text="SHA-256 Constants in Motion",
            fill='#666688',
            font=('Arial', 8)
        )

    def _draw_background(self):
        """Draw subtle background effects."""
        # Radial gradient effect
        max_r = min(self.width, self.height) // 2
        for i in range(10):
            r = max_r - i * (max_r // 10)
            shade = 5 + i * 2
            color = f'#{shade:02x}{shade:02x}{int(shade * 1.2):02x}'

            self.create_oval(
                self.center_x - r, self.center_y - r,
                self.center_x + r, self.center_y + r,
                fill=color,
                outline=''
            )

    def animate(self):
        """Animation loop."""
        if self.is_animating:
            # Update time
            self.time += 0.05

            # Update wheel rotations
            for wheel in self.wheels:
                wheel['angle'] += wheel['speed']
                wheel['angle'] %= 2 * math.pi

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

    def set_wheel_speeds(self, speeds: List[float]):
        """Set individual wheel speeds."""
        for i, speed in enumerate(speeds[:len(self.wheels)]):
            direction = 1 if i % 2 == 0 else -1
            self.wheels[i]['speed'] = speed * 0.03 * direction

    def pulse_wheel(self, wheel_idx: int):
        """Trigger a pulse effect on a specific wheel."""
        if 0 <= wheel_idx < len(self.wheels):
            # Temporarily increase speed
            original_speed = self.wheels[wheel_idx]['speed']
            self.wheels[wheel_idx]['speed'] *= 3

            # Reset after delay
            def reset_speed():
                if wheel_idx < len(self.wheels):
                    self.wheels[wheel_idx]['speed'] = original_speed

            self.after(500, reset_speed)
