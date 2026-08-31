#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCC Literature Scout & Introduction Synthesizer (V2.0 - Massive Scale)
======================================================================
Two-Stage Automated Academic Pipeline:
- STAGE 1: Massively search per keyword (up to 1000 papers per keyword with full abstracts)
           and export dedicated '<keyword>.bib' and '<keyword>_matrix.csv' files.
- STAGE 2: Deep synthesis across all keyword bibs (deduplication, landmark ranking,
           thematic clustering, timeline trends) and draft 5-stage publication-grade
           LaTeX/Markdown Introduction with real citation anchors.

Supported Engines:
- Web of Science Clarivate API (Starter / Expanded API via WOS_API_KEY)
- OpenAlex API (250M+ open catalog, paginated up to 1000+ items with full abstract reconstruction)
- arXiv API (paginated CS/AI/Physics/Math preprints)
- Crossref API (official DOIs & publisher metadata)
- Campus Web of Science Export Ingestion (.ciw / .txt / .bib / .ris batch folder)
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
# Search & Fetch Engines (Massive Pagination up to 1000)
# ==============================================================================

class WoSClarivateFetcher:
    """Fetches papers directly from Clarivate Web of Science Starter/Expanded API."""
    BASE_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"

    @classmethod
    def search(
        cls,
        query: str,
        limit: int = 1000,
        api_key: Optional[str] = None
    ) -> List[Paper]:
        key = api_key or os.environ.get("WOS_API_KEY") or "46a27738d76806c95a4a2797cdada4126ff8f800"
        if not key:
            return []

        papers = []
        page = 1
        per_page = 50  # Clarivate starter API limit per page

        while len(papers) < limit:
            params = {
                "q": f"TS=({query})",
                "limit": per_page,
                "page": page
            }
            url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(
                url,
                headers={
                    "X-ApiKey": key,
                    "User-Agent": "CCC-WoS-Scout/2.0"
                }
            )

            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    hits = data.get("hits", [])
                    if not hits:
                        break

                    for doc in hits:
                        title = doc.get("title", "")
                        authors = [a.get("displayName", "") for a in doc.get("names", {}).get("authors", [])]
                        pub = doc.get("publication", {})
                        year = pub.get("year")
                        journal = pub.get("sourceTitle", "")
                        doi = doc.get("links", {}).get("doi", "")
                        abstract = doc.get("abstract", "")
                        cites = 0
                        if doc.get("citations"):
                            cites = doc["citations"][0].get("count", 0)

                        papers.append(Paper(
                            title=title,
                            authors=authors,
                            year=year,
                            journal=journal,
                            doi=doi,
                            abstract=abstract,
                            citations=cites,
                            source="WebOfScience_API"
                        ))

                    if len(hits) < per_page or len(papers) >= limit:
                        break
                    page += 1
                    time.sleep(0.2)
            except Exception as e:
                print(f"[WoS API] Error at page {page}: {e}", file=sys.stderr)
                break

        return papers[:limit]


class OpenAlexFetcher:
    """Fetches up to 1000 papers per keyword with full abstract reconstruction from OpenAlex (250M+ catalog)."""
    BASE_URL = "https://api.openalex.org/works"

    @classmethod
    def search(
        cls,
        query: str,
        limit: int = 1000,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        verbose: bool = True
    ) -> List[Paper]:
        papers = []
        page = 1
        per_page = 100  # Max per_page allowed by OpenAlex

        filters = []
        if year_min and year_max:
            filters.append(f"publication_year:{year_min}-{year_max}")
        elif year_min:
            filters.append(f"publication_year:>{year_min - 1}")
        elif year_max:
            filters.append(f"publication_year:<{year_max + 1}")

        filter_str = ",".join(filters) if filters else ""

        while len(papers) < limit:
            batch_size = min(per_page, limit - len(papers))
            params = {
                "search": query,
                "per_page": batch_size,
                "page": page,
                "sort": "relevance_score:desc"
            }
            if filter_str:
                params["filter"] = filter_str

            url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "mailto:academic-researcher@university.edu (CCC-Literature-Scout-Bot)"
                }
            )

            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    results = data.get("results", [])
                    if not results:
                        break

                    for work in results:
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

                    if verbose:
                        print(f"        -> [OpenAlex] Page {page}: fetched {len(results)} items (Total: {len(papers)}/{limit})")

                    if len(results) < batch_size or len(papers) >= limit:
                        break
                    
                    page += 1
                    time.sleep(0.1)  # Respect polite rate limit
            except Exception as e:
                if verbose:
                    print(f"        [OpenAlex] Warning at page {page}: {e}", file=sys.stderr)
                break

        return papers[:limit]


class ArxivFetcher:
    """Fetches paginated preprints with abstracts from arXiv API."""
    BASE_URL = "http://export.arxiv.org/api/query"

    @classmethod
    def search(cls, query: str, limit: int = 100) -> List[Paper]:
        papers = []
        start = 0
        batch_size = 100

        while len(papers) < limit:
            cur_batch = min(batch_size, limit - len(papers))
            clean_query = query.replace(" ", "+")
            url = f"{cls.BASE_URL}?search_query=all:{urllib.parse.quote(clean_query)}&start={start}&max_results={cur_batch}&sortBy=relevance&sortOrder=descending"
            
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "CCC-Literature-Scout-Bot"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    xml_data = resp.read()
                    root = ET.fromstring(xml_data)
                    
                    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
                    entries = root.findall('atom:entry', ns)
                    if not entries:
                        break

                    for entry in entries:
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
                        
                        papers.append(Paper(
                            title=title,
                            authors=authors,
                            year=year,
                            journal=f"arXiv preprint arXiv:{arxiv_id}" if arxiv_id else "arXiv",
                            doi=doi,
                            abstract=abstract,
                            url=url_str,
                            citations=0,
                            source="arXiv"
                        ))

                    if len(entries) < cur_batch or len(papers) >= limit:
                        break
                    start += len(entries)
                    time.sleep(0.3)
            except Exception as e:
                print(f"[arXiv] Warning at offset {start}: {e}", file=sys.stderr)
                break

        return papers[:limit]


class CrossrefFetcher:
    """Fetches paginated records with DOIs and abstracts from Crossref API."""
    BASE_URL = "https://api.crossref.org/works"

    @classmethod
    def search(cls, query: str, limit: int = 200) -> List[Paper]:
        papers = []
        offset = 0
        rows = 50

        while len(papers) < limit:
            cur_rows = min(rows, limit - len(papers))
            params = {
                "query": query,
                "rows": cur_rows,
                "offset": offset,
                "sort": "relevance"
            }
            url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers={"User-Agent": "CCC-Literature-Scout (mailto:researcher@univ.edu)"})
            
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    items = data.get("message", {}).get("items", [])
                    if not items:
                        break

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
                        
                        papers.append(Paper(
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
                        ))

                    if len(items) < cur_rows or len(papers) >= limit:
                        break
                    offset += len(items)
                    time.sleep(0.2)
            except Exception as e:
                print(f"[Crossref] Warning at offset {offset}: {e}", file=sys.stderr)
                break
                
        return papers[:limit]


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
    def parse_directory(cls, dirpath: str) -> List[Paper]:
        """Parses all WoS export files in a directory."""
        if not os.path.isdir(dirpath):
            return []
        all_papers = []
        for root, _, files in os.walk(dirpath):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in [".ciw", ".txt", ".bib", ".ris", ".enw"]:
                    full_path = os.path.join(root, file)
                    try:
                        p_list = cls.parse_file(full_path)
                        all_papers.extend(p_list)
                    except Exception as e:
                        print(f"Warning parsing {full_path}: {e}", file=sys.stderr)
        return all_papers

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
        landmarks = sorted_by_cites[:min(12, total)]
        
        current_year = max(years) if years else 2026
        recent = [p for p in self.papers if p.year and p.year >= current_year - 2][:12]

        report = []
        report.append(f"# Literature Synthesis Report: {topic or 'Academic Corpus'}")
        report.append(f"\n- **Total Papers in Unified Corpus**: {total}")
        report.append(f"- **Papers with Full Abstract**: {with_abstract} ({with_abstract/total*100:.1f}%)" if total else "- **Papers**: 0")
        report.append(f"- **Time Horizon**: {min(years) if years else 'N/A'} — {max(years) if years else 'N/A'}")
        
        report.append("\n## 1. Chronological Timeline & Publication Trend\n")
        report.append("| Year | Count | Key Milestones |")
        report.append("| :--- | :--- | :--- |")
        for y in sorted_years[-12:]:
            yr_papers = [p.bib_key for p in self.papers if p.year == y]
            report.append(f"| **{y}** | {year_counts[y]} papers | `\\cite{{{', '.join(yr_papers[:4])}}}` |")

        report.append("\n## 2. Landmark & Foundational Works (High Impact Ranking)\n")
        for i, p in enumerate(landmarks, 1):
            report.append(f"{i}. **{p.title}** ({p.year})")
            report.append(f"   - **Key**: `\\cite{{{p.bib_key}}}` | **Citations**: {p.citations} | **Venue**: *{p.journal}*")
            if p.abstract:
                report.append(f"   - *Summary*: {p.abstract[:220]}...")
            report.append("")

        report.append("## 3. Emerging Frontier Papers (Recent Advances 2024-2026)\n")
        for i, p in enumerate(recent, 1):
            report.append(f"{i}. **{p.title}** ({p.year}) — `\\cite{{{p.bib_key}}}`")
            report.append(f"   - *Venue*: *{p.journal}* | *Citations*: {p.citations}")
            if p.abstract:
                report.append(f"   - *Abstract*: {p.abstract[:200]}...")
            report.append("")

        return "\n".join(report)


# ==============================================================================
# Academic 5-Stage Introduction Generator
# ==============================================================================

class AcademicIntroGenerator:
    """
    Constructs a publication-grade LaTeX / Markdown Introduction following
    the standard 5-part Nature / Elsevier / IEEE logic chain.
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

        landmark_keys = [p.bib_key for p in sorted(papers, key=lambda x: x.citations, reverse=True)[:6]]
        recent_keys = [p.bib_key for p in sorted(papers, key=lambda x: (x.year or 0), reverse=True)[:8]]

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
            f"% Generated automatically by CCC Literature Scout (Deep Multi-Keyword Synthesis)",
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
                safe_group = Paper._latex_escape(group_name.lower())
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
            f"% CCC Literature Scout 自动构建（多关键词大规模融合）",
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
                safe_group = Paper._latex_escape(group_name)
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
# Stage 1 & Stage 2 Execution Controllers
# ==============================================================================

def slugify_keyword(keyword: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '_', keyword.strip()).strip('_')
    return slug[:50] or "keyword"


def stage1_fetch_keywords(
    keywords: List[str],
    output_dir: str,
    limit_per_kw: int = 1000,
    wos_api_key: Optional[str] = None,
    wos_dir: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None
) -> List[str]:
    """
    STAGE 1: Executes massive-scale retrieval per keyword (up to 1000 papers each).
    Outputs one dedicated '<slug>.bib' and '<slug>_matrix.csv' for each keyword.
    Returns list of generated .bib file paths.
    """
    bib_dir = os.path.join(output_dir, "bib_by_keyword")
    os.makedirs(bib_dir, exist_ok=True)
    generated_bibs = []

    print(f"\n{'='*75}")
    print(f"📦 [STAGE 1] Massive Literature Retrieval (Limit: {limit_per_kw} papers/keyword)")
    print(f"{'='*75}")
    print(f"📂 Output Folder for Keyword Bibs: {bib_dir}")

    # Check for Web of Science export directory if specified
    wos_papers_pool = []
    if wos_dir and os.path.isdir(wos_dir):
        print(f"[*] Ingesting campus Web of Science directory: {wos_dir}...")
        wos_papers_pool = WoSParser.parse_directory(wos_dir)
        print(f"    Found {len(wos_papers_pool)} total papers in WoS export files.")

    for i, kw in enumerate(keywords, 1):
        slug = f"{i:02d}_{slugify_keyword(kw)}"
        bib_file = os.path.join(bib_dir, f"{slug}.bib")
        csv_file = os.path.join(bib_dir, f"{slug}_matrix.csv")
        
        print(f"\n[{i}/{len(keywords)}] 🔍 Fetching keyword: '{kw}' (Target: max {limit_per_kw} papers)...")
        kw_corpus = LiteratureCorpus()

        # 1. WoS API (Clarivate Starter API)
        wos_key = wos_api_key or os.environ.get("WOS_API_KEY") or "46a27738d76806c95a4a2797cdada4126ff8f800"
        if wos_key:
            print(f"      - Querying Web of Science Clarivate API...")
            wos_api_results = WoSClarivateFetcher.search(kw, limit=limit_per_kw, api_key=wos_key)
            added_wos = kw_corpus.add_papers(wos_api_results)
            print(f"        -> WoS API: {len(wos_api_results)} records (Added {added_wos})")

        # 2. WoS Directory matches
        if wos_papers_pool:
            matched_wos = [p for p in wos_papers_pool if kw.lower() in (p.title + " " + p.abstract).lower()]
            added_pool = kw_corpus.add_papers(matched_wos)
            if added_pool > 0:
                print(f"        -> WoS Local Exports: Matched and added {added_pool} papers")

        # 3. OpenAlex massive pagination (250M catalog)
        needed = limit_per_kw - len(kw_corpus.papers)
        if needed > 0:
            print(f"      - Querying OpenAlex Catalog (paginating up to {needed} items)...")
            oa_results = OpenAlexFetcher.search(kw, limit=needed, year_min=year_min, year_max=year_max, verbose=True)
            added_oa = kw_corpus.add_papers(oa_results)
            print(f"        -> OpenAlex: retrieved {len(oa_results)} works (Added {added_oa})")

        # 4. arXiv supplement
        needed = limit_per_kw - len(kw_corpus.papers)
        if needed > 0:
            arxiv_results = ArxivFetcher.search(kw, limit=min(100, needed))
            added_arxiv = kw_corpus.add_papers(arxiv_results)
            if added_arxiv > 0:
                print(f"        -> arXiv: retrieved {len(arxiv_results)} preprints (Added {added_arxiv})")

        # 5. Crossref supplement
        needed = limit_per_kw - len(kw_corpus.papers)
        if needed > 0:
            cr_results = CrossrefFetcher.search(kw, limit=min(100, needed))
            added_cr = kw_corpus.add_papers(cr_results)
            if added_cr > 0:
                print(f"        -> Crossref: retrieved {len(cr_results)} works (Added {added_cr})")

        # Sort and export keyword bib
        kw_corpus.sort_by("citations_desc")
        kw_corpus.export_bibtex(bib_file)
        kw_corpus.export_matrix_csv(csv_file)
        generated_bibs.append(bib_file)

        print(f"      ✅ Saved {len(kw_corpus.papers)} papers to: {os.path.basename(bib_file)}")
        print(f"      ✅ Saved matrix to: {os.path.basename(csv_file)}")

    print(f"\n🎉 [STAGE 1 COMPLETE] Generated {len(generated_bibs)} individual keyword BibTeX files.")
    return generated_bibs


def stage2_synthesize_introduction(
    bib_sources: List[str],
    topic: str,
    output_dir: str,
    method_name: str = "the proposed hierarchical implicit framework",
    key_advantages: Optional[List[str]] = None,
    lang: str = "en"
):
    """
    STAGE 2: Merges and analyzes all keyword bib files, performs global deduplication,
    builds the master literature matrix, and writes the 5-stage Introduction draft.
    """
    os.makedirs(output_dir, exist_ok=True)
    master_corpus = LiteratureCorpus()

    print(f"\n{'='*75}")
    print(f"🧠 [STAGE 2] Deep Literature Synthesis & Academic Introduction Drafting")
    print(f"{'='*75}")
    print(f"🎯 Target Topic: {topic}")
    print(f"🌐 Language: {'Chinese (中文)' if lang == 'zh' else 'English'}")

    # Ingest all bib files
    total_raw_entries = 0
    for b_path in bib_sources:
        if os.path.isfile(b_path):
            papers = WoSParser.parse_file(b_path)
            total_raw_entries += len(papers)
            master_corpus.add_papers(papers)
        elif os.path.isdir(b_path):
            papers = WoSParser.parse_directory(b_path)
            total_raw_entries += len(papers)
            master_corpus.add_papers(papers)

    master_corpus.sort_by("citations_desc")

    print(f"[*] Ingested {total_raw_entries} raw entries across all keyword Bibs.")
    print(f"[*] Global Deduplication Result: {len(master_corpus.papers)} unique academic papers.")

    # Export master unified files
    master_bib = os.path.join(output_dir, "master_unified_references.bib")
    master_csv = os.path.join(output_dir, "master_literature_matrix.csv")
    master_json = os.path.join(output_dir, "master_literature_corpus.json")
    report_path = os.path.join(output_dir, "master_literature_synthesis.md")

    master_corpus.export_bibtex(master_bib)
    master_corpus.export_matrix_csv(master_csv)
    master_corpus.export_json(master_json)

    synthesis_report = master_corpus.generate_synthesis_report(topic=topic)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(synthesis_report)

    print(f"      ✅ Master Unified BibTeX ({len(master_corpus.papers)} entries): {master_bib}")
    print(f"      ✅ Master Literature Matrix CSV: {master_csv}")
    print(f"      ✅ Master Synthesis Report: {report_path}")

    # Draft 5-Stage Introduction
    print(f"\n[*] Drafting 5-Stage Publication-Grade Introduction ({lang})...")
    drafts = AcademicIntroGenerator.generate(
        corpus=master_corpus,
        topic=topic,
        method_name=method_name,
        key_advantages=key_advantages,
        lang=lang
    )

    tex_path = os.path.join(output_dir, "introduction_draft.tex")
    md_path = os.path.join(output_dir, "introduction_draft.md")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(drafts["latex"])
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(drafts["markdown"])

    print(f"      ✅ LaTeX Introduction (with real \\cite{{...}}): {tex_path}")
    print(f"      ✅ Markdown Introduction Draft: {md_path}")
    print(f"\n🎉 [STAGE 2 COMPLETE] All literature analysis & introduction drafts ready in '{output_dir}'.\n")


def run_full_pipeline(
    keywords: List[str],
    topic: str,
    output_dir: str,
    limit_per_kw: int = 1000,
    wos_api_key: Optional[str] = None,
    wos_dir: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    method_name: str = "the proposed hierarchical implicit framework",
    lang: str = "en"
):
    """Executes Stage 1 followed immediately by Stage 2."""
    bib_files = stage1_fetch_keywords(
        keywords=keywords,
        output_dir=output_dir,
        limit_per_kw=limit_per_kw,
        wos_api_key=wos_api_key,
        wos_dir=wos_dir,
        year_min=year_min,
        year_max=year_max
    )

    stage2_synthesize_introduction(
        bib_sources=bib_files,
        topic=topic,
        output_dir=output_dir,
        method_name=method_name,
        lang=lang
    )


# ==============================================================================
# CLI Entry Point
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CCC Literature Scout V2: 2-Stage Massive Academic Retrieval (up to 1000 papers/kw) & Introduction Synthesizer."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available execution modes")

    # Command: pipeline (Stage 1 + Stage 2)
    p_pipe = subparsers.add_parser("pipeline", help="Run full 2-stage pipeline: fetch 1000 papers/keyword to separate bibs, then synthesize introduction.")
    p_pipe.add_argument("--keywords", "-k", nargs="+", required=True, help="List of keyword phrases.")
    p_pipe.add_argument("--topic", "-t", required=True, help="Paper research topic / title.")
    p_pipe.add_argument("--output-dir", "-o", default="./literature_out", help="Root output directory.")
    p_pipe.add_argument("--limit", "-l", type=int, default=1000, help="Max papers per keyword (default: 1000).")
    p_pipe.add_argument("--wos-api-key", default=None, help="Clarivate Web of Science API Key.")
    p_pipe.add_argument("--wos-dir", default=None, help="Directory containing campus Web of Science export files (.ciw, .txt, .bib).")
    p_pipe.add_argument("--year-min", type=int, default=None, help="Earliest publication year.")
    p_pipe.add_argument("--year-max", type=int, default=None, help="Latest publication year.")
    p_pipe.add_argument("--method-name", default="the proposed hierarchical implicit framework", help="Proposed framework name.")
    p_pipe.add_argument("--lang", choices=["en", "zh"], default="en", help="Language (en or zh).")

    # Command: stage1-fetch
    p_s1 = subparsers.add_parser("stage1-fetch", help="Stage 1 ONLY: Fetch up to 1000 papers per keyword and save one bib file per keyword.")
    p_s1.add_argument("--keywords", "-k", nargs="+", required=True, help="List of keywords.")
    p_s1.add_argument("--output-dir", "-o", default="./literature_out", help="Output directory.")
    p_s1.add_argument("--limit", "-l", type=int, default=1000, help="Max papers per keyword (default: 1000).")
    p_s1.add_argument("--wos-api-key", default=None, help="Clarivate API key.")
    p_s1.add_argument("--wos-dir", default=None, help="Directory with WoS exports.")
    p_s1.add_argument("--year-min", type=int, default=None, help="Earliest year.")
    p_s1.add_argument("--year-max", type=int, default=None, help="Latest year.")

    # Command: stage2-synthesize
    p_s2 = subparsers.add_parser("stage2-synthesize", help="Stage 2 ONLY: Ingest all keyword bib files, synthesize corpus, and write Introduction.")
    p_s2.add_argument("--bib-dir", "-b", required=True, help="Directory containing keyword .bib files, or path to specific .bib file.")
    p_s2.add_argument("--topic", "-t", required=True, help="Research topic.")
    p_s2.add_argument("--output-dir", "-o", default="./literature_out", help="Output directory.")
    p_s2.add_argument("--method-name", default="the proposed hierarchical implicit framework", help="Proposed framework name.")
    p_s2.add_argument("--lang", choices=["en", "zh"], default="en", help="Language (en or zh).")

    args = parser.parse_args()

    if args.command == "pipeline":
        run_full_pipeline(
            keywords=args.keywords,
            topic=args.topic,
            output_dir=args.output_dir,
            limit_per_kw=args.limit,
            wos_api_key=args.wos_api_key,
            wos_dir=args.wos_dir,
            year_min=args.year_min,
            year_max=args.year_max,
            method_name=args.method_name,
            lang=args.lang
        )
    elif args.command == "stage1-fetch":
        stage1_fetch_keywords(
            keywords=args.keywords,
            output_dir=args.output_dir,
            limit_per_kw=args.limit,
            wos_api_key=args.wos_api_key,
            wos_dir=args.wos_dir,
            year_min=args.year_min,
            year_max=args.year_max
        )
    elif args.command == "stage2-synthesize":
        stage2_synthesize_introduction(
            bib_sources=[args.bib_dir],
            topic=args.topic,
            output_dir=args.output_dir,
            method_name=args.method_name,
            lang=args.lang
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
