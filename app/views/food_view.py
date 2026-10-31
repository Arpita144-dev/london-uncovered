"""London Food Guide View ("A TASTE OF LONDON")."""

from typing import Callable, Any
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


class FoodView(ctk.CTkScrollableFrame):
    """The gastronomic exploration screen for London's culinary traditions."""

    FOOD_CATEGORIES = [
        "All",
        "Traditional British Food",
        "Afternoon Tea",
        "Street Food",
        "International Cuisine",
        "Bakeries & Cafés",
        "Food Markets"
    ]

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        navigate_callback: Callable[[str, Any], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager
        self.navigate = navigate_callback
        self.active_category = "All"
        self.cat_buttons = {}

        self._build_ui()

    def _build_ui(self) -> None:
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=25)

        # Header
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header,
            text="CULINARY HERITAGE & MODERN DINING",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="A TASTE OF LONDON",
            font=get_font(size=28, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(4, 6))

        ctk.CTkLabel(
            header,
            text="From 19th-century afternoon tea rituals and sizzling historic food markets to vibrant Chinatown dumplings and artisan bakeries.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        ).pack(anchor="w")

        # Category Filter Bar (horizontal chips)
        chips_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        chips_frame.pack(fill="x", pady=(15, 20))

        for cat in self.FOOD_CATEGORIES:
            is_active = (cat == self.active_category)
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
                command=lambda c=cat: self._filter_food(c)
            )
            btn.pack(side="left", padx=4, pady=2)
            self.cat_buttons[cat] = btn

        # Food Cards Container (2 columns)
        self.grid_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.grid_frame.pack(fill="x")

        self.grid_frame.grid_columnconfigure(0, weight=1, uniform="food_col")
        self.grid_frame.grid_columnconfigure(1, weight=1, uniform="food_col")

        self._render_food_cards()

        # Bottom spacer
        ctk.CTkFrame(self.container, fg_color="transparent", height=40).pack()

    def _filter_food(self, category: str) -> None:
        self.active_category = category
        for cat, btn in self.cat_buttons.items():
            if cat == category:
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
        self._render_food_cards()

    def _render_food_cards(self) -> None:
        for w in self.grid_frame.winfo_children():
            w.destroy()

        all_food = self.data_manager.get_food_guide()
        filtered = [f for f in all_food if self.active_category == "All" or f.get("category") == self.active_category]

        for idx, item in enumerate(filtered):
            row = idx // 2
            col = idx % 2
            self._render_single_food_card(self.grid_frame, item, row, col)

    def _render_single_food_card(self, parent: ctk.CTkFrame, item: dict, row: int, col: int) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Photo
        img = ImageManager.get_image(
            filename=item.get("image_file", "borough_market.jpg"),
            width=430,
            height=200,
            fallback_title=item.get("name")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=img, corner_radius=10)
        img_lbl.pack(fill="x", padx=12, pady=(12, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Category Badge
        cat_badge = ctk.CTkLabel(
            content,
            text=f"🍴 {item.get('category')}",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_BURGUNDY,
            fg_color=COLOR_TAG_BG,
            corner_radius=4,
            padx=8,
            pady=2
        )
        cat_badge.pack(anchor="w")

        # Name
        name_lbl = ctk.CTkLabel(
            content,
            text=item.get("name"),
            font=get_font(size=18, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        name_lbl.pack(anchor="w", pady=(4, 6))

        # Description
        desc_lbl = ctk.CTkLabel(
            content,
            text=item.get("description"),
            font=get_font(size=13),
            text_color=COLOR_DARK_TEXT,
            wraplength=400,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 10))

        # Signature Dishes Box
        dishes_box = ctk.CTkFrame(content, fg_color=COLOR_TAG_BG, corner_radius=6)
        dishes_box.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            dishes_box,
            text="Signature Dishes to Try:",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_NAVY
        ).pack(anchor="w", padx=10, pady=(6, 2))

        for dish in item.get("signature_dishes", [])[:3]:
            ctk.CTkLabel(
                dishes_box,
                text=f"• {dish}",
                font=get_font(size=12),
                text_color=COLOR_DARK_TEXT,
                wraplength=380,
                justify="left"
            ).pack(anchor="w", padx=14, pady=1)
        ctk.CTkFrame(dishes_box, fg_color="transparent", height=6).pack()

        # Where to try callout
        where_lbl = ctk.CTkLabel(
            content,
            text=f"📍 Where: {item.get('where_to_try')}",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        )
        where_lbl.pack(anchor="w", pady=(0, 10))

        # Bottom Button to Explore Related Food Destinations
        explore_btn = ctk.CTkButton(
            content,
            text="Explore London Food & Markets →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=lambda: self.navigate("explore", "Food & Markets")
        )
        explore_btn.pack(fill="x")
