"""
Academic Standard Sub/Superscript & Italic Engine for tex-to-word-converter.
Enforces International Standard (ISO 80000-2 / IUPAP / Elsevier / Nature):
1. Physical variables (scalar variables, tensors, coordinates): ITALIC (e.g. c, p, q, u, K, x, y, z, \sigma, \varepsilon, \phi)
2. Units and Chemical formulas: REGULAR / ROMAN (e.g. g/cm³, kPa, MPa, kN, m/s, CO₂, Fe₂O₃)
3. Mathematical index subscripts (i, j, k, x, y, z): ITALIC
4. Descriptive/textual subscripts (max, min, ref, vol, cr, opt, ini, res): REGULAR / ROMAN
5. Numerical indices (1, 2, 3, 0): REGULAR / ROMAN
6. Degree signs and temperatures (20 °C, 45°): REGULAR / ROMAN
"""
import re
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

GREEK_SYMS = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'varepsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'vartheta': 'θ',
    'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν',
    'xi': 'ξ', 'pi': 'π', 'varpi': 'ϖ', 'rho': 'ρ', 'varrho': 'ϱ',
    'sigma': 'σ', 'varsigma': 'ς', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ',
    'varphi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
    'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ', 'Xi': 'Ξ',
    'Pi': 'Π', 'Sigma': 'Σ', 'Upsilon': 'Υ', 'Phi': 'Φ', 'Psi': 'Ψ', 'Omega': 'Ω',
    'pm': '±', 'times': '×', 'div': '÷', 'cdot': '·', 'leq': '≤', 'le': '≤',
    'geq': '≥', 'ge': '≥', 'neq': '≠', 'ne': '≠', 'approx': '≈', 'sim': '~',
    'infty': '∞', 'nabla': '∇', 'partial': '∂', 'in': '∈', 'leftarrow': '←',
    'rightarrow': '→', 'leftrightarrow': '↔', 'degree': '°', 'circ': '°'
}

KNOWN_UNITS = {'g', 'kg', 'mg', 'm', 'cm', 'mm', 'km', 's', 'min', 'h', 'pa', 'kpa', 'mpa', 'gpa', 'n', 'kn', 'hz', 'khz', 'mhz', 'j', 'kj', 'w', 'kw', 'v', 'a', 'mol', 'l', 'ml', 'fe', 'o', 'c', 'h', 'si', 'al', 'ca'}
DESCRIPTIVE_SUBS = {'max', 'min', 'ref', 'vol', 'ult', 'opt', 'res', 'ini', 'crit', 'cr', 'nc', 'oc', 'drain', 'undrain', 'sat', 'dry'}

def should_italicize(text, is_sub=False):
    t = text.strip()
    tl = t.lower()
    if is_sub:
        if tl in DESCRIPTIVE_SUBS or t.isdigit() or re.match(r'^\d+([,\.]\w+)?$', t):
            return False
        if len(t) == 1 and t.isalpha():
            return True
        return False
    
    if tl in KNOWN_UNITS or '/' in t or t in ('°', '°C', '%'):
        return False
    if t.isdigit() or re.match(r'^\d+(\.\d+)?$', t):
        return False
    if len(t) == 1 and t.isalpha():
        return True
    if t in GREEK_SYMS.values() or tl in GREEK_SYMS:
        return True
    return False

def clean_text(t):
    if not t:
        return ""
    t = t.strip().replace('\\,', '').replace('\\ ', ' ').replace('{', '').replace('}', '')
    if t.startswith('\\'):
        t = t[1:]
    return GREEK_SYMS.get(t, t)

def create_run(text, italic=False, sub=False, sup=False):
    rPr = ['<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>']
    if italic:
        rPr.append('<w:i/>')
    if sub:
        rPr.append('<w:vertAlign w:val="subscript"/>')
    elif sup:
        rPr.append('<w:vertAlign w:val="superscript"/>')
        
    rPr_str = "".join(rPr)
    xml = f'<w:r {nsdecls("w")}><w:rPr>{rPr_str}</w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>'
    return parse_xml(xml)

def process_inline_element(child):
    runs = []
    
    # 1. Simultaneous Sub and Sup: m:sSubSup
    s_subsups = child.findall(qn('m:sSubSup'))
    if s_subsups:
        for node in s_subsups:
            e = "".join(node.find(qn('m:e')).itertext()).strip() if node.find(qn('m:e')) is not None else ""
            sub = "".join(node.find(qn('m:sub')).itertext()).strip() if node.find(qn('m:sub')) is not None else ""
            sup = "".join(node.find(qn('m:sup')).itertext()).strip() if node.find(qn('m:sup')) is not None else ""
            
            e_txt = clean_text(e)
            sub_txt = clean_text(sub)
            sup_txt = clean_text(sup)
            
            runs.append(create_run(e_txt, italic=should_italicize(e_txt)))
            runs.append(create_run(sub_txt, italic=should_italicize(sub_txt, is_sub=True), sub=True))
            if sup_txt in ('°', 'circ', '\\circ'):
                runs.append(create_run('°'))
            else:
                runs.append(create_run(sup_txt, sup=True))
        return runs

    # 2. Standalone Subscript: m:sSub
    s_subs = child.findall(qn('m:sSub'))
    if s_subs:
        for node in s_subs:
            e = "".join(node.find(qn('m:e')).itertext()).strip() if node.find(qn('m:e')) is not None else ""
            sub = "".join(node.find(qn('m:sub')).itertext()).strip() if node.find(qn('m:sub')) is not None else ""
            e_txt = clean_text(e)
            sub_txt = clean_text(sub)
            runs.append(create_run(e_txt, italic=should_italicize(e_txt)))
            runs.append(create_run(sub_txt, italic=should_italicize(sub_txt, is_sub=True), sub=True))
        return runs

    # 3. Standalone Superscript: m:sSup
    s_sups = child.findall(qn('m:sSup'))
    if s_sups:
        for node in s_sups:
            e = "".join(node.find(qn('m:e')).itertext()).strip() if node.find(qn('m:e')) is not None else ""
            sup = "".join(node.find(qn('m:sup')).itertext()).strip() if node.find(qn('m:sup')) is not None else ""
            e_txt = clean_text(e)
            sup_txt = clean_text(sup)
            runs.append(create_run(e_txt, italic=should_italicize(e_txt)))
            if sup_txt in ('°', 'circ'):
                runs.append(create_run('°'))
            else:
                runs.append(create_run(sup_txt, sup=True))
        return runs

    # 4. Plain symbol or variable
    raw_text = "".join(child.itertext()).strip()
    txt = clean_text(raw_text)
    runs.append(create_run(txt, italic=should_italicize(txt)))
    return runs

def sanitize_all_inline_math(docx_path):
    doc = Document(docx_path)
    total_converted = 0
    
    for p in doc.paragraphs:
        p_elm = p._p
        children = list(p_elm)
        for child in children:
            if child.tag == qn('m:oMath'):
                if child.getparent().tag == qn('m:oMathPara'):
                    continue
                runs = process_inline_element(child)
                if runs:
                    idx = p_elm.index(child)
                    p_elm.remove(child)
                    for r_node in reversed(runs):
                        p_elm.insert(idx, r_node)
                    total_converted += 1

    doc.save(docx_path)
    print(f"[OK] Sub/Superscript & Italic Engine: Processed {total_converted} element(s) with ISO standard italic/subscript rules.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sanitize_all_inline_math(sys.argv[1])
