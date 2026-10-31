"""London Practical Travel Tips View."""

from typing import Any
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
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


class TravelTipsView(ctk.CTkScrollableFrame):
    """Practical travel tips, transport secrets, and etiquette guidance for London visitors."""

    def __init__(self, master: Any, data_manager: Any, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager

        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=25)

        # Header Bar
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(
            header,
            text="ESSENTIAL VISITOR ADVICE",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_BURGUNDY
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="LONDON TRAVEL TIPS & INSIGHTS",
            font=get_font(size=28, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(4, 6))

        ctk.CTkLabel(
            header,
            text="Everything you need to navigate the Tube like a Londoner, discover world-class free museums, and prepare for British weather.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        ).pack(anchor="w")

        # Visual banner for the London Underground
        banner = ctk.CTkFrame(
            container,
            fg_color=COLOR_NAVY,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        banner.pack(fill="x", pady=(0, 25))

        banner.grid_columnconfigure(0, weight=7)
        banner.grid_columnconfigure(1, weight=4)

        b_text = ctk.CTkFrame(banner, fg_color="transparent")
        b_text.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        ctk.CTkLabel(
            b_text,
            text="🚇 LOCAL GOLDEN RULE: MIND THE GAP & STAND ON THE RIGHT",
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            b_text,
            text="The Golden Rule of London Transit",
            font=get_font(size=22, weight="bold", serif=True),
            text_color=COLOR_WHITE
        ).pack(anchor="w", pady=(4, 8))

        sub_desc = (
            "No matter how busy the station, always stand on the right side of escalator steps to let hurrying commuters pass on the left. "
            "Never stop right at the top of stairs or ticket barriers. Tap your phone or contactless card directly on yellow readers for the cheapest automatic daily fare cap!"
        )
        ctk.CTkLabel(
            b_text,
            text=sub_desc,
            font=get_font(size=13),
            text_color=COLOR_LIGHT_GREY,
            wraplength=520,
            justify="left"
        ).pack(anchor="w")

        # Right image
        tube_img = ImageManager.get_image(
            filename="tube_transport.jpg",
            width=280,
            height=160,
            fallback_title="London Underground"
        )
        img_lbl = ctk.CTkLabel(banner, text="", image=tube_img, corner_radius=10)
        img_lbl.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)

        # 2-Column Grid for the 8 Detailed Travel Tips Cards
        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.pack(fill="x")

        grid.grid_columnconfigure(0, weight=1, uniform="tips_col")
        grid.grid_columnconfigure(1, weight=1, uniform="tips_col")

        tips = self.data_manager.get_travel_tips()
        for idx, tip in enumerate(tips):
            row = idx // 2
            col = idx % 2
            self._render_tip_card(grid, tip, row, col)

        # Bottom spacer
        ctk.CTkFrame(container, fg_color="transparent", height=40).pack()

    def _render_tip_card(self, parent: ctk.CTkFrame, tip: dict, row: int, col: int) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with icon and category
        head_row = ctk.CTkFrame(content, fg_color="transparent")
        head_row.pack(fill="x", pady=(0, 4))

        icon_lbl = ctk.CTkLabel(
            head_row,
            text=tip.get("icon", "💡"),
            font=get_font(size=22)
        )
        icon_lbl.pack(side="left", padx=(0, 10))

        cat_lbl = ctk.CTkLabel(
            head_row,
            text=tip.get("category", "Advice").upper(),
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_BURGUNDY,
            fg_color=COLOR_TAG_BG,
            corner_radius=4,
            padx=8,
            pady=2
        )
        cat_lbl.pack(side="left")

        # Title
        title_lbl = ctk.CTkLabel(
            content,
            text=tip.get("title", ""),
            font=get_font(size=17, weight="bold", serif=True),
            text_color=COLOR_NAVY,
            wraplength=400,
            justify="left"
        )
        title_lbl.pack(anchor="w", pady=(6, 4))

        # Summary
        sum_lbl = ctk.CTkLabel(
            content,
            text=tip.get("summary", ""),
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD,
            wraplength=400,
            justify="left"
        )
        sum_lbl.pack(anchor="w", pady=(0, 10))

        # Bullet Tips
        for bullet in tip.get("tips", []):
            b_row = ctk.CTkFrame(content, fg_color="transparent")
            b_row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                b_row,
                text="•",
                font=get_font(size=14, weight="bold"),
                text_color=COLOR_BURGUNDY
            ).pack(side="left", anchor="n", padx=(0, 8))

            ctk.CTkLabel(
                b_row,
                text=bullet,
                font=get_font(size=12),
                text_color=COLOR_DARK_TEXT,
                wraplength=380,
                justify="left"
            ).pack(side="left", anchor="w")
