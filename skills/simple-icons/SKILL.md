---
name: simple-icons
description: "Brand and technology vector icons library using Simple Icons (simple-icons/simple-icons). Seamlessly embeds thousands of official SVG brand icons for tech stacks, social channels, and tooling ecosystems."
metadata:
  short-description: "Vector brand and technology icon assets & embedding rules"
---

# Simple Icons — Brand & Technology Vector Assets

Simple Icons provides over 3,000 official SVG brand icons for popular technologies, languages, frameworks, cloud providers, and developer tools.

---

## 1. Direct SVG Integration Pattern

Every Simple Icon is standardized on a `24x24` viewBox with optimized single-path geometry:

```html
<!-- Example: Python Icon -->
<svg role="img" viewBox="0 0 24 24" width="20" height="20" fill="#3776AB" xmlns="http://www.w3.org/2000/svg">
  <title>Python</title>
  <path d="M14.25.18l.9.2.73.26.59.3..."/>
</svg>
```

---

## 2. Dynamic CDN Integration

When embedding dynamically into documentation, markdown, or lightweight HTML surfaces without local assets:

```markdown
<!-- Using jsDelivr CDN -->
<img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/electron.svg" width="24" height="24" alt="Electron" />
<img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/typescript.svg" width="24" height="24" alt="TypeScript" />
<img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/tailwindcss.svg" width="24" height="24" alt="Tailwind CSS" />
<img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/pytorch.svg" width="24" height="24" alt="PyTorch" />
```

---

## 3. Pairing Rules

- **Strict Monochrome Consistency**: In toolbars and technical cards, override brand colors with semantic interface tokens (e.g., `fill="currentColor"` or `fill="var(--muted-foreground)"`). Reserve full brand colors for badges or dedicated integration showcases.
- **Equal Aspect Ratios**: Always bound icons within identical containers (`w-5 h-5` or `w-6 h-6`) to prevent alignment jitter across multi-row lists.
