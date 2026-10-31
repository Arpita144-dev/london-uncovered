"""Dedicated Destination Detail View."""

from typing import Callable, Any, Dict
import customtkinter as ctk

from app.config import (
    COLOR_BG,
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_BURGUNDY,
    COLOR_BURGUNDY_HOVER,
    COLOR_GOLD,
    COLOR_GOLD_HOVER,
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


class DetailView(ctk.CTkScrollableFrame):
    """Magazine editorial presentation of a single London destination."""

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        dest_id: str,
        back_callback: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager
        self.dest_id = dest_id
        self.back_callback = back_callback

        self.dest: Dict[str, Any] = self.data_manager.get_destination_by_id(dest_id) or {}
        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=25)

        # 1. Navigation Top Bar (Back button + Action Buttons)
        top_bar = ctk.CTkFrame(container, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 20))

        back_btn = ctk.CTkButton(
            top_bar,
            text="← Back to Destinations",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_WHITE,
            hover_color=COLOR_LIGHT_GREY,
            text_color=COLOR_NAVY,
            border_width=1,
            border_color=COLOR_BORDER,
            height=38,
            corner_radius=8,
            command=self.back_callback
        )
        back_btn.pack(side="left")

        # Action Buttons Group (Right side)
        actions_group = ctk.CTkFrame(top_bar, fg_color="transparent")
        actions_group.pack(side="right")

        # Favourite Toggle Button
        is_fav = self.data_manager.is_favourite(self.dest_id)
        self.fav_btn = ctk.CTkButton(
            actions_group,
            text="❤️ Saved in Favourites" if is_fav else "🤍 Save to Favourites",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_BURGUNDY if is_fav else COLOR_WHITE,
            hover_color=COLOR_BURGUNDY_HOVER if is_fav else COLOR_LIGHT_GREY,
            text_color=COLOR_WHITE if is_fav else COLOR_BURGUNDY,
            border_width=1,
            border_color=COLOR_BURGUNDY if is_fav else COLOR_BORDER,
            height=38,
            corner_radius=8,
            command=self._toggle_fav
        )
        self.fav_btn.pack(side="left", padx=(0, 10))

        # Add to My Trip Button
        is_in_trip = self.dest_id in self.data_manager.get_trip_destination_ids()
        self.trip_btn = ctk.CTkButton(
            actions_group,
            text="✓ Added to My Trip" if is_in_trip else "➕ Add to My Trip",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_GOLD if is_in_trip else COLOR_NAVY,
            hover_color=COLOR_GOLD_HOVER if is_in_trip else COLOR_NAVY_HOVER,
            text_color=COLOR_NAVY if is_in_trip else COLOR_WHITE,
            height=38,
            corner_radius=8,
            command=self._toggle_trip
        )
        self.trip_btn.pack(side="left")

        # 2. Hero Visual & Headline Banner
        hero_card = ctk.CTkFrame(
            container,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        hero_card.pack(fill="x", pady=(0, 25))

        # Big photograph
        large_img = ImageManager.get_image(
            filename=self.dest.get("image_file", "london_hero.jpg"),
            width=920,
            height=380,
            fallback_title=self.dest.get("name", "London")
        )
        img_lbl = ctk.CTkLabel(hero_card, text="", image=large_img, corner_radius=14)
        img_lbl.pack(fill="x", padx=14, pady=14)

        # Meta info underneath the image
        meta_panel = ctk.CTkFrame(hero_card, fg_color="transparent")
        meta_panel.pack(fill="x", padx=25, pady=(5, 20))

        # Badges row
        badges_row = ctk.CTkFrame(meta_panel, fg_color="transparent")
        badges_row.pack(fill="x", pady=(0, 8))

        cat_badge = ctk.CTkLabel(
            badges_row,
            text=f"🏷️ {self.dest.get('category', 'Landmark')}",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_TAG_BG,
            text_color=COLOR_BURGUNDY,
            corner_radius=6,
            padx=10,
            pady=4
        )
        cat_badge.pack(side="left", padx=(0, 10))

        nh_badge = ctk.CTkLabel(
            badges_row,
            text=f"📍 {self.dest.get('neighbourhood', 'London')}",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_GOLD_LIGHT,
            text_color=COLOR_NAVY,
            corner_radius=6,
            padx=10,
            pady=4
        )
        nh_badge.pack(side="left", padx=(0, 10))

        dur_badge = ctk.CTkLabel(
            badges_row,
            text=f"⏱ Suggested Visit: {self.dest.get('duration', '2 hours')}",
            font=get_font(size=12),
            fg_color=COLOR_LIGHT_GREY,
            text_color=COLOR_DARK_TEXT,
            corner_radius=6,
            padx=10,
            pady=4
        )
        dur_badge.pack(side="left")

        # Destination Title
        title_lbl = ctk.CTkLabel(
            meta_panel,
            text=self.dest.get("name", "London Attraction"),
            font=get_font(size=30, weight="bold", serif=True),
            text_color=COLOR_NAVY,
            wraplength=880,
            justify="left"
        )
        title_lbl.pack(anchor="w", pady=(8, 4))

        # 3. Two-Column Magazine Content Layout
        content_grid = ctk.CTkFrame(container, fg_color="transparent")
        content_grid.pack(fill="x", pady=(0, 20))

        content_grid.grid_columnconfigure(0, weight=6)
        content_grid.grid_columnconfigure(1, weight=4)

        # Left Column: Editorial narrative & why famous
        left_col = ctk.CTkFrame(content_grid, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Description Card
        desc_card = self._create_card(left_col, "ABOUT THIS DESTINATION")
        full_desc = self.dest.get("full_description", self.dest.get("short_description", ""))
        desc_lbl = ctk.CTkLabel(
            desc_card,
            text=full_desc,
            font=get_font(size=14),
            text_color=COLOR_DARK_TEXT,
            wraplength=520,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(5, 18))

        # Why It Is Famous Card
        why_card = self._create_card(left_col, "WHY IT IS FAMOUS")
        why_lbl = ctk.CTkLabel(
            why_card,
            text=self.dest.get("why_famous", "An iconic cornerstone of London's cultural heritage."),
            font=get_font(size=14, weight="normal"),
            text_color=COLOR_NAVY,
            wraplength=520,
            justify="left"
        )
        why_lbl.pack(anchor="w", padx=20, pady=(5, 18))

        # Things To Do Card
        things_card = self._create_card(left_col, "THINGS TO DO & EXPERIENCE")
        for act in self.dest.get("things_to_do", []):
            item_frame = ctk.CTkFrame(things_card, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=4)

            bullet = ctk.CTkLabel(
                item_frame,
                text="✦",
                font=get_font(size=13, weight="bold"),
                text_color=COLOR_GOLD
            )
            bullet.pack(side="left", anchor="n", padx=(0, 8))

            act_lbl = ctk.CTkLabel(
                item_frame,
                text=act,
                font=get_font(size=13),
                text_color=COLOR_DARK_TEXT,
                wraplength=480,
                justify="left"
            )
            act_lbl.pack(side="left", anchor="w")
        ctk.CTkFrame(things_card, fg_color="transparent", height=12).pack()

        # Right Column: Interesting Facts & Practical Visitor Tips
        right_col = ctk.CTkFrame(content_grid, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        # Interesting Facts Card
        facts_card = self._create_card(right_col, "DID YOU KNOW?")
        for fact in self.dest.get("interesting_facts", []):
            f_frame = ctk.CTkFrame(facts_card, fg_color="transparent")
            f_frame.pack(fill="x", padx=20, pady=5)

            icon = ctk.CTkLabel(
                f_frame,
                text="💡",
                font=get_font(size=14)
            )
            icon.pack(side="left", anchor="n", padx=(0, 8))

            f_lbl = ctk.CTkLabel(
                f_frame,
                text=fact,
                font=get_font(size=13),
                text_color=COLOR_DARK_TEXT,
                wraplength=300,
                justify="left"
            )
            f_lbl.pack(side="left", anchor="w")
        ctk.CTkFrame(facts_card, fg_color="transparent", height=12).pack()

        # Practical Visitor Tips Card
        tips_card = self._create_card(right_col, "PRACTICAL VISITOR TIPS")
        tip_text = self.dest.get("visitor_tips", "Plan your visit during off-peak morning hours for the best experience.")
        tips_lbl = ctk.CTkLabel(
            tips_card,
            text=tip_text,
            font=get_font(size=13),
            text_color=COLOR_MUTED_TEXT,
            wraplength=310,
            justify="left"
        )
        tips_lbl.pack(anchor="w", padx=20, pady=(5, 18))

        # Bottom spacer
        ctk.CTkFrame(container, fg_color="transparent", height=40).pack()

    def _create_card(self, parent: ctk.CTkFrame, title_text: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", pady=(0, 16))

        h_lbl = ctk.CTkLabel(
            card,
            text=title_text,
            font=get_font(size=14, weight="bold", serif=True),
            text_color=COLOR_BURGUNDY
        )
        h_lbl.pack(anchor="w", padx=20, pady=(16, 6))
        return card

    def _toggle_fav(self) -> None:
        new_status = self.data_manager.toggle_favourite(self.dest_id)
        if new_status:
            self.fav_btn.configure(
                text="❤️ Saved in Favourites",
                fg_color=COLOR_BURGUNDY,
                text_color=COLOR_WHITE,
                border_color=COLOR_BURGUNDY
            )
        else:
            self.fav_btn.configure(
                text="🤍 Save to Favourites",
                fg_color=COLOR_WHITE,
                text_color=COLOR_BURGUNDY,
                border_color=COLOR_BORDER
            )

    def _toggle_trip(self) -> None:
        is_in = self.dest_id in self.data_manager.get_trip_destination_ids()
        if is_in:
            self.data_manager.remove_from_trip(self.dest_id)
            self.trip_btn.configure(
                text="➕ Add to My Trip",
                fg_color=COLOR_NAVY,
                text_color=COLOR_WHITE
            )
        else:
            self.data_manager.add_to_trip(self.dest_id)
            self.trip_btn.configure(
                text="✓ Added to My Trip",
                fg_color=COLOR_GOLD,
                text_color=COLOR_NAVY
            )
