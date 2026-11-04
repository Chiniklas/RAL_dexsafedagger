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

The generated document is `output/main.pdf`. `latexmk` automatically runs the
required LaTeX and BibTeX passes.

To generate a separate change-highlighted `main_highlighted.pdf`:

```bash
./build-paper.sh highlighted
```

This creates `output/main_highlighted.pdf` without overwriting the regular
`output/main.pdf`.

Highlighted mode compares the current working tree, including uncommitted
manuscript edits, with Git snapshot `5a42fcb`. That snapshot contains the
source corresponding to the last submitted revision at
`comments/RAL/first_rebutal/output/revision/main.pdf`. Revised material is
shown as normal black text over yellow highlight stripes; deleted material is
omitted rather than crossed out. Changed figures receive yellow marking, and
changed equations are marked as complete units. The flattened diff source and
build diagnostics are retained under `.latex-build/highlighted/`.

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

The second-round response source belongs in
`comments/RAL/second_rebutal/response/response.tex`. Build it from the
repository root with:

```bash
./build-response.sh
./build-appendix.sh
```

The generated files are `output/response.pdf` and `output/appendix.pdf`.
The response-folder copies and all LaTeX auxiliary/build files remain together
under `comments/RAL/second_rebutal/response/`, matching the previous rebuttal's
directory structure. The root build scripts publish atomic copies of the two
PDFs into `output/`.

The four final rebuttal deliverables are collected in `output/`:

- `output/main.pdf`
- `output/main_highlighted.pdf`
- `output/response.pdf`
- `output/appendix.pdf`
