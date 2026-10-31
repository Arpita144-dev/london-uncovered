"""Interactive Itinerary Planner View."""

import webbrowser
from typing import Callable, Any, List, Dict, Optional
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
from app.utils.itinerary_generator import ItineraryGenerator


class ItineraryView(ctk.CTkScrollableFrame):
    """Personalised Itinerary Planner with multi-step wizard, interactive timeline, and export."""

    DURATIONS = [
        ("1 Day", 1),
        ("2 Days", 2),
        ("3 Days", 3),
        ("5 Days", 5)
    ]

    INTERESTS_LIST = [
        "History & Landmarks",
        "Museums & Art",
        "Food & Cafés",
        "Shopping",
        "Nature & Parks",
        "Photography",
        "Hidden Gems",
        "Culture & Entertainment"
    ]

    BUDGETS = ["Budget-friendly", "Balanced", "Premium"]
    PACES = ["Relaxed", "Balanced", "Packed"]

    def __init__(
        self,
        master: Any,
        data_manager: Any,
        open_detail_callback: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.data_manager = data_manager
        self.open_detail = open_detail_callback

        # State variables
        self.selected_duration = 3
        self.selected_interests = {"History & Landmarks", "Food & Cafés"}
        self.selected_budget = "Balanced"
        self.selected_pace = "Balanced"

        self.interest_buttons: Dict[str, ctk.CTkButton] = {}
        self.duration_buttons: Dict[int, ctk.CTkButton] = {}
        self.budget_buttons: Dict[str, ctk.CTkButton] = {}
        self.pace_buttons: Dict[str, ctk.CTkButton] = {}

        self.current_itinerary: Optional[Dict[str, Any]] = None
        self.active_day_tab = 1

        self._build_ui()

    def _build_ui(self) -> None:
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=25)

        # Header Bar
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            header,
            text="PLAN YOUR LONDON ADVENTURE",
            font=get_font(size=28, weight="bold", serif=True),
            text_color=COLOR_NAVY
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Choose your interests and let London Uncovered help you organise your trip.",
            font=get_font(size=14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Saved itineraries top shortcut button
        saved_count = len(self.data_manager.get_saved_itineraries())
        self.saved_nav_btn = ctk.CTkButton(
            header,
            text=f"📂 Saved Itineraries ({saved_count})",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_WHITE,
            hover_color=COLOR_LIGHT_GREY,
            text_color=COLOR_NAVY,
            border_width=1,
            border_color=COLOR_BORDER,
            height=34,
            command=self._show_saved_itineraries_dialog
        )
        self.saved_nav_btn.place(relx=1.0, rely=0.1, anchor="ne")

        # 4-Step Interactive Configuration Wizard
        self._build_wizard_panel()

        # Results Container (Timeline / Day-by-Day schedule)
        self.results_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.results_frame.pack(fill="x", pady=(25, 0))

        # Bottom spacer
        ctk.CTkFrame(self.container, fg_color="transparent", height=40).pack()

    def _build_wizard_panel(self) -> None:
        wizard_card = ctk.CTkFrame(
            self.container,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER
        )
        wizard_card.pack(fill="x", pady=(0, 10))

        # Step 1: Duration
        self._build_step_duration(wizard_card)

        # Step 2: Interests
        self._build_step_interests(wizard_card)

        # Two-column row for Step 3 (Budget) and Step 4 (Pace)
        two_col = ctk.CTkFrame(wizard_card, fg_color="transparent")
        two_col.pack(fill="x", padx=25, pady=(10, 15))
        two_col.grid_columnconfigure(0, weight=1)
        two_col.grid_columnconfigure(1, weight=1)

        self._build_step_budget(two_col, col=0)
        self._build_step_pace(two_col, col=1)

        # Custom "Add to My Trip" indicator if user added places
        trip_ids = self.data_manager.get_trip_destination_ids()
        if trip_ids:
            banner = ctk.CTkFrame(wizard_card, fg_color=COLOR_GOLD_LIGHT, corner_radius=8)
            banner.pack(fill="x", padx=25, pady=(0, 15))
            ctk.CTkLabel(
                banner,
                text=f"✨ {len(trip_ids)} hand-picked places from 'Add to My Trip' will be prioritized in your generated itinerary!",
                font=get_font(size=12, weight="bold"),
                text_color=COLOR_NAVY
            ).pack(anchor="w", padx=14, pady=8)

        # Action: "CREATE MY ITINERARY" Button
        cta_bar = ctk.CTkFrame(wizard_card, fg_color="transparent")
        cta_bar.pack(fill="x", padx=25, pady=(5, 25))

        create_btn = ctk.CTkButton(
            cta_bar,
            text="✨ CREATE MY ITINERARY",
            font=get_font(size=15, weight="bold"),
            fg_color=COLOR_BURGUNDY,
            hover_color=COLOR_BURGUNDY_HOVER,
            text_color=COLOR_WHITE,
            height=46,
            corner_radius=8,
            command=self._generate_itinerary
        )
        create_btn.pack(side="left", padx=(0, 15))

        reset_btn = ctk.CTkButton(
            cta_bar,
            text="Start Over",
            font=get_font(size=13),
            fg_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_BORDER,
            text_color=COLOR_DARK_TEXT,
            height=46,
            corner_radius=8,
            command=self._reset_wizard
        )
        reset_btn.pack(side="left")

    def _build_step_duration(self, parent: ctk.CTkFrame) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            frame,
            text="STEP 1: TRIP DURATION",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame,
            text="How long is your stay in London?",
            font=get_font(size=15, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(2, 8))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(anchor="w")

        for label, days in self.DURATIONS:
            is_active = (days == self.selected_duration)
            btn = ctk.CTkButton(
                btn_row,
                text=label,
                font=get_font(size=13, weight="bold"),
                fg_color=COLOR_NAVY if is_active else COLOR_WHITE,
                hover_color=COLOR_NAVY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_NAVY,
                border_width=1,
                border_color=COLOR_NAVY if is_active else COLOR_BORDER,
                height=36,
                width=100,
                corner_radius=8,
                command=lambda d=days: self._set_duration(d)
            )
            btn.pack(side="left", padx=(0, 10))
            self.duration_buttons[days] = btn

    def _set_duration(self, days: int) -> None:
        self.selected_duration = days
        for d, btn in self.duration_buttons.items():
            if d == days:
                btn.configure(fg_color=COLOR_NAVY, text_color=COLOR_WHITE, border_color=COLOR_NAVY)
            else:
                btn.configure(fg_color=COLOR_WHITE, text_color=COLOR_NAVY, border_color=COLOR_BORDER)

    def _build_step_interests(self, parent: ctk.CTkFrame) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=(10, 10))

        ctk.CTkLabel(
            frame,
            text="STEP 2: TRAVEL INTERESTS (Select multiple)",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame,
            text="What experiences excite you most?",
            font=get_font(size=15, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(2, 8))

        chips_row = ctk.CTkFrame(frame, fg_color="transparent")
        chips_row.pack(fill="x")

        for interest in self.INTERESTS_LIST:
            is_active = interest in self.selected_interests
            btn = ctk.CTkButton(
                chips_row,
                text=f"✓ {interest}" if is_active else interest,
                font=get_font(size=12, weight="bold"),
                fg_color=COLOR_BURGUNDY if is_active else COLOR_WHITE,
                hover_color=COLOR_BURGUNDY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_DARK_TEXT,
                border_width=1,
                border_color=COLOR_BURGUNDY if is_active else COLOR_BORDER,
                height=34,
                corner_radius=17,
                command=lambda i=interest: self._toggle_interest(i)
            )
            btn.pack(side="left", padx=4, pady=4)
            self.interest_buttons[interest] = btn

    def _toggle_interest(self, interest: str) -> None:
        if interest in self.selected_interests:
            if len(self.selected_interests) > 1:
                self.selected_interests.remove(interest)
        else:
            self.selected_interests.add(interest)

        # Update button styles
        for i, btn in self.interest_buttons.items():
            is_sel = i in self.selected_interests
            btn.configure(
                text=f"✓ {i}" if is_sel else i,
                fg_color=COLOR_BURGUNDY if is_sel else COLOR_WHITE,
                text_color=COLOR_WHITE if is_sel else COLOR_DARK_TEXT,
                border_color=COLOR_BURGUNDY if is_sel else COLOR_BORDER
            )

    def _build_step_budget(self, parent: ctk.CTkFrame, col: int) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            frame,
            text="STEP 3: BUDGET STYLE",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame,
            text="Target spending preference:",
            font=get_font(size=14, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(2, 6))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(anchor="w")

        for b in self.BUDGETS:
            is_active = (b == self.selected_budget)
            btn = ctk.CTkButton(
                btn_row,
                text=b,
                font=get_font(size=12),
                fg_color=COLOR_NAVY if is_active else COLOR_WHITE,
                hover_color=COLOR_NAVY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_NAVY,
                border_width=1,
                border_color=COLOR_NAVY if is_active else COLOR_BORDER,
                height=32,
                corner_radius=6,
                command=lambda val=b: self._set_budget(val)
            )
            btn.pack(side="left", padx=(0, 6))
            self.budget_buttons[b] = btn

    def _set_budget(self, val: str) -> None:
        self.selected_budget = val
        for b, btn in self.budget_buttons.items():
            if b == val:
                btn.configure(fg_color=COLOR_NAVY, text_color=COLOR_WHITE, border_color=COLOR_NAVY)
            else:
                btn.configure(fg_color=COLOR_WHITE, text_color=COLOR_NAVY, border_color=COLOR_BORDER)

    def _build_step_pace(self, parent: ctk.CTkFrame, col: int) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            frame,
            text="STEP 4: TRAVEL PACE",
            font=get_font(size=12, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame,
            text="Daily schedule intensity:",
            font=get_font(size=14, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(anchor="w", pady=(2, 6))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(anchor="w")

        for p in self.PACES:
            is_active = (p == self.selected_pace)
            btn = ctk.CTkButton(
                btn_row,
                text=p,
                font=get_font(size=12),
                fg_color=COLOR_NAVY if is_active else COLOR_WHITE,
                hover_color=COLOR_NAVY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_NAVY,
                border_width=1,
                border_color=COLOR_NAVY if is_active else COLOR_BORDER,
                height=32,
                corner_radius=6,
                command=lambda val=p: self._set_pace(val)
            )
            btn.pack(side="left", padx=(0, 6))
            self.pace_buttons[p] = btn

    def _set_pace(self, val: str) -> None:
        self.selected_pace = val
        for p, btn in self.pace_buttons.items():
            if p == val:
                btn.configure(fg_color=COLOR_NAVY, text_color=COLOR_WHITE, border_color=COLOR_NAVY)
            else:
                btn.configure(fg_color=COLOR_WHITE, text_color=COLOR_NAVY, border_color=COLOR_BORDER)

    def _reset_wizard(self) -> None:
        self._set_duration(3)
        self.selected_interests = {"History & Landmarks", "Food & Cafés"}
        self._set_budget("Balanced")
        self._set_pace("Balanced")
        for i, btn in self.interest_buttons.items():
            is_sel = i in self.selected_interests
            btn.configure(
                text=f"✓ {i}" if is_sel else i,
                fg_color=COLOR_BURGUNDY if is_sel else COLOR_WHITE,
                text_color=COLOR_WHITE if is_sel else COLOR_DARK_TEXT,
                border_color=COLOR_BURGUNDY if is_sel else COLOR_BORDER
            )
        self.current_itinerary = None
        for w in self.results_frame.winfo_children():
            w.destroy()

    def _generate_itinerary(self) -> None:
        all_dests = self.data_manager.get_all_destinations()
        trip_ids = self.data_manager.get_trip_destination_ids()

        self.current_itinerary = ItineraryGenerator.generate(
            destinations=all_dests,
            duration_days=self.selected_duration,
            interests=list(self.selected_interests),
            budget=self.selected_budget,
            pace=self.selected_pace,
            user_trip_dest_ids=trip_ids
        )
        self.active_day_tab = 1
        self._render_itinerary_results()

    def _render_itinerary_results(self) -> None:
        for w in self.results_frame.winfo_children():
            w.destroy()

        if not self.current_itinerary:
            return

        itin = self.current_itinerary
        days = itin.get("days", [])

        # Itinerary Header Card
        header_card = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLOR_NAVY,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        header_card.pack(fill="x", pady=(0, 20))

        h_content = ctk.CTkFrame(header_card, fg_color="transparent")
        h_content.pack(fill="x", padx=25, pady=20)

        ctk.CTkLabel(
            h_content,
            text=f"✦ {itin.get('title')} ✦",
            font=get_font(size=22, weight="bold", serif=True),
            text_color=COLOR_WHITE
        ).pack(anchor="w")

        meta_text = (
            f"📅 {itin.get('duration_days')} Days • ⚡ Pace: {itin.get('pace')} • "
            f"💰 Budget: {itin.get('budget')} • Interests: {', '.join(itin.get('interests', []))}"
        )
        ctk.CTkLabel(
            h_content,
            text=meta_text,
            font=get_font(size=12),
            text_color=COLOR_GOLD
        ).pack(anchor="w", pady=(4, 14))

        # Itinerary Toolbar (Save, Print, Add Dest, Generate Again)
        toolbar = ctk.CTkFrame(h_content, fg_color="transparent")
        toolbar.pack(fill="x")

        # Save Button
        save_btn = ctk.CTkButton(
            toolbar,
            text="💾 Save Itinerary",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color=COLOR_NAVY,
            height=34,
            corner_radius=6,
            command=self._save_current_itinerary
        )
        save_btn.pack(side="left", padx=(0, 10))

        # Print / Export Button
        print_btn = ctk.CTkButton(
            toolbar,
            text="🖨️ Print / HTML Export",
            font=get_font(size=12, weight="bold"),
            fg_color=COLOR_BURGUNDY,
            hover_color=COLOR_BURGUNDY_HOVER,
            text_color=COLOR_WHITE,
            height=34,
            corner_radius=6,
            command=self._export_print_itinerary
        )
        print_btn.pack(side="left", padx=(0, 10))

        # Add Extra Destination Button
        add_dest_btn = ctk.CTkButton(
            toolbar,
            text="➕ Add Destination",
            font=get_font(size=12),
            fg_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_BORDER,
            text_color=COLOR_DARK_TEXT,
            height=34,
            corner_radius=6,
            command=self._show_add_destination_dialog
        )
        add_dest_btn.pack(side="left", padx=(0, 10))

        # Generate Again Button
        regen_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Generate Again",
            font=get_font(size=12),
            fg_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_BORDER,
            text_color=COLOR_DARK_TEXT,
            height=34,
            corner_radius=6,
            command=self._generate_itinerary
        )
        regen_btn.pack(side="left")

        # Day Tabs Row
        day_tabs_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        day_tabs_frame.pack(fill="x", pady=(0, 15))

        for d in days:
            d_num = d.get("day_number")
            is_active = (d_num == self.active_day_tab)
            t_btn = ctk.CTkButton(
                day_tabs_frame,
                text=f"Day {d_num}",
                font=get_font(size=13, weight="bold"),
                fg_color=COLOR_NAVY if is_active else COLOR_WHITE,
                hover_color=COLOR_NAVY_HOVER if is_active else COLOR_LIGHT_GREY,
                text_color=COLOR_WHITE if is_active else COLOR_NAVY,
                border_width=1,
                border_color=COLOR_NAVY if is_active else COLOR_BORDER,
                height=36,
                width=90,
                corner_radius=8,
                command=lambda num=d_num: self._switch_day_tab(num)
            )
            t_btn.pack(side="left", padx=(0, 8))

        # Render active day timeline
        active_day_data = next((d for d in days if d.get("day_number") == self.active_day_tab), days[0] if days else None)
        if active_day_data:
            self._render_day_timeline(active_day_data)

        # Disclaimer Notice
        disc_box = ctk.CTkFrame(self.results_frame, fg_color=COLOR_TAG_BG, corner_radius=8)
        disc_box.pack(fill="x", pady=(20, 0))

        ctk.CTkLabel(
            disc_box,
            text=f"ℹ️ {itin.get('disclaimer')}",
            font=get_font(size=12),
            text_color=COLOR_MUTED_TEXT,
            wraplength=850,
            justify="left"
        ).pack(anchor="w", padx=16, pady=10)

    def _switch_day_tab(self, day_num: int) -> None:
        self.active_day_tab = day_num
        self._render_itinerary_results()

    def _render_day_timeline(self, day_data: dict) -> None:
        day_card = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        day_card.pack(fill="x")

        # Day Title Bar
        title_bar = ctk.CTkFrame(day_card, fg_color="transparent")
        title_bar.pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkLabel(
            title_bar,
            text=day_data.get("title", f"Day {day_data.get('day_number')}"),
            font=get_font(size=18, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(side="left")

        # Timeline Items
        schedule = day_data.get("schedule", [])
        for idx, item in enumerate(schedule):
            self._render_timeline_item(day_card, item, item_idx=idx, day_number=day_data.get("day_number"))

    def _render_timeline_item(self, parent: ctk.CTkFrame, item: dict, item_idx: int, day_number: int) -> None:
        is_food = item.get("is_food", False)
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FBF9F5" if is_food else COLOR_CARD_BG,
            corner_radius=8,
            border_width=1 if is_food else 0,
            border_color=COLOR_GOLD if is_food else COLOR_BORDER
        )
        item_frame.pack(fill="x", padx=20, pady=6)

        # Left: Time badge
        time_frame = ctk.CTkFrame(item_frame, fg_color="transparent", width=100)
        time_frame.pack(side="left", padx=(10, 15), pady=12)

        ctk.CTkLabel(
            time_frame,
            text=item.get("time", ""),
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_BURGUNDY if not is_food else COLOR_GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            time_frame,
            text=f"⏱ {item.get('duration', '1 hr')}",
            font=get_font(size=11),
            text_color=COLOR_MUTED_TEXT
        ).pack(anchor="w")

        # Center: Content Details
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, pady=10)

        # Header: Name & Neighbourhood badge
        head_row = ctk.CTkFrame(content, fg_color="transparent")
        head_row.pack(fill="x")

        icon = "🍽️ " if is_food else "📍 "
        name_lbl = ctk.CTkLabel(
            head_row,
            text=f"{icon}{item.get('name', '')}",
            font=get_font(size=14, weight="bold"),
            text_color=COLOR_NAVY
        )
        name_lbl.pack(side="left")

        if item.get("neighbourhood"):
            nh_lbl = ctk.CTkLabel(
                head_row,
                text=f"({item.get('neighbourhood')})",
                font=get_font(size=12),
                text_color=COLOR_MUTED_TEXT
            )
            nh_lbl.pack(side="left", padx=6)

        # Description
        desc_lbl = ctk.CTkLabel(
            content,
            text=item.get("description", ""),
            font=get_font(size=12),
            text_color=COLOR_DARK_TEXT,
            wraplength=480,
            justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(2, 0))

        # Right Actions: View details or Remove
        right_actions = ctk.CTkFrame(item_frame, fg_color="transparent")
        right_actions.pack(side="right", padx=(10, 15), pady=10)

        dest_id = item.get("id")
        if dest_id:
            view_btn = ctk.CTkButton(
                right_actions,
                text="Details",
                font=get_font(size=11),
                fg_color=COLOR_LIGHT_GREY,
                hover_color=COLOR_BORDER,
                text_color=COLOR_NAVY,
                height=28,
                width=65,
                corner_radius=4,
                command=lambda d=dest_id: self.open_detail(d)
            )
            view_btn.pack(side="left", padx=(0, 6))

        # Remove item button
        del_btn = ctk.CTkButton(
            right_actions,
            text="✕",
            font=get_font(size=11, weight="bold"),
            fg_color="transparent",
            hover_color="#FFEEEE",
            text_color="#C0392B",
            height=28,
            width=28,
            corner_radius=4,
            command=lambda d_num=day_number, idx=item_idx: self._remove_item_from_day(d_num, idx)
        )
        del_btn.pack(side="left")

    def _remove_item_from_day(self, day_number: int, item_idx: int) -> None:
        if not self.current_itinerary:
            return
        days = self.current_itinerary.get("days", [])
        for d in days:
            if d.get("day_number") == day_number:
                sched = d.get("schedule", [])
                if 0 <= item_idx < len(sched):
                    sched.pop(item_idx)
                break
        self._render_itinerary_results()

    def _save_current_itinerary(self) -> None:
        if not self.current_itinerary:
            return
        saved_id = self.data_manager.save_itinerary(self.current_itinerary)
        self.saved_nav_btn.configure(text=f"📂 Saved Itineraries ({len(self.data_manager.get_saved_itineraries())})")

        # Visual confirmation notification banner
        toast = ctk.CTkFrame(self.results_frame, fg_color=COLOR_GOLD, corner_radius=8)
        toast.pack(fill="x", pady=(0, 10), before=self.results_frame.winfo_children()[0])
        ctk.CTkLabel(
            toast,
            text=f"✓ Itinerary successfully saved! Access it anytime from 'Saved Itineraries'.",
            font=get_font(size=13, weight="bold"),
            text_color=COLOR_NAVY
        ).pack(padx=16, pady=8)
        self.after(3500, toast.destroy)

    def _export_print_itinerary(self) -> None:
        if not self.current_itinerary:
            return
        file_path = ItineraryGenerator.export_html(self.current_itinerary)
        try:
            webbrowser.open(f"file://{file_path}")
        except Exception as e:
            print(f"[ItineraryView] Error opening browser: {e}")

    def _show_add_destination_dialog(self) -> None:
        """Modal dialog to select a destination and add it to the active day."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Destination to Itinerary")
        dialog.geometry("500x420")
        dialog.configure(fg_color=COLOR_BG)
        dialog.transient(self.winfo_toplevel())

        ctk.CTkLabel(
            dialog,
            text="Add Destination to Current Day",
            font=get_font(size=16, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(padx=20, pady=(20, 10))

        # Destination selection list
        dests = self.data_manager.get_all_destinations()
        dest_names = [d.get("name") for d in dests]

        combo = ctk.CTkComboBox(
            dialog,
            values=dest_names,
            width=380,
            height=36,
            font=get_font(size=13)
        )
        combo.pack(padx=20, pady=10)

        # Time entry
        ctk.CTkLabel(
            dialog,
            text="Suggested Time Slot (e.g. 04:00 PM):",
            font=get_font(size=12),
            text_color=COLOR_DARK_TEXT
        ).pack(anchor="w", padx=60, pady=(10, 2))

        time_entry = ctk.CTkEntry(dialog, width=380, height=36, font=get_font(size=13))
        time_entry.insert(0, "04:00 PM")
        time_entry.pack(padx=20, pady=5)

        def do_add():
            chosen_name = combo.get()
            chosen_time = time_entry.get().strip() or "04:00 PM"
            match_dest = next((d for d in dests if d.get("name") == chosen_name), None)
            if match_dest and self.current_itinerary:
                for day in self.current_itinerary.get("days", []):
                    if day.get("day_number") == self.active_day_tab:
                        day.get("schedule", []).append({
                            "time": chosen_time,
                            "type": "activity",
                            "id": match_dest.get("id"),
                            "name": match_dest.get("name"),
                            "neighbourhood": match_dest.get("neighbourhood"),
                            "duration": match_dest.get("duration", "1.5 hours"),
                            "description": match_dest.get("short_description"),
                            "category": match_dest.get("category"),
                            "is_food": False
                        })
                        break
                dialog.destroy()
                self._render_itinerary_results()

        add_btn = ctk.CTkButton(
            dialog,
            text="Add to Day Schedule",
            font=get_font(size=13, weight="bold"),
            fg_color=COLOR_BURGUNDY,
            hover_color=COLOR_BURGUNDY_HOVER,
            text_color=COLOR_WHITE,
            height=38,
            command=do_add
        )
        add_btn.pack(pady=20)

    def _show_saved_itineraries_dialog(self) -> None:
        """Modal dialog to browse and load previously saved itineraries."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Saved London Itineraries")
        dialog.geometry("600x500")
        dialog.configure(fg_color=COLOR_BG)
        dialog.transient(self.winfo_toplevel())

        ctk.CTkLabel(
            dialog,
            text="Saved London Itineraries",
            font=get_font(size=18, weight="bold", serif=True),
            text_color=COLOR_NAVY
        ).pack(padx=20, pady=(20, 10))

        saved = self.data_manager.get_saved_itineraries()
        if not saved:
            ctk.CTkLabel(
                dialog,
                text="No saved itineraries found yet.\nGenerate an itinerary and click 'Save Itinerary'!",
                font=get_font(size=13),
                text_color=COLOR_MUTED_TEXT,
                justify="center"
            ).pack(pady=40)
            return

        scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for item in saved:
            card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD_BG, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            card.pack(fill="x", pady=6)

            left = ctk.CTkFrame(card, fg_color="transparent")
            left.pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(
                left,
                text=item.get("title", "London Trip"),
                font=get_font(size=14, weight="bold"),
                text_color=COLOR_NAVY
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=f"📅 {item.get('duration_days')} Days • Created: {item.get('created_at', '')}",
                font=get_font(size=11),
                text_color=COLOR_MUTED_TEXT
            ).pack(anchor="w")

            # Actions
            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=15, pady=12)

            def make_load_cmd(it):
                return lambda: self._load_itinerary(it, dialog)

            load_btn = ctk.CTkButton(
                btn_frame,
                text="Load",
                font=get_font(size=12, weight="bold"),
                fg_color=COLOR_NAVY,
                text_color=COLOR_WHITE,
                height=30,
                width=60,
                command=make_load_cmd(item)
            )
            load_btn.pack(side="left", padx=(0, 6))

            def make_del_cmd(itin_id):
                return lambda: self._delete_saved_itin(itin_id, dialog)

            del_btn = ctk.CTkButton(
                btn_frame,
                text="Delete",
                font=get_font(size=12),
                fg_color=COLOR_LIGHT_GREY,
                hover_color="#FFDDDD",
                text_color="#C0392B",
                height=30,
                width=60,
                command=make_del_cmd(item.get("id"))
            )
            del_btn.pack(side="left")

    def _load_itinerary(self, item: dict, dialog: ctk.CTkToplevel) -> None:
        self.current_itinerary = item
        self.active_day_tab = 1
        dialog.destroy()
        self._render_itinerary_results()

    def _delete_saved_itin(self, itin_id: str, dialog: ctk.CTkToplevel) -> None:
        self.data_manager.delete_itinerary(itin_id)
        dialog.destroy()
        self.saved_nav_btn.configure(text=f"📂 Saved Itineraries ({len(self.data_manager.get_saved_itineraries())})")
        self._show_saved_itineraries_dialog()
