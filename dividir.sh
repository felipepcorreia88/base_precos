#!/bin/bash
# Wrapper para dividir planilha em N partes
# Uso: ./dividir.sh [-n NUMERO_PARTES] [-i ARQUIVO_ENTRADA]
# Exemplos:
#   ./dividir.sh           # Divide em 6 partes (padrão)
#   ./dividir.sh -n 10     # Divide em 10 partes
#   ./dividir.sh -n 3      # Divide em 3 partes

cd "$(dirname "$0")"
python3 scripts/dividir_planilha.py "$@"

