#!/bin/bash
# Wrapper para processar partes (modo interativo)
cd "$(dirname "$0")"
python3 scripts/processar_parte.py "$@"

