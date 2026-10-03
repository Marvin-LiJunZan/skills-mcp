import os
import win32com.client
from pdf2image import convert_from_path

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
docx_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_Master_Template.docx"))
pdf_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_Master_Template.pdf"))
png_p1 = os.path.abspath(os.path.join(out_dir, "master_template_page1.png"))
png_p2 = os.path.abspath(os.path.join(out_dir, "master_template_page2.png"))

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(docx_path)
doc.SaveAs(pdf_path, FileFormat=17) # wdFormatPDF = 17
doc.Close()
word.Quit()
print("[OK] Exported master template to PDF.")

images = convert_from_path(pdf_path, dpi=180)
if len(images) >= 1:
    images[0].save(png_p1, "PNG")
    print(f"[OK] Saved {png_p1}")
if len(images) >= 2:
    images[1].save(png_p2, "PNG")
    print(f"[OK] Saved {png_p2}")
