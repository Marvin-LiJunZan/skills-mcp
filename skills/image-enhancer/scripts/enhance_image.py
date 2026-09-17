#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Enhancer Script for Academic & Technical Figures
Supports Real-ESRGAN / High-fidelity Lanczos Resampling with Unsharp Mask
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

def enhance_with_realesrgan(input_path: Path, output_path: Path, scale: int = 4) -> bool:
    """Try invoking local realesrgan-ncnn-vulkan if available."""
    bin_dir = Path(__file__).resolve().parent.parent / "bin"
    candidates = [
        bin_dir / "realesrgan-ncnn-vulkan.exe",
        shutil.which("realesrgan-ncnn-vulkan"),
        shutil.which("realesrgan-ncnn-vulkan.exe")
    ]
    exe = next((c for c in candidates if c and Path(c).is_file()), None)
    if not exe:
        return False

    print(f"[*] Found Real-ESRGAN engine: {exe}")
    cmd = [
        str(exe),
        "-i", str(input_path),
        "-o", str(output_path),
        "-s", str(scale),
        "-n", "realesrgan-x4plus"
    ]
    try:
        ret = subprocess.run(cmd, check=True)
        return ret.returncode == 0
    except Exception as e:
        print(f"[-] Real-ESRGAN execution failed: {e}. Falling back to high-order sharpening.")
        return False

def enhance_with_pillow(input_path: Path, output_path: Path, scale: int = 4) -> bool:
    """High-order Lanczos resampling + Unsharp Mask filtering fallback."""
    try:
        from PIL import Image, ImageFilter, ImageEnhance
    except ImportError:
        print("[-] Pillow not installed. Trying to install pillow...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"], check=True)
        from PIL import Image, ImageFilter, ImageEnhance

    print(f"[*] Running High-order Resampling & Sharpening on: {input_path}")
    img = Image.open(input_path)
    
    # Convert RGBA / P safely if needed
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info else "RGB")

    new_width = img.width * scale
    new_height = img.height * scale

    # 1. High quality Lanczos upscale
    upscaled = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 2. Unsharp mask (enhance line edges and text in scientific figures)
    sharpened = upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # 3. Micro contrast enhancement
    if sharpened.mode == "RGBA":
        r, g, b, a = sharpened.split()
        rgb_img = Image.merge("RGB", (r, g, b))
        enhancer = ImageEnhance.Contrast(rgb_img)
        rgb_enhanced = enhancer.enhance(1.08)
        r2, g2, b2 = rgb_enhanced.split()
        final_img = Image.merge("RGBA", (r2, g2, b2, a))
    else:
        enhancer = ImageEnhance.Contrast(sharpened)
        final_img = enhancer.enhance(1.08)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_img.save(output_path, quality=95)
    print(f"[+] Enhanced image saved: {output_path} ({new_width}x{new_height})")
    return True

def main():
    parser = argparse.ArgumentParser(description="Image Resolution Enhancer Skill")
    parser.add_argument("--input", "-i", required=True, help="Input image file path")
    parser.add_argument("--output", "-o", help="Output image file path (optional)")
    parser.add_argument("--scale", "-s", type=int, default=4, help="Upscale factor: 2 or 4 (default 4)")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.is_file():
        print(f"[!] Error: Input file not found: {input_path}")
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_name(f"{input_path.stem}_enhanced_x{args.scale}{input_path.suffix}")

    # Step 1: Try Real-ESRGAN
    success = enhance_with_realesrgan(input_path, output_path, args.scale)
    if not success:
        # Step 2: Fallback to high-order filtering
        enhance_with_pillow(input_path, output_path, args.scale)

if __name__ == "__main__":
    main()
