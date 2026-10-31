"""Saved Places (Favourites) View."""

from typing import Callable, Any
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_BURGUNDY,
    COLOR_GOLD,
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


class FavouritesView(ctk.CTkFrame):
    """View displaying saved favourite destinations with removal & detail viewing."""

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        navigate_callback: Callable[[str, Any], None],
        open_detail_callback: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, **kwargs)
        self.data_manager = data_manager
        self.navigate = navigate_callback
        self.open_detail = open_detail_callback

        self._build_ui()
        self._refresh_favourites()

    def _build_ui(self) -> None:
        # Header bar
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(25, 15))

        title = ctk.CTkLabel(
            header,
            text="SAVED PLACES",
            font=get_font(size=26, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Your curated personal collection of London landmarks, markets, and hidden gems.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(anchor="w", pady=(2, 8))

        self.count_lbl = ctk.CTkLabel(
            header,
            text="",
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_GOLD
        )
        self.count_lbl.pack(anchor="w")

        # Scrollable grid container
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=35, pady=(10, 25))

        for col in range(3):
            self.scroll_area.grid_columnconfigure(col, weight=1, uniform="fav_col")

    def _refresh_favourites(self) -> None:
        for widget in self.scroll_area.winfo_children():
            widget.destroy()

        fav_dests = self.data_manager.get_favourite_destinations()
        total = len(fav_dests)
        self.count_lbl.configure(text=f"{total} Saved Destination{'s' if total != 1 else ''}")

        if not fav_dests:
            # Welcoming empty state as specified in Section 13
            empty_card = ctk.CTkFrame(
                self.scroll_area,
                fg_color=COLOR_CARD_BG,
                corner_radius=16,
                border_width=1,
                border_color=COLOR_BORDER
            )
            empty_card.grid(row=0, column=0, columnspan=3, sticky="ew", pady=50, padx=20)

            ctk.CTkLabel(
                empty_card,
                text="🤍",
                font=get_font(size=42)
            ).pack(pady=(35, 10))

            ctk.CTkLabel(
                empty_card,
                text="Your London collection starts here.",
                font=get_font(size=22, weight="bold", serif=True),
                text_color=COLOR_NAVY
            ).pack(pady=(0, 8))

            ctk.CTkLabel(
                empty_card,
                text="As you explore London's sights, click the heart icon on any card\nto save places to your personal travel wishlist.",
                font=get_font(size=14),
                text_color=COLOR_MUTED_TEXT,
                justify="center"
            ).pack(pady=(0, 25))

            ctk.CTkButton(
                empty_card,
                text="EXPLORE LONDON DESTINATIONS",
                font=get_font(size=13, weight="bold"),
                fg_color=COLOR_BURGUNDY,
                hover_color=COLOR_BURGUNDY_HOVER,
                text_color=COLOR_WHITE,
                height=42,
                corner_radius=8,
                command=lambda: self.navigate("explore", "All")
            ).pack(pady=(0, 35))
            return

        for idx, dest in enumerate(fav_dests):
            row = idx // 3
            col = idx % 3
            self._render_card(dest, row, col)

    def _render_card(self, dest: dict, row: int, col: int) -> None:
        card = ctk.CTkFrame(
            self.scroll_area,
            fg_color=COLOR_CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        # Image thumbnail
        card_img = ImageManager.get_image(
            filename=dest.get("image_file", "london_hero.jpg"),
            width=300,
            height=165,
            fallback_title=dest.get("name", "London")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=card_img, corner_radius=10)
        img_lbl.pack(fill="x", padx=10, pady=(10, 8))

        # Details
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Category and duration tags
        meta_row = ctk.CTkFrame(body, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(
            meta_row,
            text=dest.get("category", "Landmark"),
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_BURGUNDY,
            fg_color=COLOR_TAG_BG,
            corner_radius=4,
            padx=6,
            pady=2
        ).pack(side="left")

        ctk.CTkLabel(
            meta_row,
            text=f"⏱ {dest.get('duration', '1 - 2 hrs')}",
            font=get_font(size=11),
            text_color=COLOR_MUTED_TEXT
        ).pack(side="right")

        # Title
        name_lbl = ctk.CTkLabel(
            body,
            text=dest.get("name", ""),
            font=get_font(size=15, weight="bold", serif=True),
            text_color=COLOR_NAVY,
            wraplength=270,
            justify="left"
        )
        name_lbl.pack(anchor="w", pady=(4, 2))

        # Neighbourhood
        nh_lbl = ctk.CTkLabel(
            body,
            text=f"📍 {dest.get('neighbourhood', 'London')}",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        )
        nh_lbl.pack(anchor="w", pady=(0, 6))

        # Short description
        desc_text = dest.get("short_description", "")
        if len(desc_text) > 95:
            desc_text = desc_text[:92] + "..."
        desc_lbl = ctk.CTkLabel(
            body,
            text=desc_text,
            font=get_font(size=12),
            text_color=COLOR_MUTED_TEXT,
            wraplength=270,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 14))

        # Bottom Action Bar
        bottom = ctk.CTkFrame(body, fg_color="transparent")
        bottom.pack(fill="x", side="bottom")

        details_btn = ctk.CTkButton(
            bottom,
            text="Explore Details →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=lambda d_id=dest.get("id"): self.open_detail(d_id)
        )
        details_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Remove favourite button
        remove_btn = ctk.CTkButton(
            bottom,
            text="Remove",
            font=get_font(size=11),
            fg_color=COLOR_LIGHT_GREY,
            hover_color="#FFEEEE",
            text_color="#C0392B",
            height=34,
            width=70,
            corner_radius=6,
            command=lambda d_id=dest.get("id"): self._remove_fav(d_id)
        )
        remove_btn.pack(side="right")

    def _remove_fav(self, dest_id: str) -> None:
        self.data_manager.remove_favourite(dest_id)
        self._refresh_favourites()
