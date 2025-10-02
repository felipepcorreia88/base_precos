#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa UMA parte específica da planilha
Permite processar parte 1, depois parte 2, etc.
"""

import os
import sys
import argparse
from gerar_paginas_estaticas import gerar_pagina_estatica

def listar_partes_disponiveis(pasta_partes='output/partes'):
    """Lista as partes disponíveis"""
    if not os.path.exists(pasta_partes):
        return []
    
    arquivos = sorted([
        f for f in os.listdir(pasta_partes)
        if f.startswith('materiais_parte_') and f.endswith('.xlsx')
    ])
    
    return arquivos

def verificar_partes_processadas(pasta_saida='output/paginas_html'):
    """Verifica quais partes já foram processadas"""
    if not os.path.exists(pasta_saida):
        return []
    
    arquivos = [
        f for f in os.listdir(pasta_saida)
        if f.startswith('pagina_parte_') and f.endswith('.html')
    ]
    
    partes_processadas = []
    for arquivo in arquivos:
        # Extrai número da parte: pagina_parte_1.html -> 1
        numero = arquivo.replace('pagina_parte_', '').replace('.html', '')
        partes_processadas.append(int(numero))
    
    return sorted(partes_processadas)

def processar_parte(numero_parte, pasta_partes='output/partes', pasta_saida='output/paginas_html'):
    """Processa uma parte específica"""
    
    print(f"\n{'='*80}")
    print(f"🔄 PROCESSANDO PARTE {numero_parte}")
    print(f"{'='*80}\n")
    
    # Verificar se a parte existe
    arquivo_entrada = os.path.join(pasta_partes, f'materiais_parte_{numero_parte}.xlsx')
    
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Erro: Arquivo não encontrado: {arquivo_entrada}")
        print(f"\n💡 Dica: Execute primeiro 'python3 dividir_planilha.py'")
        return 1
    
    # Criar pasta de saída se não existir
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"📁 Pasta criada: {pasta_saida}\n")
    
    # Gerar página HTML
    arquivo_saida = os.path.join(pasta_saida, f'pagina_parte_{numero_parte}.html')
    
    try:
        gerar_pagina_estatica(arquivo_entrada, arquivo_saida, numero_parte)
        
        print(f"\n{'='*80}")
        print(f"✅ PARTE {numero_parte} PROCESSADA COM SUCESSO!")
        print(f"{'='*80}\n")
        
        print(f"📂 Arquivos:")
        print(f"   • Entrada: {arquivo_entrada}")
        print(f"   • Saída: {arquivo_saida}")
        
        caminho_absoluto = os.path.abspath(arquivo_saida)
        print(f"\n🌐 Para visualizar:")
        print(f"   xdg-open {arquivo_saida}")
        print(f"   \nOu abra: file://{caminho_absoluto}")
        
        # Mostrar progresso geral
        partes_processadas = verificar_partes_processadas(pasta_saida)
        partes_disponiveis = listar_partes_disponiveis(pasta_partes)
        
        if partes_disponiveis:
            print(f"\n📊 Progresso Geral:")
            print(f"   • Partes processadas: {len(partes_processadas)}/{len(partes_disponiveis)}")
            print(f"   • Partes concluídas: {sorted(partes_processadas)}")
            
            if len(partes_processadas) < len(partes_disponiveis):
                proximas = [i+1 for i in range(len(partes_disponiveis)) if (i+1) not in partes_processadas]
                if proximas:
                    print(f"   • Próximas partes: {proximas[:3]}")
                    print(f"\n💡 Para processar a próxima parte:")
                    print(f"   python3 processar_parte.py -p {proximas[0]}")
            else:
                print(f"\n🎉 TODAS AS PARTES FORAM PROCESSADAS!")
                print(f"   Abra: {pasta_saida}/index.html (será criado ao gerar índice)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro ao processar parte {numero_parte}: {e}")
        import traceback
        traceback.print_exc()
        return 1

def modo_interativo(pasta_partes='output/partes', pasta_saida='output/paginas_html'):
    """Modo interativo para escolher qual parte processar"""
    
    print("\n" + "="*80)
    print("🎯 MODO INTERATIVO - Processar Partes")
    print("="*80 + "\n")
    
    # Listar partes disponíveis
    partes_disponiveis = listar_partes_disponiveis(pasta_partes)
    
    if not partes_disponiveis:
        print(f"❌ Nenhuma parte encontrada em '{pasta_partes}/'")
        print(f"\n💡 Execute primeiro:")
        print(f"   python3 dividir_planilha.py")
        return 1
    
    # Verificar partes já processadas
    partes_processadas = verificar_partes_processadas(pasta_saida)
    
    print(f"📦 Partes disponíveis: {len(partes_disponiveis)}")
    print(f"✅ Partes processadas: {len(partes_processadas)}\n")
    
    print("Status de cada parte:")
    print("-" * 50)
    
    for i, arquivo in enumerate(partes_disponiveis, 1):
        status = "✅ Processada" if i in partes_processadas else "⏳ Pendente"
        print(f"   {i}. {arquivo:<35} {status}")
    
    print("-" * 50)
    
    # Perguntar qual parte processar
    print("\n💡 Escolha uma parte para processar:")
    print("   Digite o número da parte (1-{})".format(len(partes_disponiveis)))
    print("   Ou 'q' para sair")
    
    while True:
        try:
            escolha = input("\n➤ Parte: ").strip().lower()
            
            if escolha in ['q', 'quit', 'sair']:
                print("\n👋 Até logo!")
                return 0
            
            numero = int(escolha)
            
            if numero < 1 or numero > len(partes_disponiveis):
                print(f"❌ Número inválido. Escolha entre 1 e {len(partes_disponiveis)}")
                continue
            
            # Avisar se já foi processada
            if numero in partes_processadas:
                print(f"\n⚠️  A parte {numero} já foi processada.")
                resposta = input("   Deseja processar novamente? (s/n): ").strip().lower()
                if resposta not in ['s', 'sim', 'y', 'yes']:
                    print("   Operação cancelada.")
                    continue
            
            # Processar
            return processar_parte(numero, pasta_partes, pasta_saida)
            
        except ValueError:
            print("❌ Digite um número válido ou 'q' para sair")
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário")
            return 0

def main():
    parser = argparse.ArgumentParser(
        description='Processa UMA parte específica da planilha',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Este script permite processar partes INDIVIDUALMENTE.

Exemplos:
  # Modo interativo (escolher parte)
  python3 processar_parte.py
  
  # Processar parte 1
  python3 processar_parte.py -p 1
  
  # Processar parte 3
  python3 processar_parte.py -p 3
  
  # Customizar pastas
  python3 processar_parte.py -p 2 --pasta-partes divisoes --pasta-saida htmls

Fluxo recomendado:
  1. Dividir planilha:
     python3 dividir_planilha.py
  
  2. Processar parte 1:
     python3 processar_parte.py -p 1
  
  3. Validar resultados da parte 1 (abrir HTML, remover produtos, exportar)
  
  4. Processar parte 2:
     python3 processar_parte.py -p 2
  
  5. Repetir até processar todas as partes

⏱️  TEMPO POR PARTE (6 partes = 3306 materiais):
  • Cada parte: ~551 materiais
  • Tempo: ~40 minutos por parte
  • Total: ~4 horas (se processar uma por vez)
        """
    )
    
    parser.add_argument('-p', '--parte', type=int, 
                        help='Número da parte a processar (1, 2, 3, ...)')
    parser.add_argument('--pasta-partes', default='output/partes',
                        help='Pasta com as partes (padrão: output/partes)')
    parser.add_argument('--pasta-saida', default='output/paginas_html',
                        help='Pasta de saída (padrão: output/paginas_html)')
    parser.add_argument('-i', '--interativo', action='store_true',
                        help='Modo interativo (escolher parte)')
    
    args = parser.parse_args()
    
    # Se não especificou parte nem modo interativo, usa interativo
    if args.parte is None and not args.interativo:
        return modo_interativo(args.pasta_partes, args.pasta_saida)
    
    # Modo interativo explícito
    if args.interativo:
        return modo_interativo(args.pasta_partes, args.pasta_saida)
    
    # Processar parte específica
    return processar_parte(args.parte, args.pasta_partes, args.pasta_saida)

if __name__ == "__main__":
    sys.exit(main())

