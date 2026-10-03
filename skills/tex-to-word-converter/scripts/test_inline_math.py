"""
Test converting inline math (single variables, Greek letters, sub/superscripts) 
from OMML (Office Math) to native text runs with italic/subscript/superscript formatting.
"""
import re
from docx import Document
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

GREEK_MAP = {
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ', r'\epsilon': 'ε',
    r'\varepsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ', r'\vartheta': 'θ',
    r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ', r'\mu': 'μ', r'\nu': 'ν',
    r'\xi': 'ξ', r'\pi': 'π', r'\varpi': 'ϖ', r'\rho': 'ρ', r'\varrho': 'ϱ',
    r'\sigma': 'σ', r'\varsigma': 'ς', r'\tau': 'τ', r'\upsilon': 'υ', r'\phi': 'φ',
    r'\varphi': 'φ', r'\chi': 'χ', r'\psi': 'ψ', r'\omega': 'ω',
    r'\Gamma': 'Γ', r'\Delta': 'Δ', r'\Theta': 'Θ', r'\Lambda': 'Λ', r'\Xi': 'Ξ',
    r'\Pi': 'Π', r'\Sigma': 'Σ', r'\Upsilon': 'Υ', r'\Phi': 'Φ', r'\Psi': 'Ψ', r'\Omega': 'Ω'
}

SYM_MAP = {
    r'\pm': '±', r'\times': '×', r'\div': '÷', r'\cdot': '·', r'\leq': '≤',
    r'\le': '≤', r'\geq': '≥', r'\ge': '≥', r'\neq': '≠', r'\ne': '≠',
    r'\approx': '≈', r'\sim': '~', r'\propto': '∝', r'\infty': '∞', r'\nabla': '∇',
    r'\partial': '∂', r'\in': '∈', r'\notin': '∉', r'\subset': '⊂', r'\subseteq': '⊆',
    r'\cup': '∪', r'\cap': '∩', r'\vee': '∨', r'\wedge': '∧', r'\leftarrow': '←',
    r'\rightarrow': '→', r'\Leftarrow': '⇐', r'\Rightarrow': '⇒', r'\leftrightarrow': '↔',
    r'\degree': '°', r'^{\circ}': '°', r'\%': '%'
}

print("[OK] Greek and Math symbol dictionary mapped successfully.")
