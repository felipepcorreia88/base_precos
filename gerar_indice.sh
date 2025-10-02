#!/bin/bash
# Wrapper para gerar índice
cd "$(dirname "$0")"
python3 scripts/gerar_indice.py "$@"

