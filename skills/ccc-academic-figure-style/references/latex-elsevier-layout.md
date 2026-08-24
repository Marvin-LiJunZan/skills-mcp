# Elsevier Two-Column LaTeX Layout

Use this reference when editing or diagnosing an Elsevier manuscript whose figures, tables, equations, or floats do not fit the intended layout. These rules were distilled from a real `elsarticle` conversion and subsequent PDF-level corrections.

## Contents

- [Baseline assumptions](#baseline-assumptions)
- [Choose the correct float width](#choose-the-correct-float-width)
- [Compose multi-panel figures](#compose-multi-panel-figures)
- [Size tables without making them unreadable](#size-tables-without-making-them-unreadable)
- [Keep captions in English with ctex](#keep-captions-in-english-with-ctex)
- [Understand two-column float mechanics](#understand-two-column-float-mechanics)
- [Fix blank space below starred floats](#fix-blank-space-below-starred-floats)
- [Escalate float controls carefully](#escalate-float-controls-carefully)
- [Break long equations structurally](#break-long-equations-structurally)
- [Protect scientific asset integrity](#protect-scientific-asset-integrity)
- [Configure LaTeX Workshop](#configure-latex-workshop)
- [Compile and inspect the PDF](#compile-and-inspect-the-pdf)

## Baseline assumptions

The typical target is an Elsevier two-column manuscript:

```latex
\documentclass[5p,twocolumn]{elsarticle}
```

Use XeLaTeX when the document loads `ctex`, contains Chinese working notes, or otherwise depends on Unicode/CJK font handling. Preserve the journal class and bibliography workflow unless the journal explicitly requires another setup.

## Choose the correct float width

Match the float environment and its internal width:

| Intended span | Environment | Width inside the float |
|---|---|---|
| One column | `figure`, `table` | `\columnwidth` or `\linewidth` |
| Both columns | `figure*`, `table*` | `\textwidth` or `\linewidth` |

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/result.png}
  \caption{Single-column result.}
  \label{fig:result}
\end{figure}

\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/result-wide.png}
  \caption{Double-column result.}
  \label{fig:result-wide}
\end{figure*}
```

Do not put a `\textwidth` image in an ordinary `figure`; it will overflow a column. Do not default every image to `figure*`; unnecessary wide floats make the queue harder to place and can create sparse pages.

## Compose multi-panel figures

Prefer independently exported panels assembled in LaTeX. Useful starting widths for a full-width figure are:

- Two panels per row: `0.48\textwidth`.
- Four panels per row: approximately `0.23\textwidth`.
- Three-by-three grid: `0.30\textwidth`, separated by `\hfill`, with `\\[4pt]` between rows.

```latex
\begin{figure*}[t]
  \centering
  \begin{minipage}{0.30\textwidth}
    \centering\includegraphics[width=\linewidth]{figures/a.png}
  \end{minipage}\hfill
  \begin{minipage}{0.30\textwidth}
    \centering\includegraphics[width=\linewidth]{figures/b.png}
  \end{minipage}\hfill
  \begin{minipage}{0.30\textwidth}
    \centering\includegraphics[width=\linewidth]{figures/c.png}
  \end{minipage}\\[4pt]
  % Repeat for rows 2 and 3.
  \caption{Nine-panel comparison.}
  \label{fig:nine-panel}
\end{figure*}
```

Use `subcaption` only when panels genuinely need individual subcaptions or references. If the graphics already contain `(a)` to `(i)` labels, plain `minipage` blocks are usually simpler and more compact.

## Size tables without making them unreadable

Use `table` for a true single-column table and `table*` when both columns are required. For a full-width table that naturally fits, distribute spare width instead of scaling the text:

```latex
\begin{table*}[t]
  \centering
  \caption{Comparison of model performance.}
  \label{tab:comparison}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lccc@{}}
    \toprule
    Method & Metric 1 & Metric 2 & Metric 3 \\
    \midrule
    % rows
    \bottomrule
  \end{tabular*}
\end{table*}
```

Use `\resizebox{\textwidth}{!}{...}` only for a genuinely overwide table that cannot be corrected through column design, abbreviations, or wrapping. Repeatedly scaling tables makes text inconsistent and often causes the "too small" appearance.

Scope row spacing to the affected table rather than changing every table:

```latex
{
  \renewcommand{\arraystretch}{1.05}
  \begin{tabular}{...}
  ...
  \end{tabular}
}
```

## Keep captions in English with ctex

`ctex` may localize float names. For an English manuscript, set them explicitly with `caption`:

```latex
\usepackage{caption}
\captionsetup[figure]{name=Fig.}
\captionsetup[table]{name=Table,skip=4pt}
```

Check the generated PDF because class-level caption definitions can override package defaults. Do not hard-code `Fig.` or `Table` inside every caption.

## Understand two-column float mechanics

Ordinary and double-column floats use different placement parameters:

- `\floatpagefraction` mainly controls float pages for ordinary floats.
- `\dbltopfraction` controls the allowed double-column float area at the top of a text page.
- `\dblfloatpagefraction` controls when double-column floats may form a float-only page.
- `\dbltopnumber` limits double-column floats at the top of a page.
- `\textfraction` reserves the minimum text fraction on a mixed page.

A pure float page contains floats, not ordinary body text. A paragraph written immediately after `\end{figure*}` is not forced onto that same page. Putting the paper's analysis paragraph inside a `minipage` within the float is also not a general fix; it incorrectly turns body prose into float content.

In standard two-column LaTeX, `figure*` normally appears at the top of a page or on a float page. The `h` and `b` placement letters are commonly ineffective for starred floats unless another package changes the algorithm.

## Fix blank space below starred floats

Use this configuration when large `figure*` objects are sent to float-only pages even though a complete wide figure can fit at the top with normal two-column text below:

```latex
\setcounter{dbltopnumber}{2}
\renewcommand{\dbltopfraction}{0.90}
\renewcommand{\textfraction}{0.05}
\renewcommand{\dblfloatpagefraction}{0.80}
```

If a double-float-only page is still legitimately required, compact its vertical placement with:

```latex
\makeatletter
\setlength{\@dblfptop}{0pt}
\setlength{\@dblfpsep}{12pt}
\setlength{\@dblfpbot}{0pt plus 1fil}
\makeatother
```

This was validated on the Fig. 11/Fig. 12 case:

- Before correction, each complete three-by-three figure occupied a float-only page with roughly one-third blank below.
- After correction, each grid remained complete at the page top and ordinary two-column text flowed below.
- The manuscript decreased from 18 pages to 17 pages.
- XeLaTeX completed without fatal errors.

The key distinction is that double-column parameters fixed the starred floats. Raising only `\floatpagefraction` does not address the relevant float class.

## Escalate float controls carefully

Start with `[t]` and the correct float width. Use `[!t]` only after inspecting the output and determining that normal fraction restrictions are keeping a suitable float queued.

Do not use these as first-line spacing fixes:

- `\clearpage` or `\newpage`, which changes pagination at that point.
- `\afterpage`, which makes placement harder to reason about.
- `\FloatBarrier`, which flushes float queues and often creates giant vertical holes in two-column layouts (e.g., pushing a `figure*` down while leaving the right column completely blank). Place `figure*` environments directly at `\section{}` headings or page boundaries instead of forcing queue flushes.
- Negative `\vspace`, which hides symptoms and may cause overlap after later edits.

These commands can be legitimate at a semantic boundary, but use them only after correcting the environment, dimensions, and applicable float parameters.

## Break long equations structurally

Do not shrink an overflowing equation until it becomes unreadable. Break it at meaningful operators with `aligned`, `split`, or `cases`:

```latex
\begin{equation}
\begin{aligned}
  F(x) ={}& A(x) + B(x) \\
          &+ C(x) + D(x).
\end{aligned}
\end{equation}
```

Keep symbols in LaTeX math mode. Do not substitute raw Unicode lookalikes for commands such as `\alpha`, `\times`, or `\leq`; this can produce font inconsistency and compilation failures.

## Protect scientific asset integrity

Treat missing figure files as a hard error. Never generate placeholder scientific plots, synthetic microstructures, or dummy curves merely to make the manuscript compile.

Before changing layout, verify every `\includegraphics` path, filename, and extension. On case-sensitive build systems, capitalization must match. If a real asset is missing, stop and locate or request it.

## Configure LaTeX Workshop

For this manuscript class, make `latexmk` with XeLaTeX the first and default recipe. A workspace-level `.vscode/settings.json` can use:

```json
{
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk-xelatex",
      "command": "latexmk",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-xelatex",
        "-outdir=%OUTDIR%",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "latexmk (XeLaTeX)",
      "tools": ["latexmk-xelatex"]
    }
  ],
  "latex-workshop.latex.recipe.default": "first",
  "latex-workshop.latex.autoBuild.run": "onSave",
  "latex-workshop.view.pdf.viewer": "tab",
  "latex-workshop.synctex.afterBuild.enabled": true
}
```

Keep the recipe workspace-scoped when other repositories need different engines. Confirm that `latexmk`, `xelatex`, and the bibliography tool are available on `PATH`.

## Compile and inspect the PDF

Build from the manuscript directory with:

```powershell
latexmk -synctex=1 -interaction=nonstopmode -file-line-error -xelatex '-outdir=.' manuscript.tex
```

Compilation success alone is not layout verification:

1. Search the log for fatal errors, missing files, undefined control sequences, and unresolved references or citations.
2. Confirm figure/table numbering and cross-references against the manuscript text.
3. Open or rasterize target PDF pages and inspect panel order, font size, captions, table legibility, equation width, blank regions, and float/text flow.
4. Rebuild until references stabilize and target pages stop changing unexpectedly.

For float corrections, record page count and before/after target pages. This distinguishes a real improvement from a float that merely moved elsewhere.
