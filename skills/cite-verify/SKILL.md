---
name: cite-verify
description: "Verify citation integrity, detect AI-hallucinated references, validate DOIs against official CrossRef/arXiv APIs, and locate authentic original literature sources."
metadata:
  short-description: "Citation verification, anti-hallucination & DOI integrity engine"
---

# Cite Verify — Academic Citation Anti-Hallucination & Provenance Engine

Cite Verify protects scientific manuscripts from AI-generated fake literature, incorrect DOIs, mismatched authors, and phantom papers.

---

## The 4-Layer Verification Pipeline

1. **Layer 1: Syntax & DOI Extraction**:
   - Parses `.bib`, `.tex`, or `.md` files.
   - Extracts DOIs, arXiv IDs, author lists, publication years, and article titles.

2. **Layer 2: Real API Cross-Checking**:
   - **DOI Resolution**: Direct query to CrossRef API (`https://api.crossref.org/works/{doi}`).
   - **arXiv Verification**: Query to official arXiv API (`http://export.arxiv.org/api/query?id_list={id}`).
   - **OpenAlex / CrossRef Title Match**: Fuzzy string comparison against recorded titles.

3. **Layer 3: Metadata Congruence Scoring**:
   - Title similarity $\ge 85\%$: **VERIFIED [OK]**
   - Title similarity between $50\%$ and $84\%$: **SUSPICIOUS [WARNING]**
   - No record found or similarity $< 50\%$: **HALLUCINATED [CRITICAL ERROR]**

4. **Layer 4: Provenance Localization**:
   - If a citation is identified as suspicious or missing, searches CrossRef/OpenAlex to locate the actual target paper intended by the author.

---

## Quick Usage

```powershell
# Verify a BibTeX file
python scripts/verify_citations.py --bib "references.bib"

# Verify citations inside a LaTeX paper
python scripts/verify_citations.py --tex "manuscript.tex"

# Quick check a single DOI or title
python scripts/verify_citations.py --doi "10.1016/j.cemconcomp.2024.105555"
```

---

## Classification Badges

- `[VERIFIED]`: Confirmed existing in CrossRef/arXiv with matching metadata.
- `[DOI_MISMATCH]`: The DOI points to an entirely different paper.
- `[HALLUCINATED]`: The title and authors do not correspond to any known publication in CrossRef.
- `[UNLINKED]`: Real paper exists, but missing DOI or publication venue is incomplete.
