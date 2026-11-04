#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
appendix_dir="$project_dir/comments/RAL/second_rebutal/response"
output_dir="$project_dir/output"

if [[ ! -f "$appendix_dir/appendix.tex" ]]; then
  echo "error: appendix source is missing: $appendix_dir/appendix.tex" >&2
  exit 1
fi

mkdir -p "$appendix_dir" "$output_dir"
cd "$appendix_dir"

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -file-line-error \
  appendix.tex

cp "$appendix_dir/appendix.pdf" "$output_dir/appendix.pdf.tmp"
mv -f "$output_dir/appendix.pdf.tmp" "$output_dir/appendix.pdf"
echo "Built supplementary material: $output_dir/appendix.pdf"
