#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script MASTER para processar tudo de uma vez:
1. Divide materiais.xlsx em 6 partes
2. Processa cada parte gerando páginas HTML estáticas
3. Gera página índice
"""

import os
import sys
import argparse
from dividir_planilha import dividir_planilha
from gerar_paginas_estaticas import processar_todas_partes

def processar_completo(arquivo_entrada='materiais.xlsx', 
                       num_partes=6,
                       pasta_partes='partes',
                       pasta_saida='paginas_html'):
    """
    Executa todo o fluxo:
    1. Dividir planilha
    2. Processar e gerar páginas HTML
    """
    
    print("\n" + "="*80)
    print("🚀 PROCESSAMENTO COMPLETO - SISTEMA DE BUSCA DE PREÇOS")
    print("="*80)
    print(f"""
📋 Configuração:
   • Arquivo de entrada: {arquivo_entrada}
   • Número de partes: {num_partes}
   • Pasta das partes: {pasta_partes}/
   • Pasta de saída: {pasta_saida}/
    """)
    
    input("⏸️  Pressione ENTER para iniciar o processamento...")
    
    # PASSO 1: Dividir planilha
    print("\n" + "="*80)
    print("📊 PASSO 1: DIVIDINDO PLANILHA EM PARTES")
    print("="*80 + "\n")
    
    try:
        dividir_planilha(arquivo_entrada, num_partes, pasta_partes)
    except Exception as e:
        print(f"\n❌ Erro ao dividir planilha: {e}")
        return 1
    
    print("\n✅ Planilha dividida com sucesso!")
    input("\n⏸️  Pressione ENTER para continuar para a busca de preços...")
    
    # PASSO 2: Processar todas as partes
    print("\n" + "="*80)
    print("🔍 PASSO 2: BUSCANDO PREÇOS E GERANDO PÁGINAS HTML")
    print("="*80)
    print("""
⚠️  ATENÇÃO: Este processo pode demorar VÁRIAS HORAS!
   • Cada material leva ~3 segundos
   • Progresso será exibido em tempo real
   • Você pode acompanhar pelos logs
    """)
    
    continuar = input("Deseja continuar? (sim/não): ").strip().lower()
    if continuar not in ['sim', 's', 'yes', 'y']:
        print("\n❌ Processamento cancelado pelo usuário")
        return 0
    
    try:
        processar_todas_partes(pasta_partes, pasta_saida)
    except Exception as e:
        print(f"\n❌ Erro ao processar partes: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Finalização
    print("\n" + "="*80)
    print("🎉 PROCESSAMENTO COMPLETO FINALIZADO!")
    print("="*80)
    
    index_path = os.path.join(pasta_saida, 'index.html')
    index_abs = os.path.abspath(index_path)
    
    print(f"""
✅ Páginas HTML geradas com sucesso!

📂 Arquivos gerados:
   • Partes da planilha: {pasta_partes}/
   • Páginas HTML: {pasta_saida}/

🌐 Para visualizar:
   1. Abra o arquivo: {index_path}
   2. Ou acesse: file://{index_abs}

💡 Recursos das páginas:
   ✅ Busca em tempo real
   ✅ Remover produtos irrelevantes
   ✅ Exportar para Excel (com filtros aplicados)
   ✅ Estatísticas dinâmicas
   ✅ Links diretos para Mercado Livre
    """)
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='Script MASTER para processar tudo de uma vez',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Este script executa TODO o fluxo automaticamente:
  1. Divide materiais.xlsx em N partes
  2. Busca preços para cada material
  3. Gera páginas HTML estáticas interativas
  4. Cria página índice

Exemplos:
  # Processar tudo (padrão: 6 partes)
  python3 processar_completo.py
  
  # Processar em 10 partes
  python3 processar_completo.py -n 10
  
  # Customizar pastas
  python3 processar_completo.py -i dados.xlsx -n 4 -o resultados_html

⏱️  TEMPO ESTIMADO:
  • 3306 materiais em 6 partes ≈ 3-4 horas
  • 100 materiais em 2 partes ≈ 5-7 minutos
        """
    )
    
    parser.add_argument('-i', '--entrada', default='materiais.xlsx',
                        help='Arquivo de entrada (padrão: materiais.xlsx)')
    parser.add_argument('-n', '--num-partes', type=int, default=6,
                        help='Número de partes (padrão: 6)')
    parser.add_argument('--pasta-partes', default='partes',
                        help='Pasta para as partes (padrão: partes)')
    parser.add_argument('-o', '--pasta-saida', default='paginas_html',
                        help='Pasta de saída (padrão: paginas_html)')
    
    args = parser.parse_args()
    
    return processar_completo(
        arquivo_entrada=args.entrada,
        num_partes=args.num_partes,
        pasta_partes=args.pasta_partes,
        pasta_saida=args.pasta_saida
    )

if __name__ == "__main__":
    sys.exit(main())

