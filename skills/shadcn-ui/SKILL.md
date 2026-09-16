---
name: shadcn-ui
description: "Professional designer-grade UI component architecture using shadcn/ui (shadcn-ui/ui). Built on Tailwind CSS and Radix UI primitives with restrained typography, precise micro-interactions, dark mode tokens, and enterprise accessibility."
metadata:
  short-description: "Enterprise designer-grade UI component patterns & best practices"
---

# shadcn/ui — Designer-Grade UI Component Architecture

shadcn/ui provides copy-pasteable, highly accessible, unstyled primitives combined with Tailwind CSS. It is the gold standard for modern, professional web and desktop interfaces, entirely devoid of the bloated, generic "AI template" look.

---

## 1. Aesthetic Dogmas of shadcn/ui

1. **Subtle Elevation Over Loud Shadows**:
   - Never use `shadow-2xl` with heavy black opacity.
   - Use multi-layer soft shadows: `shadow-sm`, `border border-border/50`, and ambient backdrop blurs (`backdrop-blur-md`).
2. **Restrained Border Radius**:
   - Avoid oversized capsule corners (`rounded-3xl` everywhere).
   - Prefer systematic geometric consistency: `rounded-md` (6px) or `rounded-lg` (8px) for cards, `rounded-sm` (4px) for badges and buttons.
3. **Typography-First Layout**:
   - Crisp font tracking (`tracking-tight` for headings, `leading-none` for numeric metrics).
   - Muted secondary labels (`text-muted-foreground text-sm`) balanced against high-contrast primary text.
4. **Accessible Micro-Interactions**:
   - Subtle hover states: `hover:bg-accent hover:text-accent-foreground transition-colors duration-150`.
   - Ring-based keyboard focus: `focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`.

---

## 2. Standard Component Tokens (CSS Variables)

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --border: 217.2 32.6% 17.5%;
  }
}
```

---

## 3. Canonical Metric Card Pattern

```jsx
export function MetricCard({ title, value, change, trend = "up" }) {
  return (
    <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
      <div className="flex items-center justify-between space-y-0 pb-2">
        <span className="text-sm font-medium text-muted-foreground">{title}</span>
      </div>
      <div className="text-2xl font-bold tracking-tight">{value}</div>
      <p className="text-xs text-muted-foreground pt-1">
        <span className={trend === "up" ? "text-emerald-500 font-medium" : "text-rose-500 font-medium"}>
          {change}
        </span>{" "}
        from previous benchmark
      </p>
    </div>
  );
}
```
