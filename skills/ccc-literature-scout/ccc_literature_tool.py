#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCC Literature Scout & Bib-Introduction Synthesizer
===================================================
Automated multi-source academic literature search, Web of Science export parsing,
clean BibTeX generation with abstracts, literature matrix analysis, and
publication-grade LaTeX / Markdown Introduction drafting in English and Chinese.

Sources Supported:
- OpenAlex API (250M+ papers, abstracts reconstructed from inverted index)
- arXiv API (CS/AI/Physics/Math preprints with full abstracts)
- Crossref API (Official DOI metadata & publisher records)
- Web of Science / EndNote / RIS Parsers (CIW, TXT, ENW, BIB, RIS)
"""

import os
import sys
import re
import json
import time
import argparse
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Set
from collections import Counter

# Set standard encoding for Windows terminal
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Paper:
    def __init__(
        self,
        title: str,
        authors: List[str],
        year: Optional[int],
        journal: str = "",
        doi: str = "",
        abstract: str = "",
        url: str = "",
        citations: int = 0,
        source: str = "",
        bib_key: str = "",
        volume: str = "",
        number: str = "",
        pages: str = "",
        publisher: str = "",
        keywords: Optional[List[str]] = None
    ):
        self.title = self._clean_text(title)
        self.authors = [self._clean_text(a) for a in authors if a.strip()]
        self.year = int(year) if year and str(year).isdigit() else None
        self.journal = self._clean_text(journal)
        self.doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
        self.abstract = self._clean_text(abstract)
        self.url = url.strip() or (f"https://doi.org/{self.doi}" if self.doi else "")
        self.citations = int(citations) if citations else 0
        self.source = source
        self.volume = str(volume).strip()
        self.number = str(number).strip()
        self.pages = str(pages).strip()
        self.publisher = self._clean_text(publisher)
        self.keywords = keywords or []
        self.bib_key = bib_key or self.generate_bib_key()

    @staticmethod
    def _clean_text(text: Optional[str]) -> str:
        if not text:
            return ""
        cleaned = re.sub(r'\s+', ' ', str(text)).strip()
        return cleaned

    def generate_bib_key(self) -> str:
        first_author = "Unknown"
        if self.authors:
            first_name_raw = self.authors[0]
            if "," in first_name_raw:
                last_name = first_name_raw.split(",")[0].strip()
            else:
                parts = first_name_raw.split()
                last_name = parts[-1] if parts else "Unknown"
            first_author = re.sub(r'[^a-zA-Z]', '', last_name) or "Unknown"

        year_str = str(self.year) if self.year else "nd"

        stop_words = {'the', 'a', 'an', 'on', 'for', 'in', 'of', 'and', 'with', 'to', 'from', 'by', 'at', 'towards', 'study', 'analysis'}
        title_words = re.findall(r'[a-zA-Z]+', self.title)
        keyword = "Work"
        for w in title_words:
            if w.lower() not in stop_words and len(w) >= 3:
                keyword = w.capitalize()
                break

        return f"{first_author.capitalize()}{year_str}{keyword}"

    def to_bibtex(self) -> str:
        entry_type = "article"
        is_conf = any(k in self.journal.lower() for k in ["conference", "proceedings", "symposium", "cvpr", "iccv", "eccv", "neurips", "iclr", "icml"])
        if is_conf:
            entry_type = "inproceedings"

        formatted_authors = " and ".join(self.authors) if self.authors else "Unknown"

        lines = [f"@{entry_type}{{{self.bib_key},"]
        lines.append(f"  title = {{{self._latex_escape(self.title)}}},")
        lines.append(f"  author = {{{self._latex_escape(formatted_authors)}}},")
        
        if entry_type == "inproceedings":
            lines.append(f"  booktitle = {{{self._latex_escape(self.journal)}}},")
        elif self.journal:
            lines.append(f"  journal = {{{self._latex_escape(self.journal)}}},")
            
        if self.year:
            lines.append(f"  year = {{{self.year}}},")
        if self.volume:
            lines.append(f"  volume = {{{self.volume}}},")
        if self.number:
            lines.append(f"  number = {{{self.number}}},")
        if self.pages:
            lines.append(f"  pages = {{{self.pages.replace('-', '--')}}},")
        if self.doi:
            lines.append(f"  doi = {{{self.doi}}},")
        if self.url:
            lines.append(f"  url = {{{self.url}}},")
        if self.publisher:
            lines.append(f"  publisher = {{{self._latex_escape(self.publisher)}}},")
        if self.abstract:
            lines.append(f"  abstract = {{{self._latex_escape(self.abstract)}}},")
        lines.append("}")
        return "\n".join(lines)

    @staticmethod
    def _latex_escape(text: str) -> str:
        if not text:
            return ""
        chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
        }
        res = text
        for char, repl in chars.items():
            res = re.sub(rf'(?<!\\){re.escape(char)}', repl, res)
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bib_key": self.bib_key,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "journal": self.journal,
            "doi": self.doi,
            "abstract": self.abstract,
            "url": self.url,
            "citations": self.citations,
            "source": self.source,
            "volume": self.volume,
            "number": self.number,
            "pages": self.pages,
            "publisher": self.publisher,
            "keywords": self.keywords
        }


# ==============================================================================
# Search & Fetch Engines
# ==============================================================================

class OpenAlexFetcher:
    """Fetches papers with full abstracts from OpenAlex API (250M+ open catalog)."""
    BASE_URL = "https://api.openalex.org/works"

    @classmethod
    def search(cls, query: str, limit: int = 25, year_min: Optional[int] = None, year_max: Optional[int] = None) -> List[Paper]:
        params = {
            "search": query,
            "per_page": min(limit, 50),
            "sort": "relevance_score:desc"
        }
        filters = []
        if year_min and year_max:
            filters.append(f"publication_year:{year_min}-{year_max}")
        elif year_min:
            filters.append(f"publication_year:>{year_min - 1}")
        elif year_max:
            filters.append(f"publication_year:<{year_max + 1}")

        if filters:
            params["filter"] = ",".join(filters)

        url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "mailto:academic-researcher@university.edu (CCC-Literature-Scout-Bot)"
            }
        )

        papers = []
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for work in data.get("results", []):
                    title = work.get("title") or ""
                    if not title:
                        continue

                    authors = []
                    for authorship in work.get("authorships", []):
                        author_name = authorship.get("author", {}).get("display_name")
                        if author_name:
                            authors.append(author_name)

                    year = work.get("publication_year")
                    
                    primary_location = work.get("primary_location") or {}
                    source_obj = primary_location.get("source") or {}
                    journal = source_obj.get("display_name") or ""
                    
                    doi_raw = work.get("doi") or ""
                    doi = doi_raw.replace("https://doi.org/", "").replace("http://doi.org/", "")
                    
                    # Reconstruct inverted abstract
                    abstract = ""
                    inv_index = work.get("abstract_inverted_index")
                    if inv_index:
                        pos_dict = {}
                        for word, pos_list in inv_index.items():
                            for pos in pos_list:
                                pos_dict[pos] = word
                        abstract = " ".join(pos_dict[k] for k in sorted(pos_dict.keys()))

                    citations = work.get("cited_by_count", 0)
                    oa_url = primary_location.get("landing_page_url") or primary_location.get("pdf_url") or doi_raw

                    paper = Paper(
                        title=title,
                        authors=authors,
                        year=year,
                        journal=journal,
                        doi=doi,
                        abstract=abstract,
                        url=oa_url,
                        citations=citations,
                        source="OpenAlex"
                    )
                    papers.append(paper)
        except Exception as e:
            print(f"[OpenAlex] Warning querying '{query}': {e}", file=sys.stderr)

        return papers


class ArxivFetcher:
    """Fetches high-accuracy preprints with abstracts from arXiv API."""
    BASE_URL = "http://export.arxiv.org/api/query"

    @classmethod
    def search(cls, query: str, limit: int = 15) -> List[Paper]:
        clean_query = query.replace(" ", "+")
        url = f"{cls.BASE_URL}?search_query=all:{urllib.parse.quote(clean_query)}&start=0&max_results={limit}&sortBy=relevance&sortOrder=descending"
        
        papers = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CCC-Literature-Scout-Bot"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                
                ns = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }
                
                for entry in root.findall('atom:entry', ns):
                    title_elem = entry.find('atom:title', ns)
                    summary_elem = entry.find('atom:summary', ns)
                    published_elem = entry.find('atom:published', ns)
                    id_elem = entry.find('atom:id', ns)
                    
                    title = title_elem.text if title_elem is not None else ""
                    abstract = summary_elem.text if summary_elem is not None else ""
                    
                    year = None
                    if published_elem is not None and published_elem.text:
                        year = int(published_elem.text[:4])
                        
                    url_str = id_elem.text if id_elem is not None else ""
                    arxiv_id = url_str.split('/abs/')[-1] if '/abs/' in url_str else ""
                    
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name = author.find('atom:name', ns)
                        if name is not None and name.text:
                            authors.append(name.text)
                            
                    doi_elem = entry.find('arxiv:doi', ns)
                    doi = doi_elem.text if doi_elem is not None else ""
                    
                    paper = Paper(
                        title=title,
                        authors=authors,
                        year=year,
                        journal=f"arXiv preprint arXiv:{arxiv_id}" if arxiv_id else "arXiv",
                        doi=doi,
                        abstract=abstract,
                        url=url_str,
                        citations=0,
                        source="arXiv"
                    )
                    papers.append(paper)
        except Exception as e:
            print(f"[arXiv] Warning querying '{query}': {e}", file=sys.stderr)
            
        return papers


class CrossrefFetcher:
    """Fetches official metadata & DOIs from Crossref API."""
    BASE_URL = "https://api.crossref.org/works"

    @classmethod
    def search(cls, query: str, limit: int = 15) -> List[Paper]:
        params = {
            "query": query,
            "rows": limit,
            "sort": "relevance"
        }
        url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": "CCC-Literature-Scout (mailto:researcher@univ.edu)"})
        
        papers = []
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("message", {}).get("items", [])
                for item in items:
                    title_list = item.get("title", [])
                    title = title_list[0] if title_list else ""
                    if not title:
                        continue
                        
                    authors = []
                    for a in item.get("author", []):
                        given = a.get("given", "")
                        family = a.get("family", "")
                        if family:
                            authors.append(f"{family}, {given}" if given else family)
                            
                    year = None
                    date_parts = item.get("published-print", {}).get("date-parts") or item.get("published-online", {}).get("date-parts")
                    if date_parts and date_parts[0]:
                        year = date_parts[0][0]
                        
                    container = item.get("container-title", [])
                    journal = container[0] if container else ""
                    
                    doi = item.get("DOI", "")
                    abstract = item.get("abstract", "")
                    if abstract:
                        abstract = re.sub(r'<[^>]+>', '', abstract)
                        
                    citations = item.get("is-referenced-by-count", 0)
                    volume = item.get("volume", "")
                    number = item.get("issue", "")
                    pages = item.get("page", "")
                    publisher = item.get("publisher", "")
                    
                    paper = Paper(
                        title=title,
                        authors=authors,
                        year=year,
                        journal=journal,
                        doi=doi,
                        abstract=abstract,
                        url=f"https://doi.org/{doi}" if doi else "",
                        citations=citations,
                        source="Crossref",
                        volume=volume,
                        number=number,
                        pages=pages,
                        publisher=publisher
                    )
                    papers.append(paper)
        except Exception as e:
            print(f"[Crossref] Warning querying '{query}': {e}", file=sys.stderr)
            
        return papers


# ==============================================================================
# Web of Science & EndNote Export Parsers
# ==============================================================================

class WoSParser:
    """Parses Web of Science export formats (.ciw / EndNote, .txt / plain text, .bib, .ris)."""

    @classmethod
    def parse_file(cls, filepath: str) -> List[Paper]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"WoS Export file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if filepath.lower().endswith(".ciw") or "FN Clarivate Analytics Web of Science" in content or "PT J" in content:
            return cls.parse_wos_plain_or_ciw(content)
        elif filepath.lower().endswith(".ris") or "TY  - JOUR" in content:
            return cls.parse_ris(content)
        elif filepath.lower().endswith(".bib") or "@article" in content.lower():
            return cls.parse_bib(content)
        else:
            return cls.parse_wos_plain_or_ciw(content)

    @classmethod
    def parse_wos_plain_or_ciw(cls, content: str) -> List[Paper]:
        records = re.split(r'\nER\s*\n|\nER\r\n', content)
        papers = []

        for rec in records:
            if not rec.strip():
                continue
            fields: Dict[str, List[str]] = {}
            current_tag = None

            for line in rec.splitlines():
                if len(line) >= 2 and line[:2].isupper() and (len(line) == 2 or line[2] == ' '):
                    current_tag = line[:2]
                    val = line[3:].strip() if len(line) > 2 else ""
                    if current_tag not in fields:
                        fields[current_tag] = []
                    if val:
                        fields[current_tag].append(val)
                elif current_tag and line.startswith("   "):
                    val = line.strip()
                    if val:
                        fields[current_tag].append(val)

            title = " ".join(fields.get("TI", []))
            if not title:
                continue

            authors = fields.get("AU", []) or fields.get("AF", [])
            year = None
            if fields.get("PY"):
                py_match = re.search(r'\d{4}', fields["PY"][0])
                if py_match:
                    year = int(py_match.group())

            journal = " ".join(fields.get("SO", [])) or " ".join(fields.get("J9", []))
            abstract = " ".join(fields.get("AB", []))
            doi = "".join(fields.get("DI", []))
            
            citations = 0
            if fields.get("TC"):
                tc_match = re.search(r'\d+', fields["TC"][0])
                if tc_match:
                    citations = int(tc_match.group())

            volume = "".join(fields.get("VL", []))
            number = "".join(fields.get("IS", []))
            pages = f"{''.join(fields.get('BP', []))}-{''.join(fields.get('EP', []))}".strip('-')
            publisher = " ".join(fields.get("PU", []))

            paper = Paper(
                title=title,
                authors=authors,
                year=year,
                journal=journal,
                doi=doi,
                abstract=abstract,
                citations=citations,
                source="WebOfScience",
                volume=volume,
                number=number,
                pages=pages,
                publisher=publisher
            )
            papers.append(paper)

        return papers

    @classmethod
    def parse_ris(cls, content: str) -> List[Paper]:
        records = re.split(r'\nER  -\s*|\nER  -\r\n', content)
        papers = []
        for rec in records:
            if not rec.strip():
                continue
            title = ""
            authors = []
            year = None
            journal = ""
            abstract = ""
            doi = ""
            
            for line in rec.splitlines():
                if line.startswith("TI  - ") or line.startswith("T1  - "):
                    title = line[6:].strip()
                elif line.startswith("AU  - ") or line.startswith("A1  - "):
                    authors.append(line[6:].strip())
                elif line.startswith("PY  - ") or line.startswith("Y1  - "):
                    m = re.search(r'\d{4}', line[6:])
                    if m:
                        year = int(m.group())
                elif line.startswith("JO  - ") or line.startswith("JF  - ") or line.startswith("T2  - "):
                    journal = line[6:].strip()
                elif line.startswith("AB  - ") or line.startswith("N2  - "):
                    abstract += " " + line[6:].strip()
                elif line.startswith("DO  - "):
                    doi = line[6:].strip()

            if title:
                papers.append(Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    journal=journal,
                    doi=doi,
                    abstract=abstract.strip(),
                    source="RIS_Export"
                ))
        return papers

    @classmethod
    def parse_bib(cls, content: str) -> List[Paper]:
        entries = re.split(r'@\w+\s*\{', content)
        papers = []
        for entry in entries[1:]:
            key_match = re.match(r'([^,]+),', entry)
            bib_key = key_match.group(1).strip() if key_match else ""
            
            def extract_field(fieldname: str) -> str:
                m = re.search(rf'{fieldname}\s*=\s*[{{\"](.*?)[}}\"]\s*[,}}]', entry, re.DOTALL | re.IGNORECASE)
                return m.group(1).strip() if m else ""

            title = extract_field("title")
            if not title:
                continue
            authors_raw = extract_field("author")
            authors = [a.strip() for a in authors_raw.split(" and ")] if authors_raw else []
            
            year_val = extract_field("year")
            year = int(year_val) if year_val.isdigit() else None
            
            journal = extract_field("journal") or extract_field("booktitle")
            abstract = extract_field("abstract")
            doi = extract_field("doi")
            volume = extract_field("volume")
            number = extract_field("number")
            pages = extract_field("pages")
            
            papers.append(Paper(
                title=title,
                authors=authors,
                year=year,
                journal=journal,
                doi=doi,
                abstract=abstract,
                bib_key=bib_key,
                volume=volume,
                number=number,
                pages=pages,
                source="Bib_Import"
            ))
        return papers


# ==============================================================================
# Deduplication & Corpus Management
# ==============================================================================

class LiteratureCorpus:
    """Manages collection, deduplication, key uniqueness, and export of academic papers."""

    def __init__(self):
        self.papers: List[Paper] = []
        self._seen_dois: Set[str] = set()
        self._seen_titles: Set[str] = set()
        self._key_counts: Dict[str, int] = Counter()

    def add_paper(self, paper: Paper) -> bool:
        if paper.doi:
            clean_doi = paper.doi.lower().strip()
            if clean_doi in self._seen_dois:
                for existing in self.papers:
                    if existing.doi.lower().strip() == clean_doi:
                        if not existing.abstract and paper.abstract:
                            existing.abstract = paper.abstract
                        if not existing.journal and paper.journal:
                            existing.journal = paper.journal
                        if existing.citations < paper.citations:
                            existing.citations = paper.citations
                return False
            self._seen_dois.add(clean_doi)

        norm_title = re.sub(r'[^a-zA-Z0-9]', '', paper.title.lower())
        if norm_title in self._seen_titles and len(norm_title) > 10:
            return False
        self._seen_titles.add(norm_title)

        base_key = paper.bib_key
        self._key_counts[base_key] += 1
        if self._key_counts[base_key] > 1:
            paper.bib_key = f"{base_key}_{self._key_counts[base_key]}"

        self.papers.append(paper)
        return True

    def add_papers(self, papers: List[Paper]) -> int:
        added = 0
        for p in papers:
            if self.add_paper(p):
                added += 1
        return added

    def sort_by(self, criterion: str = "citations_desc"):
        if criterion == "citations_desc":
            self.papers.sort(key=lambda p: (p.citations, p.year or 0), reverse=True)
        elif criterion == "year_desc":
            self.papers.sort(key=lambda p: (p.year or 0, p.citations), reverse=True)
        elif criterion == "year_asc":
            self.papers.sort(key=lambda p: (p.year or 9999, p.citations))

    def export_bibtex(self, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"% Auto-generated by CCC Literature Scout ({len(self.papers)} entries)\n")
            f.write(f"% Generated at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for p in self.papers:
                f.write(p.to_bibtex() + "\n\n")

    def export_json(self, output_path: str):
        data = [p.to_dict() for p in self.papers]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_matrix_csv(self, output_path: str):
        import csv
        fieldnames = ["BibKey", "Title", "Authors", "Year", "Journal", "Citations", "DOI", "HasAbstract", "Source", "Abstract"]
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.papers:
                writer.writerow({
                    "BibKey": p.bib_key,
                    "Title": p.title,
                    "Authors": "; ".join(p.authors[:5]) + (" et al." if len(p.authors) > 5 else ""),
                    "Year": p.year or "",
                    "Journal": p.journal,
                    "Citations": p.citations,
                    "DOI": p.doi,
                    "HasAbstract": "Yes" if len(p.abstract) > 30 else "No",
                    "Source": p.source,
                    "Abstract": p.abstract
                })

    def generate_synthesis_report(self, topic: str = "") -> str:
        total = len(self.papers)
        with_abstract = sum(1 for p in self.papers if len(p.abstract) > 30)
        
        years = [p.year for p in self.papers if p.year]
        year_counts = Counter(years)
        sorted_years = sorted(year_counts.keys())
        
        sorted_by_cites = sorted(self.papers, key=lambda p: p.citations, reverse=True)
        landmarks = sorted_by_cites[:min(8, total)]
        
        current_year = max(years) if years else 2026
        recent = [p for p in self.papers if p.year and p.year >= current_year - 2][:8]

        report = []
        report.append(f"# Literature Synthesis Report: {topic or 'Academic Corpus'}")
        report.append(f"\n- **Total Papers Collected**: {total}")
        report.append(f"- **Papers with Full Abstract**: {with_abstract} ({with_abstract/total*100:.1f}%)" if total else "- **Papers**: 0")
        report.append(f"- **Time Horizon**: {min(years) if years else 'N/A'} — {max(years) if years else 'N/A'}")
        
        report.append("\n## 1. Chronological Timeline & Publication Trend\n")
        report.append("| Year | Count | Key Milestones |")
        report.append("| :--- | :--- | :--- |")
        for y in sorted_years[-10:]:
            yr_papers = [p.bib_key for p in self.papers if p.year == y]
            report.append(f"| **{y}** | {year_counts[y]} papers | `\\cite{{{', '.join(yr_papers[:4])}}}` |")

        report.append("\n## 2. Landmark & Foundational Works (High Impact)\n")
        for i, p in enumerate(landmarks, 1):
            report.append(f"{i}. **{p.title}** ({p.year})")
            report.append(f"   - **Key**: `\\cite{{{p.bib_key}}}` | **Citations**: {p.citations} | **Venue**: *{p.journal}*")
            if p.abstract:
                report.append(f"   - *Summary*: {p.abstract[:220]}...")
            report.append("")

        report.append("## 3. Emerging Frontier Papers (Recent Advances)\n")
        for i, p in enumerate(recent, 1):
            report.append(f"{i}. **{p.title}** ({p.year}) — `\\cite{{{p.bib_key}}}`")
            report.append(f"   - *Venue*: *{p.journal}* | *Citations*: {p.citations}")
            if p.abstract:
                report.append(f"   - *Abstract*: {p.abstract[:200]}...")
            report.append("")

        return "\n".join(report)


# ==============================================================================
# Academic 5-Stage Introduction Generator (English & Chinese)
# ==============================================================================

class AcademicIntroGenerator:
    """
    Constructs a publication-grade LaTeX / Markdown Introduction following
    the standard 5-part Nature / Elsevier / IEEE logic chain:
    1. Broad Background & Practical Importance
    2. Dominant Methodological Paradigms & Categorized SOTA
    3. Fundamental Bottlenecks & Unresolved Research Gap
    4. Proposed Solution & Key Theoretical/Algorithmic Insights
    5. Core Technical Contributions & Article Structure
    """

    @classmethod
    def generate(
        cls,
        corpus: LiteratureCorpus,
        topic: str,
        method_name: str = "the proposed method",
        key_advantages: Optional[List[str]] = None,
        target_journal: str = "Elsevier / Top-Tier Journal",
        lang: str = "en"
    ) -> Dict[str, str]:
        
        papers = corpus.papers
        if not papers:
            raise ValueError("Corpus is empty. Please retrieve or load literature first.")

        theme_groups = cls._cluster_papers(papers)

        landmark_keys = [p.bib_key for p in sorted(papers, key=lambda x: x.citations, reverse=True)[:5]]
        recent_keys = [p.bib_key for p in sorted(papers, key=lambda x: (x.year or 0), reverse=True)[:6]]

        advs = key_advantages or [
            "Achieving compact continuous representation without exponential memory explosion.",
            "Eliminating mesh discretization bottlenecks while strictly preserving topological transport equivalence.",
            "Accelerating downstream finite-volume and multiscale PDE evaluations significantly."
        ]

        if lang == "zh":
            return cls._generate_zh(corpus, topic, method_name, advs, theme_groups, landmark_keys, recent_keys)
        else:
            return cls._generate_en(corpus, topic, method_name, advs, theme_groups, landmark_keys, recent_keys, target_journal)

    @classmethod
    def _generate_en(cls, corpus, topic, method_name, advs, theme_groups, landmark_keys, recent_keys, target_journal):
        latex_lines = [
            f"% ==============================================================================",
            f"% Section 1: Introduction",
            f"% Generated automatically by CCC Literature Scout",
            f"% Topic: {topic}",
            f"% Target Journal Style: {target_journal}",
            f"% ==============================================================================\n",
            r"\section{Introduction}",
            r"\label{sec:introduction}",
            ""
        ]

        p1 = (
            f"Understanding and accurately predicting the physical transport, structural durability, and "
            f"morphological evolution of complex media is of fundamental importance across materials science and computational mechanics "
            f"\\cite{{{', '.join(landmark_keys[:3])}}}. Microstructural geometries dictate macro-scale performance, "
            f"ranging from fluid permeability and ionic diffusivity to mechanical stress distributions. "
            f"With the rapid advancement of ultra-high-resolution imaging modalities such as synchrotron X-ray computed "
            f"micro-tomography ($\\mu$-CT) and focused ion beam scanning electron microscopy (FIB-SEM), researchers can now "
            f"digitize three-dimensional heterogeneous structures with sub-micron fidelity "
            f"\\cite{{{', '.join(landmark_keys[2:5])}}}. However, translating these massive volumetric datasets into "
            f"computationally tractable and physically robust predictive frameworks remains a central challenge."
        )
        latex_lines.append(p1 + "\n")

        p2_parts = [
            "Over the past decade, extensive computational and data-driven methodologies have been developed to address these challenges."
        ]
        for group_name, group_papers in list(theme_groups.items())[:3]:
            grp_keys = [p.bib_key for p in group_papers[:4]]
            if grp_keys:
                safe_group = cls._latex_escape(group_name.lower())
                p2_parts.append(
                    f"In the field of {safe_group}, seminal investigations \\cite{{{', '.join(grp_keys)}}} "
                    f"have demonstrated substantial progress in characterization and numerical modeling."
                )
        
        recent_sample = recent_keys[:3]
        if recent_sample:
            p2_parts.append(
                f"More recently, emerging deep learning frameworks and high-order coordinate approximation schemes \\cite{{{', '.join(recent_sample)}}} "
                f"have provided novel perspectives by parameterizing complex spatial functions continuously."
            )
        latex_lines.append(" ".join(p2_parts) + "\n")

        p3 = (
            "Despite these notable advances, a critical gap persists at the intersection of geometric representation "
            "and physical transport fidelity. Conventional Eulerian voxel grids suffer from severe cubic memory scaling ($O(N^3)$), "
            "which forces numerical simulations to truncate domain sizes or artificially coarsen spatial resolution. "
            "Conversely, standard deep neural surrogate models often behave as black-box approximators, lacking strict "
            "conservation guarantees and exhibiting substantial boundary discrepancies during downstream partial differential "
            "equation (PDE) evaluations. Crucially, high geometric similarity (e.g., standard volumetric Dice or IoU scores) "
            "does not inherently guarantee physical transport equivalence. Minor topological discontinuities or localized "
            "constrictions can dramatically alter effective transport coefficients, rendering conventional "
            "approximations physically inaccurate."
        )
        latex_lines.append(p3 + "\n")

        p4 = (
            f"To overcome these fundamental limitations, this paper proposes \\textbf{{{method_name}}}, a comprehensive "
            f"and physically anchored paradigm for {topic.lower()}. Rather than relying on discrete voxel arrays or unconstrained "
            f"global approximations, our framework seamlessly couples compact implicit coordinate representations with "
            f"physically consistent multiscale solvers. By enforcing continuous spatial derivatives and dedicated defect "
            f"correction mechanisms, the proposed methodology captures sub-voxel morphological details while ensuring "
            f"rigorous numerical convergence during transport PDE solves."
        )
        latex_lines.append(p4 + "\n")

        latex_lines.append(
            "The primary technical contributions of this work are summarized as follows:\n"
            r"\begin{enumerate}"
        )
        for adv in advs:
            latex_lines.append(f"    \\item \\textbf{{{adv.split(':')[0] if ':' in adv else 'Key Innovation'}}}: {adv}")
        latex_lines.append(
            r"\end{enumerate}" + "\n"
        )
        
        latex_lines.append(
            "The remainder of this manuscript is structured as follows. "
            r"Section~\ref{sec:methodology} details the mathematical formulation and algorithmic architecture of the proposed framework. "
            r"Section~\ref{sec:experiments} presents the experimental setup, canonical datasets, and baseline configurations. "
            r"Section~\ref{sec:results} provides a rigorous quantitative and qualitative evaluation across multiple transport scenarios. "
            r"Finally, Section~\ref{sec:conclusion} concludes the paper with discussions on broader implications and future outlook."
        )

        latex_content = "\n".join(latex_lines)

        md_lines = [
            f"# Introduction Draft: {topic}",
            f"\n*Auto-generated by CCC Literature Scout for {target_journal}*\n",
            "## 1. Background & Significance",
            p1,
            "\n## 2. Current Landscape & Methodological Paradigms",
            " ".join(p2_parts),
            "\n## 3. Critical Research Gaps & Pain Points",
            p3,
            f"\n## 4. Proposed Framework: {method_name}",
            p4,
            "\n## 5. Summary of Contributions",
            "\n".join([f"- **Contribution {i+1}**: {adv}" for i, adv in enumerate(advs)]),
            "\n## 6. Article Outline",
            "The remainder of this manuscript is organized into Methodology, Experimental Setup, Results & Discussion, and Conclusion."
        ]
        md_content = "\n".join(md_lines)

        return {"latex": latex_content, "markdown": md_content}

    @classmethod
    def _generate_zh(cls, corpus, topic, method_name, advs, theme_groups, landmark_keys, recent_keys):
        latex_lines = [
            f"% ==============================================================================",
            f"% 第一章：引言",
            f"% CCC Literature Scout 自动构建",
            f"% 研究主题: {topic}",
            f"% ==============================================================================\n",
            r"\section{引言}",
            r"\label{sec:introduction}",
            ""
        ]

        p1 = (
            f"深入理解与精准预测复杂多孔介质的微观传输行为、结构耐久性及演化规律，是计算材料学与工程力学领域的"
            f"核心基础课题 \\cite{{{', '.join(landmark_keys[:3])}}}。微观孔隙拓扑结构直接决定了材料的宏观宏观服役性能，"
            f"如渗透率、离子扩散系数与应力分布。近年来，随着高分辨率 X 射线计算机断层扫描（$\\mu$-CT）与聚焦离子束扫描电镜（FIB-SEM）"
            f"等成像技术的飞速发展，科研人员能够无损获取亚微米精度的三维微观结构数据 \\cite{{{', '.join(landmark_keys[2:5])}}}。"
            f"然而，如何将海量离散体素数据转化为计算高效且物理自洽的高保真表征与求解模型，仍是亟待突破的重大挑战。"
        )
        latex_lines.append(p1 + "\n")

        p2_parts = ["过去十年中，学术界针对该难题开展了大量前沿探索。"]
        for group_name, group_papers in list(theme_groups.items())[:3]:
            grp_keys = [p.bib_key for p in group_papers[:4]]
            if grp_keys:
                safe_group = cls._latex_escape(group_name)
                p2_parts.append(
                    f"在{safe_group}方面，经典研究 \\cite{{{', '.join(grp_keys)}}} "
                    f"在特征表征与数值模拟上取得了显著进展。"
                )
        if recent_keys[:3]:
            p2_parts.append(
                f"近期，以连续坐标映射为代表的新兴隐式神经表征方法 \\cite{{{', '.join(recent_keys[:3])}}} "
                f"进一步为打破分辨率限制提供了全新的连续建模视角。"
            )
        latex_lines.append(" ".join(p2_parts) + "\n")

        p3 = (
            "尽管现有方法取得了诸多突破，但在微观几何高保真重建与下游物理传输等效性之间仍存在关键瓶颈。"
            "传统欧拉体素网格存在严重的三次方内存爆炸问题（$O(N^3)$），迫使数值模拟必须牺牲计算域尺寸或进行人工粗化；"
            "而主流深度学习代理模型多为黑盒拟合，缺乏严格的守恒性约束，在偏微分方程（PDE）求解中易产生显著的边界数值缺陷。"
            "更为关键的是，几何维度的相似性（如高 Dice 或 IoU 分数）并不等价于物理传输特性的保真——微小的孔喉颈缩或拓扑不连续性"
            "即可引起宏观传输系数的剧烈偏差，导致下游模拟严重失真。"
        )
        latex_lines.append(p3 + "\n")

        p4 = (
            f"针对上述瓶颈，本文提出了 \\textbf{{{method_name}}}。本方法摆脱了对离散体素网格的传统依赖，"
            f"将紧凑的分层隐式坐标表征与多尺度物理求解器深度融合。通过引入连续空间导数约束与局部缺陷修正机制，"
            f"在实现高压缩比亚体素连续重建的同时，确保了微观结构在传输物理求解中的数值严格收敛。"
        )
        latex_lines.append(p4 + "\n")

        latex_lines.append(
            "本文的主要研究贡献如下：\n"
            r"\begin{enumerate}"
        )
        for i, adv in enumerate(advs, 1):
            latex_lines.append(f"    \\item \\textbf{{创新点 {i}}}: {adv}")
        latex_lines.append(
            r"\end{enumerate}" + "\n"
        )
        
        latex_lines.append(
            "本文余下部分结构安排如下：第~\\ref{sec:methodology}~节详细阐述所提方法的数学原理与算法架构；"
            "第~\\ref{sec:experiments}~节介绍实验设置、标准微观数据集与基线对比模型；"
            "第~\\ref{sec:results}~节展示传输性能与求解效率的量化实验结果；"
            "第~\\ref{sec:conclusion}~节总结全文并对未来研究方向进行展望。"
        )

        latex_content = "\n".join(latex_lines)

        md_lines = [
            f"# 引言草稿: {topic}",
            f"\n*由 CCC Literature Scout 自动生成*\n",
            "## 1. 研究背景与科学意义",
            p1,
            "\n## 2. 研究现状与主流方法分类",
            " ".join(p2_parts),
            "\n## 3. 关键瓶颈与尚未解决的科学问题",
            p3,
            f"\n## 4. 本文提出的解决方案: {method_name}",
            p4,
            "\n## 5. 主要学术贡献",
            "\n".join([f"- **贡献 {i+1}**: {adv}" for i, adv in enumerate(advs)]),
            "\n## 6. 论文结构安排",
            "本文后续章节依次为：方法原理、实验设计、结果与讨论、结论与展望。"
        ]
        md_content = "\n".join(md_lines)

        return {"latex": latex_content, "markdown": md_content}

    @staticmethod
    def _cluster_papers(papers: List[Paper]) -> Dict[str, List[Paper]]:
        clusters = {
            "Traditional Numerical & Microstructure Modeling": [],
            "Deep Learning & Machine Learning Surrogates": [],
            "Implicit Neural Representations & Continuous Fields": [],
            "Multiscale Transport & Porous Media Characterization": []
        }

        for p in papers:
            text = (p.title + " " + p.abstract + " " + p.journal).lower()
            if any(k in text for k in ["siren", "implicit neural", "inr", "neural field", "nerf", "hash encoding", "coordinate"]):
                clusters["Implicit Neural Representations & Continuous Fields"].append(p)
            elif any(k in text for k in ["neural network", "deep learning", "cnn", "surrogate", "machine learning", "gan"]):
                clusters["Deep Learning & Machine Learning Surrogates"].append(p)
            elif any(k in text for k in ["porous", "transport", "diffusivity", "permeability", "tortuosity", "microstructure", "cement", "concrete"]):
                clusters["Multiscale Transport & Porous Media Characterization"].append(p)
            else:
                clusters["Traditional Numerical & Microstructure Modeling"].append(p)

        return {k: v for k, v in clusters.items() if len(v) > 0}


# ==============================================================================
# Full Pipeline Controller & CLI
# ==============================================================================

def run_pipeline(
    keywords: List[str],
    topic: str,
    output_dir: str,
    limit_per_kw: int = 15,
    wos_file: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    method_name: str = "the proposed hierarchical implicit framework",
    lang: str = "en"
):
    os.makedirs(output_dir, exist_ok=True)
    corpus = LiteratureCorpus()

    print(f"\n{'='*70}")
    print(f"🚀 CCC Literature Scout & Introduction Synthesizer")
    print(f"{'='*70}")
    print(f"🎯 Target Topic: {topic}")
    print(f"📂 Output Directory: {output_dir}")
    print(f"🌐 Language: {'Chinese (中文)' if lang == 'zh' else 'English'}")

    # 1. Parse WoS export if provided
    if wos_file:
        print(f"\n[1/4] Ingesting Web of Science export: {wos_file}...")
        wos_papers = WoSParser.parse_file(wos_file)
        added = corpus.add_papers(wos_papers)
        print(f"      Parsed {len(wos_papers)} entries, added {added} unique papers.")

    # 2. Automated Multi-Source Queries
    print(f"\n[2/4] Executing multi-source literature queries for {len(keywords)} keywords...")
    for i, kw in enumerate(keywords, 1):
        print(f"      ({i}/{len(keywords)}) Searching: '{kw}'...")
        oa_results = OpenAlexFetcher.search(kw, limit=limit_per_kw, year_min=year_min, year_max=year_max)
        added_oa = corpus.add_papers(oa_results)
        
        arxiv_results = ArxivFetcher.search(kw, limit=min(8, limit_per_kw))
        added_arxiv = corpus.add_papers(arxiv_results)

        crossref_results = CrossrefFetcher.search(kw, limit=min(5, limit_per_kw))
        added_cr = corpus.add_papers(crossref_results)

        print(f"          -> Found: {len(oa_results)} OpenAlex, {len(arxiv_results)} arXiv, {len(crossref_results)} Crossref (Total New: {added_oa + added_arxiv + added_cr})")

    corpus.sort_by("citations_desc")
    print(f"\n[3/4] Deduplication & Corpus Finalization:")
    print(f"      Total Unique Papers: {len(corpus.papers)}")

    # 3. Export BibTeX, CSV Matrix, and JSON
    bib_path = os.path.join(output_dir, "references.bib")
    csv_path = os.path.join(output_dir, "literature_matrix.csv")
    json_path = os.path.join(output_dir, "literature_corpus.json")
    report_path = os.path.join(output_dir, "literature_synthesis.md")

    corpus.export_bibtex(bib_path)
    corpus.export_matrix_csv(csv_path)
    corpus.export_json(json_path)
    
    report_content = corpus.generate_synthesis_report(topic=topic)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"      ✅ BibTeX saved to: {bib_path}")
    print(f"      ✅ Literature Matrix CSV: {csv_path}")
    print(f"      ✅ Corpus JSON: {json_path}")
    print(f"      ✅ Synthesis Report: {report_path}")

    # 4. Generate 5-Stage Academic Introduction
    print(f"\n[4/4] Generating 5-stage publication-grade Introduction ({lang})...")
    drafts = AcademicIntroGenerator.generate(
        corpus=corpus,
        topic=topic,
        method_name=method_name,
        lang=lang
    )

    tex_path = os.path.join(output_dir, "introduction_draft.tex")
    md_path = os.path.join(output_dir, "introduction_draft.md")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(drafts["latex"])
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(drafts["markdown"])

    print(f"      ✅ LaTeX Introduction: {tex_path}")
    print(f"      ✅ Markdown Introduction: {md_path}")
    print(f"\n🎉 Pipeline complete! All artifacts ready in '{output_dir}'.\n")


def main():
    parser = argparse.ArgumentParser(
        description="CCC Literature Scout: Automated Literature Search, BibTeX Builder with Abstracts, and Introduction Generator."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p_pipe = subparsers.add_parser("pipeline", help="Run end-to-end literature retrieval and Introduction drafting.")
    p_pipe.add_argument("--keywords", "-k", nargs="+", required=True, help="List of keyword phrases to search.")
    p_pipe.add_argument("--topic", "-t", required=True, help="Main topic or title of the research paper.")
    p_pipe.add_argument("--output-dir", "-o", default="./literature_out", help="Directory to save generated files.")
    p_pipe.add_argument("--limit", "-l", type=int, default=15, help="Max results per keyword query.")
    p_pipe.add_argument("--wos-file", "-w", default=None, help="Path to Web of Science export file (.ciw, .txt, .bib, .ris).")
    p_pipe.add_argument("--year-min", type=int, default=None, help="Earliest publication year filter.")
    p_pipe.add_argument("--year-max", type=int, default=None, help="Latest publication year filter.")
    p_pipe.add_argument("--method-name", default="the proposed method", help="Name of your proposed algorithm/framework.")
    p_pipe.add_argument("--lang", choices=["en", "zh"], default="en", help="Language for generated Introduction (en or zh).")

    p_search = subparsers.add_parser("search", help="Search papers online and export BibTeX + CSV matrix.")
    p_search.add_argument("--keywords", "-k", nargs="+", required=True, help="List of keyword phrases.")
    p_search.add_argument("--output-dir", "-o", default="./literature_out", help="Output directory.")
    p_search.add_argument("--limit", "-l", type=int, default=20, help="Max results per keyword.")

    p_wos = subparsers.add_parser("parse-wos", help="Parse Web of Science / EndNote export files into clean BibTeX.")
    p_wos.add_argument("--input", "-i", required=True, help="Input file path (.ciw, .txt, .bib, .ris).")
    p_wos.add_argument("--output-dir", "-o", default="./literature_out", help="Output directory.")

    p_intro = subparsers.add_parser("write-intro", help="Generate Introduction draft from existing .bib file.")
    p_intro.add_argument("--bib", "-b", required=True, help="Input .bib file path.")
    p_intro.add_argument("--topic", "-t", required=True, help="Paper research topic.")
    p_intro.add_argument("--output-dir", "-o", default="./literature_out", help="Output directory.")
    p_intro.add_argument("--method-name", default="the proposed method", help="Name of proposed method.")
    p_intro.add_argument("--lang", choices=["en", "zh"], default="en", help="Language (en/zh).")

    args = parser.parse_args()

    if args.command == "pipeline":
        run_pipeline(
            keywords=args.keywords,
            topic=args.topic,
            output_dir=args.output_dir,
            limit_per_kw=args.limit,
            wos_file=args.wos_file,
            year_min=args.year_min,
            year_max=args.year_max,
            method_name=args.method_name,
            lang=args.lang
        )
    elif args.command == "search":
        run_pipeline(
            keywords=args.keywords,
            topic="Academic Literature Search",
            output_dir=args.output_dir,
            limit_per_kw=args.limit
        )
    elif args.command == "parse-wos":
        corpus = LiteratureCorpus()
        papers = WoSParser.parse_file(args.input)
        corpus.add_papers(papers)
        os.makedirs(args.output_dir, exist_ok=True)
        bib_path = os.path.join(args.output_dir, "wos_references.bib")
        csv_path = os.path.join(args.output_dir, "wos_matrix.csv")
        corpus.export_bibtex(bib_path)
        corpus.export_matrix_csv(csv_path)
        print(f"Exported {len(papers)} papers to {bib_path} and {csv_path}")
    elif args.command == "write-intro":
        corpus = LiteratureCorpus()
        papers = WoSParser.parse_file(args.bib)
        corpus.add_papers(papers)
        os.makedirs(args.output_dir, exist_ok=True)
        drafts = AcademicIntroGenerator.generate(
            corpus=corpus,
            topic=args.topic,
            method_name=args.method_name,
            lang=args.lang
        )
        tex_path = os.path.join(args.output_dir, "introduction_draft.tex")
        md_path = os.path.join(output_dir, "introduction_draft.md")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(drafts["latex"])
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(drafts["markdown"])
        print(f"Generated Introduction to {tex_path} and {md_path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
