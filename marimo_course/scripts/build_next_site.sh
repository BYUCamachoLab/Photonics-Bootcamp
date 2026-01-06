#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <output-dir>" >&2
  exit 1
fi

out_dir="$1"
mkdir -p "$out_dir/lessons" "$out_dir/assignments"

cp marimo_course/site/index.html "$out_dir/index.html"

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w01_orientation_tooling.py \
  -o "$out_dir/lessons/w01_orientation_tooling.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/practice_marimo.py \
  -o "$out_dir/lessons/practice_marimo.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w02_mzi_modelling.py \
  -o "$out_dir/lessons/w02_mzi_modelling.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w02_pdk_mzi_layout.py \
  -o "$out_dir/lessons/w02_pdk_mzi_layout.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/assignments/hw02_mzi_modelling.py \
  -o "$out_dir/assignments/hw02_mzi_modelling.html" -f
