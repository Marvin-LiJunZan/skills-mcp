---
name: paper-rag
description: "RAG-powered multi-paper knowledge base for academic literature: cross-paper QA, literature corpus management, topic accumulation, and evidence retrieval."
metadata:
  short-description: "RAG knowledge base for academic papers & long-term research synthesis"
---

# Paper RAG — Literature Knowledge Base & Multi-Paper QA

Paper RAG transforms your collection of research papers (PDFs, Markdown notes, BibTeX libraries) into a queryable, evidence-grounded research knowledge base.

---

## Capabilities

1. **Cross-Paper Synthesized QA**:
   - Ask questions across dozens of papers simultaneously (e.g., *"How do different studies handle the water-to-binder ratio in alkali-activated slag?"*).
   - Returns responses strictly grounded in retrieved chunks with exact paper citation keys and section references.

2. **Long-Term Topic Knowledge Accumulation**:
   - Maintains an incremental index of papers in `corpus/`.
   - Supports adding new papers, tagging by sub-topics, and tracking conflicting findings across publications.

3. **Evidence Matrix Aggregation**:
   - Automatically gathers comparative data (metrics, datasets, parameter ranges) across papers into structured markdown tables.

---

## Quick Usage

Run the bundled lightweight Python RAG engine:

```powershell
# Index a directory of papers or notes
python scripts/paper_rag.py index --dir "path/to/papers" --db "paper_index.json"

# Query the literature base
python scripts/paper_rag.py query --db "paper_index.json" --query "How is compressive strength affected by curing temperature?"
```

---

## Query Modes

- **Synthesize Mode**: Merges viewpoints from multiple authors, highlighting agreements and controversies.
- **Compare Mode**: Constructs a head-to-head table of methodologies, assumptions, and outcomes.
- **Fact-Check Mode**: Locates whether any paper in your corpus supports or contradicts a specific claim.
