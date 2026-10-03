from PIL import Image
import os

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
im1 = Image.open(os.path.join(out_dir, "master_template_page1.png"))
im2 = Image.open(os.path.join(out_dir, "master_template_page2.png"))

w, h = im1.size
gap = 30
combined = Image.new("RGB", (w * 2 + gap, h), (240, 240, 240))
combined.paste(im1, (0, 0))
combined.paste(im2, (w + gap, 0))

combined.save(os.path.join(out_dir, "master_template_preview_twopage.png"))
print("[OK] Stitched two pages preview.")
