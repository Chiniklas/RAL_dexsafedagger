#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
response_dir="$project_dir/comments/RAL/second_rebutal/response"
output_dir="$project_dir/output"

if [[ ! -f "$response_dir/response.tex" ]]; then
  echo "error: response source is missing: $response_dir/response.tex" >&2
  exit 1
fi

mkdir -p "$response_dir" "$output_dir"
cd "$response_dir"

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -file-line-error \
  response.tex

cp "$response_dir/response.pdf" "$output_dir/response.pdf.tmp"
mv -f "$output_dir/response.pdf.tmp" "$output_dir/response.pdf"
echo "Built reviewer response: $output_dir/response.pdf"
