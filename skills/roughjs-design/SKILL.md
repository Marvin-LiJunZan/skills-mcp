---
name: roughjs-design
description: "Hand-drawn sketchy graphics and natural organic diagrams using Rough.js (rough-stuff/rough). Eliminates rigid, artificial AI plastic styling with organic human-drawn aesthetics for wireframes, charts, and diagrams."
metadata:
  short-description: "Hand-drawn sketching & organic UI graphics using Rough.js"
---

# Rough.js Design — Organic Hand-Drawn UI & Diagramming

Rough.js brings the natural, warm, imperfect quality of human hand-drawn sketches to UI mockups, architecture diagrams, and scientific schematics, instantly eliminating the sterile, artificial "AI plastic" look.

---

## 1. Core Visual Principles

1. **Controlled Roughness**:
   - `roughness: 1.2–2.0` gives a lively hand-drawn feel without losing readability.
   - `bowing: 1.0–1.5` introduces subtle curved imperfections into straight lines.
2. **Hachure & Cross-Hatch Fills**:
   - Replace flat solid fills with `hachure`, `zigzag`, `cross-hatch`, or `dots`.
   - Use semi-transparent stroke colors so underlying canvas textures show through.
3. **Typography Pairing**:
   - Pair Rough.js graphics with informal/handwritten fonts: *Virgil*, *Comic Shanns*, *Caveat*, or clean humanistic sans like *Plus Jakarta Sans*.

---

## 2. Quick HTML / Canvas Implementation Template

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/roughjs@latest/bundled/rough.js"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: #faf9f6; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    canvas { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  </style>
</head>
<body>
  <canvas id="canvas" width="600" height="400"></canvas>
  <script>
    const rc = rough.canvas(document.getElementById('canvas'));
    
    // Hand-drawn UI card
    rc.rectangle(40, 40, 520, 320, {
      roughness: 1.5,
      stroke: '#1e293b',
      strokeWidth: 2,
      fill: 'rgba(241, 245, 249, 0.5)',
      fillStyle: 'cross-hatch'
    });
    
    // Header bar
    rc.rectangle(60, 60, 480, 50, {
      roughness: 1.2,
      stroke: '#0284c7',
      fill: 'rgba(186, 230, 253, 0.4)',
      fillStyle: 'hachure'
    });
    
    // Status button
    rc.rectangle(420, 290, 120, 40, {
      roughness: 2.0,
      stroke: '#059669',
      fill: 'rgba(167, 243, 208, 0.6)',
      fillStyle: 'solid'
    });
  </script>
</body>
</html>
```

---

## 3. When to Use Rough.js in the Software Lifecycle

- **Phase 1 (Ideation & Wireframing)**: Create low-fidelity wireframes that invite feedback rather than premature pixel-polishing debates.
- **System Architecture Explanations**: Present high-level conceptual flows in documentation that look human-crafted and accessible.
- **Playful / Creative Product Dashboards**: Inject personality into empty states, loading screens, and onboarding walkthroughs.
