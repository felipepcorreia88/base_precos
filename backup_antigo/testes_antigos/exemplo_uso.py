#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do sistema de busca de preços de materiais
"""

from busca_materiais_planilha import BuscadorMateriaisPlanilha
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def exemplo_uso():
    """Demonstra como usar o sistema"""
    
    print("🚀 Sistema de Busca de Preços de Materiais")
    print("=" * 50)
    
    # Criar buscador
    buscador = BuscadorMateriaisPlanilha()
    
    print("\n📋 Opções disponíveis:")
    print("1. Teste pequeno (5 materiais)")
    print("2. Teste médio (50 materiais)")
    print("3. Processar toda a planilha (3306 materiais)")
    print("4. Busca individual")
    
    opcao = input("\nEscolha uma opção (1-4): ").strip()
    
    if opcao == "1":
        print("\n🧪 Executando teste pequeno...")
        buscador.processar_planilha('materiais.xlsx', 'teste_pequeno_5_materiais.xlsx')
        
    elif opcao == "2":
        print("\n🔬 Executando teste médio...")
        # Processar apenas os primeiros 50 materiais
        import pandas as pd
        df = pd.read_excel('materiais.xlsx')
        df_teste = df.head(50).copy()
        df_teste.to_excel('materiais_teste_50.xlsx', index=False)
        buscador.processar_planilha('materiais_teste_50.xlsx', 'teste_medio_50_materiais.xlsx')
        
    elif opcao == "3":
        print("\n⚠️  ATENÇÃO: Processamento completo!")
        print("   - 3306 materiais")
        print("   - Tempo estimado: ~3-4 horas")
        print("   - Pausa de 30s a cada 100 itens")
        
        confirmar = input("\nDeseja continuar? (s/N): ").strip().lower()
        if confirmar == 's':
            buscador.processar_planilha('materiais.xlsx', 'materiais_com_precos_completo.xlsx')
        else:
            print("❌ Operação cancelada.")
            
    elif opcao == "4":
        termo = input("\nDigite o termo para buscar: ").strip()
        if termo:
            print(f"\n🔍 Buscando: {termo}")
            resultado = buscador.buscar_produtos_material(termo)
            
            print(f"\n📊 Resultados:")
            print(f"   Status: {resultado['status']}")
            print(f"   Produtos encontrados: {resultado['total_encontrado']}")
            
            if resultado['estatisticas']:
                stats = resultado['estatisticas']
                print(f"   Preço mínimo: R$ {stats['preco_minimo']:.2f}")
                print(f"   Preço máximo: R$ {stats['preco_maximo']:.2f}")
                print(f"   Preço médio: R$ {stats['preco_medio']:.2f}")
                print(f"   Preço mediana: R$ {stats['preco_mediana']:.2f}")
                print(f"   Desvio padrão: R$ {stats['desvio_padrao']:.2f}")
                print(f"   Outliers removidos: {stats['outliers_removidos']}")
            
            if resultado['produtos']:
                print(f"\n🛍️  Primeiros 3 produtos:")
                for i, produto in enumerate(resultado['produtos'][:3], 1):
                    print(f"   {i}. {produto['nome'][:60]}...")
                    print(f"      Preço: R$ {produto['preco']:.2f}")
                    print(f"      Loja: {produto['loja']}")
    
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    exemplo_uso()
