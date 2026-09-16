---
name: markdown-badges
description: "Visual status tags, technology stack shields, and documentation badges using Markdown Badges (Ileriayo/markdown-badges). Standardizes Shields.io-style pills, licenses, build badges, and tech icons for software deliverables."
metadata:
  short-description: "Visual status tags, technology badges & Shields.io pills"
---

# Markdown Badges — Status Tags & Tech Stack Badges

Markdown Badges provides clean, uniform visual badges for software repositories, documentation headers, architecture dashboards, and deliverable packages.

---

## 1. Badge Aesthetic Formats

Prefer the clean `for-the-badge` or `flat-square` styles for modern technical documentation:

### Technology Stack Badges

```markdown
<!-- Tech Stack Row -->
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Electron](https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
```

### Operational & Status Badges

```markdown
<!-- Build & Deployment Status -->
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![Coverage](https://img.shields.io/badge/coverage-98%25-success?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Version](https://img.shields.io/badge/release-v2.4.0-informational?style=flat-square)
```

---

## 2. In-App HTML / CSS Equivalent (No External Requests)

When building offline software dashboards (e.g. Electron apps), render badges natively without network calls:

```html
<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
  System Online
</span>

<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
  <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
  Sensory Warning
</span>
```
