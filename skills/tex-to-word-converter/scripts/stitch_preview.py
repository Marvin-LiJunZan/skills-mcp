from PIL import Image
import os

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
im_a = Image.open(os.path.join(out_dir, "sub_a.png"))
im_b = Image.open(os.path.join(out_dir, "sub_b.png"))
im_c = Image.open(os.path.join(out_dir, "sub_c.png"))
im_d = Image.open(os.path.join(out_dir, "sub_d.png"))

w, h = im_a.size
gap = 40
combined = Image.new("RGB", (w * 2 + gap, h * 2 + gap), (255, 255, 255))

combined.paste(im_a, (0, 0))
combined.paste(im_b, (w + gap, 0))
combined.paste(im_c, (0, h + gap))
combined.paste(im_d, (w + gap, h + gap))

stitch_path = os.path.join(out_dir, "preview_2x2_subfigures.png")
combined.save(stitch_path)
print("[OK] Preview image stitched successfully.")
