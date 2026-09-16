---
name: mermaid-charts
description: "Structured technical diagramming with Mermaid.js (mermaid-js/mermaid). Generates publication-grade architecture schematics, sequence flows, state machines, and Gantt project roadmaps with clean styling."
metadata:
  short-description: "Structured architecture, sequence & flowchart diagramming"
---

# Mermaid Charts — Structured Technical & Architecture Diagramming

Mermaid generates diagrams and visualizations using text-based markdown definitions. It integrates seamlessly into GitHub, GitLab, Notion, and Markdown documentation.

---

## 1. Professional Styling Principles

Default Mermaid charts often look garish with bright cyan and pink nodes. Always enforce clean, minimalist themes:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f1f5f9', 'primaryTextColor': '#0f172a', 'primaryBorderColor': '#cbd5e1', 'lineColor': '#64748b', 'secondaryColor': '#e2e8f0', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    A[Client UI Request] --> B[API Gateway]
    B --> C{Authentication}
    C -->|Authorized| D[Core Microservice]
    C -->|Unauthorized| E[403 Forbidden Response]
    D --> F[(PostgreSQL DB)]
    D --> G[(Redis Cache)]
```

---

## 2. Supported Diagram Types & Use Cases

1. **Flowcharts (`flowchart TD / LR`)**:
   - Algorithmic branching, business logic workflows, user journeys.
2. **Sequence Diagrams (`sequenceDiagram`)**:
   - Microservice communication, API handshakes, asynchronous message queue handling.
3. **State Diagrams (`stateDiagram-v2`)**:
   - Order processing states, sensor connection states, finite state machines.
4. **Class & Entity-Relationship (`classDiagram`, `erDiagram`)**:
   - Database schemas, Object-Oriented software architectures.
5. **Gantt Charts (`gantt`)**:
   - Software sprint timelines, research project milestones, delivery phases.

---

## 3. Standard Architecture Pattern Example

```mermaid
sequenceDiagram
    autonumber
    actor User as Engineer / User
    participant Frontend as shadcn/ui Desktop
    participant Backend as FastMCP / API Server
    participant Worker as GPU Inference Worker
    participant DB as SQLite / Vector DB

    User->>Frontend: Trigger "Audit Analysis"
    Frontend->>Backend: POST /api/v1/audit
    Backend->>Worker: Dispatch Compute Task
    Worker->>DB: Query Baseline Parameters
    DB-->>Worker: Return Model Tensors
    Worker-->>Backend: Yield Final Predictions
    Backend-->>Frontend: Stream JSON Results
    Frontend-->>User: Render Interactive Visualizer
```
