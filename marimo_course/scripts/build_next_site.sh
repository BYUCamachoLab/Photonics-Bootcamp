#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <output-dir>" >&2
  exit 1
fi

out_dir="$1"
export_dir="$out_dir/exports"
mkdir -p "$export_dir/lessons" "$export_dir/assignments"

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w01_orientation_tooling.py \
  -o "$export_dir/lessons/w01_orientation_tooling.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/practice_marimo.py \
  -o "$export_dir/lessons/practice_marimo.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w02_mzi_modelling.py \
  -o "$export_dir/lessons/w02_mzi_modelling.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/lessons/w02_pdk_mzi_layout.py \
  -o "$export_dir/lessons/w02_pdk_mzi_layout.html" -f

PB_SKIP_GF=1 marimo export html marimo_course/assignments/hw02_mzi_modelling.py \
  -o "$export_dir/assignments/hw02_mzi_modelling.html" -f
