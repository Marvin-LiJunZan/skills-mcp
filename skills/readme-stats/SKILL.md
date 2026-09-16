---
name: readme-stats
description: "Visual metrics and dynamic statistic cards inspired by GitHub Readme Stats (anuraghazra/github-readme-stats). Generates polished, vector-sharp SVG/HTML overview cards, progress meters, and dashboard KPI summaries."
metadata:
  short-description: "Dynamic visual statistics, KPI overview cards & progress meters"
---

# README Stats — Visual KPI Cards & Dynamic Metric Summaries

README Stats turns raw numbers, project health metrics, and performance telemetry into compact, beautifully styled SVG/HTML summary cards.

---

## 1. Visual Card Anatomy

A professional metric summary card consists of 4 tightly organized zones:

```text
┌────────────────────────────────────────────────────────┐
│  ⚡ System / Project Overview          [● Live Status] │
├────────────────────────────────────────────────────────┤
│  ⭐ Primary Metric: 99.4%   │  📈 Throughput: 1.2k/s   │
│  🔧 Active Nodes:   48      │  ⏱️ Latency:    14ms     │
├────────────────────────────────────────────────────────┤
│  Progress / Distribution Meter:                        │
│  ██████████████████████░░░░░░░░ 72% Capacity           │
└────────────────────────────────────────────────────────┘
```

---

## 2. Reusable SVG Card Template

```xml
<svg width="450" height="195" viewBox="0 0 450 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header { font: 600 16px 'Plus Jakarta Sans', -apple-system, sans-serif; fill: #0284c7; }
    .stat-label { font: 400 12px 'Plus Jakarta Sans', sans-serif; fill: #64748b; }
    .stat-val { font: 700 14px 'JetBrains Mono', monospace; fill: #0f172a; }
    .bold { font-weight: 700; }
  </style>
  <rect x="0.5" y="0.5" rx="8" width="449" height="194" fill="#ffffff" stroke="#e2e8f0" />
  
  <!-- Title & Icon -->
  <g transform="translate(25, 32)">
    <circle cx="6" cy="6" r="4" fill="#10b981" />
    <text x="18" y="10" class="header">Telemetry Overview</text>
  </g>
  
  <!-- Metrics Grid -->
  <g transform="translate(25, 75)">
    <text x="0" y="0" class="stat-label">Model Convergence:</text>
    <text x="180" y="0" class="stat-val">99.82%</text>
    
    <text x="0" y="26" class="stat-label">RMSE Loss:</text>
    <text x="180" y="26" class="stat-val">0.0014</text>
    
    <text x="0" y="52" class="stat-label">GPU Memory Peak:</text>
    <text x="180" y="52" class="stat-val">6.2 GB</text>
  </g>
  
  <!-- Progress Bar -->
  <g transform="translate(25, 155)">
    <rect width="400" height="6" rx="3" fill="#f1f5f9" />
    <rect width="320" height="6" rx="3" fill="#0284c7" />
  </g>
</svg>
```

---

## 3. Best Practices

- **Zero Blurry Bitmaps**: Always render metric cards as scalable vector graphics (`.svg`) or native HTML/CSS flexboxes.
- **Monospace for Numbers**: Always format numbers, units, and timestamps using clean monospace fonts (`JetBrains Mono`, `Fira Code`) to prevent column jitter when numbers update.
