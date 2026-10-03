"""
Comprehensive test for complex academic sub/superscripts:
1. Multi-level / compound subscripts: \sigma_{v0}', \varepsilon_{vol}, K_{0,nc}, p'_{ref}
2. Simultaneous sub and superscripts: \sigma_1^2, c_u^{(t)}, \tau_{max}^*, F_s^{min}
3. Complex units and chemistry: g/cm^3, m^3/s, Fe_2O_3, CO_2
4. Temperature and degrees: 20^\circ C, \pm 0.5\%
"""
import re
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

def parse_compound_inline_math(math_text):
    """
    Test parser that decomposes complex inline math into exact (base, sub, sup) components.
    """
    # Clean math_text
    t = math_text.strip().replace('\\,', '').replace('\\ ', ' ')
    
    # Check simultaneous sub and sup: e.g. \sigma_1^2 or \sigma^2_1
    sub_sup_match = re.search(r'([%a-zA-Z\\]+)\_\{?([^{}\^]+)\}?\^\{?([^{}\_]+)\}?', t)
    if not sub_sup_match:
        sub_sup_match = re.search(r'([%a-zA-Z\\]+)\^\{?([^{}\_]+)\}?\_\{?([^{}\^]+)\}?', t)
        if sub_sup_match:
            # Invert so base, sup, sub
            base, sup, sub = sub_sup_match.groups()
            return {"type": "sub_sup", "base": base, "sub": sub, "sup": sup}
            
    if sub_sup_match:
        base, sub, sup = sub_sup_match.groups()
        return {"type": "sub_sup", "base": base, "sub": sub, "sup": sup}
        
    return {"type": "normal", "text": t}

samples = [
    r"\sigma_3", r"\sigma_{v0}'", r"K_{0,nc}", r"\sigma_1^2", r"c_u^{(t)}", 
    r"g/cm^3", r"20^\circ C", r"p'_{ref}"
]

for s in samples:
    res = parse_compound_inline_math(s)
    print(f"Sample: {s} -> {res}")
