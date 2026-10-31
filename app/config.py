"""Application configuration, themes, styling constants and filesystem paths."""

from pathlib import Path
import customtkinter as ctk

# Base paths
APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"

# Ensure storage directory exists
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Brand strings
APP_NAME = "LONDON UNCOVERED"
TAGLINE = "Discover London, One Experience at a Time."
HERO_HEADLINE = "LONDON IS CALLING."
HERO_SUBTITLE = "Discover the city beyond the guidebooks."
FOOTER_TEXT = "Your personal guide to London."

# Color Palette (Strictly following the project specification)
COLOR_BG = "#F8F5EF"           # Background cream
COLOR_NAVY = "#142B3B"         # Deep navy
COLOR_NAVY_HOVER = "#1E3F57"   # Navy hover state
COLOR_NAVY_LIGHT = "#213D52"   # Elevated navy
COLOR_BURGUNDY = "#762E3D"     # Burgundy highlight
COLOR_BURGUNDY_HOVER = "#8E374A"
COLOR_GOLD = "#C5A46D"         # Muted gold accent
COLOR_GOLD_HOVER = "#D4B680"
COLOR_GOLD_LIGHT = "#F3EDE3"   # Soft gold tint for tags/chips
COLOR_WHITE = "#FFFFFF"        # Pure white
COLOR_LIGHT_GREY = "#E9E5DE"   # Light grey
COLOR_BORDER = "#DDD7CD"       # Soft border
COLOR_DARK_TEXT = "#292929"    # Dark primary text
COLOR_MUTED_TEXT = "#687076"   # Muted secondary text
COLOR_CARD_BG = "#FFFFFF"      # White card surface
COLOR_TAG_BG = "#F0ECE4"       # Soft background for badges

# Typography Helpers (Serif for headings, Sans-serif for UI/body)
FONT_SERIF = "Georgia"
FONT_SANS = "Helvetica Neue"

def get_font(size: int = 14, weight: str = "normal", serif: bool = False) -> ctk.CTkFont:
    family = FONT_SERIF if serif else FONT_SANS
    return ctk.CTkFont(family=family, size=size, weight=weight)
