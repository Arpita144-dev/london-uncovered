"""London Experiences View."""

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


class ExperiencesView(ctk.CTkScrollableFrame):
    """Four curated London experiences: Food & Cafés, Shopping, Culture, and Scenic London."""

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
            text="CURATED EXPERIENCES",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="THE LONDON EXPERIENCES",
            font=get_font(size=28, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(4, 6))

        ctk.CTkLabel(
            header,
            text="Immerse yourself in world-class theatre, historic tea salons, legendary shopping streets, and picturesque Thames walks.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        ).pack(anchor="w")

        # Experiences list (4 full-width editorial cards)
        experiences = self.data_manager.get_experiences()
        for exp in experiences:
            self._render_experience_card(container, exp)

        # Bottom spacer
        ctk.CTkFrame(container, fg_color="transparent", height=40).pack()

    def _render_experience_card(self, parent: ctk.CTkFrame, exp: dict) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", pady=(0, 25))

        card.grid_columnconfigure(0, weight=5)
        card.grid_columnconfigure(1, weight=7)

        # Left Image
        img = ImageManager.get_image(
            filename=exp.get("image_file", "london_hero.jpg"),
            width=380,
            height=260,
            fallback_title=exp.get("title")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=img, corner_radius=12)
        img_lbl.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        # Right Content Body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.grid(row=0, column=1, sticky="nsew", padx=(10, 24), pady=20)

        # Title
        title_lbl = ctk.CTkLabel(
            body,
            text=exp.get("title", "Experience"),
            font=get_font(size=22, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title_lbl.pack(anchor="w")

        tagline_lbl = ctk.CTkLabel(
            body,
            text=exp.get("tagline", ""),
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_BURGUNDY
        )
        tagline_lbl.pack(anchor="w", pady=(2, 6))

        desc_lbl = ctk.CTkLabel(
            body,
            text=exp.get("description", ""),
            font=get_font(size=13),
            text_color=COLOR_DARK_TEXT,
            wraplength=480,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 10))

        # Highlights chips / bullets
        hl_frame = ctk.CTkFrame(body, fg_color="transparent")
        hl_frame.pack(fill="x", pady=(0, 14))

        for hl in exp.get("highlights", [])[:3]:
            row = ctk.CTkFrame(hl_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row,
                text="✦",
                font=get_font(size=11, weight="bold"),
                text_color=COLOR_GOLD
            ).pack(side="left", padx=(0, 6))

            ctk.CTkLabel(
                row,
                text=hl,
                font=get_font(size=12),
                text_color=COLOR_MUTED_TEXT,
                wraplength=460,
                justify="left"
            ).pack(side="left")

        # Bottom Action Bar
        action_bar = ctk.CTkFrame(body, fg_color="transparent")
        action_bar.pack(fill="x", side="bottom")

        # Explore Button
        btn = ctk.CTkButton(
            action_bar,
            text=f"Explore {exp.get('title')} Places →",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=lambda cat=exp.get("title"): self._explore_category(cat)
        )
        btn.pack(side="left")

    def _explore_category(self, title: str) -> None:
        # Map experience category title to destination search category
        mapping = {
            "Food & Cafés": "Food & Markets",
            "Shopping & Markets": "Shopping",
            "Culture & Entertainment": "Museums",
            "Scenic London": "Landmarks"
        }
        dest_cat = mapping.get(title, "All")
        self.navigate("explore", dest_cat)
