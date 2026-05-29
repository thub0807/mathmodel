# CUMCM LaTeX Template Interface Audit

Stage: Stage 0 audit only. This document records the current CUMCM template interface without modifying `templates/latex/cumcm/cumcmthesis/`, active stage references, runtime scripts, legacy files, or old state.

## Template Entry File

The current formal template entry is:

```text
templates/latex/cumcm/cumcmthesis/MathModel.tex
```

The entry uses:

```tex
\documentclass[bwprint]{gmcmthesis}
```

The previously tracked `example.tex` / `cumcmthesis.cls` files are not present in the current working tree. The active template should therefore be treated as the `MathModel.tex` + `gmcmthesis.cls` interface currently present in the template directory.

## Dependency Files

Current visible template dependencies and assets:

```text
templates/latex/cumcm/cumcmthesis/gmcmthesis.cls
templates/latex/cumcm/cumcmthesis/figures/logo2025.png
templates/latex/cumcm/cumcmthesis/figures/title2025.pdf
templates/latex/cumcm/cumcmthesis/test.jpg
```

The directory also contains generated LaTeX build artifacts such as `.aux`, `.log`, `.out`, `.toc`, `.xdv`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, and `MathModel.pdf`. These are audit observations, not required template source dependencies for Stage 8 rendering.

## Recommended Compile Command

Recommended Stage 8 compile command:

```bash
xelatex paper.tex
xelatex paper.tex
```

Use UTF-8 source. Run from the generated source directory:

```text
workspace/output/final/source/
```

If the environment lacks `xelatex`, keep `paper.md`, `paper.tex`, `source/`, `latex_compile.log`, and `render_report.json`, and record the failure instead of claiming that `paper.pdf` was generated.

## Content Fill Points

The formal template has a conventional CUMCM body rather than explicit machine placeholders. Conservative fill points are:

```text
\title{...}
\begin{abstract} ... \keywords{...} \end{abstract}
\tableofcontents
\section{问题重述}
\section{模型假设}
\section{符号说明}
\section{问题的分析}
\section{模型的评价}
\section{参考文献}
\appendix
\section{程序代码}
```

Recommended mapping:

| Paper Content | Formal Template Location |
|---|---|
| Title placeholder | `\title{...}` |
| Abstract | inside `\begin{abstract}` before `\keywords{...}` |
| Keywords | `\keywords{...}` |
| Problem restatement | `\section{问题重述}` |
| Model assumptions | `\section{模型假设}` |
| Notation | `\section{符号说明}` |
| Data processing, model building, solving, per-question results | `\section{问题的分析}` and per-question subsections |
| Validation and sensitivity | body subsections after result discussion |
| Figures and tables | nearest supporting body paragraph, using assets copied to `source/figures/` and `source/tables/` |
| Model advantages, limitations, next experiments | `\section{模型的评价}` |
| Bibliography / references | `\section{参考文献}` with `thebibliography` unless a `.bib` file is introduced later |
| Appendix | after `\appendix` |

Because the current formal template does not expose stable placeholder tokens, Stage 8 should preserve the template preamble and document structure, then replace the body between `\begin{document}` and `\end{document}` with generated CUMCM-safe content. If insertion cannot be reliably located, Stage 8 must record a fallback reason in both `latex_compile.log` and `render_report.json`.

## Figure And Table Resource Directory

Generated Stage 8 source layout should use:

```text
workspace/output/final/source/figures/
workspace/output/final/source/tables/
```

Template-native assets may remain under:

```text
workspace/output/final/source/figures/
```

Final figure/table indexes should point to existing files. Missing files must be reported as warnings; Stage 8 must not fabricate visual assets.

## Bibliography / References Handling

The current template uses an inline `thebibliography` block. Stage 8 should generate a conservative references placeholder unless verified bibliography entries exist in the workspace.

If a future template revision adds `.bib` / `.bst` files, Stage 8 should copy them to `source/` and record the bibliography strategy in `render_report.json`. Until then, do not invent references.

## Stage 8 Use Recommendation

Stage 8 should prefer:

```bash
python scripts/render_workspace_paper.py <workspace>
```

For intermediate review without compiling PDF:

```bash
python scripts/render_workspace_paper.py <workspace> --no-pdf
```

The helper should read `docs/cumcm_latex_template_interface.md`, use `templates/latex/cumcm/cumcmthesis/` as the highest-priority formal template, and use only an internal temporary LaTeX draft when formal assets are unavailable.

## Compile Failure Recording

When compilation fails, record:

```text
workspace/output/final/latex_compile.log
workspace/output/final/render_report.json
```

The record must include the command, engine, exit code, stderr/stdout summary, whether `paper.md` and `paper.tex` were preserved, and whether `paper.pdf` exists.

## Relationship To Fallback Scaffold

An internal temporary LaTeX draft is not the preferred formal CUMCM template and should not be presented as the official competition template when `templates/latex/cumcm/cumcmthesis/` is available.

## Legacy And State Boundary

Stage 8 rendering and Stage 9 validation must not read:

```text
legacy/
decision_log
cwd/state
score_artifact.py
old state files
```

`reference.pdf` remains audit-only and is not an automatic source of truth for paper generation.
