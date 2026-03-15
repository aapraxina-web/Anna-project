#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/anna_pycache"

if [[ -x /opt/homebrew/bin/python3 ]]; then
  PYTHON_BIN="/opt/homebrew/bin/python3"
elif [[ -x /usr/local/bin/python3 ]]; then
  PYTHON_BIN="/usr/local/bin/python3"
elif [[ -x /usr/bin/python3 ]]; then
  PYTHON_BIN="/usr/bin/python3"
else
  echo "Python 3 не найден."
  read -r "?Нажмите Enter для выхода..."
  exit 1
fi

cd "$SCRIPT_DIR"
"$PYTHON_BIN" tic_tac_toe.py
