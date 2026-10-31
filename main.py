"""Main entry point for London Uncovered — A Visual London Travel Guide.

Author: Antigravity
College Frontend Development Project
"""

import sys
from pathlib import Path
import customtkinter as ctk

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import (
    APP_NAME,
    COLOR_BG,
    COLOR_NAVY
)
from app.data_manager import DataManager
from app.navigation import NavigationSidebar

# Views
from app.views.home_view import HomeView
from app.views.explore_view import ExploreView
from app.views.detail_view import DetailView
from app.views.hidden_gems_view import HiddenGemsView
from app.views.experiences_view import ExperiencesView
from app.views.neighbourhood_view import NeighbourhoodView
from app.views.itinerary_view import ItineraryView
from app.views.favourites_view import FavouritesView
from app.views.food_view import FoodView
from app.views.travel_tips_view import TravelTipsView


class LondonUncoveredApp(ctk.CTk):
    """Main Application Window."""

    def __init__(self):
        super().__init__()

        # Appearance configuration: Set strictly to Light mode for cream & navy magazine aesthetic
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Window settings
        self.title(f"{APP_NAME} — Discover London, One Experience at a Time")
        self.geometry("1280x840")
        self.minsize(1050, 720)
        self.configure(fg_color=COLOR_BG)

        # Initialize data manager
        self.data_manager = DataManager()

        # Navigation state tracking
        self.previous_route = "home"
        self.current_route = "home"
        self.active_view = None

        # Build main layout
        self._build_layout()

        # Display initial home screen
        self.navigate_to("home")

    def _build_layout(self) -> None:
        # Left persistent sidebar
        self.sidebar = NavigationSidebar(self, on_navigate=self.navigate_to)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        # Main content host container
        self.content_container = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.content_container.pack(side="right", fill="both", expand=True)

    def navigate_to(self, route: str, extra_data: any = None) -> None:
        """Central router managing seamless transition between application screens."""
        # Clean up current active view
        if self.active_view is not None:
            self.active_view.destroy()
            self.active_view = None

        if route != "detail":
            self.previous_route = route
            self.sidebar.set_active(route)

        self.current_route = route

        # Instantiation of target view
        if route == "home":
            self.active_view = HomeView(
                self.content_container,
                data_manager=self.data_manager,
                navigate_callback=self.navigate_to,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "explore":
            category = extra_data if isinstance(extra_data, str) else "All"
            self.active_view = ExploreView(
                self.content_container,
                data_manager=self.data_manager,
                open_detail_callback=self.open_destination_detail,
                initial_category=category
            )
        elif route == "explore_search":
            search_query = str(extra_data) if extra_data else ""
            self.active_view = ExploreView(
                self.content_container,
                data_manager=self.data_manager,
                open_detail_callback=self.open_destination_detail,
                initial_category="All"
            )
            if hasattr(self.active_view, "search_var"):
                self.active_view.search_var.set(search_query)
            self.sidebar.set_active("explore")
        elif route == "detail":
            dest_id = str(extra_data) if extra_data else "big_ben"
            self.active_view = DetailView(
                self.content_container,
                data_manager=self.data_manager,
                dest_id=dest_id,
                back_callback=self._handle_back_from_detail
            )
        elif route == "hidden_gems":
            self.active_view = HiddenGemsView(
                self.content_container,
                data_manager=self.data_manager,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "experiences":
            self.active_view = ExperiencesView(
                self.content_container,
                data_manager=self.data_manager,
                navigate_callback=self.navigate_to,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "neighbourhoods":
            self.active_view = NeighbourhoodView(
                self.content_container,
                data_manager=self.data_manager,
                navigate_callback=self.navigate_to,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "itinerary":
            self.active_view = ItineraryView(
                self.content_container,
                data_manager=self.data_manager,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "favourites":
            self.active_view = FavouritesView(
                self.content_container,
                data_manager=self.data_manager,
                navigate_callback=self.navigate_to,
                open_detail_callback=self.open_destination_detail
            )
        elif route == "food":
            self.active_view = FoodView(
                self.content_container,
                data_manager=self.data_manager,
                navigate_callback=self.navigate_to
            )
        elif route == "travel_tips":
            self.active_view = TravelTipsView(
                self.content_container,
                data_manager=self.data_manager
            )
        else:
            # Fallback to home
            self.navigate_to("home")
            return

        if self.active_view:
            self.active_view.pack(fill="both", expand=True)

    def open_destination_detail(self, dest_id: str) -> None:
        """Open the dedicated detail view for a specific destination."""
        self.navigate_to("detail", dest_id)

    def _handle_back_from_detail(self) -> None:
        """Return to the previously active view prior to entering the detail view."""
        self.navigate_to(self.previous_route)


def main():
    app = LondonUncoveredApp()
    app.mainloop()


if __name__ == "__main__":
    main()
