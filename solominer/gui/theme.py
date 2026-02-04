"""
Theme configuration for SoloMiner GUI
Beautiful dark theme with Bitcoin orange accents
"""

# Color Palette
COLORS = {
    # Primary colors
    "bg_dark": "#0d1117",
    "bg_medium": "#161b22",
    "bg_light": "#21262d",
    "bg_card": "#1c2128",

    # Accent colors
    "bitcoin_orange": "#f7931a",
    "bitcoin_gold": "#ffd700",
    "accent_blue": "#58a6ff",
    "accent_green": "#3fb950",
    "accent_red": "#f85149",
    "accent_purple": "#a371f7",
    "accent_cyan": "#39c5cf",

    # Text colors
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "text_muted": "#6e7681",

    # Border colors
    "border": "#30363d",
    "border_highlight": "#f7931a",

    # Status colors
    "success": "#238636",
    "warning": "#9e6a03",
    "error": "#da3633",
    "info": "#1f6feb",

    # Hash visualization colors
    "hash_zero": "#3fb950",
    "hash_normal": "#8b949e",
}

# Font configurations
FONTS = {
    "heading_large": ("Segoe UI", 28, "bold"),
    "heading": ("Segoe UI", 20, "bold"),
    "subheading": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "mono": ("Consolas", 11),
    "mono_large": ("Consolas", 14),
    "mono_small": ("Consolas", 9),
}

# Spacing
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48,
}

# Widget dimensions
DIMENSIONS = {
    "button_width": 200,
    "button_height": 45,
    "input_height": 40,
    "card_padding": 20,
    "border_radius": 8,
}

# Animation timings (ms)
ANIMATIONS = {
    "fast": 150,
    "normal": 300,
    "slow": 500,
}


def get_button_style(variant: str = "primary") -> dict:
    """Get button style configuration"""
    styles = {
        "primary": {
            "fg_color": COLORS["bitcoin_orange"],
            "hover_color": "#e8850f",
            "text_color": COLORS["bg_dark"],
        },
        "secondary": {
            "fg_color": COLORS["bg_light"],
            "hover_color": COLORS["bg_medium"],
            "text_color": COLORS["text_primary"],
        },
        "success": {
            "fg_color": COLORS["success"],
            "hover_color": "#2ea043",
            "text_color": COLORS["text_primary"],
        },
        "danger": {
            "fg_color": COLORS["error"],
            "hover_color": "#b62324",
            "text_color": COLORS["text_primary"],
        },
    }
    return styles.get(variant, styles["primary"])


def get_card_style() -> dict:
    """Get card/frame style configuration"""
    return {
        "fg_color": COLORS["bg_card"],
        "border_color": COLORS["border"],
        "corner_radius": DIMENSIONS["border_radius"],
    }
