#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de TESTE RÁPIDO para o sistema de páginas estáticas
Processa apenas alguns materiais para demonstração
"""

import pandas as pd
import os
import sys
import sys
import os
# Adicionar diretório scripts ao path
sys.path.insert(0, os.path.dirname(__file__))
from gerar_paginas_estaticas import gerar_pagina_estatica

def criar_planilha_teste(num_materiais=5):
    """Cria planilha de teste com N primeiros materiais"""
    
    print(f"📖 Criando planilha de teste com {num_materiais} materiais...")
    
    if not os.path.exists('materiais.xlsx'):
        print("❌ Arquivo materiais.xlsx não encontrado!")
        return None
    
    df = pd.read_excel('materiais.xlsx')
    
    if 'Nome' not in df.columns:
        print("❌ Planilha deve ter coluna 'Nome'")
        return None
    
    df_teste = df.head(num_materiais)
    
    arquivo_teste = 'teste_materiais_estatica.xlsx'
    df_teste.to_excel(arquivo_teste, index=False)
    
    print(f"✅ Planilha de teste criada: {arquivo_teste}")
    print(f"📊 Materiais selecionados:")
    for i, row in df_teste.iterrows():
        print(f"   {i+1}. {row['Nome']}")
    
    return arquivo_teste

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Teste rápido do sistema de páginas estáticas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Este script facilita testes rápidos:
  1. Cria planilha com N primeiros materiais
  2. Busca preços
  3. Gera página HTML estática
  4. Mostra instruções de abertura

Exemplos:
  python3 testar_paginas_estaticas.py           # 5 materiais (padrão)
  python3 testar_paginas_estaticas.py -n 3      # 3 materiais
  python3 testar_paginas_estaticas.py -n 10     # 10 materiais

⏱️  TEMPO ESTIMADO:
  • 3 materiais: ~15 segundos
  • 5 materiais: ~25 segundos
  • 10 materiais: ~50 segundos
        """
    )
    
    parser.add_argument('-n', '--num-materiais', type=int, default=5,
                        help='Número de materiais para testar (padrão: 5)')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("🧪 TESTE RÁPIDO - SISTEMA DE PÁGINAS ESTÁTICAS")
    print("="*80)
    print(f"""
📋 Configuração:
   • Materiais para teste: {args.num_materiais}
   • Tempo estimado: ~{args.num_materiais * 5} segundos
    """)
    
    # Passo 1: Criar planilha de teste
    print("="*80)
    print("📊 PASSO 1: CRIANDO PLANILHA DE TESTE")
    print("="*80 + "\n")
    
    arquivo_teste = criar_planilha_teste(args.num_materiais)
    
    if not arquivo_teste:
        return 1
    
    print("\n" + "="*80)
    print("🔍 PASSO 2: BUSCANDO PREÇOS E GERANDO PÁGINA HTML")
    print("="*80 + "\n")
    
    try:
        arquivo_html = 'teste_pagina_estatica.html'
        gerar_pagina_estatica(arquivo_teste, arquivo_html, numero_parte="TESTE")
        
        print("\n" + "="*80)
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("="*80)
        
        caminho_absoluto = os.path.abspath(arquivo_html)
        
        print(f"""
✅ Página HTML gerada!

📂 Arquivos:
   • Planilha: {arquivo_teste}
   • Página HTML: {arquivo_html}

🌐 Para visualizar, execute:
   
   xdg-open {arquivo_html}
   
   Ou abra manualmente:
   file://{caminho_absoluto}

💡 Funcionalidades disponíveis:
   ✅ Busca em tempo real
   ✅ Remover produtos manualmente
   ✅ Exportar para Excel
   ✅ Estatísticas dinâmicas
   ✅ Links para Mercado Livre

🎯 Próximos passos:
   1. Teste a remoção de produtos
   2. Experimente a exportação para Excel
   3. Se funcionar bem, processe tudo:
      python3 processar_completo.py
        """)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

