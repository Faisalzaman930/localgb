#!/usr/bin/env python3
"""Download Unsplash images and apply a cartoonish effect."""

import requests
import io
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

IMAGES = {
    "hero-k2":           "https://images.unsplash.com/photo-1580502304784-8985b7eb7260?w=1600&q=85",  # K2/Karakoram peaks
    "hero-hunza":        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600&q=85",  # Hunza valley
    "hero-fairy-meadows":"https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=1600&q=85",  # mountain meadow
    "hero-gilgit":       "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600&q=85",  # mountain town
    "hero-nanga-parbat": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=85",  # dramatic peak
    "hero-blossom":      "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1600&q=85",  # cherry blossom
    "hero-stargazing":   "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1600&q=85",  # stars milky way
    "hero-islamabad":    "https://images.unsplash.com/photo-1548013146-72479768bada?w=1600&q=85",  # road mountain
}

def cartoonify(img):
    """Apply cartoon/comic-book effect."""
    # 1. Resize for consistency
    img = img.convert("RGB")
    w, h = img.size
    img = img.resize((1200, int(h * 1200 / w)), Image.LANCZOS)

    # 2. Boost saturation strongly
    img = ImageEnhance.Color(img).enhance(2.2)

    # 3. Boost contrast
    img = ImageEnhance.Contrast(img).enhance(1.4)

    # 4. Posterize (reduce colour depth — flat comic look)
    img = ImageOps.posterize(img, 4)

    # 5. Smooth slightly to blend the flat areas
    img = img.filter(ImageFilter.SMOOTH_MORE)

    # 6. Edge detection overlay
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    edges = ImageEnhance.Contrast(edges).enhance(3.0)
    # Invert: white edges on black → black edges on transparent
    edges = ImageOps.invert(edges).convert("RGB")

    # 7. Blend edges onto the posterized image (darken mode approximation)
    from PIL import ImageChops
    result = ImageChops.multiply(img, edges)

    # 8. Final brightness lift
    result = ImageEnhance.Brightness(result).enhance(1.15)

    return result

headers = {"User-Agent": "Mozilla/5.0"}
out_dir = "/Users/mac/Desktop/localgb/images"

for name, url in IMAGES.items():
    print(f"Downloading {name}...", end=" ", flush=True)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        img = Image.open(io.BytesIO(r.content))
        cartoon = cartoonify(img)
        out_path = f"{out_dir}/{name}.jpg"
        cartoon.save(out_path, "JPEG", quality=88, optimize=True)
        size_kb = len(open(out_path,"rb").read()) // 1024
        print(f"saved {size_kb}KB → {out_path}")
    except Exception as e:
        print(f"FAILED: {e}")

print("Done.")
