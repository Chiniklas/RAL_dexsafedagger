# VLM-DexSafeDagger Paper

## Local LaTeX build

The root document is `main.tex`. On Ubuntu, install the required LaTeX tools and
packages with:

```bash
sudo apt update
sudo apt install latexmk texlive-latex-extra texlive-publishers \
  texlive-bibtex-extra texlive-science latexdiff
```

Build the regular paper from the repository root:

```bash
./build-paper.sh
```

The generated document is `main.pdf`. `latexmk` automatically runs the required
LaTeX and BibTeX passes.

To generate a separate change-highlighted `main_highlighted.pdf`:

```bash
./build-paper.sh highlighted
```

This creates `main_highlighted.pdf` without overwriting the regular `main.pdf`.

Highlighted mode compares the current working tree, including uncommitted
manuscript edits, with Git snapshot `498ab21`. That snapshot exactly matches
`output/vlm_dexsafedagger_compressed.pdf`, the pre-revision submission. Added
text is blue and underlined, deleted text is red and struck out, changed
figures are framed, and changed equations are marked as complete units. The
flattened diff source and build diagnostics are retained under
`.latex-build/highlighted/`.

To compare against another source snapshot, pass any valid Git ref:

```bash
./build-paper.sh highlighted <baseline-git-ref>
```

To remove generated build files:

```bash
latexmk -C
```

If a build reports invalid characters such as `^^@` in `main.aux`, clean the
auxiliary files and rebuild:

```bash
latexmk -C
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Avoid running simultaneous builds from the terminal and VS Code because both
processes write to the same auxiliary files.

## VS Code

Install the **LaTeX Workshop** extension. Open `main.tex`, then run:

1. `Ctrl+Shift+P`
2. Select **LaTeX Workshop: Build LaTeX project**

Use **LaTeX Workshop: View LaTeX PDF file** to open the generated PDF.

## Review response and supplementary material

The review response and its supplementary material are separate documents.
Build them from the repository root with:

```bash
./build-response.sh
./build-appendix.sh
```

The generated files are `comments/RAL/response/response.pdf` and
`comments/RAL/response/appendix.pdf`, respectively.
