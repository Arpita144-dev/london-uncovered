"""Home Dashboard View for London Uncovered."""

from typing import Callable, Any
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_BURGUNDY,
    COLOR_BURGUNDY_HOVER,
    COLOR_GOLD,
    COLOR_GOLD_HOVER,
    COLOR_WHITE,
    COLOR_LIGHT_GREY,
    COLOR_BORDER,
    COLOR_DARK_TEXT,
    COLOR_MUTED_TEXT,
    COLOR_CARD_BG,
    COLOR_TAG_BG,
    HERO_HEADLINE,
    HERO_SUBTITLE,
    get_font
)
from app.image_manager import ImageManager


class HomeView(ctk.CTkScrollableFrame):
    """The visual magazine-style landing dashboard."""

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
        # Outer padding container
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=35, pady=25)

        # 1. Hero Photographic Banner
        self._build_hero_panel(content)

        # 2. Section: Explore The City (Featured destination cards)
        self._build_featured_destinations(content)

        # 3. Section: Find Your London (Category discovery cards)
        self._build_category_showcase(content)

        # Bottom spacer
        ctk.CTkFrame(content, fg_color="transparent", height=40).pack()

    def _build_hero_panel(self, parent: ctk.CTkFrame) -> None:
        hero_frame = ctk.CTkFrame(
            parent,
            fg_color=COLOR_NAVY,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        hero_frame.pack(fill="x", pady=(0, 35))

        # Two-column layout: Left text & CTA, Right hero photograph
        hero_frame.grid_columnconfigure(0, weight=6)
        hero_frame.grid_columnconfigure(1, weight=5)

        # Left Column: Editorial Text & Buttons
        text_col = ctk.CTkFrame(hero_frame, fg_color="transparent")
        text_col.grid(row=0, column=0, sticky="nsew", padx=(40, 20), pady=40)

        # Crown / Badge
        badge = ctk.CTkLabel(
            text_col,
            text="✦ THE VISUAL TRAVEL GUIDE ✦",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        )
        badge.pack(anchor="w", pady=(0, 10))

        # Headline
        headline = ctk.CTkLabel(
            text_col,
            text=HERO_HEADLINE,
            font=get_font(size=36, weight="bold", serif=True),
            text_color=COLOR_WHITE
        )
        headline.pack(anchor="w", pady=(0, 12))

        # Subtitle
        sub_desc = (
            f"{HERO_SUBTITLE}\n"
            "Discover iconic landmarks, hidden streets, unforgettable food, "
            "and the timeless magic of London."
        )
        subtitle = ctk.CTkLabel(
            text_col,
            text=sub_desc,
            font=get_font(size=15),
            text_color=COLOR_LIGHT_GREY,
            justify="left",
            wraplength=420
        )
        subtitle.pack(anchor="w", pady=(0, 28))

        # CTA Buttons Row
        btn_row = ctk.CTkFrame(text_col, fg_color="transparent")
        btn_row.pack(anchor="w")

        explore_btn = ctk.CTkButton(
            btn_row,
            text="EXPLORE LONDON",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color=COLOR_NAVY,
            height=44,
            corner_radius=8,
            command=lambda: self.navigate("explore", None)
        )
        explore_btn.pack(side="left", padx=(0, 14))

        plan_btn = ctk.CTkButton(
            btn_row,
            text="PLAN MY TRIP",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_BURGUNDY,
            hover_color=COLOR_BURGUNDY_HOVER,
            text_color=COLOR_WHITE,
            height=44,
            corner_radius=8,
            command=lambda: self.navigate("itinerary", None)
        )
        plan_btn.pack(side="left")

        # Right Column: Hero Image
        hero_img = ImageManager.get_image(
            filename="london_hero.jpg",
            width=480,
            height=300,
            fallback_title="London Skyline"
        )
        img_label = ctk.CTkLabel(hero_frame, text="", image=hero_img)
        img_label.grid(row=0, column=1, sticky="nsew", padx=(10, 25), pady=25)

    def _build_featured_destinations(self, parent: ctk.CTkFrame) -> None:
        # Section Header
        sec_header = ctk.CTkFrame(parent, fg_color="transparent")
        sec_header.pack(fill="x", pady=(0, 18))

        title = ctk.CTkLabel(
            sec_header,
            text="EXPLORE THE CITY",
            font=get_font(size=22, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(side="left")

        view_all_btn = ctk.CTkButton(
            sec_header,
            text="View All 20+ Places →",
            font=get_font(size=13, weight="bold"),
            fg_color="transparent",
            hover_color=COLOR_LIGHT_GREY,
            text_color=COLOR_BURGUNDY,
            height=32,
            command=lambda: self.navigate("explore", None)
        )
        view_all_btn.pack(side="right")

        # Featured cards container
        cards_grid = ctk.CTkFrame(parent, fg_color="transparent")
        cards_grid.pack(fill="x", pady=(0, 35))

        # Configure 4 columns
        for c in range(4):
            cards_grid.grid_columnconfigure(c, weight=1, uniform="featured_col")

        featured_items = self.data_manager.get_featured_destinations()
        # Ensure we have the 4 specified in prompt: Big Ben, Tower Bridge, Buckingham Palace, London Eye
        if len(featured_items) < 4:
            target_ids = ["big_ben", "tower_bridge", "buckingham_palace", "london_eye"]
            featured_items = [self.data_manager.get_destination_by_id(tid) for tid in target_ids if self.data_manager.get_destination_by_id(tid)]

        for idx, dest in enumerate(featured_items[:4]):
            self._render_destination_card(cards_grid, dest, col_idx=idx)

    def _render_destination_card(self, parent: ctk.CTkFrame, dest: dict, col_idx: int) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=0, column=col_idx, sticky="nsew", padx=8, pady=4)

        # Image thumbnail
        card_img = ImageManager.get_image(
            filename=dest.get("image_file", "london_hero.jpg"),
            width=230,
            height=145,
            fallback_title=dest.get("name", "London")
        )
        img_lbl = ctk.CTkLabel(card, text="", image=card_img, corner_radius=10)
        img_lbl.pack(fill="x", padx=10, pady=(10, 8))

        # Text details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Neighbourhood tag
        nh_lbl = ctk.CTkLabel(
            details_frame,
            text=f"📍 {dest.get('neighbourhood', 'London')}",
            font=get_font(size=11, weight="bold"),
            text_color=COLOR_GOLD
        )
        nh_lbl.pack(anchor="w")

        # Name
        name_lbl = ctk.CTkLabel(
            details_frame,
            text=dest.get("name", ""),
            font=get_font(size=14, weight="bold", serif=True),
            text_color=COLOR_NAVY,
            wraplength=205,
            justify="left"
        )
        name_lbl.pack(anchor="w", pady=(2, 6))

        # Short description
        desc_lbl = ctk.CTkLabel(
            details_frame,
            text=dest.get("short_description", "")[:80] + "...",
            font=get_font(size=12),
            text_color=COLOR_MUTED_TEXT,
            wraplength=205,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 10))

        # Bottom row: Details button & Favourite toggle
        bottom_row = ctk.CTkFrame(details_frame, fg_color="transparent")
        bottom_row.pack(fill="x", side="bottom")

        details_btn = ctk.CTkButton(
            bottom_row,
            text="Explore Details",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            height=32,
            corner_radius=6,
            command=lambda d_id=dest.get("id"): self.open_detail(d_id)
        )
        details_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        # Favourite Heart Button
        is_fav = self.data_manager.is_favourite(dest.get("id"))
        fav_btn = ctk.CTkButton(
            bottom_row,
            text="❤️" if is_fav else "🤍",
            width=36,
            height=32,
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

    def _build_category_showcase(self, parent: ctk.CTkFrame) -> None:
        # Section Header
        sec_header = ctk.CTkFrame(parent, fg_color="transparent")
        sec_header.pack(fill="x", pady=(0, 18))

        title = ctk.CTkLabel(
            sec_header,
            text="FIND YOUR LONDON",
            font=get_font(size=22, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            sec_header,
            text="Curated collections tailored to your travel passions",
            font=get_font(size=13),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(side="left", padx=15)

        # 6 Category Cards in 3x2 Grid
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x")

        for c in range(3):
            grid_frame.grid_columnconfigure(c, weight=1, uniform="cat_col")

        categories = [
            ("Iconic Landmarks", "big_ben.jpg", "Landmarks", "Majestic towers, historic abbeys & royal halls"),
            ("Hidden Gems", "neals_yard.jpg", "Hidden Gems", "Secret courtyards, quiet canals & mews"),
            ("Food & Markets", "borough_market.jpg", "Food & Markets", "Artisan street bites & historic stalls"),
            ("History & Museums", "british_museum.jpg", "Museums", "World antiquity & natural science"),
            ("Parks & Gardens", "hyde_park.jpg", "Parks", "Verdant Royal Parks & scenic ponds"),
            ("Shopping & Style", "covent_garden.jpg", "Shopping", "Vintage markets & West End boutiques")
        ]

        for i, (cat_title, img_name, filter_tag, summary) in enumerate(categories):
            row = i // 3
            col = i % 3

            cat_card = ctk.CTkFrame(
                grid_frame,
                fg_color=COLOR_CARD_BG,
                corner_radius=12,
                border_width=1,
                border_color=COLOR_BORDER
            )
            cat_card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            # Image banner
            card_img = ImageManager.get_image(
                filename=img_name,
                width=310,
                height=130,
                fallback_title=cat_title
            )
            img_lbl = ctk.CTkLabel(cat_card, text="", image=card_img, corner_radius=10)
            img_lbl.pack(fill="x", padx=10, pady=(10, 6))

            content = ctk.CTkFrame(cat_card, fg_color="transparent")
            content.pack(fill="x", padx=12, pady=(0, 12))

            h_lbl = ctk.CTkLabel(
                content,
                text=cat_title,
                font=get_font(size=15, weight="bold", serif=True),
                text_color=COLOR_NAVY
            )
            h_lbl.pack(anchor="w")

            s_lbl = ctk.CTkLabel(
                content,
                text=summary,
                font=get_font(size=12),
                text_color=COLOR_MUTED_TEXT,
                wraplength=280,
                justify="left"
            )
            s_lbl.pack(anchor="w", pady=(2, 10))

            explore_cat_btn = ctk.CTkButton(
                content,
                text="Discover Collection →",
                font=get_font(size=12, weight="bold"),
                fg_color=COLOR_TAG_BG,
                hover_color=COLOR_LIGHT_GREY,
                text_color=COLOR_BURGUNDY,
                height=30,
                corner_radius=6,
                command=lambda tag=filter_tag: self.navigate("explore", tag)
            )
            explore_cat_btn.pack(fill="x")
