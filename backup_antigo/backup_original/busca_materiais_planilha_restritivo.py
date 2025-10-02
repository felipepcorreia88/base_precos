#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ULTRA-RESTRITIVO para buscar preços de materiais
EXIGE que TODAS as palavras-chave apareçam no produto
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

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('busca_materiais_restritivo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BuscadorMateriaisRestritivo:
    """Classe ULTRA-RESTRITIVA - EXIGE todas as palavras-chave"""
    
    # Stopwords em português
    STOPWORDS = {
        'a', 'o', 'e', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
        'para', 'com', 'por', 'sobre', 'entre', 'até', 'um', 'uma', 'uns', 'umas',
        'ao', 'aos', 'à', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'este', 'esta',
        'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela',
        'aqueles', 'aquelas', 'que', 'se', 'mais', 'menos', 'muito', 'pouco'
    }
    
    # Palavras genéricas
    PALAVRAS_GENERICAS = {
        'atividades', 'atividade', 'materiais', 'material', 'produtos', 'produto',
        'itens', 'item', 'equipamentos', 'equipamento', 'acessórios', 'acessório',
        'conjunto', 'coleção', 'kit', 'set', 'linha', 'modelo'
    }
    
    def __init__(self, modo_estrito=True, min_palavras_obrigatorias=None):
        """
        Args:
            modo_estrito (bool): Se True, exige TODAS as palavras-chave
            min_palavras_obrigatorias (int): Mínimo de palavras que devem aparecer (None = todas)
        """
        self.base_url = "https://lista.mercadolivre.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.contador_requisicoes = 0
        self.tempo_base = 2
        self.tempo_pausa_longa = 30
        self.modo_estrito = modo_estrito
        self.min_palavras_obrigatorias = min_palavras_obrigatorias
        
    def otimizar_termo_busca(self, termo_original):
        """Otimiza termo de busca removendo partes genéricas"""
        logger.info(f"📝 Otimizando termo: {termo_original}")
        
        # Separa por hífen e pega a parte mais específica
        partes = re.split(r'\s*[-–—]\s*', termo_original)
        
        if len(partes) > 1:
            termo_base = partes[-1].strip()
            logger.info(f"   ✂️  Usando parte após hífen: '{termo_base}'")
        else:
            termo_base = termo_original.strip()
        
        # Extrai palavras e remove stopwords
        palavras = re.findall(r'\b\w+\b', termo_base.lower())
        palavras_importantes = []
        
        for palavra in palavras:
            if len(palavra) >= 3 and palavra not in self.STOPWORDS:
                # Mantém palavras não-genéricas
                if palavra not in self.PALAVRAS_GENERICAS:
                    palavras_importantes.append(palavra)
        
        # Se ficou sem palavras (tudo era genérico), mantém pelo menos 2
        if not palavras_importantes and palavras:
            palavras_importantes = [p for p in palavras if len(p) >= 3][:2]
        
        # Reconstroi termo (máximo 4 palavras)
        palavras_finais = palavras_importantes[:4]
        termo_otimizado = ' '.join(palavras_finais)
        
        logger.info(f"   ✅ Termo otimizado: '{termo_otimizado}'")
        logger.info(f"   🔑 Palavras-chave obrigatórias: {palavras_finais}")
        
        return {
            'termo_otimizado': termo_otimizado,
            'palavras_chave': palavras_finais,
            'termo_original': termo_original
        }
    
    def calcular_score_relevancia(self, nome_produto, palavras_chave):
        """
        MODO RESTRITIVO: Calcula score exigindo TODAS as palavras
        
        Returns:
            float: 1.0 se TODAS palavras aparecem, proporção se parcial
        """
        if not palavras_chave:
            return 0.0
        
        nome_lower = nome_produto.lower()
        palavras_encontradas = 0
        
        for palavra in palavras_chave:
            if palavra in nome_lower:
                palavras_encontradas += 1
        
        # Modo estrito: EXIGE todas as palavras
        if self.modo_estrito:
            if palavras_encontradas == len(palavras_chave):
                return 1.0
            else:
                return 0.0
        
        # Modo flexível: aceita se tem mínimo de palavras
        else:
            min_necessario = self.min_palavras_obrigatorias or len(palavras_chave)
            if palavras_encontradas >= min_necessario:
                return palavras_encontradas / len(palavras_chave)
            else:
                return 0.0
    
    def filtrar_produtos_relevantes(self, produtos, palavras_chave):
        """Filtra produtos - MODO RESTRITIVO"""
        produtos_relevantes = []
        
        for produto in produtos:
            score = self.calcular_score_relevancia(produto['nome'], palavras_chave)
            
            if score > 0:
                produto['score_relevancia'] = score
                produtos_relevantes.append(produto)
        
        # Ordena por relevância
        produtos_relevantes.sort(key=lambda x: x['score_relevancia'], reverse=True)
        
        if self.modo_estrito:
            logger.info(f"   🎯 MODO ESTRITO: {len(produtos)} → {len(produtos_relevantes)} (TODAS palavras)")
        else:
            logger.info(f"   🎯 MODO FLEXÍVEL: {len(produtos)} → {len(produtos_relevantes)}")
        
        return produtos_relevantes
    
    def buscar_produtos_material(self, nome_material):
        """Busca produtos COM MODO RESTRITIVO"""
        logger.info(f"🔍 Buscando: {nome_material}")
        
        try:
            self.aplicar_temporizador()
            
            # Otimizar termo
            otimizacao = self.otimizar_termo_busca(nome_material)
            termo_busca = otimizacao['termo_otimizado']
            palavras_chave = otimizacao['palavras_chave']
            
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
            
            # FILTRO RESTRITIVO
            produtos = self.filtrar_produtos_relevantes(produtos_brutos, palavras_chave)
            
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
                    'palavras_chave': palavras_chave,
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
                    'palavras_chave': palavras_chave,
                    'estatisticas': None,
                    'links_produtos': json.dumps([], ensure_ascii=False),
                    'produtos': [],
                    'status': 'nenhum_produto_relevante'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            return {
                'total_encontrado': 0,
                'total_relevante': 0,
                'status': 'erro_geral',
                'links_produtos': json.dumps([], ensure_ascii=False),
                'produtos': []
            }
    
    def extrair_dados_produto(self, item, nome_material):
        """Extrai dados de um produto"""
        try:
            nome_element = item.find('h2', class_='ui-search-item__title')
            if not nome_element:
                nome_element = item.find('h2')
            if not nome_element:
                nome_element = item.find('h3')
            if not nome_element:
                return None
                
            nome = nome_element.get_text().strip()
            if not nome:
                return None
            
            preco_element = item.find('span', class_='andes-money-amount__fraction')
            if not preco_element:
                return None
                
            preco_texto = preco_element.get_text().strip()
            preco_texto = preco_texto.replace('R$', '').replace('.', '').replace(' ', '').replace(',', '.')
            numeros = re.findall(r'\d+\.?\d*', preco_texto)
            if not numeros:
                return None
                
            preco = float(numeros[0])
            if preco <= 0:
                return None
            
            link_element = item.find('a')
            link = link_element.get('href') if link_element else ''
            
            img_element = item.find('img')
            imagem = ''
            if img_element:
                imagem = img_element.get('data-src') or img_element.get('src', '')
            
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
            
        except Exception as e:
            return None
    
    def calcular_estatisticas(self, produtos):
        """Calcula estatísticas dos preços"""
        if not produtos:
            return None
            
        precos = [p['preco'] for p in produtos if p['preco'] > 0]
        if not precos:
            return None
            
        try:
            mediana = statistics.median(precos)
            desvio_padrao = statistics.stdev(precos) if len(precos) > 1 else 0
            limite_inferior = mediana - desvio_padrao
            limite_superior = mediana + desvio_padrao
            precos_filtrados = [p for p in precos if limite_inferior <= p <= limite_superior]
            
            if not precos_filtrados:
                precos_filtrados = precos
            
            return {
                'quantidade_total': len(precos),
                'quantidade_filtrada': len(precos_filtrados),
                'preco_minimo': min(precos_filtrados),
                'preco_maximo': max(precos_filtrados),
                'preco_medio': statistics.mean(precos_filtrados),
                'preco_mediana': statistics.median(precos_filtrados),
                'desvio_padrao': statistics.stdev(precos_filtrados) if len(precos_filtrados) > 1 else 0,
                'outliers_removidos': len(precos) - len(precos_filtrados)
            }
        except:
            return None
    
    def aplicar_temporizador(self):
        """Aplica temporizador entre requisições"""
        self.contador_requisicoes += 1
        if self.contador_requisicoes % 100 == 0:
            time.sleep(self.tempo_pausa_longa)
        else:
            time.sleep(self.tempo_base)
    
    def processar_planilha(self, arquivo_entrada, arquivo_saida=None):
        """Processa planilha com MODO RESTRITIVO"""
        if arquivo_saida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"materiais_restritivo_{timestamp}.xlsx"
        
        logger.info(f"📖 Lendo planilha: {arquivo_entrada}")
        logger.info(f"🎯 MODO: {'ESTRITO (todas palavras)' if self.modo_estrito else 'FLEXÍVEL'}")
        
        try:
            df = pd.read_excel(arquivo_entrada)
            
            if 'Nome' not in df.columns:
                raise ValueError("Planilha deve ter uma coluna 'Nome'")
            
            logger.info(f"📊 Total de materiais: {len(df)}")
            
            # Criar colunas
            df['Total_Produtos_Encontrados'] = 0
            df['Total_Produtos_Relevantes'] = 0
            df['Termo_Otimizado'] = ''
            df['Palavras_Chave'] = ''
            df['Preco_Minimo'] = None
            df['Preco_Maximo'] = None
            df['Preco_Medio'] = None
            df['Preco_Mediana'] = None
            df['Desvio_Padrao'] = None
            df['Outliers_Removidos'] = 0
            df['Links_Produtos_JSON'] = ''
            df['Status_Busca'] = ''
            df['Data_Hora_Busca'] = ''
            
            total_materiais = len(df)
            
            for idx, row in df.iterrows():
                nome_material = str(row['Nome']).strip()
                logger.info(f"🔄 Processando {idx + 1}/{total_materiais}: {nome_material}")
                
                resultado = self.buscar_produtos_material(nome_material)
                
                df.at[idx, 'Total_Produtos_Encontrados'] = resultado.get('total_encontrado', 0)
                df.at[idx, 'Total_Produtos_Relevantes'] = resultado.get('total_relevante', 0)
                df.at[idx, 'Termo_Otimizado'] = resultado.get('termo_otimizado', '')
                df.at[idx, 'Palavras_Chave'] = ', '.join(resultado.get('palavras_chave', []))
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
                
                if (idx + 1) % 50 == 0:
                    logger.info(f"✅ Progresso: {idx + 1}/{total_materiais}")
            
            logger.info(f"💾 Salvando: {arquivo_saida}")
            df.to_excel(arquivo_saida, index=False)
            logger.info(f"🎉 Concluído!")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            raise

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Buscar preços - MODO RESTRITIVO (exige todas palavras)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
MODO RESTRITIVO:
  ✅ EXIGE que TODAS as palavras-chave apareçam no produto
  ✅ Remove produtos parcialmente relevantes
  ✅ Menos produtos, MAS 100% relevantes

Exemplos:
  # Modo estrito (padrão - TODAS palavras)
  python3 busca_materiais_planilha_restritivo.py

  # Modo flexível (mínimo 2 palavras)
  python3 busca_materiais_planilha_restritivo.py --flexivel --min-palavras 2
        """
    )
    
    parser.add_argument('--entrada', default='materiais.xlsx')
    parser.add_argument('--saida', help='Arquivo de saída')
    parser.add_argument('--flexivel', action='store_true', help='Modo flexível (não exige todas)')
    parser.add_argument('--min-palavras', type=int, help='Mínimo de palavras obrigatórias')
    
    args = parser.parse_args()
    
    logger.info("🚀 MODO RESTRITIVO - Exige TODAS as palavras-chave")
    
    buscador = BuscadorMateriaisRestritivo(
        modo_estrito=not args.flexivel,
        min_palavras_obrigatorias=args.min_palavras
    )
    
    try:
        buscador.processar_planilha(args.entrada, args.saida)
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
