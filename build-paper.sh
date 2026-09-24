#!/usr/bin/env bash
set -euo pipefail

paper_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
build_dir="$paper_dir/.latex-build"
mode="${1:-normal}"

# This source snapshot exactly corresponds to
# output/vlm_dexsafedagger_compressed.pdf (SHA-256 below).
submission_ref="498ab21"
submission_pdf="$paper_dir/output/vlm_dexsafedagger_compressed.pdf"
submission_pdf_sha256="cc377f5a9aa957f3610b6975a887e6eb841eeded6cc7abd6d5c27a196d033ac6"

usage() {
  cat <<'EOF'
Usage:
  ./build-paper.sh
  ./build-paper.sh normal
  ./build-paper.sh highlighted [baseline-git-ref]

Modes:
  normal       Build the current manuscript normally.
  highlighted  Build main_highlighted.pdf with additions highlighted in blue
               and deletions struck out in red relative to the submission.

The highlighted mode defaults to Git snapshot 498ab21, which exactly matches
output/vlm_dexsafedagger_compressed.pdf. Pass a different Git ref to override
the comparison baseline.

Environment:
  LATEXDIFF_BIN  latexdiff executable to use (default: latexdiff).
EOF
}

publish_pdf() {
  local source_pdf="$1"
  local destination_pdf="$2"

  # Publish only a completed PDF, so viewers never display an intermediate
  # LaTeX/BibTeX pass with unresolved or malformed citations.
  cp "$source_pdf" "$destination_pdf.tmp"
  mv -f "$destination_pdf.tmp" "$destination_pdf"
}

build_normal() {
  mkdir -p "$build_dir"
  cd "$paper_dir"

  latexmk \
    -pdf \
    -interaction=nonstopmode \
    -file-line-error \
    -outdir="$build_dir" \
    main.tex

  publish_pdf "$build_dir/main.pdf" "$paper_dir/main.pdf"
  echo "Built normal manuscript: $paper_dir/main.pdf"
}

build_highlighted() {
  local baseline_ref="$1"
  local latexdiff_bin="${LATEXDIFF_BIN:-latexdiff}"
  local highlighted_dir="$build_dir/highlighted"
  local temporary_dir
  local baseline_dir
  local current_dir
  local baseline_archive
  local current_archive
  local diff_tex
  local diff_tex_tmp
  local diff_log
  local actual_submission_sha

  if ! command -v git >/dev/null 2>&1; then
    echo "error: highlighted mode requires git." >&2
    exit 1
  fi

  if ! command -v "$latexdiff_bin" >/dev/null 2>&1; then
    cat >&2 <<'EOF'
error: highlighted mode requires latexdiff.
Install it on Ubuntu with:
  sudo apt install latexdiff
Or set LATEXDIFF_BIN to an existing latexdiff executable.
EOF
    exit 1
  fi

  if ! git -C "$paper_dir" rev-parse --verify "${baseline_ref}^{commit}" >/dev/null 2>&1; then
    echo "error: baseline Git ref does not exist: $baseline_ref" >&2
    exit 1
  fi

  if [[ "$baseline_ref" == "$submission_ref" ]]; then
    if [[ ! -f "$submission_pdf" ]]; then
      echo "error: authoritative baseline PDF is missing: $submission_pdf" >&2
      exit 1
    fi
    actual_submission_sha="$(sha256sum "$submission_pdf" | awk '{print $1}')"
    if [[ "$actual_submission_sha" != "$submission_pdf_sha256" ]]; then
      echo "error: baseline PDF no longer matches the recorded submission." >&2
      echo "expected: $submission_pdf_sha256" >&2
      echo "actual:   $actual_submission_sha" >&2
      exit 1
    fi
  fi

  mkdir -p "$highlighted_dir"
  temporary_dir="$(mktemp -d /tmp/ral-paper-highlight.XXXXXX)"
  baseline_dir="$temporary_dir/baseline"
  current_dir="$temporary_dir/current"
  baseline_archive="$temporary_dir/baseline.tar"
  current_archive="$temporary_dir/current.tar"
  diff_tex="$highlighted_dir/main-highlighted.tex"
  diff_tex_tmp="$highlighted_dir/main-highlighted.tex.tmp"
  diff_log="$highlighted_dir/latexdiff.log"

  cleanup() {
    if [[ -n "${temporary_dir:-}" && "$temporary_dir" == /tmp/ral-paper-highlight.* ]]; then
      rm -rf -- "$temporary_dir"
    fi
  }
  trap cleanup EXIT

  mkdir -p "$baseline_dir" "$current_dir"

  # Recover the source that produced the baseline PDF.
  git -C "$paper_dir" archive --format=tar "$baseline_ref" -o "$baseline_archive"
  tar -xf "$baseline_archive" -C "$baseline_dir"

  # Snapshot the current working tree, including uncommitted manuscript edits,
  # while excluding Git metadata and generated artifacts.
  tar -C "$paper_dir" \
    --exclude=.git \
    --exclude=.latex-build \
    --exclude=main.pdf \
    --exclude=main_highlighted.pdf \
    --exclude='*.aux' \
    --exclude='*.bbl' \
    --exclude='*.blg' \
    --exclude='*.brf' \
    --exclude='*.fdb_latexmk' \
    --exclude='*.fls' \
    --exclude='*.log' \
    --exclude='*.synctex.gz' \
    -cf "$current_archive" .
  tar -xf "$current_archive" -C "$current_dir"

  if [[ ! -f "$baseline_dir/main.tex" || ! -f "$current_dir/main.tex" ]]; then
    echo "error: main.tex is missing from the baseline or current snapshot." >&2
    exit 1
  fi

  # Do not diff generated .bbl internals: latexdiff markup can invalidate
  # bibliography control sequences. Citation changes remain highlighted in the
  # manuscript, and latexmk regenerates the current bibliography from main.bib.
  rm -f "$baseline_dir/main.bbl" "$current_dir/main.bbl"

  echo "Generating highlighted manuscript against baseline $baseline_ref..."
  if ! "$latexdiff_bin" \
    --encoding=utf8 \
    --flatten \
    --graphics-markup=both \
    --math-markup=whole \
    "$baseline_dir/main.tex" \
    "$current_dir/main.tex" \
    > "$diff_tex_tmp" 2> "$diff_log"; then
    echo "error: latexdiff failed; see $diff_log" >&2
    exit 1
  fi
  mv -f "$diff_tex_tmp" "$diff_tex"

  # latexdiff treats changed tabular blocks as atomic floats. Activate the
  # cell-level markers embedded in the source so added columns/rows are blue.
  sed -i '/^\\begin{document}$/a\
\\providecommand{\\revisionadded}[1]{#1}\
\\renewcommand{\\revisionadded}[1]{\\textcolor{blue}{#1}}\
\\renewcommand{\\DIFaddFL}[1]{{\\color{blue}#1}}' \
    "$diff_tex"

  # A title fragment stored in \methodtask is invisible to latexdiff's normal
  # markup. Spell out the complete old and new subtitles in the review copy.
  if ! grep -q '^\\methodname: \\methodfullname ' "$diff_tex"; then
    echo "error: could not locate the manuscript title in $diff_tex" >&2
    exit 1
  fi
  sed -i '/^\\methodname: \\methodfullname /c\
\\methodname: \\methodfullname\\\\\
\\DIFdel{for Safety-Critical Visuomotor Skill Distillation}\\\\[-0.15em]\
\\DIFadd{Towards Safer Visuomotor Skill Distillation}' \
    "$diff_tex"

  cd "$paper_dir"
  TEXINPUTS="$paper_dir:" \
  BIBINPUTS="$paper_dir:" \
  BSTINPUTS="$paper_dir:" \
  latexmk \
    -gg \
    -pdf \
    -interaction=nonstopmode \
    -file-line-error \
    -outdir="$highlighted_dir" \
    "$diff_tex"

  publish_pdf "$highlighted_dir/main-highlighted.pdf" "$paper_dir/main_highlighted.pdf"
  echo "Built highlighted manuscript: $paper_dir/main_highlighted.pdf"
  echo "Baseline PDF: $submission_pdf"
  echo "Legend: additions are blue/underlined; deletions are red/struck out."
  if [[ -s "$diff_log" ]]; then
    echo "latexdiff diagnostics: $diff_log"
  fi
}

case "$mode" in
  normal)
    if [[ $# -gt 1 ]]; then
      usage >&2
      exit 2
    fi
    build_normal
    ;;
  highlighted|highlight)
    if [[ $# -gt 2 ]]; then
      usage >&2
      exit 2
    fi
    build_highlighted "${2:-${PAPER_DIFF_BASELINE:-$submission_ref}}"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "error: unknown build mode: $mode" >&2
    usage >&2
    exit 2
    ;;
esac
