"""
Unit and variable distinction:
1. Physical variables ($c$, $p$, $q$, $u$, $K$, $\sigma$, $\varepsilon$, $\phi$): ITALIC
2. Units and Chemical formulas (g/cm³, kN/m², kPa, MPa, m/s, CO₂, Fe₂O₃): NOT italic (UPRIGHT/ROMAN)
3. Descriptive subscripts (e.g. max, min, ref, vol, cr): UPRIGHT / ROMAN
4. Mathematical index subscripts (e.g. i, j, k, x, y, z): ITALIC
"""
import re

KNOWN_UNITS = {'g', 'kg', 'mg', 'm', 'cm', 'mm', 'km', 's', 'min', 'h', 'pa', 'kpa', 'mpa', 'gpa', 'n', 'kn', 'hz', 'khz', 'mhz', 'j', 'kj', 'w', 'kw', 'v', 'a', 'mol', 'l', 'ml', 'fe', 'o', 'c', 'h', 'si', 'al', 'ca'}
DESCRIPTIVE_SUBS = {'max', 'min', 'ref', 'vol', 'ult', 'opt', 'res', 'ini', 'crit', 'cr', 'nc', 'oc', 'drain', 'undrain', 'sat', 'dry'}

def should_italicize(text, is_sub=False):
    t = text.strip().lower()
    if is_sub:
        if t in DESCRIPTIVE_SUBS or t.isdigit():
            return False
        if len(t) == 1 and t.isalpha():
            return True
        return False
    
    # Units check
    if t in KNOWN_UNITS or '/' in t:
        return False
    # Numbers
    if t.isdigit() or re.match(r'^\d+(\.\d+)?$', t):
        return False
    # Variables (single letter or Greek)
    if len(t) == 1 and t.isalpha():
        return True
    return True

print("Test units and variables:")
print("sigma:", should_italicize("sigma"))
print("cm:", should_italicize("cm"))
print("sub 'max':", should_italicize("max", is_sub=True))
print("sub 'i':", should_italicize("i", is_sub=True))
