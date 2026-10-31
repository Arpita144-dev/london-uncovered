"""Image management, Pillow cropping, caching, and graceful fallback rendering."""

from pathlib import Path
from typing import Dict, Tuple, Optional
from PIL import Image, ImageOps, ImageDraw, ImageFont
import customtkinter as ctk

from app.config import (
    ASSETS_DIR,
    COLOR_NAVY,
    COLOR_GOLD,
    COLOR_BURGUNDY,
    COLOR_WHITE,
    COLOR_LIGHT_GREY
)


class ImageManager:
    """Manages loading, high-quality cropping (ImageOps.fit), and caching of images."""

    _cache: Dict[Tuple[str, int, int], ctk.CTkImage] = {}
    _keepalive: list = []  # Keeps strong references to prevent garbage collection

    @classmethod
    def get_image(
        cls,
        filename: str,
        width: int,
        height: int,
        fallback_title: Optional[str] = None
    ) -> ctk.CTkImage:
        """Load, crop without distortion, and return a cached CTkImage.

        If the image file is missing or fails to load, generates a magazine-style
        editorial placeholder with London Uncovered branding.
        """
        cache_key = (filename, width, height)
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        image_path = ASSETS_DIR / filename
        pil_image: Optional[Image.Image] = None

        if image_path.exists():
            try:
                with Image.open(image_path) as raw_img:
                    # Convert to RGB if needed
                    if raw_img.mode != "RGB":
                        raw_img = raw_img.convert("RGB")
                    # High quality crop and resize without distortion
                    pil_image = ImageOps.fit(
                        raw_img,
                        (width, height),
                        method=Image.Resampling.LANCZOS,
                        centering=(0.5, 0.5)
                    )
            except Exception as e:
                print(f"[ImageManager] Error loading {filename}: {e}. Generating fallback.")
                pil_image = None

        if pil_image is None:
            # Generate styled fallback image
            display_title = fallback_title or filename.replace(".jpg", "").replace("_", " ").title()
            pil_image = cls._create_editorial_placeholder(display_title, width, height)

        # Create CTkImage for high-DPI scaling
        ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(width, height))
        cls._cache[cache_key] = ctk_img
        cls._keepalive.append(ctk_img)
        return ctk_img

    @classmethod
    def _create_editorial_placeholder(cls, title: str, width: int, height: int) -> Image.Image:
        """Create an elegant London-themed editorial placeholder."""
        img = Image.new("RGB", (width, height), color=COLOR_NAVY)
        draw = ImageDraw.Draw(img)

        # Elegant double decorative border
        if width > 60 and height > 60:
            draw.rectangle([6, 6, width - 6, height - 6], outline=COLOR_GOLD, width=2)
            draw.rectangle([10, 10, width - 10, height - 10], outline=COLOR_BURGUNDY, width=1)

        # Decorative typography and insignia
        center_x = width // 2
        center_y = height // 2

        # Small brand crown / diamond
        draw.text((center_x, max(18, center_y - 32)), "✦ LONDON UNCOVERED ✦", fill=COLOR_GOLD, anchor="mm")

        # Destination name
        truncated_title = title if len(title) <= 24 else title[:21] + "..."
        draw.text((center_x, center_y), truncated_title, fill=COLOR_WHITE, anchor="mm")

        # Subtle subline
        draw.text((center_x, min(height - 18, center_y + 28)), "Visual Guide", fill=COLOR_LIGHT_GREY, anchor="mm")

        return img

    @classmethod
    def clear_cache(cls) -> None:
        """Clear cached image assets."""
        cls._cache.clear()
        cls._keepalive.clear()
