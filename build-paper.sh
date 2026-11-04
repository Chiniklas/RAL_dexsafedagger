#!/usr/bin/env bash
set -euo pipefail

paper_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
build_dir="$paper_dir/.latex-build"
output_dir="$paper_dir/output"
mode="${1:-normal}"

# This snapshot contains the source used for the last submitted manuscript
# revision. The archived PDF is pinned below so the default comparison target
# cannot silently change.
revision_ref="5a42fcb"
revision_pdf="$paper_dir/comments/RAL/first_rebutal/output/revision/main.pdf"
revision_pdf_sha256="33c6e17f4b69925ef7c86f28454b7abeba1125ea8b118c7ac43eacbfb5b44070"

usage() {
  cat <<'EOF'
Usage:
  ./build-paper.sh
  ./build-paper.sh normal
  ./build-paper.sh highlighted [baseline-git-ref]

Modes:
  normal       Build the current manuscript normally.
  highlighted  Build main_highlighted.pdf with revised material marked by
               yellow highlight stripes relative to the last submitted
               manuscript revision. Deleted material is omitted.

The highlighted mode defaults to Git snapshot 5a42fcb, the source corresponding
to comments/RAL/first_rebutal/output/revision/main.pdf. Pass a different Git
ref to override the comparison baseline.

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
  mkdir -p "$build_dir" "$output_dir"
  cd "$paper_dir"

  latexmk \
    -pdf \
    -interaction=nonstopmode \
    -file-line-error \
    -outdir="$build_dir" \
    main.tex

  publish_pdf "$build_dir/main.pdf" "$output_dir/main.pdf"
  echo "Built normal manuscript: $output_dir/main.pdf"
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
  local actual_revision_sha

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

  if [[ "$baseline_ref" == "$revision_ref" ]]; then
    if [[ ! -f "$revision_pdf" ]]; then
      echo "error: authoritative baseline PDF is missing: $revision_pdf" >&2
      exit 1
    fi
    actual_revision_sha="$(sha256sum "$revision_pdf" | awk '{print $1}')"
    if [[ "$actual_revision_sha" != "$revision_pdf_sha256" ]]; then
      echo "error: baseline PDF no longer matches the recorded revision." >&2
      echo "expected: $revision_pdf_sha256" >&2
      echo "actual:   $actual_revision_sha" >&2
      exit 1
    fi
  fi

  mkdir -p "$highlighted_dir" "$output_dir"
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
    --exclude=output \
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
    --no-del \
    --graphics-markup=new-only \
    --math-markup=whole \
    "$baseline_dir/main.tex" \
    "$current_dir/main.tex" \
    > "$diff_tex_tmp" 2> "$diff_log"; then
    echo "error: latexdiff failed; see $diff_log" >&2
    exit 1
  fi
  mv -f "$diff_tex_tmp" "$diff_tex"

  # Render additions as black text over yellow highlighter stripes. The ulem
  # machinery generated by latexdiff allows the stripe to wrap across lines.
  # Existing \revisionadded markers belong to the previous review round and
  # intentionally retain their no-op definition from main.tex.
  sed -i '/^\\begin{document}$/a\
\\providecommand{\\DIFyellowstripe}{\\bgroup\\markoverwith{\\textcolor{yellow}{\\rule[-0.5ex]{2pt}{2.5ex}}}\\ULon}\
\\renewcommand{\\DIFaddtex}[1]{\\DIFyellowstripe{#1}}\
\\renewcommand{\\DIFaddFL}[1]{\\texorpdfstring{\\colorbox{yellow}{\\strut #1}}{#1}}' \
    "$diff_tex"

  # latexdiff's figure-markup helper uses blue by default. Keep all visible
  # revision marks in the requested yellow style.
  sed -i 's/\\color{blue}/\\color{yellow}/g' "$diff_tex"

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

  publish_pdf "$highlighted_dir/main-highlighted.pdf" "$output_dir/main_highlighted.pdf"
  echo "Built highlighted manuscript: $output_dir/main_highlighted.pdf"
  if [[ "$baseline_ref" == "$revision_ref" ]]; then
    echo "Baseline PDF: $revision_pdf"
  else
    echo "Baseline Git ref: $baseline_ref"
  fi
  echo "Legend: revised material is marked with yellow highlight stripes; deletions are omitted."
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
    build_highlighted "${2:-${PAPER_DIFF_BASELINE:-$revision_ref}}"
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
