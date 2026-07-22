"""
Prep a photo for ASCII conversion.

A flatly-lit face converts to a dark, unreadable blob. Three steps fix that:
  1. Remove the background with rembg so the subject is isolated.
  2. Boost local contrast with OpenCV's CLAHE (contrast-limited adaptive
     histogram equalization) -- gives a flat face real highlights/shadows.
  3. Composite onto pure white so the background maps to the blank end of
     the ASCII ramp (white -> spaces).

Usage:
    python scripts/prep_photo.py source-photo.jpg
Output:
    source-prepped.png (grayscale, ready for make_ascii_svg.py)
"""

import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep(input_path: str, output_path: str = "source-prepped.png"):
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    # 1. Remove background -> RGBA with alpha mask around the subject.
    result_bytes = remove(input_bytes)
    rgba = Image.open(__import__("io").BytesIO(result_bytes)).convert("RGBA")

    # Composite onto pure white using the alpha channel.
    white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba).convert("RGB")

    # 2. Boost local contrast with CLAHE on the grayscale version.
    gray = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    contrasted = clahe.apply(gray)

    # 3. Re-flatten background to white (CLAHE can slightly lift it off pure white).
    _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    contrasted[mask == 255] = 255

    Image.fromarray(contrasted).save(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep(sys.argv[1])
