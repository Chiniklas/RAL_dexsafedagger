#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
appendix_dir="$project_dir/comments/RAL/response"

mkdir -p "$appendix_dir"
cd "$appendix_dir"

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -file-line-error \
  appendix.tex
