#!/usr/bin/env python3
"""
build_survey.py — Generates structured literature review matrices and taxonomy outlines.
"""

import sys
import json
import argparse
from pathlib import Path


def generate_survey_outline(topic, categories, papers=None):
    md = []
    md.append(f"# A Comprehensive Survey on {topic}\n")
    md.append("## 1. Introduction & Motivation\n")
    md.append("- **Emergence & Need**: Rapid progress in this field necessitates a systematic synthesis.")
    md.append("- **Contributions of this Survey**: Novel taxonomy, comprehensive matrix, open challenges.\n")
    
    md.append("## 2. Taxonomy & Structural Classification\n")
    for i, cat in enumerate(categories, 1):
        md.append(f"### 2.{i} {cat}")
        md.append(f"- Principles, governing assumptions, and standard formulation of {cat}.\n")
        
    md.append("## 3. Methodological Comparison Matrix\n")
    md.append("| Method Paradigm | Input Modality | Core Assumption | Primary Advantage | Major Bottleneck | Representative Studies |")
    md.append("|---|---|---|---|---|---|")
    for cat in categories:
        md.append(f"| **{cat}** | Multi-modal / Tabular | Empirical consistency | High precision | Generalizability | Author et al. (2024) |")
    md.append("\n")
    
    md.append("## 4. Historical Trajectory & Paradigm Evolution\n")
    md.append("1. **Phase I (Foundations)**: Hand-crafted feature engineering and classical theories.")
    md.append("2. **Phase II (Deep Era)**: Representation learning and non-linear approximations.")
    md.append("3. **Phase III (Foundation & Generative)**: Multimodal integration and Physics-Informed reasoning.\n")
    
    md.append("## 5. Open Research Deadlocks & Future Horizons\n")
    md.append("- **Challenge 1**: Real-world data scarcity and domain drift.")
    md.append("- **Challenge 2**: Physics-governed interpretability vs black-box throughput.")
    md.append("- **Challenge 3**: Multi-scale cross-validation and standard benchmark suites.\n")
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Survey Builder Outline Generator")
    parser.add_argument("--topic", default="Machine Learning in Structural & Material Engineering", help="Survey Topic")
    parser.add_argument("--categories", nargs="+", default=["Classical ML", "Physics-Informed Neural Nets (PINNs)", "Graph Neural Networks", "Generative Modeling"], help="Taxonomy Categories")
    parser.add_argument("--output", default="survey_framework.md", help="Output file")
    args = parser.parse_args()
    
    content = generate_survey_outline(args.topic, args.categories)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Generated comprehensive survey structure at: {args.output}")


if __name__ == "__main__":
    main()
