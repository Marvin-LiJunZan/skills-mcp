import os
import win32com.client
from pdf2image import convert_from_path

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
docx_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_Three_Line_Table_Demo.docx"))
pdf_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_Three_Line_Table_Demo.pdf"))
png_path = os.path.abspath(os.path.join(out_dir, "preview_three_line_table.png"))

try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(docx_path)
    # Save as PDF (wdFormatPDF = 17)
    doc.SaveAs(pdf_path, FileFormat=17)
    doc.Close()
    word.Quit()
    print("[OK] Converted docx to PDF via Word COM.")
    
    # Try render PDF to PNG
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)
        if images:
            images[0].save(png_path, "PNG")
            print("[OK] Rendered preview PNG.")
    except Exception as img_err:
        print(f"[Info] pdf2image skipped: {img_err}")
except Exception as e:
    print(f"[Warning] Word COM export failed: {e}")
