import docx
from docx import Document

doc = Document(r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output\test_math_clean.docx")
p0 = doc.paragraphs[0]
print("Has m:oMath in P0?", '<m:oMath' in p0._p.xml)
print("P0 XML:", p0._p.xml)
