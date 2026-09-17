---
name: image-enhancer
description: Enhance image resolution, sharpen blurry figures, upscale academic diagrams, and restore low-resolution plots using Real-ESRGAN / AI super-resolution techniques.
---

# Image Enhancer Skill

Use this skill whenever you need to:
1. **Upscale low-resolution images**: Enlarge blurry plots, charts, architecture diagrams, or experimental scans (2x, 4x).
2. **Denoise and Sharpen**: Clarify blurry text, tick labels, or legend markers in academic figures.
3. **Batch restoration**: Enhance figures before paper drafting, journal submission, or presentation slide compilation.

## Architecture & Engines

The bundled Python script `scripts/enhance_image.py` supports multiple backends with automatic fallback:
- **Engine 1 (Local Real-ESRGAN NCNN / PyTorch)**: Ultra-high quality AI super-resolution (Vulkan / CUDA / TensorRT).
- **Engine 2 (Pillow / OpenCV High-order Lanczos & Unsharp Mask fallback)**: Guaranteed zero-dependency fallback that sharpens and upscales images instantly without GPU requirements.

## Quick CLI Usage

Run with Python (supports Windows `py -3.11` or standard `python`):

```powershell
# Upscale 4x with automatic sharpening
py -3.11 skills/image-enhancer/scripts/enhance_image.py --input "path/to/blurry.png" --scale 4

# Specify explicit output path
py -3.11 skills/image-enhancer/scripts/enhance_image.py --input "path/to/blurry.png" --output "path/to/enhanced.png" --scale 4
```

## Real-ESRGAN NCNN Integration
If Real-ESRGAN executable (`realesrgan-ncnn-vulkan.exe`) is placed in `skills/image-enhancer/bin/` or in system PATH, the script automatically activates the neural network for publication-grade diagram & photo restoration.
