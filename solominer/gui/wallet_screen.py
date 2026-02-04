"""
Wallet Generation Screen
Beautiful UI for generating and confirming BTC wallets
"""

import customtkinter as ctk
from typing import Callable, Optional
import threading
import time

from ..core.wallet import WalletGenerator, WalletInfo
from .theme import COLORS, FONTS, SPACING, DIMENSIONS


class WalletScreen(ctk.CTkFrame):
    """Wallet generation and confirmation screen"""

    def __init__(self, parent, on_wallet_confirmed: Callable[[WalletInfo], None]):
        super().__init__(parent, fg_color=COLORS["bg_dark"])

        self.wallet_generator = WalletGenerator()
        self.on_wallet_confirmed = on_wallet_confirmed
        self.current_wallet: Optional[WalletInfo] = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup the wallet screen UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self._create_header()

        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=SPACING["xl"], pady=SPACING["lg"])
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Show initial wallet generation view
        self._show_generate_view()

    def _create_header(self):
        """Create the header section"""
        header_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_medium"], height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)

        # Bitcoin icon and title
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.5, anchor="center")

        btc_label = ctk.CTkLabel(
            title_frame,
            text="₿",
            font=("Segoe UI", 36, "bold"),
            text_color=COLORS["bitcoin_orange"]
        )
        btc_label.pack(side="left", padx=(0, SPACING["sm"]))

        title_label = ctk.CTkLabel(
            title_frame,
            text="Wallet Generator",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        )
        title_label.pack(side="left")

    def _show_generate_view(self):
        """Show the wallet generation view"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Icon
        icon_label = ctk.CTkLabel(
            center_frame,
            text="🔐",
            font=("Segoe UI", 64)
        )
        icon_label.pack(pady=(0, SPACING["lg"]))

        # Description
        desc_label = ctk.CTkLabel(
            center_frame,
            text="Generate a new Bitcoin wallet for solo mining",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        desc_label.pack(pady=(0, SPACING["xl"]))

        # Security info card
        security_card = ctk.CTkFrame(center_frame, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])
        security_card.pack(fill="x", pady=(0, SPACING["xl"]))

        security_inner = ctk.CTkFrame(security_card, fg_color="transparent")
        security_inner.pack(padx=SPACING["lg"], pady=SPACING["lg"])

        security_items = [
            "🔒  Cryptographically secure key generation",
            "📝  12-word mnemonic seed phrase",
            "🛡️  Keys never leave your device",
            "⚡  Instant wallet creation"
        ]

        for item in security_items:
            item_label = ctk.CTkLabel(
                security_inner,
                text=item,
                font=FONTS["body"],
                text_color=COLORS["text_secondary"],
                anchor="w"
            )
            item_label.pack(fill="x", pady=SPACING["xs"])

        # Generate button
        generate_btn = ctk.CTkButton(
            center_frame,
            text="Generate New Wallet",
            font=FONTS["body_bold"],
            fg_color=COLORS["bitcoin_orange"],
            hover_color="#e8850f",
            text_color=COLORS["bg_dark"],
            width=DIMENSIONS["button_width"],
            height=DIMENSIONS["button_height"],
            corner_radius=DIMENSIONS["border_radius"],
            command=self._generate_wallet
        )
        generate_btn.pack()

        # Or import existing
        import_label = ctk.CTkLabel(
            center_frame,
            text="or import existing wallet",
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            cursor="hand2"
        )
        import_label.pack(pady=SPACING["md"])
        import_label.bind("<Button-1>", lambda e: self._show_import_view())

    def _show_import_view(self):
        """Show wallet import view"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title_label = ctk.CTkLabel(
            center_frame,
            text="Import Existing Wallet",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        )
        title_label.pack(pady=(0, SPACING["lg"]))

        # Address input
        address_label = ctk.CTkLabel(
            center_frame,
            text="Bitcoin Address",
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"]
        )
        address_label.pack(anchor="w", pady=(0, SPACING["xs"]))

        self.address_entry = ctk.CTkEntry(
            center_frame,
            width=400,
            height=DIMENSIONS["input_height"],
            font=FONTS["mono"],
            fg_color=COLORS["bg_light"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text="Enter your Bitcoin address (e.g., 1A1zP1...)"
        )
        self.address_entry.pack(pady=(0, SPACING["lg"]))

        # Button frame
        btn_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        btn_frame.pack()

        # Back button
        back_btn = ctk.CTkButton(
            btn_frame,
            text="← Back",
            font=FONTS["body"],
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["bg_medium"],
            text_color=COLORS["text_primary"],
            width=120,
            height=DIMENSIONS["button_height"],
            command=self._show_generate_view
        )
        back_btn.pack(side="left", padx=(0, SPACING["md"]))

        # Import button
        import_btn = ctk.CTkButton(
            btn_frame,
            text="Import Wallet",
            font=FONTS["body_bold"],
            fg_color=COLORS["bitcoin_orange"],
            hover_color="#e8850f",
            text_color=COLORS["bg_dark"],
            width=160,
            height=DIMENSIONS["button_height"],
            command=self._import_wallet
        )
        import_btn.pack(side="left")

    def _generate_wallet(self):
        """Generate a new wallet with animation"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Loading animation
        loading_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        loading_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.loading_label = ctk.CTkLabel(
            loading_frame,
            text="🔄",
            font=("Segoe UI", 48)
        )
        self.loading_label.pack()

        self.status_label = ctk.CTkLabel(
            loading_frame,
            text="Generating secure entropy...",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(pady=SPACING["md"])

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            loading_frame,
            width=300,
            height=8,
            fg_color=COLORS["bg_light"],
            progress_color=COLORS["bitcoin_orange"]
        )
        self.progress_bar.pack(pady=SPACING["md"])
        self.progress_bar.set(0)

        # Start generation in thread
        threading.Thread(target=self._generate_wallet_async, daemon=True).start()

    def _generate_wallet_async(self):
        """Async wallet generation with visual steps"""
        steps = [
            ("Generating secure entropy...", 0.2),
            ("Creating mnemonic seed phrase...", 0.4),
            ("Deriving master key...", 0.6),
            ("Generating key pair...", 0.8),
            ("Creating Bitcoin address...", 1.0),
        ]

        for status, progress in steps:
            self.after(0, lambda s=status, p=progress: self._update_generation_status(s, p))
            time.sleep(0.5)

        # Generate the actual wallet
        self.current_wallet = self.wallet_generator.generate_wallet()

        # Show confirmation view
        self.after(0, self._show_wallet_confirmation)

    def _update_generation_status(self, status: str, progress: float):
        """Update generation status display"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=status)
        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(progress)

    def _show_wallet_confirmation(self):
        """Show wallet confirmation screen"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.current_wallet:
            return

        # Scrollable container
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, pady=SPACING["md"])
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Success icon
        success_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        success_frame.pack(pady=(0, SPACING["lg"]))

        success_icon = ctk.CTkLabel(
            success_frame,
            text="✅",
            font=("Segoe UI", 48)
        )
        success_icon.pack()

        success_label = ctk.CTkLabel(
            success_frame,
            text="Wallet Generated Successfully!",
            font=FONTS["heading"],
            text_color=COLORS["accent_green"]
        )
        success_label.pack(pady=SPACING["sm"])

        # Wallet details card
        details_card = ctk.CTkFrame(scroll_frame, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])
        details_card.pack(fill="x", pady=SPACING["md"], padx=SPACING["xl"])

        details_inner = ctk.CTkFrame(details_card, fg_color="transparent")
        details_inner.pack(padx=SPACING["lg"], pady=SPACING["lg"], fill="x")

        # Bitcoin Address
        self._create_detail_row(details_inner, "Bitcoin Address", self.current_wallet.address, copyable=True)

        # Public Key (truncated)
        pub_key_display = f"{self.current_wallet.public_key[:32]}..."
        self._create_detail_row(details_inner, "Public Key", pub_key_display)

        # Mnemonic card with warning
        mnemonic_card = ctk.CTkFrame(scroll_frame, fg_color=COLORS["bg_card"], corner_radius=DIMENSIONS["border_radius"])
        mnemonic_card.pack(fill="x", pady=SPACING["md"], padx=SPACING["xl"])

        mnemonic_inner = ctk.CTkFrame(mnemonic_card, fg_color="transparent")
        mnemonic_inner.pack(padx=SPACING["lg"], pady=SPACING["lg"], fill="x")

        # Warning header
        warning_frame = ctk.CTkFrame(mnemonic_inner, fg_color=COLORS["warning"], corner_radius=6)
        warning_frame.pack(fill="x", pady=(0, SPACING["md"]))

        warning_label = ctk.CTkLabel(
            warning_frame,
            text="⚠️  IMPORTANT: Write down these words and store them safely!",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"]
        )
        warning_label.pack(padx=SPACING["md"], pady=SPACING["sm"])

        # Mnemonic label
        mnemonic_title = ctk.CTkLabel(
            mnemonic_inner,
            text="Recovery Seed Phrase (12 words)",
            font=FONTS["subheading"],
            text_color=COLORS["text_primary"]
        )
        mnemonic_title.pack(anchor="w", pady=(0, SPACING["sm"]))

        # Mnemonic words grid
        words = self.current_wallet.mnemonic.split()
        words_frame = ctk.CTkFrame(mnemonic_inner, fg_color=COLORS["bg_light"], corner_radius=8)
        words_frame.pack(fill="x", pady=SPACING["sm"])

        words_inner = ctk.CTkFrame(words_frame, fg_color="transparent")
        words_inner.pack(padx=SPACING["md"], pady=SPACING["md"])

        # Display words in 3x4 grid
        for i, word in enumerate(words):
            row = i // 4
            col = i % 4

            word_frame = ctk.CTkFrame(words_inner, fg_color="transparent")
            word_frame.grid(row=row, column=col, padx=SPACING["sm"], pady=SPACING["xs"])

            num_label = ctk.CTkLabel(
                word_frame,
                text=f"{i+1}.",
                font=FONTS["mono_small"],
                text_color=COLORS["text_muted"],
                width=25
            )
            num_label.pack(side="left")

            word_label = ctk.CTkLabel(
                word_frame,
                text=word,
                font=FONTS["mono"],
                text_color=COLORS["bitcoin_orange"]
            )
            word_label.pack(side="left")

        # Confirmation checkbox
        self.confirm_var = ctk.BooleanVar(value=False)

        confirm_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        confirm_frame.pack(pady=SPACING["lg"])

        confirm_check = ctk.CTkCheckBox(
            confirm_frame,
            text="I have securely saved my recovery seed phrase",
            font=FONTS["body"],
            text_color=COLORS["text_primary"],
            fg_color=COLORS["bitcoin_orange"],
            hover_color="#e8850f",
            variable=self.confirm_var,
            command=self._toggle_confirm_button
        )
        confirm_check.pack()

        # Button frame
        btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        btn_frame.pack(pady=SPACING["lg"])

        # Generate new button
        regenerate_btn = ctk.CTkButton(
            btn_frame,
            text="↻ Generate New",
            font=FONTS["body"],
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["bg_medium"],
            text_color=COLORS["text_primary"],
            width=140,
            height=DIMENSIONS["button_height"],
            command=self._generate_wallet
        )
        regenerate_btn.pack(side="left", padx=(0, SPACING["md"]))

        # Confirm button
        self.confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm & Continue →",
            font=FONTS["body_bold"],
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["bg_light"],
            text_color=COLORS["text_muted"],
            width=180,
            height=DIMENSIONS["button_height"],
            state="disabled",
            command=self._confirm_wallet
        )
        self.confirm_btn.pack(side="left")

    def _create_detail_row(self, parent, label: str, value: str, copyable: bool = False):
        """Create a detail row with label and value"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=SPACING["sm"])

        label_widget = ctk.CTkLabel(
            row_frame,
            text=label,
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"]
        )
        label_widget.pack(anchor="w")

        value_frame = ctk.CTkFrame(row_frame, fg_color=COLORS["bg_light"], corner_radius=6)
        value_frame.pack(fill="x", pady=(SPACING["xs"], 0))

        value_label = ctk.CTkLabel(
            value_frame,
            text=value,
            font=FONTS["mono"],
            text_color=COLORS["text_primary"]
        )
        value_label.pack(side="left", padx=SPACING["sm"], pady=SPACING["sm"])

        if copyable:
            copy_btn = ctk.CTkButton(
                value_frame,
                text="📋",
                font=("Segoe UI", 14),
                fg_color="transparent",
                hover_color=COLORS["bg_medium"],
                width=30,
                height=30,
                command=lambda: self._copy_to_clipboard(value)
            )
            copy_btn.pack(side="right", padx=SPACING["xs"])

    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)

    def _toggle_confirm_button(self):
        """Toggle confirm button state based on checkbox"""
        if self.confirm_var.get():
            self.confirm_btn.configure(
                fg_color=COLORS["bitcoin_orange"],
                hover_color="#e8850f",
                text_color=COLORS["bg_dark"],
                state="normal"
            )
        else:
            self.confirm_btn.configure(
                fg_color=COLORS["bg_light"],
                hover_color=COLORS["bg_light"],
                text_color=COLORS["text_muted"],
                state="disabled"
            )

    def _confirm_wallet(self):
        """Confirm wallet and proceed"""
        if self.current_wallet:
            self.wallet_generator.confirm_wallet()
            self.on_wallet_confirmed(self.current_wallet)

    def _import_wallet(self):
        """Import existing wallet by address"""
        address = self.address_entry.get().strip()

        if not address:
            self._show_error("Please enter a Bitcoin address")
            return

        if not self.wallet_generator.validate_address(address):
            self._show_error("Invalid Bitcoin address format")
            return

        # Create wallet info for imported address
        self.current_wallet = WalletInfo(
            address=address,
            private_key="[Imported - Not Available]",
            public_key="[Imported - Not Available]",
            mnemonic="[Imported Wallet]",
            confirmed=True
        )

        self.on_wallet_confirmed(self.current_wallet)

    def _show_error(self, message: str):
        """Show error message"""
        # Simple error display - could be enhanced with a popup
        if hasattr(self, 'address_entry'):
            self.address_entry.configure(border_color=COLORS["error"])
