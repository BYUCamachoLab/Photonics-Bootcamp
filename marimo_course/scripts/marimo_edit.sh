#!/usr/bin/env bash
set -euo pipefail

VENV_PATH="/Users/ryancamacho/venvs/photonics-bootcamp"

if [[ ! -x "${VENV_PATH}/bin/marimo" ]]; then
  echo "Missing marimo in ${VENV_PATH}. Did you create the venv?" >&2
  exit 1
fi

export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/tmp/pycache}"

exec "${VENV_PATH}/bin/marimo" edit "$@"
