"""Destination Discovery & Exploration View."""

from typing import Callable, Any, Optional
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_BURGUNDY,
    COLOR_BURGUNDY_HOVER,
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


class ExploreView(ctk.CTkFrame):
    """Destination Discovery screen with integrated search, category chips, and responsive grid."""

    CATEGORIES = ["All", "Landmarks", "Museums", "Parks", "Food & Markets", "Shopping", "Hidden Gems"]

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        open_detail_callback: Callable[[str], None],
        initial_category: Optional[str] = "All",
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, **kwargs)
        self.data_manager = data_manager
        self.open_detail = open_detail_callback
        self.current_category = initial_category or "All"
        self.current_query = ""

        self.category_buttons = {}

        self._build_ui()
        self._refresh_destinations()

    def _build_ui(self) -> None:
        # Top Header Bar (Fixed at top)
        header_bar = ctk.CTkFrame(self, fg_color="transparent")
        header_bar.pack(fill="x", padx=35, pady=(25, 15))

        title = ctk.CTkLabel(
            header_bar,
            text="EXPLORE LONDON",
            font=get_font(size=26, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header_bar,
            text="Discover iconic landmarks, secret courtyards, vibrant markets, and world-class museums.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(anchor="w", pady=(2, 14))

        # Search Bar & Filter Controls Row
        controls_frame = ctk.CTkFrame(header_bar, fg_color="transparent")
        controls_frame.pack(fill="x")

        # Search Entry with icon styling
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)

        search_entry = ctk.CTkEntry(
            controls_frame,
            textvariable=self.search_var,
            placeholder_text="Search London destinations...",
            font=get_font(size=14),
            fg_color=COLOR_WHITE,
            text_color=COLOR_DARK_TEXT,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=8,
            height=42,
            width=360
        )
        search_entry.pack(side="left", padx=(0, 15))

        # Category Filter Chips Frame (horizontal scrollable or clean pack)
        chips_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        chips_frame.pack(side="left", fill="x", expand=True)

        for cat in self.CATEGORIES:
            is_active = (cat.lower() == self.current_category.lower())
            btn = ctk.CTkButton(
                chips_frame,
                text=cat,
                font=get_font(size=12, weight="bold"),
                fg_color=COLOR_BURGUNDY if is_active else COLOR_WHITE,
                hover_color=COLOR_BURGUNDY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_NAVY,
                border_width=1,
                border_color=COLOR_BURGUNDY if is_active else COLOR_BORDER,
                height=34,
                corner_radius=17,
                command=lambda c=cat: self._set_category(c)
            )
            btn.pack(side="left", padx=4)
            self.category_buttons[cat] = btn

        # Result count label
        self.count_lbl = ctk.CTkLabel(
            header_bar,
            text="",
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_GOLD
        )
        self.count_lbl.pack(anchor="w", pady=(10, 0))

        # Scrollable Destination Grid Container
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=35, pady=(5, 25))

        # We configure 3 columns for responsiveness
        for col in range(3):
            self.scroll_area.grid_columnconfigure(col, weight=1, uniform="explore_col")

    def _set_category(self, category: str) -> None:
        self.current_category = category
        # Update chip styling
        for cat, btn in self.category_buttons.items():
            if cat.lower() == category.lower():
                btn.configure(
                    fg_color=COLOR_BURGUNDY,
                    text_color=COLOR_WHITE,
                    border_color=COLOR_BURGUNDY,
                    hover_color=COLOR_BURGUNDY_HOVER
                )
            else:
                btn.configure(
                    fg_color=COLOR_WHITE,
                    text_color=COLOR_NAVY,
                    border_color=COLOR_BORDER,
                    hover_color=COLOR_LIGHT_GREY
                )
        self._refresh_destinations()

    def _on_search_change(self, *args) -> None:
        self.current_query = self.search_var.get()
        self._refresh_destinations()

    def _refresh_destinations(self) -> None:
        # Clear existing card widgets
        for widget in self.scroll_area.winfo_children():
            widget.destroy()

        results = self.data_manager.search_destinations(
            query=self.current_query,
            category=self.current_category
        )

        total_count = len(results)
        self.count_lbl.configure(text=f"Showing {total_count} Destination{'s' if total_count != 1 else ''}")

        if not results:
            # Empty State
            empty_box = ctk.CTkFrame(self.scroll_area, fg_color=COLOR_CARD_BG, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
            empty_box.grid(row=0, column=0, columnspan=3, sticky="ew", pady=40, padx=20)

            ctk.CTkLabel(
                empty_box,
                text="🔍 No London Destinations Found",
                font=get_font(size=18, weight="bold", serif=True),
                text_color=COLOR_NAVY
            ).pack(pady=(30, 8))

            ctk.CTkLabel(
                empty_box,
                text=f"No results matched '{self.current_query}' in '{self.current_category}'.\nTry searching for 'market', 'thames', 'parliament', or select 'All'.",
                font=get_font(size=14),
                text_color=COLOR_MUTED_TEXT,
                justify="center"
            ).pack(pady=(0, 20))

            ctk.CTkButton(
                empty_box,
                text="Reset Search & Filters",
                font=get_font(size=13, weight="bold"),
                fg_color=COLOR_NAVY,
                text_color=COLOR_WHITE,
                hover_color=COLOR_NAVY_HOVER,
                height=36,
                command=self._reset_filters
            ).pack(pady=(0, 30))
            return

        # Render cards in 3 columns
        for idx, dest in enumerate(results):
            row = idx // 3
            col = idx % 3
            self._render_card(dest, row, col)

    def _reset_filters(self) -> None:
        self.search_var.set("")
        self._set_category("All")

    def _render_card(self, dest: dict, row: int, col: int) -> None:
        card = ctk.CTkFrame(
            self.scroll_area,
            fg_color=COLOR_CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        # Image Banner
        card_img = ImageManager.get_image(
            filename=dest.get("image_file", "london_hero.jpg"),
            width=300,
            height=165,
            fallback_title=dest.get("name", "London")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=card_img, corner_radius=10)
        img_lbl.pack(fill="x", padx=10, pady=(10, 8))

        # Details body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Meta tags row (Category + Duration)
        meta_row = ctk.CTkFrame(body, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 4))

        cat_tag = ctk.CTkLabel(
            meta_row,
            text=dest.get("category", "Landmark"),
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_BURGUNDY,
            fg_color=COLOR_TAG_BG,
            corner_radius=4,
            padx=6,
            pady=2
        )
        cat_tag.pack(side="left")

        dur_tag = ctk.CTkLabel(
            meta_row,
            text=f"⏱ {dest.get('duration', '1 - 2 hrs')}",
            font=get_font(size=11),
            text_color=COLOR_MUTED_TEXT
        )
        dur_tag.pack(side="right")

        # Name
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
            text=f"📍 {dest.get('neighbourhood', 'Central London')}",
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
        bottom_row = ctk.CTkFrame(body, fg_color="transparent")
        bottom_row.pack(fill="x", side="bottom")

        details_btn = ctk.CTkButton(
            bottom_row,
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

        # Favourite Toggle Heart Button
        is_fav = self.data_manager.is_favourite(dest.get("id"))
        fav_btn = ctk.CTkButton(
            bottom_row,
            text="❤️" if is_fav else "🤍",
            width=38,
            height=34,
            fg_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_BORDER,
            text_color=COLOR_BURGUNDY,
            corner_radius=6
        )
        fav_btn.configure(command=lambda d_id=dest.get("id"), btn=fav_btn: self._toggle_fav(d_id, btn))
        fav_btn.pack(side="right")

    def _toggle_fav(self, dest_id: str, button: ctk.CTkButton) -> None:
        new_status = self.data_manager.toggle_favourite(dest_id)
        button.configure(text="❤️" if new_status else "🤍")
