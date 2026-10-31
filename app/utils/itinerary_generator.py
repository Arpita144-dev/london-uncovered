"""Rule-based, geo-aware London itinerary recommendation and export engine."""

import math
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.config import (
    COLOR_NAVY,
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_BG,
    COLOR_DARK_TEXT,
    STORAGE_DIR
)


class ItineraryGenerator:
    """Generates customized day-by-day itineraries based on user selections and geographic clustering."""

    PACE_ACTIVITY_COUNTS = {
        "Relaxed": 2,
        "Balanced": 3,
        "Packed": 5
    }

    TIME_SLOTS = {
        "Relaxed": ["10:00 AM", "02:30 PM", "07:00 PM"],
        "Balanced": ["09:30 AM", "11:30 AM", "02:30 PM", "05:00 PM", "07:30 PM"],
        "Packed": ["09:00 AM", "11:00 AM", "01:30 PM", "03:30 PM", "05:30 PM", "08:00 PM"]
    }

    INTEREST_TO_CATEGORIES = {
        "History & Landmarks": ["Landmarks", "History & Landmarks"],
        "Museums & Art": ["Museums"],
        "Food & Cafés": ["Food & Markets", "Food & Cafés"],
        "Shopping": ["Shopping", "Food & Markets"],
        "Nature & Parks": ["Parks"],
        "Photography": ["Landmarks", "Hidden Gems", "Scenic London"],
        "Hidden Gems": ["Hidden Gems"],
        "Culture & Entertainment": ["Museums", "Landmarks", "West End"]
    }

    FOOD_RECOMMENDATIONS = [
        {"name": "Borough Market Gourmet Lunch", "nh": "Southwark", "desc": "Artisan hot street food, raclette, and farmhouse cheeses."},
        {"name": "Traditional Afternoon Tea", "nh": "Covent Garden / Mayfair", "desc": "Warm clotted cream scones, delicate finger sandwiches, and fine tea."},
        {"name": "Soho & Chinatown Dinner", "nh": "Soho", "desc": "Dim sum, Cantonese roast duck, or buzzing Italian pasta bars."},
        {"name": "Camden Lock Waterside Street Food", "nh": "Camden", "desc": "Global street food eaten canal-side alongside the locks."},
        {"name": "Historic River Pub Dinner", "nh": "City / South Bank", "desc": "Traditional ale and Sunday roast overlooking the illuminated Thames."},
        {"name": "Brick Lane Curry Feast", "nh": "Shoreditch", "desc": "Aromatic regional biryanis, samosas, and freshly baked naan."}
    ]

    @classmethod
    def generate(
        cls,
        destinations: List[Dict[str, Any]],
        duration_days: int = 3,
        interests: Optional[List[str]] = None,
        budget: str = "Balanced",
        pace: str = "Balanced",
        user_trip_dest_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate a structured, personalised day-by-day travel plan."""
        interests = interests or ["History & Landmarks", "Food & Cafés"]
        user_trip_dest_ids = user_trip_dest_ids or []

        # Target number of primary activities per day
        acts_per_day = cls.PACE_ACTIVITY_COUNTS.get(pace, 3)
        total_acts_needed = duration_days * acts_per_day

        # 1. Score destinations based on match with user interests and priority picks
        scored_destinations = []
        user_selected_set = set(user_trip_dest_ids)

        # Map active interest categories
        active_categories = set()
        for interest in interests:
            active_categories.update(cls.INTEREST_TO_CATEGORIES.get(interest, []))

        for dest in destinations:
            score = 0.0
            dest_cat = dest.get("category", "")

            # Highest priority: user explicitly clicked 'Add to My Trip'
            if dest.get("id") in user_selected_set:
                score += 50.0

            # Direct category match
            if any(cat.lower() in dest_cat.lower() for cat in active_categories):
                score += 15.0

            # Hidden Gems bonus if selected
            if "Hidden Gems" in interests and dest.get("is_hidden_gem"):
                score += 20.0

            # Nature/Parks match
            if "Nature & Parks" in interests and "Park" in dest_cat:
                score += 18.0

            # Budget weighting
            cost_cat = dest.get("cost_category", "Moderate")
            if budget == "Budget-friendly":
                if cost_cat == "Free":
                    score += 12.0
                elif cost_cat == "Paid":
                    score -= 5.0
            elif budget == "Premium":
                if cost_cat in ("Paid", "Moderate"):
                    score += 6.0

            # Featured landmark baseline
            if dest.get("featured"):
                score += 5.0

            scored_destinations.append((score, dest))

        # Sort highest score first
        scored_destinations.sort(key=lambda x: x[0], reverse=True)
        candidate_pool = [d for _, d in scored_destinations]

        # 2. Cluster geographically across days to avoid zigzagging across London
        days = cls._cluster_into_days(
            candidate_pool=candidate_pool,
            duration_days=duration_days,
            acts_per_day=acts_per_day,
            pace=pace
        )

        itinerary = {
            "title": f"My {duration_days}-Day London Adventure",
            "duration_days": duration_days,
            "interests": interests,
            "budget": budget,
            "pace": pace,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "disclaimer": "This itinerary is an intelligent recommendation. Actual timings depend on opening hours, transport, and visitor preferences.",
            "days": days
        }
        return itinerary

    @classmethod
    def _cluster_into_days(
        cls,
        candidate_pool: List[Dict[str, Any]],
        duration_days: int,
        acts_per_day: int,
        pace: str
    ) -> List[Dict[str, Any]]:
        """Cluster candidate destinations into days based on proximity."""
        remaining = list(candidate_pool)
        days = []
        time_slots = cls.TIME_SLOTS.get(pace, cls.TIME_SLOTS["Balanced"])

        for day_idx in range(1, duration_days + 1):
            day_acts = []
            if not remaining:
                # Reset if pool exhausted for longer trips
                remaining = list(candidate_pool)

            # Pick anchor destination for the day
            anchor = remaining.pop(0)
            day_acts.append(anchor)

            # Find closest destinations to this day's anchor
            needed = acts_per_day - 1
            for _ in range(needed):
                if not remaining:
                    break
                closest_idx = cls._find_closest_dest_idx(anchor, remaining)
                day_acts.append(remaining.pop(closest_idx))

            # Assemble day schedule with times and food pause
            schedule = []
            food_recommendation = cls.FOOD_RECOMMENDATIONS[(day_idx - 1) % len(cls.FOOD_RECOMMENDATIONS)]

            slot_idx = 0
            for i, act in enumerate(day_acts):
                # Insert lunch suggestion around midday
                if i == 1 and slot_idx < len(time_slots):
                    lunch_time = "01:00 PM"
                    schedule.append({
                        "time": lunch_time,
                        "type": "food",
                        "name": food_recommendation["name"],
                        "neighbourhood": food_recommendation["nh"],
                        "duration": "1 hour",
                        "description": food_recommendation["desc"],
                        "is_food": True
                    })

                slot_time = time_slots[slot_idx] if slot_idx < len(time_slots) else f"{10 + slot_idx}:00"
                slot_idx += 1

                schedule.append({
                    "time": slot_time,
                    "type": "activity",
                    "id": act.get("id"),
                    "name": act.get("name"),
                    "neighbourhood": act.get("neighbourhood"),
                    "duration": act.get("duration", "1.5 hours"),
                    "description": act.get("short_description"),
                    "category": act.get("category"),
                    "tips": act.get("visitor_tips", ""),
                    "image_file": act.get("image_file", "london_hero.jpg"),
                    "is_food": False
                })

            # Determine dominant area for the day
            neighbourhoods = list({act.get("neighbourhood") for act in day_acts if act.get("neighbourhood")})
            day_title = f"Day {day_idx}: " + (" & ".join(neighbourhoods[:2]) if neighbourhoods else "City Exploration")

            days.append({
                "day_number": day_idx,
                "title": day_title,
                "schedule": schedule
            })

        return days

    @classmethod
    def _find_closest_dest_idx(cls, anchor: Dict[str, Any], pool: List[Dict[str, Any]]) -> int:
        anchor_lat = anchor.get("lat", 51.5074)
        anchor_lon = anchor.get("lon", -0.1278)

        best_idx = 0
        min_dist = float("inf")

        for idx, item in enumerate(pool):
            lat = item.get("lat", 51.5074)
            lon = item.get("lon", -0.1278)
            # Euclidean distance approximation for nearby coordinates
            dist = math.hypot(lat - anchor_lat, lon - anchor_lon)
            if dist < min_dist:
                min_dist = dist
                best_idx = idx

        return best_idx

    @classmethod
    def export_html(cls, itinerary: Dict[str, Any]) -> str:
        """Export itinerary as a styled, print-friendly HTML document and save to storage."""
        title = itinerary.get("title", "London Uncovered Itinerary")
        days = itinerary.get("days", [])
        disclaimer = itinerary.get("disclaimer", "")
        created_at = itinerary.get("created_at", "")
        duration = itinerary.get("duration_days", 1)
        pace = itinerary.get("pace", "Balanced")
        budget = itinerary.get("budget", "Balanced")

        days_html = ""
        for day in days:
            day_num = day.get("day_number")
            day_title = day.get("title")
            schedule_html = ""

            for item in day.get("schedule", []):
                time = item.get("time")
                name = item.get("name")
                nh = item.get("neighbourhood", "")
                dur = item.get("duration", "")
                desc = item.get("description", "")
                is_food = item.get("is_food", False)

                item_class = "timeline-item food-item" if is_food else "timeline-item"
                badge = f'<span class="badge">🍽️ Culinary Pause</span>' if is_food else f'<span class="badge duration">{dur}</span>'

                schedule_html += f"""
                <div class="{item_class}">
                    <div class="time-col">{time}</div>
                    <div class="content-col">
                        <div class="item-header">
                            <span class="item-name">{name}</span>
                            <span class="item-nh">📍 {nh}</span>
                            {badge}
                        </div>
                        <p class="item-desc">{desc}</p>
                    </div>
                </div>
                """

            days_html += f"""
            <div class="day-card">
                <div class="day-header">
                    <h2>{day_title}</h2>
                </div>
                <div class="timeline">
                    {schedule_html}
                </div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — London Uncovered</title>
<style>
    @media print {{
        body {{ background: #fff !important; color: #000 !important; font-size: 11pt; }}
        .no-print {{ display: none; }}
        .day-card {{ page-break-inside: avoid; border: 1px solid #ddd; }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: {COLOR_BG};
        color: {COLOR_DARK_TEXT};
        margin: 0;
        padding: 40px 20px;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background: #fff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 24px rgba(20, 43, 59, 0.08);
    }}
    .header {{
        border-bottom: 3px double {COLOR_GOLD};
        padding-bottom: 24px;
        margin-bottom: 30px;
        text-align: center;
    }}
    .brand {{
        font-size: 14px;
        letter-spacing: 3px;
        color: {COLOR_BURGUNDY};
        font-weight: 700;
        text-transform: uppercase;
    }}
    h1 {{
        font-family: Georgia, serif;
        color: {COLOR_NAVY};
        font-size: 32px;
        margin: 10px 0;
    }}
    .meta-bar {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
        font-size: 14px;
        color: #666;
    }}
    .day-card {{
        background: #fff;
        border: 1px solid #e0dad0;
        border-radius: 8px;
        margin-bottom: 30px;
        overflow: hidden;
    }}
    .day-header {{
        background: {COLOR_NAVY};
        color: #fff;
        padding: 14px 20px;
    }}
    .day-header h2 {{
        margin: 0;
        font-family: Georgia, serif;
        font-size: 20px;
    }}
    .timeline {{
        padding: 20px;
    }}
    .timeline-item {{
        display: flex;
        gap: 20px;
        padding: 14px 0;
        border-bottom: 1px solid #f0ede8;
    }}
    .timeline-item:last-child {{
        border-bottom: none;
    }}
    .food-item {{
        background: #fdfaf5;
        border-radius: 6px;
        padding: 12px 14px;
    }}
    .time-col {{
        font-weight: 700;
        color: {COLOR_BURGUNDY};
        width: 90px;
        flex-shrink: 0;
    }}
    .content-col {{
        flex-grow: 1;
    }}
    .item-header {{
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 4px;
    }}
    .item-name {{
        font-weight: 700;
        font-size: 16px;
        color: {COLOR_NAVY};
    }}
    .item-nh {{
        font-size: 13px;
        color: #666;
    }}
    .badge {{
        font-size: 12px;
        background: #f2ece1;
        color: {COLOR_NAVY};
        padding: 2px 8px;
        border-radius: 12px;
    }}
    .item-desc {{
        margin: 4px 0 0 0;
        font-size: 14px;
        color: #444;
        line-height: 1.5;
    }}
    .disclaimer {{
        margin-top: 30px;
        padding: 16px;
        background: #f8f6f0;
        border-left: 4px solid {COLOR_GOLD};
        font-size: 13px;
        color: #555;
        font-style: italic;
    }}
    .actions {{
        text-align: center;
        margin-bottom: 20px;
    }}
    button.print-btn {{
        background: {COLOR_NAVY};
        color: #fff;
        border: none;
        padding: 10px 24px;
        border-radius: 6px;
        font-size: 14px;
        cursor: pointer;
        font-weight: 600;
    }}
    button.print-btn:hover {{
        background: {COLOR_BURGUNDY};
    }}
</style>
</head>
<body>
<div class="container">
    <div class="actions no-print">
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
    <div class="header">
        <div class="brand">London Uncovered • Travel Guide</div>
        <h1>{title}</h1>
        <div class="meta-bar">
            <span>📅 {duration} Days</span>
            <span>⚡ Pace: {pace}</span>
            <span>💰 Budget: {budget}</span>
            <span>🕒 Created: {created_at}</span>
        </div>
    </div>
    {days_html}
    <div class="disclaimer">
        <strong>Visitor Notice:</strong> {disclaimer}
    </div>
</div>
</body>
</html>"""

        output_file = STORAGE_DIR / f"itinerary_{itinerary.get('id', 'custom')}.html"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"[ItineraryGenerator] Error writing HTML export: {e}")

        return str(output_file)
