"""
Algorithm display panel showing SHA-256 and mining algorithm steps.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Optional, Callable
import time


class AlgorithmPanel(tk.Frame):
    """
    Panel displaying the Bitcoin mining algorithm with
    step-by-step visualization.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#0a0a15', **kwargs)

        self.current_step = 0
        self.is_mining = False
        self.mining_callback: Optional[Callable] = None

        self._create_widgets()

    def _create_widgets(self):
        """Create the panel widgets."""
        # Title
        title_frame = tk.Frame(self, bg='#0a0a15')
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = tk.Label(
            title_frame,
            text="⚡ BITCOIN ALGORITHM ⚡",
            font=('Arial', 14, 'bold'),
            fg='#ffcc00',
            bg='#0a0a15'
        )
        title_label.pack()

        # Algorithm steps display
        steps_frame = tk.LabelFrame(
            self,
            text="SHA-256 Algorithm Steps",
            font=('Arial', 10),
            fg='#00ffcc',
            bg='#0a0a15',
            relief=tk.RIDGE
        )
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Steps list
        self.steps_canvas = tk.Canvas(
            steps_frame,
            bg='#050510',
            highlightthickness=0,
            width=280,
            height=300
        )
        self.steps_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Algorithm steps
        self.algorithm_steps = [
            {
                'name': '1. Block Header',
                'desc': 'Assemble 80-byte header:\nVersion + Prev Hash + Merkle Root\n+ Timestamp + Bits + Nonce',
                'icon': '📦'
            },
            {
                'name': '2. Padding',
                'desc': 'Pad message to 512-bit blocks:\nAppend 1 bit, zeros, length',
                'icon': '📐'
            },
            {
                'name': '3. Initialize',
                'desc': 'Set hash values H₀-H₇\nfrom square roots of primes',
                'icon': '🔢'
            },
            {
                'name': '4. Expand',
                'desc': 'Expand 16 words to 64:\nWₜ = σ₁(Wₜ₋₂)+Wₜ₋₇+σ₀(Wₜ₋₁₅)+Wₜ₋₁₆',
                'icon': '📈'
            },
            {
                'name': '5. Compress',
                'desc': '64 rounds of mixing:\nCh, Maj, Σ functions with\nround constants K₀-K₆₃',
                'icon': '🔄'
            },
            {
                'name': '6. Add',
                'desc': 'Add compressed values\nto running hash total',
                'icon': '➕'
            },
            {
                'name': '7. Double Hash',
                'desc': 'Apply SHA-256 again:\nHash = SHA256(SHA256(header))',
                'icon': '🔐'
            },
            {
                'name': '8. Check',
                'desc': 'Compare to target:\nIf hash < target → Valid!\nElse → Try new nonce',
                'icon': '✅'
            }
        ]

        self._draw_steps()

        # Mining controls
        controls_frame = tk.LabelFrame(
            self,
            text="Mining Simulation",
            font=('Arial', 10),
            fg='#ff8800',
            bg='#0a0a15',
            relief=tk.RIDGE
        )
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # Mining status
        self.status_label = tk.Label(
            controls_frame,
            text="Status: Idle",
            font=('Courier', 10),
            fg='#888888',
            bg='#0a0a15'
        )
        self.status_label.pack(pady=5)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            controls_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=260
        )
        self.progress_bar.pack(pady=5)

        # Hash display
        self.hash_label = tk.Label(
            controls_frame,
            text="Hash: ---",
            font=('Courier', 8),
            fg='#00ff88',
            bg='#0a0a15',
            wraplength=270
        )
        self.hash_label.pack(pady=5)

        # Nonce display
        self.nonce_label = tk.Label(
            controls_frame,
            text="Nonce: 0",
            font=('Courier', 10),
            fg='#ffff00',
            bg='#0a0a15'
        )
        self.nonce_label.pack(pady=2)

        # Difficulty display
        self.diff_label = tk.Label(
            controls_frame,
            text="Difficulty: 4 leading zeros",
            font=('Courier', 9),
            fg='#aaaaaa',
            bg='#0a0a15'
        )
        self.diff_label.pack(pady=2)

        # Buttons
        btn_frame = tk.Frame(controls_frame, bg='#0a0a15')
        btn_frame.pack(pady=10)

        self.mine_btn = tk.Button(
            btn_frame,
            text="▶ START MINING",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#228822',
            activebackground='#33aa33',
            command=self._toggle_mining,
            width=15
        )
        self.mine_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            btn_frame,
            text="↺ RESET",
            font=('Arial', 10),
            fg='white',
            bg='#444444',
            activebackground='#666666',
            command=self._reset,
            width=10
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Constants display
        const_frame = tk.LabelFrame(
            self,
            text="SHA-256 Constants (K)",
            font=('Arial', 9),
            fg='#8888ff',
            bg='#0a0a15',
            relief=tk.RIDGE
        )
        const_frame.pack(fill=tk.X, padx=10, pady=5)

        self.const_text = tk.Text(
            const_frame,
            height=4,
            width=35,
            font=('Courier', 7),
            fg='#00ffff',
            bg='#050510',
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.const_text.pack(padx=5, pady=5)

        # Insert first 16 constants
        k_constants = [
            "428a2f98", "71374491", "b5c0fbcf", "e9b5dba5",
            "3956c25b", "59f111f1", "923f82a4", "ab1c5ed5",
            "d807aa98", "12835b01", "243185be", "550c7dc3",
            "72be5d74", "80deb1fe", "9bdc06a7", "c19bf174"
        ]
        self.const_text.insert('1.0', ' '.join(k_constants))
        self.const_text.config(state=tk.DISABLED)

    def _draw_steps(self):
        """Draw algorithm steps on the canvas."""
        self.steps_canvas.delete('all')

        y = 10
        for i, step in enumerate(self.algorithm_steps):
            # Determine colors based on current step
            if i < self.current_step:
                bg_color = '#0a2a0a'  # Completed - dark green
                text_color = '#00ff00'
                status = '✓'
            elif i == self.current_step:
                bg_color = '#2a2a0a'  # Current - dark yellow
                text_color = '#ffff00'
                status = '►'
            else:
                bg_color = '#0a0a1a'  # Pending - dark blue
                text_color = '#666688'
                status = '○'

            # Draw step background
            self.steps_canvas.create_rectangle(
                5, y, 275, y + 35,
                fill=bg_color,
                outline='#333355'
            )

            # Draw step icon and name
            self.steps_canvas.create_text(
                15, y + 12,
                text=step['icon'],
                font=('Arial', 10),
                anchor='w'
            )

            self.steps_canvas.create_text(
                35, y + 12,
                text=f"{status} {step['name']}",
                fill=text_color,
                font=('Courier', 9, 'bold'),
                anchor='w'
            )

            # Draw brief description
            desc_short = step['desc'].split('\n')[0][:30]
            self.steps_canvas.create_text(
                35, y + 26,
                text=desc_short,
                fill='#888888',
                font=('Arial', 7),
                anchor='w'
            )

            y += 37

    def set_step(self, step: int):
        """Set the current algorithm step."""
        self.current_step = step
        self._draw_steps()

    def _toggle_mining(self):
        """Toggle mining simulation on/off."""
        if self.is_mining:
            self.is_mining = False
            self.mine_btn.config(text="▶ START MINING", bg='#228822')
            self.status_label.config(text="Status: Stopped", fg='#ff8888')
        else:
            self.is_mining = True
            self.mine_btn.config(text="■ STOP MINING", bg='#882222')
            self.status_label.config(text="Status: Mining...", fg='#88ff88')
            self._simulate_mining()

    def _simulate_mining(self):
        """Simulate the mining process."""
        if not self.is_mining:
            return

        import random
        import hashlib

        # Generate a pseudo-random hash
        nonce = int(self.nonce_label.cget('text').split(': ')[1])
        nonce += random.randint(1, 1000)

        # Create sample header and hash
        header = f"block_header_{nonce}".encode()
        hash_result = hashlib.sha256(hashlib.sha256(header).digest()).hexdigest()

        # Update display
        self.nonce_label.config(text=f"Nonce: {nonce}")
        self.hash_label.config(text=f"Hash: {hash_result}")

        # Check for "valid" hash (starts with zeros)
        leading_zeros = len(hash_result) - len(hash_result.lstrip('0'))

        # Update progress (fake progress for visualization)
        progress = min(100, self.progress_var.get() + random.uniform(0.5, 2))
        self.progress_var.set(progress)

        # Cycle through algorithm steps
        self.current_step = (self.current_step + 1) % len(self.algorithm_steps)
        self._draw_steps()

        # Check for "success"
        if leading_zeros >= 4:
            self.is_mining = False
            self.mine_btn.config(text="▶ START MINING", bg='#228822')
            self.status_label.config(text="Status: BLOCK FOUND!", fg='#00ff00')
            self.progress_var.set(100)
            self.hash_label.config(fg='#00ffff')

            # Trigger callback if set
            if self.mining_callback:
                self.mining_callback(hash_result, nonce)
            return

        # Continue mining
        delay = random.randint(50, 150)
        self.after(delay, self._simulate_mining)

    def _reset(self):
        """Reset the mining simulation."""
        self.is_mining = False
        self.current_step = 0
        self.progress_var.set(0)
        self.nonce_label.config(text="Nonce: 0")
        self.hash_label.config(text="Hash: ---", fg='#00ff88')
        self.status_label.config(text="Status: Idle", fg='#888888')
        self.mine_btn.config(text="▶ START MINING", bg='#228822')
        self._draw_steps()

    def set_mining_callback(self, callback: Callable):
        """Set callback for when mining finds a block."""
        self.mining_callback = callback

    def update_hash(self, hash_str: str, nonce: int):
        """Update the displayed hash and nonce."""
        self.hash_label.config(text=f"Hash: {hash_str}")
        self.nonce_label.config(text=f"Nonce: {nonce}")

    def set_difficulty(self, difficulty: int):
        """Set the displayed difficulty."""
        self.diff_label.config(text=f"Difficulty: {difficulty} leading zeros")
