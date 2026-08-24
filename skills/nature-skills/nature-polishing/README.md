# nature-polishing skill

An academic writing skill built from close reading of five *Nature* (s41586, 2026) papers
and a graduate-level scientific English writing course. Transforms draft academic text —
including Chinese-to-English translation — into prose that matches *Nature* journal
standards in sentence structure, hedging calibration, vocabulary, and logical flow.

---

## File structure

```
nature-polishing/
├── SKILL.md      ← 25 polishing rules + 12-step workflow (loaded by Claude automatically)
└── README.md     ← this file
```

---

## When to use

- Polishing Chinese-language academic drafts into publishable English
- Refining existing English text to match *Nature*-tier style
- Structural revision of Abstract, Introduction, Results, Discussion, Conclusion, or Methods
- Title and abstract redrafting before submission
- Language revision during peer-review response

## When NOT to use

- Drafting an entire paper from scratch (follow the target journal's author guidelines instead)
- Non-academic writing: science communication, blog posts, grant lay summaries
- Cases where a specific institutional voice or house style must be preserved

---

## Knowledge base

Derived from systematic analysis of:

| Source | Details |
|--------|---------|
| *Nature* papers | 5 papers sampled from 18 published in the s41586 series, 2026 |
| Writing course | Graduate scientific English writing curriculum |

Rules extracted cover sentence architecture, section-specific conventions, citation
practice, British English, *Nature* house style, overclaim detection, and AI usage ethics.

---

## Core capabilities

| Capability | What it does |
|------------|-------------|
| **Sentence length enforcement** | Splits any sentence exceeding 20–30 words; the last sentence in a paragraph receives the same scrutiny as the first |
| **Section-aware polishing** | Applies different rules depending on which section the text belongs to: Introduction, Results, Discussion, Methods, Abstract, or Conclusion |
| **Tense control** | Results → past tense + quantitative detail; Discussion → hedging verbs + mechanism/implication language |
| **Hedging calibration** | Matches claim strength to evidence level: *demonstrate* → *suggest* → *may reflect* |
| **Vocabulary upgrade** | Replaces weak or vague verbs and adjectives with precise scientific alternatives |
| **Structural realignment** | Aligns paragraphs to the hourglass pattern (broad → narrow → broad) |
| **Title optimisation** | Removes jargon, improves searchability, enforces ≤75-character limit |
| **Citation audit** | Checks attribution type (support / borrow / contrast / reproduce) and primary vs. secondary source integrity |
| **Overclaim detection** | Flags absolute claims, unwarranted causal language, scope expansion, and unverified "first" claims |
| **Copy-ready output** | Returns plain, unformatted text ready to paste directly into a manuscript |

---

## The 25 rules (summary)

### Sentence architecture

1. **Sentence length ≤ 30 words** — count every sentence individually; split anything over 20 words; the last sentence of a paragraph is the most common failure point
2. **Cohesion variety** — rotate between subject restatement, adverbial connectives, pronoun reference, definite article + noun, demonstratives + noun, participle openers, *such* modifiers, and zero-connective juxtaposition; no more than one demonstrative (*This/These/Such*) per paragraph
3. **One proposition per sentence** — never compress a main clause + participial phrase + enumeration list into a single sentence
4. **Information density** — every sentence must carry weight; remove filler (*It is well known that*, *It is worth noting that*, *As a matter of fact*)
5. **Active voice** — prefer *We show that* over *It was shown that*; front-load the main point; conditions and qualifiers follow

### Paper structure

6. **Hourglass pattern** — Introduction: broad context → specific gap → *Here we…*; Discussion/Conclusion: specific findings → broader implications
7. **Writing order ≠ reading order** — draft in the order: Results → Introduction/Conclusion → Title → Authors → Discussion → Methods → Abstract
8. **Introduction: four questions** — (i) what is known, (ii) what remains unknown, (iii) what specific question is posed, (iv) how the author addresses it; *do not* summarise results or conclusions in the Introduction
9. **Results: data summary only** — past tense, quantitative detail, objects and conditions; do not interpret mechanism (belongs in Discussion)
10. **Discussion: interpret, not repeat** — use hedging (*may*, *suggests*, *could*), causal language (*owing to*, *likely reflects*), generalisation (*may facilitate*), and limitation statements (*may fail when*)
11. **Methods: reproducibility standard** — another group must be able to replicate from the Methods section alone; seven forbidden vague phrases: *under standard conditions*, *using routine methods*, *data were analyzed statistically*, *differences were significant*, *samples were randomly assigned*, *the method was validated*, *analyzed with standard software*

### Hedging and vocabulary

12. **Hedging three-level calibration**

    | Evidence level | Verbs to use |
    |---------------|-------------|
    | Experimental demonstration | demonstrate, show, establish, reveal, identify |
    | Consistent with interpretation | suggest, indicate, are consistent with, support the view that |
    | Hypothesis or extrapolation | may reflect, probably, could, seem to, appears to |

13. **Verb upgrade** — replace *look at* → examine; *find out* → determine; *use* → employ; *help* → facilitate; *cause* → induce/trigger/drive; *change* → modulate/alter; *get* → obtain/achieve

14. **Sentence pattern templates**
    ```
    [Agent] [strong verb] that [finding], [participial phrase elaborating mechanism].
    Although [prior work/assumption], [gap/limitation].
    Here we [verb] that [key finding].
    Using [method], we [action verb] that [result].
    ```

### Document-level conventions

15. **Title** — avoid technical jargon; include searchable keywords; *curiosity + credibility*; ≤ 75 characters including spaces
16. **Abstract framework** — five-move mini-paper: context/problem → gap/objective → approach → key results with numbers → implication/application; ≤ 200 words
17. **Conclusion structure** — three parts: (i) restate central contribution (1 sentence), (ii) summarise key evidence (1–2 sentences), (iii) implication + scope boundary; never introduce new data

### Citation integrity

18. **Four citation types** — Support, Borrow, Contrast/Positioning, Reproduce; each requires explicit attribution
19. **Primary vs. secondary sources** — cite the source you personally read and verified; if you only encountered Paper A through Paper B's summary, cite Paper B
20. **Straw-man prohibition** — do not portray prior work as generically limited to highlight your own; frame comparisons with fair, specific language

### House style

21. **British English** — signalling, colour, analyse, programme, modelling, behaviour, centre, defence
22. **Article usage** — first mention: *a/an*; subsequent: *the*; generic plural: no article; unique entity: *the*; abstract nouns in general context: no article
23. **Abbreviations** — define on first use (*ethylene response factors (ERFVIIs)*); exception: DNA, RNA, ATP, pH; italic for variables and gene names; bold for vectors
24. **Numbers and units** — numerals for measurements; space between number and unit (*25 cm²*); en-dash for ranges (*0.01–1,000 years*)

### Ethics

25. **AI usage traffic-light model**

    | Signal | Permitted |
    |--------|-----------|
    | Green | Grammar, clarity, tone improvement; alternative phrasings; translation with verification |
    | Yellow | Translation (verify terminology and causality); wording support for methods/results |
    | Red | AI-generated references, data, or claims without checking; drafting core arguments; uploading unpublished data to public models |

---

## 12-step polishing workflow

1. **Sentence length check (iterative)** — identify sentences > 20 words or Chinese sentences > 40 characters with 3+ clauses; split; count again; verify the last sentence
2. **Section identification** — determine Introduction / Results / Discussion / Conclusion / Abstract / Methods and load section-specific rules
3. **Hourglass check** — verify broad → narrow → broad flow
4. **Tense audit** — Results: past tense + quantitative detail; Discussion: hedging + mechanism
5. **Sentence-level edit** — strengthen verbs, remove filler, recalibrate hedging
6. **Vocabulary upgrade** — replace generic terms with precise scientific alternatives
7. **Title / Conclusion / Abstract template check** — apply section-specific structure
8. **Citation audit** — verify attribution type and primary vs. secondary source
9. **British English + articles + abbreviations** — apply house style conventions
10. **Overclaim detection** — flag absolutes, unwarranted causation, scope expansion, unverified "first" claims
11. **Proofreading pass** — subject-verb agreement, typos, figure references, citation completeness
12. **Output** — plain unformatted text ready to paste, plus a 3–5-bullet summary of changes

---

## Output format

The skill always returns:

1. **Polished text as plain prose** — not in a code block or blockquote; copy-paste ready
2. **Change summary** — 3–5 bullet points describing what was altered and why
3. **Structural note** — if sentence splitting or section realignment was performed, a brief explanation is provided

---

## Trigger phrases

Any of the following will activate the skill:

```
"Polish this in Nature style"
"Rewrite this paragraph for a Nature paper"
"Translate and polish this draft"
"Check the hedging and sentence length"
"Make this sound like Nature"
```
