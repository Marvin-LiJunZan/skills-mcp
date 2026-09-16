#!/usr/bin/env python3
"""
paper_rag.py — Standalone Academic Paper RAG & Retrieval Engine.
Indexes Markdown, Text, and LaTeX files into searchable chunks using BM25 / TF-IDF scoring.
Zero external dependencies required (uses standard library).
"""

import sys
import os
import re
import math
import json
import argparse
from pathlib import Path
from collections import Counter


def tokenize(text):
    text = text.lower()
    words = re.findall(r"\b[a-z0-9_\-\u4e00-\u9fa5]{2,}\b", text)
    return words


def chunk_text(text, max_words=200, overlap=40):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = []
    current_len = 0
    
    for p in paragraphs:
        tokens = tokenize(p)
        if current_len + len(tokens) > max_words and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = current_chunk[-1:] if overlap > 0 else []
            current_len = len(tokenize(current_chunk[0])) if current_chunk else 0
        current_chunk.append(p)
        current_len += len(tokens)
        
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks


def build_index(doc_dir, output_db):
    docs = []
    doc_paths = list(Path(doc_dir).glob("**/*.md")) + list(Path(doc_dir).glob("**/*.txt")) + list(Path(doc_dir).glob("**/*.tex"))
    
    print(f"Indexing {len(doc_paths)} documents from {doc_dir}...")
    chunk_list = []
    
    for p in doc_paths:
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            chunks = chunk_text(content)
            for idx, c in enumerate(chunks):
                tokens = tokenize(c)
                if len(tokens) < 10:
                    continue
                chunk_list.append({
                    "id": f"{p.stem}_{idx}",
                    "source": str(p),
                    "text": c,
                    "tokens": tokens
                })
        except Exception as e:
            print(f"Error reading {p}: {e}")
            
    # Calculate IDF
    N = len(chunk_list)
    df = Counter()
    for item in chunk_list:
        unique_words = set(item["tokens"])
        for w in unique_words:
            df[w] += 1
            
    idf = {w: math.log((N - freq + 0.5) / (freq + 0.5) + 1) for w, freq in df.items()}
    
    db_data = {
        "num_chunks": N,
        "idf": idf,
        "chunks": [{"id": c["id"], "source": c["source"], "text": c["text"], "tokens": c["tokens"]} for c in chunk_list]
    }
    
    with open(output_db, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False)
        
    print(f"Successfully indexed {N} chunks to {output_db}")


def search_index(db_path, query, top_k=5):
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return []
        
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    q_tokens = tokenize(query)
    if not q_tokens:
        print("Query has no valid tokens.")
        return []
        
    chunks = db["chunks"]
    idf = db["idf"]
    k1 = 1.5
    b = 0.75
    
    avg_dl = sum(len(c["tokens"]) for c in chunks) / (len(chunks) or 1)
    
    scores = []
    for c in chunks:
        tokens = c["tokens"]
        doc_len = len(tokens)
        counts = Counter(tokens)
        score = 0.0
        for qt in q_tokens:
            if qt in counts:
                tf = counts[qt]
                q_idf = idf.get(qt, 0.5)
                score += q_idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_dl)))
        if score > 0:
            scores.append((score, c))
            
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Paper RAG search engine")
    subparsers = parser.add_subparsers(dest="command")
    
    idx_p = subparsers.add_parser("index")
    idx_p.add_argument("--dir", required=True, help="Directory containing papers or notes")
    idx_p.add_argument("--db", default="paper_index.json", help="Output database file")
    
    qry_p = subparsers.add_parser("query")
    qry_p.add_argument("--db", default="paper_index.json", help="Database file")
    qry_p.add_argument("--query", required=True, help="Search query")
    qry_p.add_argument("--top_k", type=int, default=3, help="Number of results")
    
    args = parser.parse_args()
    if args.command == "index":
        build_index(args.dir, args.db)
    elif args.command == "query":
        results = search_index(args.db, args.query, args.top_k)
        print("=" * 60)
        print(f"Top {len(results)} Evidence Chunks for: '{args.query}'")
        print("=" * 60)
        for i, (score, chunk) in enumerate(results, 1):
            print(f"\n[{i}] Source: {chunk['source']} (Score: {score:.3f})")
            print("-" * 50)
            print(chunk["text"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
