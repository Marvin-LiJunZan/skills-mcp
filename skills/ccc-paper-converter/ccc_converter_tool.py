#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCC Paper Converter & Experimental Data Extractor
=================================================
A specialized academic converter designed for the CCC Skills Ecosystem.
Converts scientific PDFs to publication-grade Markdown (with LaTeX formulas and tables),
binds metadata with ccc-literature-scout reference libraries, and extracts experimental
data tables into unified comparison matrices.

Key Features:
- Multi-Engine Architecture:
    * MinerU (Magic-PDF): State-of-the-art for academic double-column layout & LaTeX formulas.
    * IBM Docling: Outstanding for multi-page complex table structures and RAG.
    * Native Fallback (PyMuPDF + pdfplumber): Lightweight, instant zero-model engine.
- GPU Acceleration (NVIDIA RTX 5070 Ti / CUDA supported).
- Ecosystem Metadata Binder: Matches PDFs with master_unified_references.bib or matrix.csv,
  injects standard academic YAML frontmatter, and standardizes file naming.
- Academic Table & Data Extractor: Gathers all experimental tables across papers into
  master_extracted_tables.md and summary CSV matrices for rapid paper writing.
"""

import os
import sys
import re
import csv
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ==============================================================================
# 1. Environment & Hardware Diagnostics
# ==============================================================================

def check_environment() -> Dict[str, Any]:
    """Inspects GPU hardware and installed engines."""
    report = {
        "gpu_available": False,
        "gpu_name": "None",
        "gpu_memory": "0 MB",
        "cuda_version": "Unknown",
        "pytorch_cuda": False,
        "engines": {
            "mineru": False,
            "docling": False,
            "pymupdf": False,
            "pdfplumber": False
        }
    }

    # 1. GPU Check via nvidia-smi
    try:
        smi_out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        if smi_out:
            lines = smi_out.splitlines()
            first_gpu = lines[0].split(",")
            report["gpu_available"] = True
            report["gpu_name"] = first_gpu[0].strip()
            report["gpu_memory"] = f"{first_gpu[1].strip()} MB"
    except Exception:
        pass

    # 2. PyTorch CUDA check
    try:
        import torch
        report["pytorch_cuda"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            report["cuda_version"] = torch.version.cuda
    except Exception:
        pass

    # 3. Engine checks
    try:
        import magic_pdf
        report["engines"]["mineru"] = True
    except ImportError:
        pass

    try:
        import docling
        report["engines"]["docling"] = True
    except ImportError:
        pass

    try:
        import fitz
        report["engines"]["pymupdf"] = True
    except ImportError:
        pass

    try:
        import pdfplumber
        report["engines"]["pdfplumber"] = True
    except ImportError:
        pass

    return report


def print_env_report():
    """Prints a user-friendly environment diagnostics report."""
    diag = check_environment()
    print("=" * 65)
    print("  CCC Paper Converter - System & Hardware Diagnostics")
    print("=" * 65)
    print(f"[*] GPU Hardware    : {'[YES] ' + diag['gpu_name'] if diag['gpu_available'] else '[NO] CPU Mode Only'}")
    print(f"[*] VRAM Available  : {diag['gpu_memory']}")
    print(f"[*] PyTorch CUDA    : {'Enabled (CUDA ' + str(diag['cuda_version']) + ')' if diag['pytorch_cuda'] else 'Not Enabled / No Torch'}")
    print("-" * 65)
    print("Installed Conversion Engines:")
    print(f"  - MinerU (Magic-PDF)  : {'[INSTALLED] (Best for Formulas & Double-Column)' if diag['engines']['mineru'] else '[NOT FOUND]'}")
    print(f"  - IBM Docling         : {'[INSTALLED] (Best for Multi-page Tables & RAG)' if diag['engines']['docling'] else '[NOT FOUND]'}")
    print(f"  - Native (PyMuPDF)    : {'[INSTALLED] (Fast Lightweight Text)' if diag['engines']['pymupdf'] else '[NOT FOUND]'}")
    print(f"  - Native (pdfplumber) : {'[INSTALLED] (Fast Lightweight Tables)' if diag['engines']['pdfplumber'] else '[NOT FOUND]'}")
    print("=" * 65)

    if not diag['engines']['mineru'] and not diag['engines']['docling']:
        print("\n[!] Recommendation:")
        print("  To enable deep-learning layout analysis with formulas & complex tables:")
        print("  * For MinerU : pip install magic-pdf[full] detectron2 --extra-index-url https://wheels.myhloli.com")
        print("  * For Docling: pip install docling")
        print("  * Current status: Native fallback engine is ready and can be used immediately.\n")


# ==============================================================================
# 2. Ecosystem Metadata Binder (with ccc-literature-scout)
# ==============================================================================

class MetadataBinder:
    """Binds converted markdown files with ccc-literature-scout BibTeX/CSV libraries."""

    def __init__(self, bib_path: Optional[str] = None, csv_path: Optional[str] = None):
        self.entries: Dict[str, Dict[str, Any]] = {}  # key: normalized_title / doi -> record
        self.bib_entries_by_key: Dict[str, Dict[str, Any]] = {}
        if bib_path and os.path.exists(bib_path):
            self.load_bibtex(bib_path)
        if csv_path and os.path.exists(csv_path):
            self.load_csv(csv_path)

    @staticmethod
    def normalize_str(s: str) -> str:
        if not s:
            return ""
        return re.sub(r'[^a-zA-Z0-9]', '', s.lower())

    def load_bibtex(self, path: str):
        """Parses bibtex references generated by ccc-literature-scout."""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"[!] Error reading bib file: {e}")
            return

        # Simple robust bibtex parser
        blocks = re.split(r'@\w+\s*\{', content)
        for block in blocks[1:]:
            parts = block.split(',', 1)
            if len(parts) < 2:
                continue
            bib_key = parts[0].strip()
            body = parts[1]

            fields = {}
            for match in re.finditer(r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"](?=\s*,|\s*\}\s*$)', body, re.DOTALL):
                k = match.group(1).lower().strip()
                v = re.sub(r'\s+', ' ', match.group(2)).strip()
                fields[k] = v

            title = fields.get('title', '')
            doi = fields.get('doi', '').lower().replace('https://doi.org/', '').replace('http://doi.org/', '')
            year = fields.get('year', '')
            authors = fields.get('author', '')
            journal = fields.get('journal', '') or fields.get('booktitle', '')
            abstract = fields.get('abstract', '')

            item = {
                "bib_key": bib_key,
                "title": title,
                "doi": doi,
                "year": year,
                "authors": authors,
                "journal": journal,
                "abstract": abstract
            }

            self.bib_entries_by_key[bib_key] = item
            if doi:
                self.entries[f"doi:{doi}"] = item
            if title:
                norm_title = self.normalize_str(title)
                if norm_title:
                    self.entries[f"title:{norm_title}"] = item

    def load_csv(self, path: str):
        """Parses ccc-literature-scout master matrix CSV."""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get('Title', '')
                    doi = row.get('DOI', '').lower().replace('https://doi.org/', '').replace('http://doi.org/', '')
                    bib_key = row.get('BibKey', '')
                    year = row.get('Year', '')
                    authors = row.get('Authors', '')
                    journal = row.get('Journal', '')
                    abstract = row.get('Abstract', '')

                    item = {
                        "bib_key": bib_key,
                        "title": title,
                        "doi": doi,
                        "year": year,
                        "authors": authors,
                        "journal": journal,
                        "abstract": abstract
                    }
                    if bib_key and bib_key not in self.bib_entries_by_key:
                        self.bib_entries_by_key[bib_key] = item
                    if doi and f"doi:{doi}" not in self.entries:
                        self.entries[f"doi:{doi}"] = item
                    if title:
                        norm_title = self.normalize_str(title)
                        if norm_title and f"title:{norm_title}" not in self.entries:
                            self.entries[f"title:{norm_title}"] = item
        except Exception as e:
            print(f"[!] Error reading csv file: {e}")

    def find_match(self, file_stem: str, text_head: str = "") -> Optional[Dict[str, Any]]:
        """Finds matching metadata record using file stem or text snippet."""
        # 1. Direct BibKey match
        if file_stem in self.bib_entries_by_key:
            return self.bib_entries_by_key[file_stem]

        # 2. Check stem as normalized title
        stem_norm = self.normalize_str(file_stem)
        if f"title:{stem_norm}" in self.entries:
            return self.entries[f"title:{stem_norm}"]

        # 3. Match DOI in text_head
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text_head)
        if doi_match:
            cand_doi = doi_match.group(0).lower().rstrip('.')
            if f"doi:{cand_doi}" in self.entries:
                return self.entries[f"doi:{cand_doi}"]

        # 4. Fuzzy title match against entries
        for key, item in self.entries.items():
            if key.startswith("title:"):
                t_norm = key.replace("title:", "")
                if len(t_norm) > 20:
                    if t_norm in stem_norm or stem_norm in t_norm:
                        return item
                    # Check in head text
                    if len(text_head) > 50 and self.normalize_str(item['title'])[:30] in self.normalize_str(text_head):
                        return item

        return None

    def inject_frontmatter(self, md_path: Path) -> Tuple[bool, str]:
        """Injects YAML frontmatter and standardizes the markdown file."""
        try:
            content = md_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return False, ""

        # Avoid re-injecting if frontmatter already exists
        if content.startswith("---\n"):
            return True, md_path.name

        # Read first 1500 chars for matching
        head_snippet = content[:1500]
        meta = self.find_match(md_path.stem, head_snippet)

        if not meta:
            # Create minimal frontmatter
            frontmatter = f"---\ntitle: \"{md_path.stem}\"\nconverted_by: \"ccc-paper-converter\"\n---\n\n"
            new_content = frontmatter + content
            md_path.write_text(new_content, encoding='utf-8')
            return True, md_path.name

        # Construct comprehensive academic frontmatter
        author_list = [a.strip() for a in meta['authors'].replace(' and ', ';').split(';') if a.strip()]
        authors_yaml = json.dumps(author_list, ensure_ascii=False) if author_list else "[]"
        
        safe_title = meta.get('title', '').replace('"', '\\"')
        safe_journal = meta.get('journal', '').replace('"', '\\"')

        frontmatter_lines = [
            "---",
            f"bib_key: \"{meta.get('bib_key', '')}\"",
            f"title: \"{safe_title}\"",
            f"authors: {authors_yaml}",
            f"year: {meta.get('year', '')}",
            f"journal: \"{safe_journal}\"",
            f"doi: \"{meta.get('doi', '')}\"",
            "converted_by: \"ccc-paper-converter\"",
            "---\n\n"
        ]
        
        new_content = "\n".join(frontmatter_lines) + content
        
        # Optionally rename file to BibKey if available
        new_name = md_path.name
        bib_key = meta.get('bib_key')
        if bib_key and bib_key != md_path.stem:
            target_path = md_path.parent / f"{bib_key}.md"
            if not target_path.exists():
                md_path.write_text(new_content, encoding='utf-8')
                shutil.move(str(md_path), str(target_path))
                return True, target_path.name

        md_path.write_text(new_content, encoding='utf-8')
        return True, new_name


# ==============================================================================
# 3. Conversion Engines
# ==============================================================================

class BaseConverter:
    """Abstract interface for PDF to Markdown converter."""
    def convert(self, pdf_path: Path, output_dir: Path, use_gpu: bool = True) -> Path:
        raise NotImplementedError


class MinerUConverter(BaseConverter):
    """MinerU (Magic-PDF) Converter Engine."""
    def convert(self, pdf_path: Path, output_dir: Path, use_gpu: bool = True) -> Path:
        target_dir = output_dir / pdf_path.stem
        target_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "magic-pdf",
            "-p", str(pdf_path.resolve()),
            "-o", str(output_dir.resolve()),
            "-m", "auto"
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"MinerU execution failed: {result.stderr[:300]}")
            
        candidates = list(target_dir.rglob("*.md"))
        if not candidates:
            raise FileNotFoundError(f"MinerU completed but no markdown was found in {target_dir}")
        return candidates[0]


class DoclingConverter(BaseConverter):
    """IBM Docling Converter Engine."""
    def __init__(self):
        from docling.document_converter import DocumentConverter
        self.converter = DocumentConverter()

    def convert(self, pdf_path: Path, output_dir: Path, use_gpu: bool = True) -> Path:
        output_file = output_dir / f"{pdf_path.stem}.md"
        conv_res = self.converter.convert(str(pdf_path.resolve()))
        md_text = conv_res.document.export_to_markdown()
        output_file.write_text(md_text, encoding='utf-8')
        return output_file


class NativeConverter(BaseConverter):
    """
    Native Fallback Converter using PyMuPDF (fitz) and pdfplumber.
    Does not require downloading multi-gigabyte models.
    Supports smart two-column un-wrapping and GFM table extraction.
    """
    def convert(self, pdf_path: Path, output_dir: Path, use_gpu: bool = True) -> Path:
        import fitz
        output_file = output_dir / f"{pdf_path.stem}.md"

        # 1. Extract tables with pdfplumber if installed
        tables_by_page = {}
        try:
            import pdfplumber
            with pdfplumber.open(str(pdf_path)) as pdf:
                for p_idx, page in enumerate(pdf.pages):
                    extracted = page.extract_tables()
                    if extracted:
                        tables_by_page[p_idx] = extracted
        except Exception:
            pass

        # 2. Extract text & layout with PyMuPDF
        doc = fitz.open(str(pdf_path))
        markdown_sections = []

        for p_idx, page in enumerate(doc):
            markdown_sections.append(f"\n<!-- Page {p_idx + 1} -->\n")
            
            # Insert extracted tables for this page first if available
            if p_idx in tables_by_page:
                for t_idx, tbl in enumerate(tables_by_page[p_idx]):
                    if not tbl or len(tbl) < 2:
                        continue
                    markdown_sections.append(f"\n**[Table {p_idx+1}-{t_idx+1}]**\n")
                    header = tbl[0]
                    clean_header = [re.sub(r'\s+', ' ', str(c or '')).strip() for c in header]
                    markdown_sections.append("| " + " | ".join(clean_header) + " |")
                    markdown_sections.append("| " + " | ".join(["---"] * len(clean_header)) + " |")
                    for row in tbl[1:]:
                        clean_row = [re.sub(r'\s+', ' ', str(c or '')).strip() for c in row]
                        markdown_sections.append("| " + " | ".join(clean_row) + " |")
                    markdown_sections.append("\n")

            # Extract blocks (x0, y0, x1, y1, text, block_no, block_type)
            blocks = page.get_text("blocks")
            page_width = page.rect.width
            mid_x = page_width / 2.0

            left_col = []
            right_col = []
            full_span = []

            for b in blocks:
                if b[6] != 0:  # ignore images in text flow
                    continue
                x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
                text = text.strip()
                if not text:
                    continue

                if x1 <= mid_x + 20:
                    left_col.append((y0, text))
                elif x0 >= mid_x - 20:
                    right_col.append((y0, text))
                else:
                    full_span.append((y0, text))

            # Sort by vertical coordinates
            left_col.sort(key=lambda item: item[0])
            right_col.sort(key=lambda item: item[0])
            full_span.sort(key=lambda item: item[0])

            for _, t in full_span:
                markdown_sections.append(self._format_text_block(t))
            for _, t in left_col:
                markdown_sections.append(self._format_text_block(t))
            for _, t in right_col:
                markdown_sections.append(self._format_text_block(t))

        doc.close()
        full_markdown = "\n\n".join(markdown_sections)
        output_file.write_text(full_markdown, encoding='utf-8')
        return output_file

    @staticmethod
    def _format_text_block(text: str) -> str:
        lines = text.splitlines()
        first_line = lines[0].strip() if lines else ""
        if re.match(r'^(?:[0-9]+\.?\s+|[I|V|X]+\.?\s+)?(Introduction|Abstract|Method|Experiment|Result|Discussion|Conclusion|References)\b', first_line, re.IGNORECASE):
            return f"## {text}"
        return text


# ==============================================================================
# 4. Experimental Data & Table Extractor
# ==============================================================================

class TableDataExtractor:
    """Scans converted Markdown files and aggregates experimental tables into unified matrices."""

    @staticmethod
    def extract_from_directory(md_dir: Path, output_md: Path, output_csv: Optional[Path] = None):
        md_files = list(md_dir.rglob("*.md"))
        print(f"[*] Scanning {len(md_files)} Markdown files for experimental tables...")

        all_tables: List[Dict[str, Any]] = []
        csv_rows: List[Dict[str, Any]] = []

        table_regex = re.compile(
            r'((?:(?:\*\*\[?(?:Table|表)\s*\d+[^\]\n]*\]?\*\*|[^\n]*(?:Table|表)\s*\d+[:\.\s][^\n]*)\n\s*)?'
            r'\|[^\n]+\|\n\s*\|[\s\-:|]+\|\n(?:\s*\|[^\n]+\|\n?)+)',
            re.IGNORECASE
        )

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            meta = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    for line in parts[1].splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            meta[k.strip()] = v.strip().strip('"')

            paper_id = meta.get('bib_key') or md_file.stem
            paper_title = meta.get('title') or md_file.stem
            paper_year = meta.get('year') or ''
            paper_doi = meta.get('doi') or ''

            matches = table_regex.finditer(content)
            tbl_count = 0
            for match in matches:
                tbl_count += 1
                raw_block = match.group(1).strip()
                lines = [l.strip() for l in raw_block.splitlines() if l.strip()]

                caption = f"Table {tbl_count}"
                table_start_idx = 0

                if not lines[0].startswith("|"):
                    caption = lines[0].replace("**", "").replace("[", "").replace("]", "").strip()
                    table_start_idx = 1

                if len(lines) <= table_start_idx + 1:
                    continue

                table_md_lines = lines[table_start_idx:]
                header_line = table_md_lines[0]
                headers = [h.strip() for h in header_line.split("|") if h.strip()]

                all_tables.append({
                    "paper_id": paper_id,
                    "paper_title": paper_title,
                    "year": paper_year,
                    "doi": paper_doi,
                    "caption": caption,
                    "markdown": "\n".join(table_md_lines)
                })

                for data_line in table_md_lines[2:]:
                    cells = [c.strip() for c in data_line.split("|")[1:-1]]
                    if not cells:
                        continue
                    row_dict = {
                        "Paper_ID": paper_id,
                        "Year": paper_year,
                        "DOI": paper_doi,
                        "Table_Caption": caption,
                        "Primary_Key": cells[0] if len(cells) > 0 else "",
                        "Attributes_JSON": json.dumps(dict(zip(headers, cells)), ensure_ascii=False)
                    }
                    csv_rows.append(row_dict)

        print(f"[*] Found {len(all_tables)} tables across all literature.")
        output_md.parent.mkdir(parents=True, exist_ok=True)
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write("# Master Extracted Experimental Tables\n\n")
            f.write(f"Aggregated by `ccc-paper-converter` across {len(md_files)} papers.\n\n")
            f.write("---\n\n")

            for item in all_tables:
                f.write(f"### [{item['paper_id']}] {item['caption']}\n\n")
                f.write(f"- **Paper**: {item['paper_title']}\n")
                if item['doi']:
                    f.write(f"- **DOI**: [{item['doi']}](https://doi.org/{item['doi']})\n")
                if item['year']:
                    f.write(f"- **Year**: {item['year']}\n")
                f.write("\n")
                f.write(item['markdown'])
                f.write("\n\n---\n\n")

        print(f"[+] Tables Markdown saved to: {output_md}")

        if output_csv and csv_rows:
            output_csv.parent.mkdir(parents=True, exist_ok=True)
            with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
                fieldnames = ["Paper_ID", "Year", "DOI", "Table_Caption", "Primary_Key", "Attributes_JSON"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)
            print(f"[+] Data Matrix CSV saved to: {output_csv}")


# ==============================================================================
# 5. CLI Controller & Main Pipeline
# ==============================================================================

def select_engine(requested: str) -> BaseConverter:
    """Selects and instantiates the appropriate converter engine."""
    env = check_environment()
    req = requested.lower()

    if req == "mineru":
        if not env["engines"]["mineru"]:
            raise RuntimeError("MinerU (magic-pdf) is not installed. Run: pip install magic-pdf[full]")
        return MinerUConverter()

    elif req == "docling":
        if not env["engines"]["docling"]:
            raise RuntimeError("Docling is not installed. Run: pip install docling")
        return DoclingConverter()

    elif req == "native":
        if not env["engines"]["pymupdf"]:
            raise RuntimeError("PyMuPDF (fitz) is not installed. Run: pip install pymupdf")
        return NativeConverter()

    # AUTO Mode
    if env["engines"]["mineru"]:
        print("[*] Engine selected: MinerU (Magic-PDF) [Auto - Academic Quality]")
        return MinerUConverter()
    elif env["engines"]["docling"]:
        print("[*] Engine selected: IBM Docling [Auto - Table Quality]")
        return DoclingConverter()
    elif env["engines"]["pymupdf"]:
        print("[*] Engine selected: Native Engine (PyMuPDF + pdfplumber) [Auto - Lightweight]")
        return NativeConverter()
    else:
        raise RuntimeError("No PDF engine available! Please install pymupdf, docling, or magic-pdf.")


def cmd_convert(args):
    """Handles batch or single conversion."""
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        pdf_files = [input_path]
    elif input_path.is_dir():
        pdf_files = sorted(list(input_path.glob("*.pdf")))
    else:
        print(f"[!] Input path not found: {input_path}")
        return

    if not pdf_files:
        print(f"[!] No PDF files found in: {input_path}")
        return

    print(f"[*] Found {len(pdf_files)} PDF file(s) to process.")
    engine = select_engine(args.engine)

    success = 0
    failed = 0

    for idx, pdf in enumerate(pdf_files, 1):
        target_md = output_dir / f"{pdf.stem}.md"
        if not args.force and (target_md.exists() or any((output_dir / pdf.stem).glob("*.md"))):
            print(f"[{idx}/{len(pdf_files)}] [SKIP] Already converted: {pdf.name}")
            success += 1
            continue

        print(f"[{idx}/{len(pdf_files)}] Converting: {pdf.name} ...")
        try:
            engine.convert(pdf, output_dir, use_gpu=(not args.cpu))
            print(f"    --> [OK] Converted {pdf.name}")
            success += 1
        except Exception as e:
            print(f"    --> [FAILED] {pdf.name}: {e}")
            failed += 1

    print(f"\n[+] Batch Conversion Finished: {success} succeeded, {failed} failed.")


def cmd_bind(args):
    """Binds converted markdown with ccc-literature-scout BibTeX/CSV metadata."""
    md_dir = Path(args.md_dir)
    binder = MetadataBinder(bib_path=args.bib, csv_path=args.csv)

    md_files = list(md_dir.rglob("*.md"))
    print(f"[*] Binding metadata for {len(md_files)} Markdown files...")

    bound = 0
    for md_file in md_files:
        ok, new_name = binder.inject_frontmatter(md_file)
        if ok:
            bound += 1

    print(f"[+] Metadata binding complete: {bound} files enriched.")


def cmd_extract_tables(args):
    """Aggregates all tables from Markdown files."""
    md_dir = Path(args.md_dir)
    out_md = Path(args.output_file)
    out_csv = Path(args.output_csv) if args.output_csv else None
    TableDataExtractor.extract_from_directory(md_dir, out_md, out_csv)


def cmd_pipeline(args):
    """End-to-End Pipeline: Batch Convert -> Metadata Bind -> Table Extraction."""
    print("=" * 65)
    print("  CCC Paper Converter: End-to-End Execution Pipeline")
    print("=" * 65)

    cmd_convert(args)

    if args.bib or args.csv:
        print("\n--- Phase 2: Metadata Binding ---")
        args.md_dir = args.output_dir
        cmd_bind(args)

    if args.extract_tables:
        print("\n--- Phase 3: Experimental Table & Data Extraction ---")
        out_dir = Path(args.output_dir)
        args.md_dir = args.output_dir
        args.output_file = str(out_dir / "master_extracted_tables.md")
        args.output_csv = str(out_dir / "master_extracted_data.csv")
        cmd_extract_tables(args)

    print("\n[✓] Pipeline execution finished successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="CCC Paper Converter & Experimental Data Extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("check-env", help="Check GPU hardware and engine installations")

    p_conv = subparsers.add_parser("convert", help="Batch convert PDF files to Markdown")
    p_conv.add_argument("-i", "--input", required=True, help="Input PDF file or folder containing PDFs")
    p_conv.add_argument("-o", "--output-dir", required=True, help="Output directory for Markdown files")
    p_conv.add_argument("--engine", choices=["auto", "mineru", "docling", "native"], default="auto", help="Conversion engine")
    p_conv.add_argument("--cpu", action="store_true", help="Force CPU inference (disable GPU)")
    p_conv.add_argument("--force", action="store_true", help="Force overwrite existing converted files")

    p_bind = subparsers.add_parser("bind-metadata", help="Inject YAML frontmatter from BibTeX or CSV")
    p_bind.add_argument("--md-dir", required=True, help="Directory containing converted markdown files")
    p_bind.add_argument("--bib", help="Path to master_unified_references.bib")
    p_bind.add_argument("--csv", help="Path to master_literature_matrix.csv")

    p_tbl = subparsers.add_parser("extract-tables", help="Extract all experimental tables into unified markdown & CSV")
    p_tbl.add_argument("--md-dir", required=True, help="Directory containing converted markdown files")
    p_tbl.add_argument("--output-file", default="./master_extracted_tables.md", help="Output summary markdown file")
    p_tbl.add_argument("--output-csv", default="./master_extracted_data.csv", help="Output CSV file")

    p_pipe = subparsers.add_parser("pipeline", help="Run full pipeline: convert -> bind metadata -> extract tables")
    p_pipe.add_argument("-i", "--input", required=True, help="Input PDF file or folder")
    p_pipe.add_argument("-o", "--output-dir", required=True, help="Output directory")
    p_pipe.add_argument("--engine", choices=["auto", "mineru", "docling", "native"], default="auto", help="Conversion engine")
    p_pipe.add_argument("--cpu", action="store_true", help="Force CPU inference")
    p_pipe.add_argument("--force", action="store_true", help="Force overwrite")
    p_pipe.add_argument("--bib", help="Path to master_unified_references.bib")
    p_pipe.add_argument("--csv", help="Path to master_literature_matrix.csv")
    p_pipe.add_argument("--extract-tables", action="store_true", default=True, help="Extract experimental tables")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "check-env":
        print_env_report()
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "bind-metadata":
        cmd_bind(args)
    elif args.command == "extract-tables":
        cmd_extract_tables(args)
    elif args.command == "pipeline":
        cmd_pipeline(args)


if __name__ == "__main__":
    main()
