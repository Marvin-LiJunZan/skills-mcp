import os
import fitz  # PyMuPDF
from PIL import Image

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
pdf_path = os.path.join(out_dir, "Publication_Grade_Master_Template.pdf")
doc = fitz.open(pdf_path)

images = []
for page_num in range(min(2, len(doc))):
    page = doc[page_num]
    pix = page.get_pixmap(dpi=150)
    png_path = os.path.join(out_dir, f"master_template_page_{page_num+1}.png")
    pix.save(png_path)
    images.append(Image.open(png_path))
    print(f"[OK] Saved page {page_num+1}: {png_path}")

if len(images) == 2:
    w, h = images[0].size
    gap = 30
    combined = Image.new("RGB", (w * 2 + gap, h), (230, 230, 230))
    combined.paste(images[0], (0, 0))
    combined.paste(images[1], (w + gap, 0))
    preview_all = os.path.join(out_dir, "master_template_preview_twopage.png")
    combined.save(preview_all)
    print(f"[SUCCESS] Generated side-by-side preview: {preview_all}")
