#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: run_klayout_drc.sh <input_gds> [output_lyrdb] [drc_deck]

Runs KLayout batch DRC on the given GDS using the SiEPIC EBeam DRC deck.
Defaults:
  output_lyrdb: <input_gds_basename>.lyrdb in the same folder
  drc_deck: SiEPIC_EBeam_PDK_public/klayout/EBeam/drc/SiEPIC_EBeam_DRC.lydrc
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || -z "${1:-}" ]]; then
  usage
  exit 0
fi

INPUT_GDS="$1"
OUTPUT_LYRDB="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEFAULT_DRC="${REPO_ROOT}/marimo_course/scripts/SiEPIC_EBeam_batch.drc"
DRC_DECK="${3:-${DEFAULT_DRC}}"

if [[ -z "${OUTPUT_LYRDB}" ]]; then
  base="$(basename "${INPUT_GDS}")"
  OUTPUT_LYRDB="$(dirname "${INPUT_GDS}")/${base%.*}.lyrdb"
fi

INPUT_GDS="$(cd "$(dirname "${INPUT_GDS}")" && pwd)/$(basename "${INPUT_GDS}")"
OUTPUT_LYRDB="$(cd "$(dirname "${OUTPUT_LYRDB}")" && pwd)/$(basename "${OUTPUT_LYRDB}")"
DRC_DECK="$(cd "$(dirname "${DRC_DECK}")" && pwd)/$(basename "${DRC_DECK}")"

if [[ ! -f "${INPUT_GDS}" ]]; then
  echo "Input GDS not found: ${INPUT_GDS}" >&2
  exit 1
fi

if [[ ! -f "${DRC_DECK}" ]]; then
  echo "DRC deck not found: ${DRC_DECK}" >&2
  exit 1
fi

if command -v klayout >/dev/null 2>&1; then
  KLAYOUT_BIN="klayout"
elif [[ -x "/Applications/KLayout.app/Contents/MacOS/klayout" ]]; then
  KLAYOUT_BIN="/Applications/KLayout.app/Contents/MacOS/klayout"
else
  echo "KLayout binary not found. Install KLayout or add it to PATH." >&2
  exit 1
fi

echo "Running DRC..."
echo "  input : ${INPUT_GDS}"
echo "  report: ${OUTPUT_LYRDB}"
echo "  deck  : ${DRC_DECK}"

"${KLAYOUT_BIN}" -b -r "${DRC_DECK}" \
  -rd "input=${INPUT_GDS}" \
  -rd "output=${OUTPUT_LYRDB}"

echo "DRC report written to: ${OUTPUT_LYRDB}"
