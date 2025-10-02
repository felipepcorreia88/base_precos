#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar e comparar otimização de termos de busca
Agora com suporte para processar N linhas da planilha e SALVAR resultados
"""

import argparse
import pandas as pd
from datetime import datetime
from busca_materiais_planilha_otimizado import BuscadorMateriaisPlanilhaOtimizado

def testar_otimizacao_visual():
    """Testa otimização de termos (SEM buscar no Mercado Livre)"""
    
    print("=" * 80)
    print("🧪 TESTE VISUAL DE OTIMIZAÇÃO DE BUSCA")
    print("=" * 80)
    print()
    
    # Exemplos de termos problemáticos
    termos_teste = [
        "ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD",
        "MATERIAIS ESPORTIVOS - Cones de Treinamento",
        "EQUIPAMENTOS PARA EXERCÍCIOS - Faixa Elástica Thera Band",
        "Kit de Alongamento - Bastão de Madeira",
        "ACESSÓRIOS FITNESS - Rolo de Espuma"
    ]
    
    buscador = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=0.3)
    
    for termo in termos_teste:
        print(f"\n{'='*80}")
        print(f"📝 TERMO ORIGINAL:")
        print(f"   {termo}")
        print()
        
        # Otimizar termo
        otimizacao = buscador.otimizar_termo_busca(termo)
        
        print(f"✅ TERMO OTIMIZADO:")
        print(f"   {otimizacao['termo_otimizado']}")
        print()
        
        print(f"🔑 PALAVRAS-CHAVE:")
        print(f"   {', '.join(otimizacao['palavras_chave'])}")
        print()
        
        # Exemplo de scores
        produtos_exemplo = [
            "Kit Bola Suíça 65cm PCD Pilates Premium",
            "Bola Suíça Profissional 55cm",
            "Kit 50 Bolas Para Piscina De Bolinhas Baby",
            "Bola de Pilates com Bomba",
        ]
        
        print(f"📊 SCORES DE RELEVÂNCIA (exemplos):")
        for i, prod in enumerate(produtos_exemplo, 1):
            score = buscador.calcular_score_relevancia(prod, otimizacao['palavras_chave'])
            status = "✅ MANTIDO" if score >= 0.3 else "❌ REMOVIDO"
            print(f"   [{score:.2f}] {status} - {prod}")
    
    print()
    print("=" * 80)
    print("💡 DICA: Produtos com score >= 0.3 são considerados relevantes")
    print("=" * 80)


def testar_planilha(arquivo_planilha, num_linhas, min_score=0.3, fazer_busca=False, arquivo_saida=None):
    """
    Testa otimização com N linhas da planilha
    
    Args:
        arquivo_planilha (str): Caminho da planilha
        num_linhas (int): Número de linhas a processar
        min_score (float): Score mínimo de relevância
        fazer_busca (bool): Se True, faz busca real no Mercado Livre
        arquivo_saida (str): Arquivo Excel para salvar resultados (opcional)
    """
    print("=" * 80)
    print(f"🧪 TESTE COM PLANILHA - {num_linhas} LINHAS")
    print("=" * 80)
    print()
    
    try:
        # Ler planilha
        print(f"📖 Lendo planilha: {arquivo_planilha}")
        df = pd.read_excel(arquivo_planilha)
        
        if 'Nome' not in df.columns:
            print("❌ Erro: Planilha deve ter uma coluna 'Nome'")
            return
        
        # Limitar ao número de linhas especificado
        df_teste = df.head(num_linhas)
        
        print(f"📊 Total de materiais na planilha: {len(df)}")
        print(f"🎯 Processando: {len(df_teste)} materiais")
        print(f"⚙️  Score mínimo: {min_score}")
        print(f"🔍 Fazer busca real: {'SIM' if fazer_busca else 'NÃO (apenas otimização)'}")
        if arquivo_saida:
            print(f"💾 Salvar resultados em: {arquivo_saida}")
        print()
        
        # Criar buscador
        buscador = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=min_score)
        
        # Lista para coletar resultados (para salvar em Excel)
        resultados = []
        
        # Processar cada linha
        for idx, row in df_teste.iterrows():
            nome_material = str(row['Nome']).strip()
            
            print(f"\n{'='*80}")
            print(f"📋 MATERIAL {idx + 1}/{len(df_teste)}")
            print(f"{'='*80}")
            print(f"📝 ORIGINAL: {nome_material}")
            print()
            
            if fazer_busca:
                # Fazer busca real
                print("🔄 Buscando no Mercado Livre...")
                resultado = buscador.buscar_produtos_material(nome_material)
                
                print(f"✅ OTIMIZADO: {resultado.get('termo_otimizado', 'N/A')}")
                print(f"🔑 PALAVRAS: {', '.join(resultado.get('palavras_chave', []))}")
                print(f"📦 BRUTOS: {resultado.get('total_encontrado', 0)} produtos")
                print(f"🎯 RELEVANTES: {resultado.get('total_relevante', 0)} produtos (score >= {min_score})")
                
                if resultado.get('produtos'):
                    print(f"\n🏆 TOP 3 PRODUTOS RELEVANTES:")
                    for i, p in enumerate(resultado['produtos'][:3], 1):
                        score = p.get('score_relevancia', 0)
                        print(f"   {i}. [{score:.2f}] {p['nome'][:70]}...")
                        print(f"      💰 R$ {p['preco']:.2f}")
                else:
                    print(f"\n❌ Nenhum produto relevante encontrado")
                
                # Coletar dados para salvar
                if arquivo_saida:
                    # Calcular estatísticas
                    stats = resultado.get('estatisticas', {})
                    
                    resultado_linha = {
                        'Nome_Original': nome_material,
                        'Termo_Otimizado': resultado.get('termo_otimizado', ''),
                        'Palavras_Chave': ', '.join(resultado.get('palavras_chave', [])),
                        'Total_Produtos_Encontrados': resultado.get('total_encontrado', 0),
                        'Total_Produtos_Relevantes': resultado.get('total_relevante', 0),
                        'Preco_Minimo': stats.get('preco_minimo') if stats else None,
                        'Preco_Maximo': stats.get('preco_maximo') if stats else None,
                        'Preco_Medio': stats.get('preco_medio') if stats else None,
                        'Preco_Mediana': stats.get('preco_mediana') if stats else None,
                        'Desvio_Padrao': stats.get('desvio_padrao') if stats else None,
                        'Outliers_Removidos': stats.get('outliers_removidos', 0) if stats else 0,
                        'Links_Produtos_JSON': resultado.get('links_produtos', ''),
                        'Status_Busca': resultado.get('status', ''),
                        'Data_Hora_Busca': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    resultados.append(resultado_linha)
                
                # Pausa entre requisições
                if idx < len(df_teste) - 1:
                    print(f"\n⏸️  Aguardando 3 segundos...")
                    import time
                    time.sleep(3)
            else:
                # Apenas otimização (sem buscar)
                otimizacao = buscador.otimizar_termo_busca(nome_material)
                
                print(f"✅ OTIMIZADO: {otimizacao['termo_otimizado']}")
                print(f"�� PALAVRAS: {', '.join(otimizacao['palavras_chave'])}")
                print()
                print("💡 Use --buscar para fazer busca real no Mercado Livre")
                
                # Coletar dados para salvar (apenas otimização)
                if arquivo_saida:
                    resultado_linha = {
                        'Nome_Original': nome_material,
                        'Termo_Otimizado': otimizacao['termo_otimizado'],
                        'Palavras_Chave': ', '.join(otimizacao['palavras_chave']),
                        'Total_Produtos_Encontrados': None,
                        'Total_Produtos_Relevantes': None,
                        'Preco_Minimo': None,
                        'Preco_Maximo': None,
                        'Preco_Medio': None,
                        'Preco_Mediana': None,
                        'Desvio_Padrao': None,
                        'Outliers_Removidos': None,
                        'Links_Produtos_JSON': '',
                        'Status_Busca': 'apenas_otimizacao',
                        'Data_Hora_Busca': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    resultados.append(resultado_linha)
        
        print()
        print("=" * 80)
        print("✅ TESTE CONCLUÍDO!")
        print("=" * 80)
        
        # Salvar resultados em Excel se solicitado
        if arquivo_saida and resultados:
            print()
            print(f"💾 Salvando resultados em: {arquivo_saida}")
            
            df_resultado = pd.DataFrame(resultados)
            df_resultado.to_excel(arquivo_saida, index=False)
            
            print(f"✅ Planilha salva com sucesso!")
            print(f"📊 Total de linhas salvas: {len(resultados)}")
            print(f"📁 Arquivo: {arquivo_saida}")
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{arquivo_planilha}' não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Teste de otimização de busca de preços',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Teste visual (sem planilha)
  python3 teste_otimizacao.py

  # Testar 5 linhas da planilha (apenas otimização)
  python3 teste_otimizacao.py --linhas 5

  # Testar 3 linhas com busca REAL e SALVAR resultados
  python3 teste_otimizacao.py --linhas 3 --buscar --salvar teste_resultados.xlsx

  # Testar 10 linhas com score mínimo 0.4 e salvar
  python3 teste_otimizacao.py --linhas 10 --min-score 0.4 --buscar --salvar resultados.xlsx

  # Testar 5 linhas sem buscar mas salvando otimizações
  python3 teste_otimizacao.py --linhas 5 --salvar otimizacoes.xlsx

  # Especificar arquivo da planilha
  python3 teste_otimizacao.py --linhas 5 --planilha minha_planilha.xlsx --buscar --salvar saida.xlsx
        """
    )
    
    parser.add_argument(
        '--linhas', '-n',
        type=int,
        help='Número de linhas da planilha para processar'
    )
    
    parser.add_argument(
        '--planilha', '-p',
        default='materiais.xlsx',
        help='Arquivo da planilha (padrão: materiais.xlsx)'
    )
    
    parser.add_argument(
        '--min-score', '-s',
        type=float,
        default=0.3,
        help='Score mínimo de relevância 0.0-1.0 (padrão: 0.3)'
    )
    
    parser.add_argument(
        '--buscar', '-b',
        action='store_true',
        help='Fazer busca REAL no Mercado Livre (padrão: apenas otimização)'
    )
    
    parser.add_argument(
        '--salvar', '--saida', '-o',
        dest='arquivo_saida',
        help='Arquivo Excel para salvar resultados (ex: resultados.xlsx)'
    )
    
    args = parser.parse_args()
    
    # Decidir qual teste executar
    if args.linhas:
        # Teste com planilha
        testar_planilha(
            args.planilha,
            args.linhas,
            args.min_score,
            args.buscar,
            args.arquivo_saida
        )
    else:
        # Teste visual padrão
        if args.arquivo_saida:
            print("⚠️  Aviso: --salvar só funciona com --linhas")
            print()
        testar_otimizacao_visual()


if __name__ == "__main__":
    main()
