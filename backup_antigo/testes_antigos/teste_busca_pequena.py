#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para buscar apenas alguns materiais
Útil para testar o sistema antes de processar toda a planilha
"""

import pandas as pd
from busca_materiais_planilha import BuscadorMateriaisPlanilha
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def teste_pequeno(quantidade=5):
    """Testa o sistema com apenas alguns materiais"""
    
    logger.info(f"🧪 Iniciando teste com {quantidade} materiais")
    
    # Ler planilha
    df = pd.read_excel('materiais.xlsx')
    
    # Pegar apenas os primeiros N materiais
    df_teste = df.head(quantidade).copy()
    
    logger.info(f"📋 Materiais para teste:")
    for idx, row in df_teste.iterrows():
        logger.info(f"   {idx + 1}. {row['Nome']}")
    
    # Criar buscador
    buscador = BuscadorMateriaisPlanilha()
    
    # Criar novas colunas
    df_teste['Total_Produtos_Encontrados'] = 0
    df_teste['Preco_Minimo'] = None
    df_teste['Preco_Maximo'] = None
    df_teste['Preco_Medio'] = None
    df_teste['Preco_Mediana'] = None
    df_teste['Desvio_Padrao'] = None
    df_teste['Outliers_Removidos'] = 0
    df_teste['Links_Produtos_JSON'] = ''
    df_teste['Status_Busca'] = ''
    df_teste['Data_Hora_Busca'] = ''
    
    # Processar cada material
    for idx, row in df_teste.iterrows():
        nome_material = str(row['Nome']).strip()
        logger.info(f"🔍 Testando: {nome_material}")
        
        resultado = buscador.buscar_produtos_material(nome_material)
        
        # Preencher dados
        df_teste.at[idx, 'Total_Produtos_Encontrados'] = resultado['total_encontrado']
        df_teste.at[idx, 'Links_Produtos_JSON'] = resultado['links_produtos']
        df_teste.at[idx, 'Status_Busca'] = resultado['status']
        df_teste.at[idx, 'Data_Hora_Busca'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if resultado['estatisticas']:
            stats = resultado['estatisticas']
            df_teste.at[idx, 'Preco_Minimo'] = stats['preco_minimo']
            df_teste.at[idx, 'Preco_Maximo'] = stats['preco_maximo']
            df_teste.at[idx, 'Preco_Medio'] = stats['preco_medio']
            df_teste.at[idx, 'Preco_Mediana'] = stats['preco_mediana']
            df_teste.at[idx, 'Desvio_Padrao'] = stats['desvio_padrao']
            df_teste.at[idx, 'Outliers_Removidos'] = stats['outliers_removidos']
        
        logger.info(f"   ✅ Status: {resultado['status']}")
        if resultado['estatisticas']:
            logger.info(f"   📊 Produtos: {resultado['total_encontrado']}")
            logger.info(f"   💰 Preço médio: R$ {resultado['estatisticas']['preco_medio']:.2f}")
    
    # Salvar resultado do teste
    arquivo_teste = 'teste_materiais_precos.xlsx'
    df_teste.to_excel(arquivo_teste, index=False)
    
    logger.info(f"💾 Teste salvo em: {arquivo_teste}")
    logger.info("🎉 Teste concluído!")
    
    return df_teste

if __name__ == "__main__":
    import sys
    
    quantidade = 3
    if len(sys.argv) > 1:
        quantidade = int(sys.argv[1])
    
    teste_pequeno(quantidade)
