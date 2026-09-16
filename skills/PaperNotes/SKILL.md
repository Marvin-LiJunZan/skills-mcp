---
name: PaperNotes
description: "Codex + Zotero bridge for academic note-taking: synchronizes literature metadata, parses reader highlights and PDF annotations, and generates structured scientific literature cards."
metadata:
  short-description: "Codex + Zotero literature note-taking & synchronization bridge"
---

# PaperNotes (Codex + Zotero Literature Bridge)

PaperNotes bridges your Zotero reference library with LLM agentic research workflows, automating literature card creation, annotation extraction, and structured reading logs.

---

## Capabilities

1. **Zotero Library Synchronization**:
   - Reads Better BibTeX exports, Zotero SQLite databases, or local Zotero storage.
   - Extracts title, authors, publication date, abstract, collections, and PDF attachment paths.

2. **Structured Literature Note Generation**:
   Generates standard Atomic Research Notes (`.md`) formatted for Obsidian/Logseq/Notion:
   - **Metadata Frontmatter** (DOI, Citekey, Tags, Reading Date)
   - **One-Sentence Core Takeaway**
   - **Key Methodology & Experimental Setups**
   - **Direct Quotes & Figure Highlights**
   - **Critical Limitations & Personal Ideas**

3. **Bi-directional Feedback**:
   - Write synthesized LLM summaries and literature review tags back into Zotero child notes.

---

## Quick Usage

```powershell
# Generate a reading note card from a BibTeX entry or paper title
python scripts/zotero_notes.py --citekey "li2024concrete" --output "notes/"

# Batch convert a BibTeX file into markdown research cards
python scripts/zotero_notes.py --bib "library.bib" --output "notes/"
```
