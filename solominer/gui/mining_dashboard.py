"""
Mining Dashboard
Beautiful real-time visualization of the mining process
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
import threading
import time

from ..core.miner import SoloMiner, MiningState, MiningStats
from ..core.wallet import WalletInfo
from ..utils.helpers import format_hashrate, format_time, format_number
from .theme import COLORS, FONTS, SPACING, DIMENSIONS


class HashVisualizer(ctk.CTkFrame):
    """Visual representation of hash attempts"""

    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])

        self.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            self,
            text="🔍 Live Hash Attempts",
            font=FONTS["subheading"],
            text_color=COLORS["text_primary"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SPACING["lg"], pady=(SPACING["md"], SPACING["sm"]))

        # Hash display area
        self.hash_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_light"], corner_radius=8)
        self.hash_frame.grid(row=1, column=0, sticky="ew", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        self.hash_labels = []
        for i in range(5):
            label = ctk.CTkLabel(
                self.hash_frame,
                text="Waiting for hashes...",
                font=FONTS["mono_small"],
                text_color=COLORS["text_muted"],
                anchor="w"
            )
            label.pack(fill="x", padx=SPACING["sm"], pady=2)
            self.hash_labels.append(label)

    def update_hashes(self, hash_data: Dict[str, Any]):
        """Update hash display with new data"""
        hash_str = hash_data.get("hash", "")
        zeros = hash_data.get("zeros", 0)

        # Color based on leading zeros
        if zeros >= 6:
            color = COLORS["bitcoin_gold"]
        elif zeros >= 4:
            color = COLORS["accent_green"]
        elif zeros >= 2:
            color = COLORS["accent_cyan"]
        else:
            color = COLORS["text_secondary"]

        # Format hash with highlighted zeros
        display_hash = hash_str[:64] if len(hash_str) > 64 else hash_str

        # Shift existing labels down
        for i in range(len(self.hash_labels) - 1, 0, -1):
            prev_text = self.hash_labels[i-1].cget("text")
            prev_color = self.hash_labels[i-1].cget("text_color")
            self.hash_labels[i].configure(text=prev_text, text_color=prev_color)

        # Set new hash at top
        self.hash_labels[0].configure(text=f"→ {display_hash}", text_color=color)


class StatsPanel(ctk.CTkFrame):
    """Mining statistics panel"""

    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])

        self.grid_columnconfigure((0, 1), weight=1)

        # Title
        title = ctk.CTkLabel(
            self,
            text="📊 Mining Statistics",
            font=FONTS["subheading"],
            text_color=COLORS["text_primary"]
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=SPACING["lg"], pady=SPACING["md"])

        # Stats grid
        self.stat_labels = {}
        stats = [
            ("Hashrate", "0 H/s"),
            ("Total Hashes", "0"),
            ("Blocks Found", "0"),
            ("Elapsed Time", "0s"),
            ("Best Hash", "N/A"),
            ("Est. Time to Block", "Calculating..."),
        ]

        for i, (name, default) in enumerate(stats):
            row = (i // 2) + 1
            col = i % 2

            stat_frame = ctk.CTkFrame(self, fg_color="transparent")
            stat_frame.grid(row=row, column=col, sticky="ew", padx=SPACING["lg"], pady=SPACING["sm"])

            name_label = ctk.CTkLabel(
                stat_frame,
                text=name,
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            )
            name_label.pack(anchor="w")

            value_label = ctk.CTkLabel(
                stat_frame,
                text=default,
                font=FONTS["body_bold"],
                text_color=COLORS["text_primary"]
            )
            value_label.pack(anchor="w")

            self.stat_labels[name] = value_label

    def update_stats(self, stats: MiningStats):
        """Update statistics display"""
        self.stat_labels["Hashrate"].configure(text=format_hashrate(stats.hashrate))
        self.stat_labels["Total Hashes"].configure(text=format_number(stats.total_hashes))
        self.stat_labels["Blocks Found"].configure(
            text=str(stats.blocks_found),
            text_color=COLORS["bitcoin_gold"] if stats.blocks_found > 0 else COLORS["text_primary"]
        )
        self.stat_labels["Elapsed Time"].configure(text=format_time(stats.elapsed_time))

        if stats.best_hash:
            zeros_display = f"{stats.best_hash_zeros} zeros"
            self.stat_labels["Best Hash"].configure(
                text=zeros_display,
                text_color=COLORS["accent_green"] if stats.best_hash_zeros >= 4 else COLORS["text_primary"]
            )

        self.stat_labels["Est. Time to Block"].configure(text=stats.estimated_time_to_block)


class DifficultySelector(ctk.CTkFrame):
    """Mining difficulty level selector (0-12)"""

    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])

        self.on_change = on_change
        self.current_level = 4

        self.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Mining Difficulty",
            font=FONTS["subheading"],
            text_color=COLORS["text_primary"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SPACING["lg"], pady=SPACING["md"])

        # Level display
        self.level_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.level_frame.grid(row=1, column=0, padx=SPACING["lg"], pady=(0, SPACING["sm"]))

        self.level_label = ctk.CTkLabel(
            self.level_frame,
            text="Level 4",
            font=FONTS["heading_large"],
            text_color=COLORS["bitcoin_orange"]
        )
        self.level_label.pack()

        self.algo_label = ctk.CTkLabel(
            self.level_frame,
            text="Standard",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        self.algo_label.pack()

        # Slider
        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=12,
            number_of_steps=12,
            width=250,
            height=20,
            fg_color=COLORS["bg_light"],
            progress_color=COLORS["bitcoin_orange"],
            button_color=COLORS["bitcoin_orange"],
            button_hover_color="#e8850f",
            command=self._on_slider_change
        )
        self.slider.set(4)
        self.slider.grid(row=2, column=0, padx=SPACING["lg"], pady=(0, SPACING["sm"]))

        # Scale labels
        scale_frame = ctk.CTkFrame(self, fg_color="transparent")
        scale_frame.grid(row=3, column=0, sticky="ew", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        ctk.CTkLabel(
            scale_frame,
            text="0 (Demo)",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        ).pack(side="left")

        ctk.CTkLabel(
            scale_frame,
            text="12 (Maximum)",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        ).pack(side="right")

        # Algorithm descriptions
        self.algorithms = SoloMiner.get_all_algorithms()

    def _on_slider_change(self, value):
        """Handle slider value change"""
        level = int(value)
        if level != self.current_level:
            self.current_level = level
            algo = self.algorithms.get(level, {})

            self.level_label.configure(text=f"Level {level}")
            self.algo_label.configure(text=algo.get("name", "Unknown"))

            self.on_change(level)

    def get_level(self) -> int:
        """Get current difficulty level"""
        return self.current_level

    def set_enabled(self, enabled: bool):
        """Enable or disable the selector"""
        state = "normal" if enabled else "disabled"
        self.slider.configure(state=state)


class MiningDashboard(ctk.CTkFrame):
    """Main mining dashboard with real-time visualization"""

    def __init__(self, parent, wallet: WalletInfo, on_back: callable):
        super().__init__(parent, fg_color=COLORS["bg_dark"])

        self.wallet = wallet
        self.on_back = on_back
        self.miner = SoloMiner(wallet_address=wallet.address)
        self.is_mining = False

        # Register callbacks
        self.miner.register_callback("stats_update", self._on_stats_update)
        self.miner.register_callback("new_best_hash", self._on_new_best_hash)
        self.miner.register_callback("block_found", self._on_block_found)
        self.miner.register_callback("mining_started", self._on_mining_started)
        self.miner.register_callback("mining_stopped", self._on_mining_stopped)

        self._setup_ui()

    def _setup_ui(self):
        """Setup the dashboard UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self._create_header()

        # Wallet info bar
        self._create_wallet_bar()

        # Main content
        self._create_main_content()

        # Control panel
        self._create_control_panel()

    def _create_header(self):
        """Create dashboard header"""
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_medium"], height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Back button
        back_btn = ctk.CTkButton(
            header,
            text="← Back",
            font=FONTS["body"],
            fg_color="transparent",
            hover_color=COLORS["bg_light"],
            text_color=COLORS["text_secondary"],
            width=80,
            command=self._handle_back
        )
        back_btn.grid(row=0, column=0, padx=SPACING["md"], pady=SPACING["md"])

        # Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=1)

        title = ctk.CTkLabel(
            title_frame,
            text="⛏️ SoloMiner Dashboard",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        )
        title.pack()

        # Status indicator
        self.status_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.status_frame.grid(row=0, column=2, padx=SPACING["lg"])

        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="●",
            font=("Segoe UI", 16),
            text_color=COLORS["text_muted"]
        )
        self.status_dot.pack(side="left", padx=(0, SPACING["xs"]))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Idle",
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        self.status_label.pack(side="left")

    def _create_wallet_bar(self):
        """Create wallet information bar"""
        wallet_bar = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], height=50)
        wallet_bar.grid(row=1, column=0, sticky="ew", padx=SPACING["lg"], pady=SPACING["md"])
        wallet_bar.grid_propagate(False)

        inner = ctk.CTkFrame(wallet_bar, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner,
            text="💰 Mining to:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=(0, SPACING["sm"]))

        ctk.CTkLabel(
            inner,
            text=self.wallet.address,
            font=FONTS["mono"],
            text_color=COLORS["bitcoin_orange"]
        ).pack(side="left")

    def _create_main_content(self):
        """Create main dashboard content"""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=2, column=0, sticky="nsew", padx=SPACING["lg"], pady=0)
        content.grid_columnconfigure((0, 1), weight=1)
        content.grid_rowconfigure((0, 1), weight=1)

        # Hash visualizer (top left)
        self.hash_visualizer = HashVisualizer(content)
        self.hash_visualizer.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["sm"]), pady=(0, SPACING["sm"]))

        # Stats panel (top right)
        self.stats_panel = StatsPanel(content)
        self.stats_panel.grid(row=0, column=1, sticky="nsew", padx=(SPACING["sm"], 0), pady=(0, SPACING["sm"]))

        # Difficulty selector (bottom left)
        self.difficulty_selector = DifficultySelector(content, self._on_difficulty_change)
        self.difficulty_selector.grid(row=1, column=0, sticky="nsew", padx=(0, SPACING["sm"]), pady=(SPACING["sm"], 0))

        # Mining progress visualization (bottom right)
        self._create_progress_panel(content)

    def _create_progress_panel(self, parent):
        """Create mining progress visualization panel"""
        progress_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])
        progress_frame.grid(row=1, column=1, sticky="nsew", padx=(SPACING["sm"], 0), pady=(SPACING["sm"], 0))

        # Title
        ctk.CTkLabel(
            progress_frame,
            text="🎯 Block Progress",
            font=FONTS["subheading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", padx=SPACING["lg"], pady=SPACING["md"])

        # Visual progress bars for hash zeros
        self.progress_bars = {}
        for i in range(8):
            bar_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
            bar_frame.pack(fill="x", padx=SPACING["lg"], pady=2)

            ctk.CTkLabel(
                bar_frame,
                text=f"{i+1}",
                font=FONTS["mono_small"],
                text_color=COLORS["text_muted"],
                width=20
            ).pack(side="left")

            bar = ctk.CTkProgressBar(
                bar_frame,
                width=150,
                height=12,
                fg_color=COLORS["bg_light"],
                progress_color=COLORS["accent_cyan"]
            )
            bar.set(0)
            bar.pack(side="left", padx=SPACING["sm"])

            self.progress_bars[i+1] = bar

        # Block found counter
        self.block_frame = ctk.CTkFrame(progress_frame, fg_color=COLORS["bg_light"], corner_radius=8)
        self.block_frame.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])

        self.block_count_label = ctk.CTkLabel(
            self.block_frame,
            text="🏆 Blocks Found: 0",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"]
        )
        self.block_count_label.pack(pady=SPACING["sm"])

    def _create_control_panel(self):
        """Create mining control panel"""
        control_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_medium"], height=80)
        control_frame.grid(row=3, column=0, sticky="ew")
        control_frame.grid_propagate(False)

        inner = ctk.CTkFrame(control_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        # Start/Stop button
        self.start_btn = ctk.CTkButton(
            inner,
            text="▶  Start Mining",
            font=FONTS["body_bold"],
            fg_color=COLORS["accent_green"],
            hover_color="#2ea043",
            text_color=COLORS["text_primary"],
            width=180,
            height=50,
            corner_radius=DIMENSIONS["border_radius"],
            command=self._toggle_mining
        )
        self.start_btn.pack(side="left", padx=SPACING["md"])

        # Pause button
        self.pause_btn = ctk.CTkButton(
            inner,
            text="⏸  Pause",
            font=FONTS["body"],
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["bg_card"],
            text_color=COLORS["text_primary"],
            width=120,
            height=50,
            state="disabled",
            command=self._toggle_pause
        )
        self.pause_btn.pack(side="left", padx=SPACING["md"])

        self.is_paused = False

    def _toggle_mining(self):
        """Start or stop mining"""
        if not self.is_mining:
            level = self.difficulty_selector.get_level()
            self.miner.start_mining(level)
            self.is_mining = True
            self.start_btn.configure(
                text="⏹  Stop Mining",
                fg_color=COLORS["error"],
                hover_color="#b62324"
            )
            self.pause_btn.configure(state="normal")
            self.difficulty_selector.set_enabled(False)
            self._update_status("Mining", COLORS["accent_green"])
        else:
            self.miner.stop_mining()
            self.is_mining = False
            self.start_btn.configure(
                text="▶  Start Mining",
                fg_color=COLORS["accent_green"],
                hover_color="#2ea043"
            )
            self.pause_btn.configure(state="disabled", text="⏸  Pause")
            self.is_paused = False
            self.difficulty_selector.set_enabled(True)
            self._update_status("Stopped", COLORS["text_muted"])

    def _toggle_pause(self):
        """Pause or resume mining"""
        if not self.is_paused:
            self.miner.pause_mining()
            self.is_paused = True
            self.pause_btn.configure(text="▶  Resume")
            self._update_status("Paused", COLORS["warning"])
        else:
            self.miner.resume_mining()
            self.is_paused = False
            self.pause_btn.configure(text="⏸  Pause")
            self._update_status("Mining", COLORS["accent_green"])

    def _update_status(self, text: str, color: str):
        """Update status indicator"""
        self.status_dot.configure(text_color=color)
        self.status_label.configure(text=text, text_color=color)

    def _on_difficulty_change(self, level: int):
        """Handle difficulty level change"""
        # Update is handled by selector, nothing else needed when not mining
        pass

    def _on_stats_update(self, stats: MiningStats):
        """Handle stats update from miner"""
        self.after(0, lambda: self.stats_panel.update_stats(stats))

        # Update progress bars
        zeros = stats.best_hash_zeros
        for i, bar in self.progress_bars.items():
            if i <= zeros:
                self.after(0, lambda b=bar: b.configure(progress_color=COLORS["accent_green"]))
                self.after(0, lambda b=bar: b.set(1.0))
            else:
                self.after(0, lambda b=bar: b.configure(progress_color=COLORS["accent_cyan"]))
                self.after(0, lambda b=bar: b.set(0))

    def _on_new_best_hash(self, data: dict):
        """Handle new best hash found"""
        self.after(0, lambda: self.hash_visualizer.update_hashes(data))

    def _on_block_found(self, data: dict):
        """Handle block found event"""
        blocks = data.get("total_hashes", 0)
        self.after(0, lambda: self.block_count_label.configure(
            text=f"🏆 Blocks Found: {self.miner.stats.blocks_found}",
            text_color=COLORS["bitcoin_gold"]
        ))

        # Flash effect
        self.after(0, lambda: self.block_frame.configure(fg_color=COLORS["bitcoin_orange"]))
        self.after(500, lambda: self.block_frame.configure(fg_color=COLORS["bg_light"]))

    def _on_mining_started(self, data):
        """Handle mining started event"""
        self._update_status("Mining", COLORS["accent_green"])

    def _on_mining_stopped(self, data):
        """Handle mining stopped event"""
        self._update_status("Stopped", COLORS["text_muted"])

    def _handle_back(self):
        """Handle back button press"""
        if self.is_mining:
            self.miner.stop_mining()
        self.on_back()

    def destroy(self):
        """Clean up when destroyed"""
        if self.is_mining:
            self.miner.stop_mining()
        super().destroy()
