---
name: ccc-ui
description: Design, redesign, and review high-quality interfaces for building and structural digital-twin applications. Use for dashboards, monitoring consoles, sensor telemetry, 3D model views, alarms, and desktop delivery. Default desktop shell is Electron; default test build is a portable, no-install package.
---

# CCC-UI

CCC-UI is the project-level design and delivery standard for the building digital-twin product.

## Product stance

- Design for civil/structural engineers first: make spatial context, structural condition, evidence, uncertainty, and action obvious.
- Treat the interface as an operational monitoring console, not a generic SaaS dashboard.
- Prefer this hierarchy: site/model context -> current health -> sensor evidence -> alarms/events -> recommended action.
- Keep domain language precise. Never present simulated values as measured data or inference as an engineering conclusion.

## Visual direction

- Establish a concrete scene before choosing a theme: control-room or field engineer, ambient light, viewing distance, and urgency.
- Use a restrained, high-contrast palette with one structural accent and explicit semantic colors for normal, attention, alarm, and unavailable.
- Use OKLCH tokens where possible and verify 4.5:1 body-text contrast.
- Use typography, spacing, alignment, and meaningful scale for hierarchy. Avoid decorative gradients, excessive rounded cards, nested cards, generic hero metrics, and repeated eyebrow labels.
- Use real structural context: grids, axes, section names, model coordinates, timestamps, sensor IDs, and event provenance.
- Motion must explain state change or data flow, remain fast, and have a reduced-motion fallback.
- Responsive behavior must preserve the monitoring task: never hide alarm state or latest measurement behind decorative layout.

## Component and implementation choices

- Inspect the existing stack before changing it. Keep a plain HTML/CSS/JS surface plain unless migration is explicitly requested.
- Use React Bits-style components only when the project already uses React or React migration is requested; adapt interaction and motion rather than copying demo styling.
- Prefer semantic HTML, accessible buttons, keyboard operation, visible focus, and readable empty/error/loading states.
- For live data, show source, last update time, connection state, units, quality, and whether values are simulated or measured.
- Keep changes surgical. Do not refactor unrelated code or add speculative abstractions.

## Required workflow

1. Inspect the target surface, current UI, data flow, and existing tokens.
2. State assumptions and define a small success checklist before coding.
3. Shape the information architecture and visual hierarchy for a civil-engineering monitoring task.
4. Implement the smallest complete change, preserving working behavior.
5. Verify connection states, empty data, alarm state, resize, keyboard focus, and reduced motion.
6. Review contrast, overflow, clutter, misleading labels, and simulated-versus-real data clarity.

## Electron default

- Use Electron as the default desktop shell when packaging or native serial access is needed.
- Keep renderer UI and device access separated: renderer for presentation, preload/main process for controlled serial IPC.
- Expose only narrow IPC methods such as `serial.list`, `serial.open`, `serial.close`, and `serial.onData`.
- Never put unrestricted Node or filesystem access in the renderer.
- The default test artifact is a portable/no-install build. Do not produce an installer unless the user explicitly requests one.
- With electron-builder, prefer the `portable` Windows target for test builds; keep installer targets opt-in.

## GPU model rendering standard

- Treat GPU-accelerated WebGL/WebGPU rendering as the default for complex structural and BIM scenes.
- Keep Chromium hardware acceleration enabled in Electron; renderer creation should request `powerPreference: high-performance` and cap device pixel ratio to a practical maximum such as 2.
- Prefer GLB/glTF runtime assets with instancing, frustum culling, level of detail, material batching, and progressive loading before adding visual effects.
- Keep the renderer responsive while importing or parsing large models by moving conversion, indexing, and heavy preprocessing out of the UI thread.
- Expose a clear fallback state when WebGL/WebGPU is unavailable and show rendering quality/performance status without claiming GPU support that was not detected.

## Standard desktop software chrome

Every CCC-UI desktop surface should use a consistent software-style top bar unless the product explicitly requires another layout.

- Top-bar order is: compact logo/icon -> `文件` -> `编辑` -> `视图` -> `窗口` -> `帮助` -> flexible title/context area -> minimize/maximize/close controls.
- Keep the logo compact so it never pushes the menu away from the far-left edge. The menu is a real keyboard-accessible button group, not decorative text.
- Use a 38-44px top bar, clear active state, visible focus ring, and a 4-8px spacing rhythm. Menus open below the trigger with a 150-220ms fade/slide transition, close on outside click or `Escape`, and support keyboard navigation.
- Use semantic menu groups: file actions, edit actions, view/camera actions, window actions, and help/about. Do not place critical alarm actions only inside a menu.
- For Electron frameless windows, mark only the empty/title region as `-webkit-app-region: drag`; mark every menu item, input, link, and window control as `no-drag`.
- Window controls use compact circular or softly rectangular icon buttons with inline SVG icons: minimize, maximize/restore, and close. Use 150-200ms transitions, a warm amber hover for minimize, green hover for maximize/restore, and red hover for close. The close action must have a clear hover/focus state and must not be hidden behind ambiguous icons.
- Window controls must expose accessible names, keyboard focus, active/pressed feedback, and a reduced-motion fallback. The maximize icon must reflect the current maximized state.
- Connect controls to narrow preload IPC methods such as `window.minimize`, `window.toggleMaximize`, `window.toggleFullscreen`, and `window.close`. In a browser fallback, keep the controls harmless and use the document Fullscreen API where appropriate.
- Verify the chrome at normal, narrow, maximized, keyboard-focus, hover, reduced-motion, and browser-fallback states before delivery.

## Standard keyboard shortcuts

Shortcuts are part of the interaction contract: if a shortcut is shown in a menu, it must be implemented and tested.

- Global menu: `Alt` or `F10` focuses the menu bar; `Esc` closes the open menu; `ArrowLeft`/`ArrowRight` switches menu groups; `Enter` or `Space` opens the focused group.
- File: `Ctrl+R` refreshes monitoring data; `Ctrl+P` opens the print/export view.
- Edit: `Ctrl+C` copies the current state only when the page is not inside a text selection or editable field.
- View: `R` resets to the full 3D view; `E`/`W`/`S`/`N` selects east/west/south/north; `T` selects top view; `I` selects the internal frame view.
- Window: `F11` toggles fullscreen. Electron window buttons remain mouse- and keyboard-operable; browser fallback must not throw when native IPC is unavailable.
- Ignore single-letter view shortcuts while focus is inside `input`, `textarea`, `select`, `button`, `[contenteditable]`, or a modal dialog. Respect platform conventions and use `Ctrl` on Windows/Linux and `Meta` on macOS where applicable.
- Show shortcut text beside the corresponding menu item, expose it through accessible labels, and provide visible focus/pressed feedback. Do not use shortcuts as the only way to reach a critical operation.
- Verify every binding by an observable result: menu focus, menu open/close, camera change, fullscreen change, copy result, refresh result, and safe behavior in editable fields.

## BIM model import standard

The structural model is a first-class product asset, not a decorative placeholder. A new digital-twin surface must provide a clear model-import path and preserve model provenance.

- Priority format: IFC for open BIM exchange and long-term project ownership.
- Runtime format: convert validated BIM geometry and metadata to glTF/GLB for efficient browser/Electron rendering, while retaining the original file reference and element IDs.
- Revit: support RVT through an explicit conversion/import service or Autodesk-compatible pipeline; do not pretend that a browser renderer can reliably parse arbitrary RVT files directly.
- CAD and common exchange: support DWG/DXF as drawing or geometry supplements, and allow OBJ/FBX only as secondary geometry inputs when their metadata limitations are clearly shown.
- Import flow must show file type, project/version, coordinate system, unit, element count, conversion progress, warnings, failure reason, and the last successful import. Never silently change units or coordinate axes.
- Preserve BIM identity where possible: building/storey/space hierarchy, element GUID, category, material, sensor binding, and source file/version. Model views must be able to filter by storey, category, structural system, and sensor coverage.
- Keep the original BIM file outside the renderer. Electron main/preload or a controlled local service handles file selection, conversion, caching, and validation; the renderer receives only approved model data and status.
- Empty, unsupported, oversized, corrupt, and coordinate-mismatch files need explicit recovery states. A sample/demo model must be labelled as demo data and must never be presented as the user's BIM model.
- The default acceptance path is: import IFC -> validate metadata/coordinates -> convert to GLB -> load the model -> select an element -> inspect properties -> bind or view sensor coverage.

## Resizable workspace standard

Engineering panels must adapt to the user's working task without hiding health or alarm context.

- Provide visible edge splitters between the primary work regions, especially model view, telemetry, and diagnosis/report panels. The splitter must have a clear hover/focus state and a `col-resize` or `row-resize` cursor.
- Dragging uses pointer events with a small hit area, live layout feedback, clamped minimum/maximum widths, and no accidental text selection. Preserve a usable minimum width for charts, labels, alarms, and the 3D viewport.
- Double-clicking a splitter restores the product's default layout. Persist the user's layout preference locally only when it is safe to do so, and provide a reset-layout action.
- Splitters are keyboard accessible: focusable, named with the regions they resize, and adjustable with arrow keys plus a larger step with `Shift`. Do not make drag the only way to resize.
- Respect responsive breakpoints: when columns stack on a narrow window, hide or disable horizontal splitters and use the natural vertical layout. Do not allow resizing to obscure critical alarms or connection status.
- Verify resize behavior at default, minimum, maximum, narrow-window, maximized, keyboard-focus, and reduced-motion states.

## Delivery convention

- Test artifact: `portable` / `免安装测试版`.
- Release artifact: `installer` / `安装版`, only after explicit request.
- Report what changed, how it was verified, and whether data is simulated or measured.

## UI/UX Pro Max integration

The source skill is typically available at `~/.codex/skills/ui-ux-pro-max/`. Its project-relevant rules are integrated here: accessibility and contrast first, 44px minimum interaction targets, 4/8px spacing rhythm, responsive mobile-first layout, semantic color tokens, 150-300ms purposeful motion, reduced-motion fallback, no emoji as structural icons, and chart legends/tooltips that do not rely on color alone.

For a new surface, first derive a design system from product type + industry + density. For this project use the query concept `structural health monitoring building digital twin control room`, then choose the matching stack guidance. Persist a project master design system when the surface is expected to grow; page-specific overrides must remain subordinate to the master system.

## Combined source principles

- `ui-ux-pro-max`: design-system-first reasoning, product/domain matching, accessibility and interaction checklist, responsive/chart guidance.
- `impeccable`: production craft, scene-based theme choice, OKLCH tokens, anti-slop constraints, contrast, typography, motion and layout review.
- `react-bits`: use polished animated components only when the host stack supports them; preserve reduced motion and host visual consistency.
- `Karpathy`: state assumptions, choose the smallest complete change, touch only relevant lines, and define observable verification criteria.
