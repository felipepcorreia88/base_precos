#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de busca de preços com FILTRO FLEXÍVEL
Confia no mecanismo de busca do Mercado Livre
Pontua produtos por relevância (não elimina)
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import statistics
import time
import re
from urllib.parse import quote
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/logs/busca_materiais_inteligente.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BuscadorInteligente:
    """Busca flexível que confia no algoritmo do Mercado Livre"""
    
    STOPWORDS = {
        'a', 'o', 'e', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
        'para', 'com', 'por', 'sobre', 'entre', 'até', 'um', 'uma', 'uns', 'umas'
    }
    
    # Palavras GENÉRICAS (podem estar ausentes)
    PALAVRAS_GENERICAS = {
        'kit', 'conjunto', 'set', 'pack', 'combo',
        'atividades', 'materiais', 'produtos', 'itens', 'equipamentos',
        'linha', 'modelo', 'serie', 'colecao'
    }
    
    def __init__(self):
        self.base_url = "https://lista.mercadolivre.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.contador_requisicoes = 0
        self.tempo_base = 2
        self.tempo_pausa_longa = 30
        
    def otimizar_termo_busca(self, termo_original):
        """Otimiza termo identificando palavras importantes para pontuação"""
        logger.info(f"📝 Otimizando: {termo_original}")
        
        # USA O TERMO COMPLETO (incluindo modalidade)
        termo_base = termo_original.strip()
        
        logger.info(f"   ✅ Usando termo completo: '{termo_base}'")
        
        # Extrai palavras
        palavras = re.findall(r'\b\w+\b', termo_base.lower())
        
        # Classifica palavras
        palavras_obrigatorias = []
        palavras_opcionais = []
        
        for palavra in palavras:
            if len(palavra) >= 3 and palavra not in self.STOPWORDS:
                if palavra in self.PALAVRAS_GENERICAS:
                    palavras_opcionais.append(palavra)
                else:
                    # Palavras ESPECÍFICAS são OBRIGATÓRIAS
                    palavras_obrigatorias.append(palavra)
        
        # Se não tem obrigatórias, usa todas
        if not palavras_obrigatorias:
            palavras_obrigatorias = palavras_opcionais[:3]
            palavras_opcionais = []
        
        todas_palavras = palavras_obrigatorias + palavras_opcionais
        termo_otimizado = ' '.join(todas_palavras[:5])
        
        logger.info(f"   ✅ Termo: '{termo_otimizado}'")
        logger.info(f"   🔵 IMPORTANTES: {palavras_obrigatorias}")
        logger.info(f"   🟡 SECUNDÁRIAS: {palavras_opcionais}")
        
        return {
            'termo_otimizado': termo_otimizado,
            'palavras_obrigatorias': palavras_obrigatorias,
            'palavras_opcionais': palavras_opcionais,
            'todas_palavras': todas_palavras,
            'termo_original': termo_original
        }
    
    def calcular_score_relevancia(self, nome_produto, palavras_obrigatorias, palavras_opcionais):
        """
        Calcula score FLEXÍVEL confiando no mecanismo do Mercado Livre
        
        NOVA REGRA: Aceita produtos do ML, apenas pontua pela relevância
        - Mais palavras importantes = score maior
        - Não elimina nenhum produto
        """
        nome_lower = nome_produto.lower()
        
        # Conta palavras importantes encontradas
        todas_palavras = palavras_obrigatorias + palavras_opcionais
        if not todas_palavras:
            return 0.5  # Score neutro se não tem palavras
        
        palavras_encontradas = sum(1 for p in todas_palavras if p in nome_lower)
        
        # Score proporcional: quanto mais palavras, maior o score
        # Mínimo 0.3 (produto está na busca do ML, então é algo relevante)
        # Máximo 1.0 (tem todas as palavras)
        score = 0.3 + (0.7 * palavras_encontradas / len(todas_palavras))
        
        return min(1.0, score)
    
    def filtrar_produtos_relevantes(self, produtos, palavras_obrigatorias, palavras_opcionais):
        """
        Pontua produtos confiando no mecanismo de busca do Mercado Livre
        NOVA ABORDAGEM: Não elimina produtos, apenas ordena por relevância
        """
        produtos_pontuados = []
        
        for produto in produtos:
            score = self.calcular_score_relevancia(
                produto['nome'],
                palavras_obrigatorias,
                palavras_opcionais
            )
            
            produto['score_relevancia'] = score
            produtos_pontuados.append(produto)
        
        # Ordena por score (mas mantém todos)
        produtos_pontuados.sort(key=lambda x: x['score_relevancia'], reverse=True)
        
        logger.info(f"   🎯 FILTRO FLEXÍVEL: {len(produtos)} produtos (todos mantidos, ordenados por relevância)")
        logger.info(f"      Palavras buscadas: {palavras_obrigatorias + palavras_opcionais}")
        
        return produtos_pontuados
    
    def buscar_produtos_material(self, nome_material):
        """Busca produtos usando mecanismo do ML e pontua por relevância"""
        logger.info(f"🔍 Buscando: {nome_material}")
        
        try:
            self.aplicar_temporizador()
            
            otimizacao = self.otimizar_termo_busca(nome_material)
            termo_busca = otimizacao['termo_otimizado']
            palavras_obrigatorias = otimizacao['palavras_obrigatorias']
            palavras_opcionais = otimizacao['palavras_opcionais']
            
            url = f"{self.base_url}/{quote(termo_busca)}"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            produtos_brutos = []
            
            items = soup.find_all('li', class_='ui-search-layout__item')[:40]
            
            for item in items:
                produto = self.extrair_dados_produto(item, nome_material)
                if produto:
                    produtos_brutos.append(produto)
            
            logger.info(f"   📦 Produtos brutos: {len(produtos_brutos)}")
            
            # PONTUAÇÃO POR RELEVÂNCIA
            produtos = self.filtrar_produtos_relevantes(
                produtos_brutos,
                palavras_obrigatorias,
                palavras_opcionais
            )
            
            if produtos:
                logger.info(f"   🏆 Top 3:")
                for i, p in enumerate(produtos[:3], 1):
                    logger.info(f"      {i}. [{p['score_relevancia']:.2f}] {p['nome'][:60]}...")
            
            if produtos:
                estatisticas = self.calcular_estatisticas(produtos)
                links_json = json.dumps([
                    {'nome': p['nome'], 'preco': p['preco'], 'link': p['link'],
                     'score_relevancia': round(p.get('score_relevancia', 0), 2)}
                    for p in produtos
                ], ensure_ascii=False, indent=2)
                
                return {
                    'total_encontrado': len(produtos_brutos),
                    'total_relevante': len(produtos),
                    'termo_otimizado': termo_busca,
                    'palavras_obrigatorias': palavras_obrigatorias,
                    'palavras_opcionais': palavras_opcionais,
                    'estatisticas': estatisticas,
                    'links_produtos': links_json,
                    'produtos': produtos,
                    'status': 'sucesso'
                }
            else:
                return {
                    'total_encontrado': len(produtos_brutos),
                    'total_relevante': 0,
                    'termo_otimizado': termo_busca,
                    'estatisticas': None,
                    'links_produtos': json.dumps([], ensure_ascii=False),
                    'produtos': [],
                    'status': 'nenhum_produto_relevante'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            return {'total_encontrado': 0, 'status': 'erro', 'links_produtos': '[]', 'produtos': []}
    
    def extrair_dados_produto(self, item, nome_material):
        """Extrai dados do produto"""
        try:
            nome_element = item.find('h2', class_='ui-search-item__title')
            if not nome_element:
                nome_element = item.find('h2') or item.find('h3')
            if not nome_element:
                return None
            nome = nome_element.get_text().strip()
            if not nome:
                return None
            
            preco_element = item.find('span', class_='andes-money-amount__fraction')
            if not preco_element:
                return None
            preco_texto = preco_element.get_text().strip().replace('.', '').replace(',', '.')
            numeros = re.findall(r'\d+\.?\d*', preco_texto)
            if not numeros:
                return None
            preco = float(numeros[0])
            if preco <= 0:
                return None
            
            link_element = item.find('a')
            link = link_element.get('href') if link_element else ''
            
            img_element = item.find('img')
            imagem = img_element.get('data-src') or img_element.get('src', '') if img_element else ''
            
            loja_element = item.find('p', class_='ui-search-official-store-item__subtitle')
            loja = loja_element.get_text().strip() if loja_element else "Vendedor não identificado"
            
            return {
                'nome': nome,
                'preco': preco,
                'link': link,
                'imagem': imagem,
                'loja': loja,
                'material_buscado': nome_material
            }
        except:
            return None
    
    def calcular_estatisticas(self, produtos):
        """Calcula estatísticas"""
        if not produtos:
            return None
        precos = [p['preco'] for p in produtos if p['preco'] > 0]
        if not precos:
            return None
        try:
            mediana = statistics.median(precos)
            desvio = statistics.stdev(precos) if len(precos) > 1 else 0
            lim_inf = mediana - desvio
            lim_sup = mediana + desvio
            precos_filt = [p for p in precos if lim_inf <= p <= lim_sup]
            if not precos_filt:
                precos_filt = precos
            return {
                'quantidade_total': len(precos),
                'quantidade_filtrada': len(precos_filt),
                'preco_minimo': min(precos_filt),
                'preco_maximo': max(precos_filt),
                'preco_medio': statistics.mean(precos_filt),
                'preco_mediana': statistics.median(precos_filt),
                'desvio_padrao': statistics.stdev(precos_filt) if len(precos_filt) > 1 else 0,
                'outliers_removidos': len(precos) - len(precos_filt)
            }
        except:
            return None
    
    def aplicar_temporizador(self):
        """Temporizador"""
        self.contador_requisicoes += 1
        if self.contador_requisicoes % 100 == 0:
            time.sleep(self.tempo_pausa_longa)
        else:
            time.sleep(self.tempo_base)
    
    def processar_planilha(self, arquivo_entrada, arquivo_saida=None):
        """Processa planilha com FILTRO FLEXÍVEL"""
        if arquivo_saida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"materiais_flexivel_{timestamp}.xlsx"
        
        logger.info(f"📖 Lendo: {arquivo_entrada}")
        logger.info(f"🎯 MODO FLEXÍVEL: Confia no mecanismo do Mercado Livre")
        
        try:
            df = pd.read_excel(arquivo_entrada)
            if 'Nome' not in df.columns:
                raise ValueError("Planilha deve ter 'Nome'")
            
            df['Total_Produtos_Encontrados'] = 0
            df['Total_Produtos_Relevantes'] = 0
            df['Termo_Otimizado'] = ''
            df['Palavras_Obrigatorias'] = ''
            df['Palavras_Opcionais'] = ''
            df['Preco_Minimo'] = None
            df['Preco_Maximo'] = None
            df['Preco_Medio'] = None
            df['Preco_Mediana'] = None
            df['Desvio_Padrao'] = None
            df['Outliers_Removidos'] = 0
            df['Links_Produtos_JSON'] = ''
            df['Status_Busca'] = ''
            df['Data_Hora_Busca'] = ''
            
            for idx, row in df.iterrows():
                nome_material = str(row['Nome']).strip()
                logger.info(f"🔄 {idx + 1}/{len(df)}: {nome_material}")
                
                resultado = self.buscar_produtos_material(nome_material)
                
                df.at[idx, 'Total_Produtos_Encontrados'] = resultado.get('total_encontrado', 0)
                df.at[idx, 'Total_Produtos_Relevantes'] = resultado.get('total_relevante', 0)
                df.at[idx, 'Termo_Otimizado'] = resultado.get('termo_otimizado', '')
                df.at[idx, 'Palavras_Obrigatorias'] = ', '.join(resultado.get('palavras_obrigatorias', []))
                df.at[idx, 'Palavras_Opcionais'] = ', '.join(resultado.get('palavras_opcionais', []))
                df.at[idx, 'Links_Produtos_JSON'] = resultado['links_produtos']
                df.at[idx, 'Status_Busca'] = resultado['status']
                df.at[idx, 'Data_Hora_Busca'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if resultado.get('estatisticas'):
                    stats = resultado['estatisticas']
                    df.at[idx, 'Preco_Minimo'] = stats['preco_minimo']
                    df.at[idx, 'Preco_Maximo'] = stats['preco_maximo']
                    df.at[idx, 'Preco_Medio'] = stats['preco_medio']
                    df.at[idx, 'Preco_Mediana'] = stats['preco_mediana']
                    df.at[idx, 'Desvio_Padrao'] = stats['desvio_padrao']
                    df.at[idx, 'Outliers_Removidos'] = stats['outliers_removidos']
            
            logger.info(f"💾 Salvando: {arquivo_saida}")
            df.to_excel(arquivo_saida, index=False)
            logger.info(f"🎉 Concluído!")
            return df
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            raise

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Busca FLEXÍVEL - confia no mecanismo do Mercado Livre',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
FILTRO FLEXÍVEL:
  ✅ Confia no mecanismo de busca do Mercado Livre
  ✅ Mantém TODOS os produtos retornados
  ✅ Pontua por relevância (mais palavras = score maior)
  ✅ Ordena do mais relevante ao menos relevante

Exemplo:
  Termo: "Kit Bolas Suíças PCD"
  Palavras importantes: suíças, pcd, bolas
  
  Resultado:
  ✅ "Bola Suíça 65cm PCD" (score 1.0 - tem todas)
  ✅ "Kit Bolas Suíça Profissional" (score 0.8 - tem 2 de 3)
  ✅ "Bola Pilates PCD" (score 0.5 - tem 1 de 3)
  ✅ "Kit Fitness" (score 0.3 - ML achou relevante)

Uso:
  python3 busca_materiais_planilha_inteligente.py
        """
    )
    parser.add_argument('--entrada', default='materiais.xlsx')
    parser.add_argument('--saida', help='Arquivo de saída')
    args = parser.parse_args()
    
    logger.info("🚀 MODO FLEXÍVEL - Confia no Mercado Livre")
    buscador = BuscadorInteligente()
    
    try:
        buscador.processar_planilha(args.entrada, args.saida)
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
