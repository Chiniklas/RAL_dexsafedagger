# VGIP-SafeDAgger Paper

## Local LaTeX build

The root document is `main.tex`. On Ubuntu, install the required LaTeX tools and
packages with:

```bash
sudo apt update
sudo apt install latexmk texlive-latex-extra texlive-publishers \
  texlive-bibtex-extra texlive-science
```

Build the paper from the repository root:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

The generated document is `main.pdf`. `latexmk` automatically runs the required
LaTeX and BibTeX passes.

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
