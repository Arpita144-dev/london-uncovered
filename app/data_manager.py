"""Data access layer for destinations, experiences, favourites, and itineraries."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from app.config import DATA_DIR, STORAGE_DIR


class DataManager:
    """Manages reading and writing application data with robust error handling."""

    def __init__(self):
        self._destinations: List[Dict[str, Any]] = []
        self._experiences: List[Dict[str, Any]] = []
        self._neighbourhoods: List[Dict[str, Any]] = []
        self._food_guide: List[Dict[str, Any]] = []
        self._travel_tips: List[Dict[str, Any]] = []

        self._favourites_file = STORAGE_DIR / "favourites.json"
        self._itineraries_file = STORAGE_DIR / "saved_itineraries.json"

        self._favourite_ids: Set[str] = set()
        self._custom_trip_destination_ids: List[str] = []

        # Load initial datasets
        self.reload_all_data()

    def reload_all_data(self) -> None:
        """Load or reload all local JSON files."""
        self._destinations = self._load_json(DATA_DIR / "destinations.json", default=[])
        self._experiences = self._load_json(DATA_DIR / "experiences.json", default=[])
        self._neighbourhoods = self._load_json(DATA_DIR / "neighbourhoods.json", default=[])
        self._food_guide = self._load_json(DATA_DIR / "food_guide.json", default=[])
        self._travel_tips = self._load_json(DATA_DIR / "travel_tips.json", default=[])
        self._load_favourites()

    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Safely load JSON from disk, falling back gracefully on error."""
        if not file_path.exists():
            return default
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[DataManager] Failed to load {file_path.name}: {e}")
            return default

    def _save_json(self, file_path: Path, data: Any) -> bool:
        """Safely save JSON to disk with pretty formatting."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[DataManager] Failed to save {file_path.name}: {e}")
            return False

    # --- Destinations ---

    def get_all_destinations(self) -> List[Dict[str, Any]]:
        return list(self._destinations)

    def get_destination_by_id(self, dest_id: str) -> Optional[Dict[str, Any]]:
        for d in self._destinations:
            if d.get("id") == dest_id:
                return d
        return None

    def get_featured_destinations(self) -> List[Dict[str, Any]]:
        return [d for d in self._destinations if d.get("featured", False)]

    def get_hidden_gems(self) -> List[Dict[str, Any]]:
        return [d for d in self._destinations if d.get("is_hidden_gem", False)]

    def get_destinations_by_neighbourhood(self, neighbourhood: str) -> List[Dict[str, Any]]:
        target = neighbourhood.lower()
        return [d for d in self._destinations if target in d.get("neighbourhood", "").lower()]

    def search_destinations(self, query: str = "", category: str = "All") -> List[Dict[str, Any]]:
        """Search destinations by text query across name, neighbourhood, category, and keywords."""
        cleaned_query = query.strip().lower()
        cleaned_category = category.strip()

        results = []
        for d in self._destinations:
            # Check category filter
            dest_cat = d.get("category", "")
            if cleaned_category != "All":
                if cleaned_category == "Hidden Gems":
                    if not d.get("is_hidden_gem", False):
                        continue
                elif cleaned_category.lower() not in dest_cat.lower():
                    continue

            # Check search query
            if cleaned_query:
                name_match = cleaned_query in d.get("name", "").lower()
                nh_match = cleaned_query in d.get("neighbourhood", "").lower()
                cat_match = cleaned_query in dest_cat.lower()
                desc_match = cleaned_query in d.get("short_description", "").lower()
                keywords = [k.lower() for k in d.get("keywords", [])]
                kw_match = any(cleaned_query in k for k in keywords)

                if not (name_match or nh_match or cat_match or desc_match or kw_match):
                    continue

            results.append(d)

        return results

    # --- Experiences, Neighbourhoods, Food, Tips ---

    def get_experiences(self) -> List[Dict[str, Any]]:
        return list(self._experiences)

    def get_neighbourhoods(self) -> List[Dict[str, Any]]:
        return list(self._neighbourhoods)

    def get_food_guide(self) -> List[Dict[str, Any]]:
        return list(self._food_guide)

    def get_travel_tips(self) -> List[Dict[str, Any]]:
        return list(self._travel_tips)

    # --- Favourites Persistence ---

    def _load_favourites(self) -> None:
        raw = self._load_json(self._favourites_file, default=[])
        if isinstance(raw, list):
            self._favourite_ids = set(raw)
        else:
            self._favourite_ids = set()

    def get_favourite_ids(self) -> Set[str]:
        return set(self._favourite_ids)

    def is_favourite(self, dest_id: str) -> bool:
        return dest_id in self._favourite_ids

    def toggle_favourite(self, dest_id: str) -> bool:
        """Toggle favourite status and persist immediately. Returns True if now favourite."""
        if dest_id in self._favourite_ids:
            self._favourite_ids.remove(dest_id)
            status = False
        else:
            self._favourite_ids.add(dest_id)
            status = True

        self._save_json(self._favourites_file, list(self._favourite_ids))
        return status

    def remove_favourite(self, dest_id: str) -> None:
        if dest_id in self._favourite_ids:
            self._favourite_ids.remove(dest_id)
            self._save_json(self._favourites_file, list(self._favourite_ids))

    def get_favourite_destinations(self) -> List[Dict[str, Any]]:
        return [d for d in self._destinations if d.get("id") in self._favourite_ids]

    # --- Custom User Trip Queue ("Add to My Trip") ---

    def get_trip_destinations(self) -> List[Dict[str, Any]]:
        return [d for d in self._destinations if d.get("id") in self._custom_trip_destination_ids]

    def get_trip_destination_ids(self) -> List[str]:
        return list(self._custom_trip_destination_ids)

    def add_to_trip(self, dest_id: str) -> bool:
        if dest_id not in self._custom_trip_destination_ids:
            self._custom_trip_destination_ids.append(dest_id)
            return True
        return False

    def remove_from_trip(self, dest_id: str) -> bool:
        if dest_id in self._custom_trip_destination_ids:
            self._custom_trip_destination_ids.remove(dest_id)
            return True
        return False

    def clear_trip(self) -> None:
        self._custom_trip_destination_ids.clear()

    # --- Saved Itineraries Persistence ---

    def get_saved_itineraries(self) -> List[Dict[str, Any]]:
        data = self._load_json(self._itineraries_file, default=[])
        if isinstance(data, list):
            return data
        return []

    def save_itinerary(self, itinerary_data: Dict[str, Any]) -> str:
        """Persist a generated itinerary to storage. Returns the saved ID."""
        itineraries = self.get_saved_itineraries()
        itin_id = itinerary_data.get("id") or str(uuid.uuid4())[:8]
        itinerary_data["id"] = itin_id
        if "created_at" not in itinerary_data:
            itinerary_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Replace existing or append
        existing_idx = next((i for i, item in enumerate(itineraries) if item.get("id") == itin_id), -1)
        if existing_idx >= 0:
            itineraries[existing_idx] = itinerary_data
        else:
            itineraries.insert(0, itinerary_data)

        self._save_json(self._itineraries_file, itineraries)
        return itin_id

    def delete_itinerary(self, itinerary_id: str) -> bool:
        itineraries = self.get_saved_itineraries()
        filtered = [item for item in itineraries if item.get("id") != itinerary_id]
        if len(filtered) != len(itineraries):
            self._save_json(self._itineraries_file, filtered)
            return True
        return False
