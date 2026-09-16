---
name: fontsource
description: "Open-source typography and self-hosted web fonts management using Fontsource (fontsource/fontsource). Provides professional typography pairing, font loading strategies, and readable scales for high-density interfaces."
metadata:
  short-description: "Professional open-source typography & self-hosted fonts"
---

# Fontsource — Professional Typography & Font Architecture

Fontsource enables self-hosted, performance-optimized, open-source fonts. It replaces unreliable third-party font CDNs with predictable, version-locked local packages.

---

## 1. Top-Tier Recommended Font Pairings

| Interface Context | Primary Sans (UI & Text) | Monospace (Data & Code) | Chinese Fallback |
|---|---|---|---|
| **Software Dashboard & SaaS** | *Inter* or *Geist Sans* | *JetBrains Mono* | *Source Han Sans CN / PingFang SC* |
| **High-End Modern Web** | *Plus Jakarta Sans* | *Fira Code* | *MiSans / Noto Sans CJK SC* |
| **Technical / Scientific Console** | *Roboto* or *IBM Plex Sans* | *IBM Plex Mono* | *Microsoft YaHei UI* |

---

## 2. Standard CSS Typography Hierarchy

```css
:root {
  /* Font Family Definitions */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Strict Type Scale */
  --text-xs: 0.75rem;     /* 12px - Timestamps, badges, secondary captions */
  --text-sm: 0.875rem;    /* 14px - Body text, table rows, button text */
  --text-base: 1.0rem;     /* 16px - Primary paragraph text, input fields */
  --text-lg: 1.125rem;    /* 18px - Card headings, modal titles */
  --text-xl: 1.25rem;     /* 20px - Subsection headers */
  --text-2xl: 1.5rem;     /* 24px - Section headers */
  --text-3xl: 1.875rem;   /* 30px - Page titles, major KPI metrics */
}

body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code, kbd, samp, pre {
  font-family: var(--font-mono);
  font-feature-settings: "calt" 1; /* Enable programming ligatures */
}
```

---

## 3. Typography Rules for Software Interfaces

1. **Tabular Numerals (`font-variant-numeric: tabular-nums`)**:
   - Always activate tabular numbers on tables, telemetry counters, and financial/engineering readings so numbers maintain strictly equal character widths.
2. **Line Height Discipline**:
   - Body copy: `1.5–1.6` for optimal readability.
   - Dense tables & menus: `1.2–1.3` to maintain compact information density.
   - Large numeric KPI metrics: `1.0–1.1` to prevent excessive vertical whitespace gaps.
