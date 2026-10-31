"""Hidden Gems View ("BEYOND THE POSTCARDS") with an asymmetrical editorial layout."""

from typing import Callable, Any
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_GOLD_LIGHT,
    COLOR_WHITE,
    COLOR_LIGHT_GREY,
    COLOR_BORDER,
    COLOR_DARK_TEXT,
    COLOR_MUTED_TEXT,
    COLOR_CARD_BG,
    COLOR_TAG_BG,
    get_font
)
from app.image_manager import ImageManager


class HiddenGemsView(ctk.CTkScrollableFrame):
    """Magazine editorial presentation of London's secret and lesser-known treasures."""

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        open_detail_callback: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager
        self.open_detail = open_detail_callback

        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=25)

        # 1. Editorial Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))

        pre_badge = ctk.CTkLabel(
            header,
            text="✦ SECRET SANCTUARIES & UNTOLD CORNERS ✦",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_BURGUNDY
        )
        pre_badge.pack(anchor="w")

        title = ctk.CTkLabel(
            header,
            text="BEYOND THE POSTCARDS",
            font=get_font(size=32, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(anchor="w", pady=(4, 6))

        subtitle = ctk.CTkLabel(
            header,
            text="Discover another side of London through its colourful corners, quiet canals, historic markets, and beautiful green spaces.",
            font=get_font(size=15),
            text_color=COLOR_MUTED_TEXT,
            wraplength=780,
            justify="left"
        )
        subtitle.pack(anchor="w")

        # 2. Hero Editorial Spotlight: Neal's Yard (Large asymmetric feature)
        neals_dest = self.data_manager.get_destination_by_id("neals_yard")
        if neals_dest:
            self._build_spotlight_feature(container, neals_dest)

        # 3. Two-Column Asymmetric Duo: Little Venice & Leadenhall Market
        duo_frame = ctk.CTkFrame(container, fg_color="transparent")
        duo_frame.pack(fill="x", pady=(0, 25))

        duo_frame.grid_columnconfigure(0, weight=1)
        duo_frame.grid_columnconfigure(1, weight=1)

        venice_dest = self.data_manager.get_destination_by_id("little_venice")
        leadenhall_dest = self.data_manager.get_destination_by_id("leadenhall_market")

        if venice_dest:
            self._build_duo_card(duo_frame, venice_dest, col=0)
        if leadenhall_dest:
            self._build_duo_card(duo_frame, leadenhall_dest, col=1)

        # 4. Wide Panorama Feature: Hampstead Heath
        heath_dest = self.data_manager.get_destination_by_id("hampstead_heath")
        if heath_dest:
            self._build_panorama_feature(container, heath_dest)

        # Bottom spacer
        ctk.CTkFrame(container, fg_color="transparent", height=40).pack()

    def _build_spotlight_feature(self, parent: ctk.CTkFrame, dest: dict) -> None:
        """Asymmetric wide spotlight card with large image on left, rich story on right."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", pady=(0, 25))

        card.grid_columnconfigure(0, weight=5)
        card.grid_columnconfigure(1, weight=6)

        # Left: Large Photograph
        card_img = ImageManager.get_image(
            filename=dest.get("image_file", "neals_yard.jpg"),
            width=420,
            height=280,
            fallback_title=dest.get("name")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=card_img, corner_radius=12)
        img_lbl.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        # Right: Story panel
        story = ctk.CTkFrame(card, fg_color="transparent")
        story.grid(row=0, column=1, sticky="nsew", padx=(10, 24), pady=24)

        tag = ctk.CTkLabel(
            story,
            text="💎 EDITORIAL SPOTLIGHT • COVENT GARDEN",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_BURGUNDY
        )
        tag.pack(anchor="w")

        title = ctk.CTkLabel(
            story,
            text=dest.get("name", "Neal's Yard"),
            font=get_font(size=24, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(anchor="w", pady=(4, 8))

        desc = ctk.CTkLabel(
            story,
            text=dest.get("short_description", "") + "\n\n" + (dest.get("why_famous", "")),
            font=get_font(size=13),
            text_color=COLOR_DARK_TEXT,
            wraplength=440,
            justify="left"
        )
        desc.pack(anchor="w", pady=(0, 16))

        # Bottom row: Duration and View button
        row = ctk.CTkFrame(story, fg_color="transparent")
        row.pack(fill="x", side="bottom")

        dur_lbl = ctk.CTkLabel(
            row,
            text=f"⏱ {dest.get('duration', '1 hour')} • Free Entry",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        )
        dur_lbl.pack(side="left")

        explore_btn = ctk.CTkButton(
            row,
            text="Read Full Story →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=lambda: self.open_detail(dest.get("id"))
        )
        explore_btn.pack(side="right")

    def _build_duo_card(self, parent: ctk.CTkFrame, dest: dict, col: int) -> None:
        """Card for the two-column asymmetric layout."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=0, column=col, sticky="nsew", padx=10, pady=0)

        # Image
        img = ImageManager.get_image(
            filename=dest.get("image_file", "london_hero.jpg"),
            width=430,
            height=200,
            fallback_title=dest.get("name")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=img, corner_radius=10)
        img_lbl.pack(fill="x", padx=12, pady=(12, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        nh_tag = ctk.CTkLabel(
            content,
            text=f"📍 {dest.get('neighbourhood')}",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_GOLD
        )
        nh_tag.pack(anchor="w")

        name = ctk.CTkLabel(
            content,
            text=dest.get("name"),
            font=get_font(size=18, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        name.pack(anchor="w", pady=(2, 6))

        desc = ctk.CTkLabel(
            content,
            text=dest.get("short_description"),
            font=get_font(size=13),
            text_color=COLOR_MUTED_TEXT,
            wraplength=400,
            justify="left"
        )
        desc.pack(anchor="w", pady=(0, 14))

        # Bottom row
        bottom = ctk.CTkFrame(content, fg_color="transparent")
        bottom.pack(fill="x", side="bottom")

        btn = ctk.CTkButton(
            bottom,
            text="Discover Secrets →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_TAG_BG,
            hover_color=COLOR_LIGHT_GREY,
            text_color=COLOR_BURGUNDY,
            height=32,
            corner_radius=6,
            command=lambda: self.open_detail(dest.get("id"))
        )
        btn.pack(side="right")

    def _build_panorama_feature(self, parent: ctk.CTkFrame, dest: dict) -> None:
        """Wide full-width panorama card with landscape photography and panoramic quote."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_NAVY,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x")

        # Top wide image
        pano_img = ImageManager.get_image(
            filename=dest.get("image_file", "hampstead_heath.jpg"),
            width=920,
            height=260,
            fallback_title=dest.get("name")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=pano_img, corner_radius=14)
        img_lbl.pack(fill="x", padx=14, pady=(14, 12))

        # Description bar
        desc_bar = ctk.CTkFrame(card, fg_color="transparent")
        desc_bar.pack(fill="x", padx=24, pady=(0, 20))

        title = ctk.CTkLabel(
            desc_bar,
            text=f"✦ {dest.get('name')} ✦",
            font=get_font(size=20, weight="bold", serif=True),
            text_color=COLOR_WHITE
        )
        title.pack(anchor="w")

        quote_text = (
            f"\"{dest.get('short_description')}\" — "
            "A wild 800-acre sanctuary protecting London's most breathtaking skyline vantage point from Parliament Hill."
        )
        quote_lbl = ctk.CTkLabel(
            desc_bar,
            text=quote_text,
            font=get_font(size=13),
            text_color=COLOR_LIGHT_GREY,
            wraplength=860,
            justify="left"
        )
        quote_lbl.pack(anchor="w", pady=(6, 12))

        btn = ctk.CTkButton(
            desc_bar,
            text="Explore Hampstead Heath",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_LIGHT,
            text_color=COLOR_NAVY,
            height=34,
            corner_radius=6,
            command=lambda: self.open_detail(dest.get("id"))
        )
        btn.pack(anchor="w")
