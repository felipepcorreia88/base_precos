#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para dividir materiais.xlsx em 6 partes iguais
"""

import pandas as pd
import math
import argparse
import os

def dividir_planilha(arquivo_entrada, num_partes=6, pasta_saida='output/partes'):
    """Divide planilha em N partes iguais"""
    
    print(f"📖 Lendo: {arquivo_entrada}")
    df = pd.read_excel(arquivo_entrada)
    
    if 'Nome' not in df.columns:
        raise ValueError("Planilha deve ter coluna 'Nome'")
    
    total_linhas = len(df)
    linhas_por_parte = math.ceil(total_linhas / num_partes)
    
    print(f"📊 Total de materiais: {total_linhas}")
    print(f"📦 Divisão em {num_partes} partes: ~{linhas_por_parte} materiais por parte")
    
    # Criar pasta de saída
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"📁 Pasta criada: {pasta_saida}")
    
    arquivos_gerados = []
    
    for i in range(num_partes):
        inicio = i * linhas_por_parte
        fim = min((i + 1) * linhas_por_parte, total_linhas)
        
        df_parte = df.iloc[inicio:fim].copy()
        
        # Resetar índice
        df_parte.reset_index(drop=True, inplace=True)
        
        arquivo_saida = os.path.join(pasta_saida, f'materiais_parte_{i+1}.xlsx')
        df_parte.to_excel(arquivo_saida, index=False)
        
        arquivos_gerados.append(arquivo_saida)
        
        print(f"   ✅ Parte {i+1}: {len(df_parte)} materiais → {arquivo_saida}")
    
    print(f"\n🎉 {num_partes} arquivos gerados em '{pasta_saida}/'")
    
    return arquivos_gerados

def main():
    parser = argparse.ArgumentParser(
        description='Divide materiais.xlsx em partes iguais',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 dividir_planilha.py                    # Divide em 6 partes (padrão)
  python3 dividir_planilha.py -n 4               # Divide em 4 partes
  python3 dividir_planilha.py -i dados.xlsx -n 10  # Arquivo customizado
        """
    )
    
    parser.add_argument('-i', '--entrada', default='materiais.xlsx',
                        help='Arquivo de entrada (padrão: materiais.xlsx)')
    parser.add_argument('-n', '--num-partes', type=int, default=6,
                        help='Número de partes (padrão: 6)')
    parser.add_argument('-o', '--pasta-saida', default='output/partes',
                        help='Pasta de saída (padrão: output/partes)')
    
    args = parser.parse_args()
    
    try:
        dividir_planilha(args.entrada, args.num_partes, args.pasta_saida)
        return 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

