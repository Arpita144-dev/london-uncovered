"""Asset download utility for London Uncovered.

Downloads high-quality, authentic London photography from Unsplash
and provides a PIL-based procedural fallback generator for offline
environments.
"""

import os
import sys
import ssl
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"

IMAGE_CATALOG = {
    "london_hero.jpg": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1400&q=85",
    "big_ben.jpg": "https://images.unsplash.com/photo-1529655683826-aba9b3e77383?auto=format&fit=crop&w=900&q=85",
    "tower_bridge.jpg": "https://images.unsplash.com/photo-1513026705753-bc3fffca8bf4?auto=format&fit=crop&w=900&q=85",
    "buckingham_palace.jpg": "https://images.unsplash.com/photo-1584467541268-b040f83be3fd?auto=format&fit=crop&w=900&q=85",
    "london_eye.jpg": "https://images.unsplash.com/photo-1520986606214-8b456906c813?auto=format&fit=crop&w=900&q=85",
    "westminster_abbey.jpg": "https://images.unsplash.com/photo-1544077960-604201fe74bc?auto=format&fit=crop&w=900&q=85",
    "st_pauls.jpg": "https://images.unsplash.com/photo-1526129318478-62ed807ebdf9?auto=format&fit=crop&w=900&q=85",
    "natural_history_museum.jpg": "https://images.unsplash.com/photo-1569974498991-d3c12a504f95?auto=format&fit=crop&w=900&q=85",
    "british_museum.jpg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=900&q=85",
    "hyde_park.jpg": "https://images.unsplash.com/photo-1577717903315-1691ae25ab3f?auto=format&fit=crop&w=900&q=85",
    "covent_garden.jpg": "https://images.unsplash.com/photo-1582234372722-50d7ccc30ebd?auto=format&fit=crop&w=900&q=85",
    "borough_market.jpg": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=900&q=85",
    "camden_market.jpg": "https://images.unsplash.com/photo-1579208575657-c595a05383b7?auto=format&fit=crop&w=900&q=85",
    "notting_hill.jpg": "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=900&q=85",
    "greenwich.jpg": "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=900&q=85",
    "leadenhall_market.jpg": "https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=900&q=85",
    "little_venice.jpg": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=900&q=85",
    "neals_yard.jpg": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=85",
    "hampstead_heath.jpg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=85",
    "soho.jpg": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=85",
    "shoreditch.jpg": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=900&q=85",
    "south_bank.jpg": "https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=900&q=85",
    "afternoon_tea.jpg": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=900&q=85",
    "chinatown.jpg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=900&q=85",
    "british_food.jpg": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=900&q=85",
    "tube_transport.jpg": "https://images.unsplash.com/photo-1543783207-ec64e4d95325?auto=format&fit=crop&w=900&q=85"
}

def generate_placeholder(filename: str, width: int = 800, height: int = 500) -> None:
    """Generate an elegant editorial placeholder if network is unavailable."""
    title = filename.replace(".jpg", "").replace("_", " ").title()
    img = Image.new("RGB", (width, height), color="#142B3B")
    draw = ImageDraw.Draw(img)

    # Gradient-like decorative borders & accents
    draw.rectangle([10, 10, width - 10, height - 10], outline="#C5A46D", width=2)
    draw.rectangle([16, 16, width - 16, height - 16], outline="#762E3D", width=1)

    # Header badge
    draw.text((width // 2, height // 2 - 40), "LONDON UNCOVERED", fill="#C5A46D", anchor="mm")
    draw.text((width // 2, height // 2 + 10), title, fill="#FFFFFF", anchor="mm")
    draw.text((width // 2, height // 2 + 50), "✦ Visual Destination Guide ✦", fill="#E9E5DE", anchor="mm")

    output_path = ASSETS_DIR / filename
    img.save(output_path, "JPEG", quality=90)


def download_single(name: str, url: str) -> bool:
    target_path = ASSETS_DIR / name
    if target_path.exists() and target_path.stat().st_size > 10000:
        return True

    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LondonUncoveredApp/1.0"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as response:
            if response.status == 200:
                data = response.read()
                with open(target_path, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"Failed downloading {name}: {e}")
        return False


def ensure_all_assets() -> None:
    """Download images or generate high-quality fallback placeholders."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    total = len(IMAGE_CATALOG)
    success = 0

    print(f"Checking {total} visual assets in {ASSETS_DIR}...")
    for name, url in IMAGE_CATALOG.items():
        ok = download_single(name, url)
        if ok:
            success += 1
        else:
            print(f"Generating fallback art for {name}...")
            generate_placeholder(name)

    print(f"Asset check complete: {success}/{total} downloaded, all present.")


if __name__ == "__main__":
    ensure_all_assets()
