"""
Main Application Window
Central hub for SoloMiner GUI
"""

import customtkinter as ctk
from typing import Optional
import sys
import os

from ..core.wallet import WalletInfo
from .theme import COLORS, FONTS, SPACING, DIMENSIONS
from .wallet_screen import WalletScreen
from .mining_dashboard import MiningDashboard


class SplashScreen(ctk.CTkFrame):
    """Beautiful splash/welcome screen"""

    def __init__(self, parent, on_start: callable):
        super().__init__(parent, fg_color=COLORS["bg_dark"])

        self.on_start = on_start

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center container
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Bitcoin logo animation placeholder
        logo_frame = ctk.CTkFrame(center, fg_color="transparent")
        logo_frame.pack(pady=(0, SPACING["xl"]))

        # Large Bitcoin symbol
        btc_label = ctk.CTkLabel(
            logo_frame,
            text="₿",
            font=("Segoe UI", 120, "bold"),
            text_color=COLORS["bitcoin_orange"]
        )
        btc_label.pack()

        # App title
        title = ctk.CTkLabel(
            center,
            text="SoloMiner",
            font=("Segoe UI", 48, "bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack()

        # Subtitle
        subtitle = ctk.CTkLabel(
            center,
            text="Bitcoin Solo Mining Made Beautiful",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        subtitle.pack(pady=(SPACING["sm"], SPACING["xxl"]))

        # Feature highlights
        features_frame = ctk.CTkFrame(center, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])
        features_frame.pack(pady=(0, SPACING["xl"]))

        features_inner = ctk.CTkFrame(features_frame, fg_color="transparent")
        features_inner.pack(padx=SPACING["xl"], pady=SPACING["lg"])

        features = [
            ("🔐", "Secure Wallet Generation"),
            ("⛏️", "Solo Mining Engine"),
            ("📊", "Real-time Statistics"),
            ("🎯", "Difficulty Levels 0-12"),
        ]

        for icon, text in features:
            feature_row = ctk.CTkFrame(features_inner, fg_color="transparent")
            feature_row.pack(fill="x", pady=SPACING["xs"])

            ctk.CTkLabel(
                feature_row,
                text=icon,
                font=("Segoe UI", 20)
            ).pack(side="left", padx=(0, SPACING["md"]))

            ctk.CTkLabel(
                feature_row,
                text=text,
                font=FONTS["body"],
                text_color=COLORS["text_primary"]
            ).pack(side="left")

        # Start button
        start_btn = ctk.CTkButton(
            center,
            text="Get Started →",
            font=FONTS["body_bold"],
            fg_color=COLORS["bitcoin_orange"],
            hover_color="#e8850f",
            text_color=COLORS["bg_dark"],
            width=200,
            height=50,
            corner_radius=DIMENSIONS["border_radius"],
            command=self.on_start
        )
        start_btn.pack()

        # Version info
        version_label = ctk.CTkLabel(
            center,
            text="v1.0.0 | Made with ⚡ by Blockhead",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        version_label.pack(pady=SPACING["lg"])


class SoloMinerApp(ctk.CTk):
    """Main SoloMiner Application Window"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("SoloMiner - Bitcoin Solo Mining")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure background
        self.configure(fg_color=COLORS["bg_dark"])

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # State
        self.current_wallet: Optional[WalletInfo] = None
        self.current_screen: Optional[ctk.CTkFrame] = None

        # Show splash screen
        self._show_splash()

    def _clear_screen(self):
        """Clear current screen"""
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None

    def _show_splash(self):
        """Show splash/welcome screen"""
        self._clear_screen()
        self.current_screen = SplashScreen(self, self._show_wallet_screen)
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def _show_wallet_screen(self):
        """Show wallet generation screen"""
        self._clear_screen()
        self.current_screen = WalletScreen(self, self._on_wallet_confirmed)
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def _on_wallet_confirmed(self, wallet: WalletInfo):
        """Handle wallet confirmation"""
        self.current_wallet = wallet
        self._show_mining_dashboard()

    def _show_mining_dashboard(self):
        """Show mining dashboard"""
        if not self.current_wallet:
            self._show_wallet_screen()
            return

        self._clear_screen()
        self.current_screen = MiningDashboard(
            self,
            self.current_wallet,
            self._show_wallet_screen
        )
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def run(self):
        """Start the application"""
        self.mainloop()


def main():
    """Entry point for the application"""
    app = SoloMinerApp()
    app.run()


if __name__ == "__main__":
    main()
