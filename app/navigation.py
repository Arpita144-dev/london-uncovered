"""Navigation sidebar component and view controller for London Uncovered."""

from typing import Callable, Dict, Any
import customtkinter as ctk

from app.config import (
    COLOR_NAVY,
    COLOR_NAVY_HOVER,
    COLOR_NAVY_LIGHT,
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_WHITE,
    COLOR_LIGHT_GREY,
    COLOR_MUTED_TEXT,
    APP_NAME,
    TAGLINE,
    FOOTER_TEXT,
    get_font
)


class NavigationSidebar(ctk.CTkFrame):
    """The persistent left-hand navigation sidebar for the desktop application."""

    NAV_ITEMS = [
        ("home", "🏛️  Home"),
        ("explore", "🧭  Explore London"),
        ("hidden_gems", "💎  Hidden Gems"),
        ("experiences", "🎭  Experiences"),
        ("food", "🍽️  Food & Cafés"),
        ("neighbourhoods", "🗺️  Neighbourhoods"),
        ("itinerary", "📅  Plan My Trip"),
        ("favourites", "❤️  Saved Places"),
        ("travel_tips", "💡  Travel Tips"),
    ]

    def __init__(
        self,
        master: Any,
        on_navigate: Callable[[str, Any], None],
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=COLOR_NAVY,
            width=255,
            corner_radius=0,
            **kwargs
        )
        self.on_navigate = on_navigate
        self.buttons: Dict[str, ctk.CTkButton] = {}
        self.active_route = "home"

        # Prevent the frame from shrinking
        self.pack_propagate(False)

        self._build_ui()

    def _build_ui(self) -> None:
        # Top Logo & Branding Area
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 24))

        # Crown insignia
        ctk.CTkLabel(
            logo_frame,
            text="👑",
            font=get_font(size=22)
        ).pack(anchor="w")

        # Application Title
        ctk.CTkLabel(
            logo_frame,
            text=APP_NAME,
            font=get_font(size=17, weight="bold", serif=True),
            text_color=COLOR_GOLD
        ).pack(anchor="w", pady=(2, 2))

        # Tagline
        ctk.CTkLabel(
            logo_frame,
            text=TAGLINE,
            font=get_font(size=11),
            text_color=COLOR_LIGHT_GREY,
            wraplength=210,
            justify="left"
        ).pack(anchor="w")

        # Decorative separator rule
        sep = ctk.CTkFrame(self, fg_color=COLOR_NAVY_LIGHT, height=1)
        sep.pack(fill="x", padx=20, pady=(0, 16))

        # Navigation buttons container
        nav_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons_frame.pack(fill="x", padx=12)

        for route_id, label in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                nav_buttons_frame,
                text=label,
                font=get_font(size=13, weight="bold"),
                anchor="w",
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLOR_NAVY_HOVER,
                text_color=COLOR_LIGHT_GREY,
                command=lambda r=route_id: self._handle_click(r)
            )
            btn.pack(fill="x", pady=2)
            self.buttons[route_id] = btn

        # Set initial active state
        self.set_active("home")

        # Bottom Footer Area
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=20, pady=24)

        ctk.CTkFrame(footer_frame, fg_color=COLOR_NAVY_LIGHT, height=1).pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            footer_frame,
            text="✦ LONDON UNCOVERED ✦",
            font=get_font(size=10, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            footer_frame,
            text=FOOTER_TEXT,
            font=get_font(size=11),
            text_color=COLOR_LIGHT_GREY
        ).pack(anchor="w", pady=(2, 0))

    def _handle_click(self, route_id: str) -> None:
        self.set_active(route_id)
        self.on_navigate(route_id, None)

    def set_active(self, route_id: str) -> None:
        self.active_route = route_id
        for rid, btn in self.buttons.items():
            if rid == route_id:
                btn.configure(
                    fg_color=COLOR_BURGUNDY,
                    text_color=COLOR_WHITE,
                    hover_color=COLOR_BURGUNDY
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLOR_LIGHT_GREY,
                    hover_color=COLOR_NAVY_HOVER
                )
