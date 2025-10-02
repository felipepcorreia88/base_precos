#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar diferentes níveis de restrição
"""

from busca_materiais_planilha_otimizado import BuscadorMateriaisPlanilhaOtimizado
from busca_materiais_planilha_restritivo import BuscadorMateriaisRestritivo

def comparar_niveis():
    """Compara 3 níveis de restrição"""
    
    termo_teste = "ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Banner PCD"
    
    print("=" * 80)
    print("�� COMPARAÇÃO DE NÍVEIS DE RESTRIÇÃO")
    print("=" * 80)
    print(f"\n📝 TERMO TESTE: {termo_teste}")
    print()
    
    # NÍVEL 1: Score 0.3 (atual)
    print("\n" + "="*80)
    print("NÍVEL 1: Score >= 0.3 (PERMISSIVO)")
    print("="*80)
    buscador1 = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=0.3)
    resultado1 = buscador1.buscar_produtos_material(termo_teste)
    
    print(f"📦 Produtos relevantes: {resultado1['total_relevante']}")
    if resultado1['produtos']:
        print(f"\n🏆 Top 5:")
        for i, p in enumerate(resultado1['produtos'][:5], 1):
            score = p.get('score_relevancia', 0)
            print(f"   {i}. [{score:.2f}] {p['nome'][:65]}")
    
    # NÍVEL 2: Score 1.0
    print("\n" + "="*80)
    print("NÍVEL 2: Score >= 1.0 (EXIGE TODAS PALAVRAS)")
    print("="*80)
    buscador2 = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=1.0)
    resultado2 = buscador2.buscar_produtos_material(termo_teste)
    
    print(f"📦 Produtos relevantes: {resultado2['total_relevante']}")
    if resultado2['produtos']:
        print(f"\n🏆 Top 5:")
        for i, p in enumerate(resultado2['produtos'][:5], 1):
            score = p.get('score_relevancia', 0)
            print(f"   {i}. [{score:.2f}] {p['nome'][:65]}")
    
    # NÍVEL 3: Modo estrito
    print("\n" + "="*80)
    print("NÍVEL 3: MODO ESTRITO (TODAS palavras obrigatórias)")
    print("="*80)
    buscador3 = BuscadorMateriaisRestritivo(modo_estrito=True)
    resultado3 = buscador3.buscar_produtos_material(termo_teste)
    
    print(f"📦 Produtos relevantes: {resultado3['total_relevante']}")
    if resultado3['produtos']:
        print(f"\n🏆 Top 5:")
        for i, p in enumerate(resultado3['produtos'][:5], 1):
            score = p.get('score_relevancia', 0)
            print(f"   {i}. [{score:.2f}] {p['nome'][:65]}")
    
    # Comparação final
    print("\n" + "="*80)
    print("📊 COMPARAÇÃO FINAL")
    print("="*80)
    print(f"NÍVEL 1 (Score >= 0.3):  {resultado1['total_relevante']} produtos")
    print(f"NÍVEL 2 (Score >= 1.0):  {resultado2['total_relevante']} produtos")
    print(f"NÍVEL 3 (Modo Estrito):  {resultado3['total_relevante']} produtos")
    print()
    print("💡 RECOMENDAÇÃO: Use Nível 2 ou 3 para maior relevância")

if __name__ == "__main__":
    import time
    print("\n⏳ Aguarde, fazendo 3 buscas no Mercado Livre...")
    print("   Tempo estimado: ~10 segundos\n")
    comparar_niveis()
