"""London Neighbourhood Guide View."""

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


class NeighbourhoodView(ctk.CTkScrollableFrame):
    """Discovery screen for London's 8 distinct neighbourhoods."""

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        navigate_callback: Callable[[str, Any], None],
        open_detail_callback: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager
        self.navigate = navigate_callback
        self.open_detail = open_detail_callback

        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=25)

        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(
            header,
            text="THE BOROUGHS & DISTRICTS",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_BURGUNDY
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="LONDON NEIGHBOURHOOD GUIDE",
            font=get_font(size=28, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(4, 6))

        ctk.CTkLabel(
            header,
            text="From the regal avenues of Westminster to the colourful mews of Notting Hill and the street art alleys of Shoreditch.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        ).pack(anchor="w")

        # 2-Column Grid for the 8 Neighbourhoods
        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.pack(fill="x")

        grid.grid_columnconfigure(0, weight=1, uniform="nh_col")
        grid.grid_columnconfigure(1, weight=1, uniform="nh_col")

        neighbourhoods = self.data_manager.get_neighbourhoods()

        for idx, nh in enumerate(neighbourhoods):
            row = idx // 2
            col = idx % 2
            self._render_nh_card(grid, nh, row, col)

        # Bottom spacer
        ctk.CTkFrame(container, fg_color="transparent", height=40).pack()

    def _render_nh_card(self, parent: ctk.CTkFrame, nh: dict, row: int, col: int) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Top Photo
        img = ImageManager.get_image(
            filename=nh.get("image_file", "london_hero.jpg"),
            width=430,
            height=180,
            fallback_title=nh.get("name")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=img, corner_radius=10)
        img_lbl.pack(fill="x", padx=12, pady=(12, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Vibe tag
        vibe_lbl = ctk.CTkLabel(
            content,
            text=f"✨ {nh.get('vibe', 'London Vibe')}",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_GOLD
        )
        vibe_lbl.pack(anchor="w")

        # Name
        name_lbl = ctk.CTkLabel(
            content,
            text=nh.get("name", ""),
            font=get_font(size=20, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        name_lbl.pack(anchor="w", pady=(2, 6))

        # Description
        desc_lbl = ctk.CTkLabel(
            content,
            text=nh.get("description", ""),
            font=get_font(size=13),
            text_color=COLOR_DARK_TEXT,
            wraplength=400,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 8))

        # Famous for callout
        famous_frame = ctk.CTkFrame(content, fg_color=COLOR_TAG_BG, corner_radius=6)
        famous_frame.pack(fill="x", pady=(0, 12), padx=2)

        ctk.CTkLabel(
            famous_frame,
            text=f"🏛 Famous for: {nh.get('what_famous_for', '')}",
            font=get_font(size=12),
            text_color=COLOR_NAVY,
            wraplength=390,
            justify="left"
        ).pack(anchor="w", padx=10, pady=6)

        # Recommended destinations buttons row
        rec_frame = ctk.CTkFrame(content, fg_color="transparent")
        rec_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            rec_frame,
            text="Top Places:",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_MUTED_TEXT
        ).pack(side="left", padx=(0, 8))

        rec_ids = nh.get("recommended_destinations", [])
        for did in rec_ids[:3]:
            dest_obj = self.data_manager.get_destination_by_id(did)
            if dest_obj:
                d_btn = ctk.CTkButton(
                    rec_frame,
                    text=dest_obj.get("name").split()[0],  # Short 1-word label
                    font=get_font(size=11),
                    fg_color=COLOR_LIGHT_GREY,
                    hover_color=COLOR_BORDER,
                    text_color=COLOR_NAVY,
                    height=24,
                    corner_radius=4,
                    command=lambda d=did: self.open_detail(d)
                )
                d_btn.pack(side="left", padx=2)

        # Action: View all destinations in this neighbourhood
        nh_name = nh.get("name", "")
        filter_btn = ctk.CTkButton(
            content,
            text=f"Explore All in {nh_name} →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=lambda q=nh_name.split()[0]: self._filter_neighbourhood(q)
        )
        filter_btn.pack(fill="x")

    def _filter_neighbourhood(self, search_term: str) -> None:
        self.navigate("explore_search", search_term)
