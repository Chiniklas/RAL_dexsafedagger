#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
response_dir="$project_dir/comments/RAL/response"

mkdir -p "$response_dir"
cd "$response_dir"

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -file-line-error \
  response.tex
