from docx import Document

doc = Document(r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output\test_sub_sup.docx")
p0 = doc.paragraphs[0]
print("P0 Runs inspection:")
for i, r in enumerate(p0.runs):
    style_info = []
    if r.font.italic: style_info.append("ITALIC")
    if r.font.subscript: style_info.append("SUB")
    if r.font.superscript: style_info.append("SUP")
    desc = f" [{', '.join(style_info)}]" if style_info else ""
    print(f"  [{i:02d}] '{r.text}'{desc}")
