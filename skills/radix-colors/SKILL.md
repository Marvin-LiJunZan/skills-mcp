---
name: radix-colors
description: "Precision color grading system using Radix Colors (radix-ui/colors). Systematic 12-step perceptual scales designed for accessibility (WCAG AA 4.5:1), dark mode symmetry, and natural P3 color gamut."
metadata:
  short-description: "12-step systematic color scales & dark mode color system"
---

# Radix Colors — Systematic Accessible Color Palette

Radix Colors provides an exquisitely calibrated 12-step color scale per hue, guaranteeing that every step serves a dedicated, predictable role in UI hierarchy across both light and dark themes.

---

## 1. The 12-Step Functional Contract

Never pick arbitrary hex codes. Every step in Radix Colors has a strictly defined architectural purpose:

| Step Range | Semantic Role | Specific Application |
|---|---|---|
| **Step 1** | App Background | The lowest layer of the viewport canvas. |
| **Step 2** | Subtle Background | Header bars, table stripes, card backgrounds. |
| **Step 3** | Normal Element Background | Default background for inactive buttons, inputs, tags. |
| **Step 4** | Hover Element Background | Interactive hover state for Step 3 components. |
| **Step 5** | Active Element Background | Pressed / selected state for interactive components. |
| **Step 6** | Subtle Border | Dividers, subtle borders separating distinct cards. |
| **Step 7** | Interactive Border | Focus rings, hover states on input borders. |
| **Step 8** | High-Contrast Border | Active input borders, focus outlines. |
| **Step 9** | Solid Primary Background | High-impact CTA buttons, primary badges (guaranteed contrast with white text). |
| **Step 10** | Solid Hover Background | Hover state for Step 9 primary buttons. |
| **Step 11** | Low-Contrast Text | Secondary descriptions, placeholder text, metadata captions. |
| **Step 12** | High-Contrast Text | Primary headings, body copy, key data numbers. |

---

## 2. Standard Recommended Scales

- **Neutrals**:
  - `slate`: Cold, technical, software engineering dashboards.
  - `gray`: Neutral, balanced, universal.
  - `mauve`: Slightly warm purple-tinted neutral for creative products.
- **Accents**:
  - `blue` / `indigo`: Primary actionable interfaces, software controls.
  - `emerald` / `green`: Success states, positive telemetry, normal sensor readings.
  - `amber` / `yellow`: Warning, caution, threshold proximity.
  - `ruby` / `red`: Alarms, critical failures, destructive actions.

---

## 3. Dark Mode Mirroring Principle

Radix Colors uses inverse lightness curves:
- Light Mode: Step 1 is near-white ($L \approx 99\%$), Step 12 is near-black ($L \approx 10\%$).
- Dark Mode: Step 1 is deep obsidian ($L \approx 5\%$), Step 12 is radiant white ($L \approx 95\%$).

Because Step 3 to Step 5 maintain identical relative luminance jumps in both modes, dark mode adaptation requires **zero manual re-tweaking of opacity or contrast**.
