#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa MODO INTELIGENTE vs outros modos
"""

from busca_materiais_planilha_inteligente import BuscadorInteligente
import pandas as pd
import argparse

def testar_modo_inteligente(arquivo_planilha='materiais.xlsx', num_linhas=3, salvar=None):
    """Testa modo inteligente com N linhas"""
    
    print("=" * 80)
    print("🧠 TESTE - MODO INTELIGENTE")
    print("   (Palavras específicas são OBRIGATÓRIAS)")
    print("=" * 80)
    print()
    
    try:
        df = pd.read_excel(arquivo_planilha)
        if 'Nome' not in df.columns:
            print("❌ Planilha deve ter coluna 'Nome'")
            return
        
        df_teste = df.head(num_linhas)
        buscador = BuscadorInteligente()
        
        print(f"📖 Planilha: {arquivo_planilha}")
        print(f"🎯 Processando: {len(df_teste)} materiais")
        print()
        
        resultados = []
        
        for idx, row in df_teste.iterrows():
            nome = str(row['Nome']).strip()
            
            print(f"\n{'='*80}")
            print(f"📋 MATERIAL {idx + 1}/{len(df_teste)}")
            print(f"{'='*80}")
            print(f"📝 ORIGINAL: {nome}")
            print()
            
            # Buscar
            print("🔄 Buscando no Mercado Livre...")
            resultado = buscador.buscar_produtos_material(nome)
            
            print(f"\n✅ OTIMIZADO: {resultado.get('termo_otimizado', '')}")
            print(f"🔴 OBRIGATÓRIAS: {resultado.get('palavras_obrigatorias', [])}")
            print(f"🟡 OPCIONAIS: {resultado.get('palavras_opcionais', [])}")
            print(f"📦 BRUTOS: {resultado.get('total_encontrado', 0)}")
            print(f"🎯 RELEVANTES: {resultado.get('total_relevante', 0)} (com TODAS obrigatórias)")
            
            if resultado.get('produtos'):
                print(f"\n🏆 TOP 5 PRODUTOS:")
                for i, p in enumerate(resultado['produtos'][:5], 1):
                    print(f"   {i}. [{p.get('score_relevancia', 0):.2f}] {p['nome'][:65]}")
                    print(f"      💰 R$ {p['preco']:.2f}")
            else:
                print(f"\n❌ Nenhum produto com TODAS as palavras obrigatórias")
            
            # Coletar para salvar
            if salvar:
                stats = resultado.get('estatisticas', {})
                produtos = resultado.get('produtos', [])
                
                # Calcular estatísticas adicionais
                preco_mediana = None
                desvio_padrao = None
                outliers_removidos = 0
                
                if produtos:
                    precos = [p['preco'] for p in produtos if 'preco' in p]
                    if precos:
                        precos.sort()
                        n = len(precos)
                        if n % 2 == 0:
                            preco_mediana = (precos[n//2-1] + precos[n//2]) / 2
                        else:
                            preco_mediana = precos[n//2]
                        
                        # Desvio padrão simples
                        media = sum(precos) / len(precos)
                        variancia = sum((p - media) ** 2 for p in precos) / len(precos)
                        desvio_padrao = variancia ** 0.5
                
                resultados.append({
                    'Nome_Original': nome,
                    'Termo_Otimizado': resultado.get('termo_otimizado', ''),
                    'Palavras_Chave': ', '.join(resultado.get('palavras_obrigatorias', []) + resultado.get('palavras_opcionais', [])),
                    'Total_Produtos_Encontrados': resultado.get('total_encontrado', 0),
                    'Total_Produtos_Relevantes': resultado.get('total_relevante', 0),
                    'Preco_Minimo': stats.get('preco_minimo') if stats else None,
                    'Preco_Maximo': stats.get('preco_maximo') if stats else None,
                    'Preco_Medio': stats.get('preco_medio') if stats else None,
                    'Preco_Mediana': preco_mediana,
                    'Desvio_Padrao': desvio_padrao,
                    'Outliers_Removidos': outliers_removidos,
                    'Links_Produtos_JSON': resultado.get('links_produtos', ''),
                    'Status_Busca': resultado.get('status', ''),
                    'Data_Hora_Busca': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            if idx < len(df_teste) - 1:
                print(f"\n⏸️  Aguardando 3s...")
                import time
                time.sleep(3)
        
        print("\n" + "=" * 80)
        print("✅ TESTE CONCLUÍDO!")
        print("=" * 80)
        
        # Salvar
        if salvar and resultados:
            print(f"\n💾 Salvando: {salvar}")
            df_result = pd.DataFrame(resultados)
            df_result.to_excel(salvar, index=False)
            print(f"✅ Salvo com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Teste modo inteligente')
    parser.add_argument('--linhas', '-n', type=int, default=3)
    parser.add_argument('--planilha', '-p', default='materiais.xlsx')
    parser.add_argument('--salvar', '-o')
    args = parser.parse_args()
    
    testar_modo_inteligente(args.planilha, args.linhas, args.salvar)

if __name__ == "__main__":
    main()
