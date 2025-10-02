#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script OTIMIZADO para buscar preços de materiais da planilha no Mercado Livre
Com melhorias significativas na relevância dos resultados
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
        logging.FileHandler('busca_materiais_otimizado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BuscadorMateriaisPlanilhaOtimizado:
    """Classe OTIMIZADA para buscar preços com maior relevância"""
    
    # Stopwords em português (palavras a serem removidas)
    STOPWORDS = {
        'a', 'o', 'e', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
        'para', 'com', 'por', 'sobre', 'entre', 'até', 'um', 'uma', 'uns', 'umas',
        'ao', 'aos', 'à', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'este', 'esta',
        'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela',
        'aqueles', 'aquelas', 'que', 'se', 'mais', 'menos', 'muito', 'pouco'
    }
    
    # Palavras genéricas que podem ser removidas
    PALAVRAS_GENERICAS = {
        'atividades', 'atividade', 'materiais', 'material', 'produtos', 'produto',
        'itens', 'item', 'equipamentos', 'equipamento', 'acessórios', 'acessório',
        'conjunto', 'coleção'
    }
    
    def __init__(self, min_score_relevancia=0.3):
        self.base_url = "https://lista.mercadolivre.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Contadores para temporizadores
        self.contador_requisicoes = 0
        self.tempo_base = 2
        self.tempo_pausa_longa = 30
        
        # Score mínimo de relevância (0.0 a 1.0)
        self.min_score_relevancia = min_score_relevancia
        
    def otimizar_termo_busca(self, termo_original):
        """
        Otimiza o termo de busca para melhor relevância
        
        Estratégia:
        1. Prioriza conteúdo após hífen/traço (mais específico)
        2. Remove stopwords e palavras genéricas
        3. Mantém palavras-chave importantes
        4. Limita tamanho do termo
        
        Args:
            termo_original (str): Termo original da planilha
            
        Returns:
            dict: {
                'termo_otimizado': str,
                'palavras_chave': list,
                'termo_original': str
            }
        """
        logger.info(f"📝 Otimizando termo: {termo_original}")
        
        # 1. Separa por hífen e pega a parte mais específica
        partes = re.split(r'\s*[-–—]\s*', termo_original)
        
        # Se tem hífen, prioriza a última parte (mais específica)
        if len(partes) > 1:
            termo_base = partes[-1].strip()
            logger.info(f"   ✂️  Usando parte após hífen: '{termo_base}'")
        else:
            termo_base = termo_original.strip()
        
        # 2. Extrai palavras e remove stopwords
        palavras = re.findall(r'\b\w+\b', termo_base.lower())
        
        # Remove stopwords mas mantém palavras importantes
        palavras_importantes = []
        for palavra in palavras:
            # Mantém palavras com 3+ caracteres que não são stopwords
            if len(palavra) >= 3 and palavra not in self.STOPWORDS:
                # Remove algumas genéricas mas mantém se for importante
                if palavra not in self.PALAVRAS_GENERICAS or len(palavras_importantes) < 2:
                    palavras_importantes.append(palavra)
        
        # 3. Reconstroi termo otimizado (máximo 5 palavras mais importantes)
        palavras_finais = palavras_importantes[:5]
        termo_otimizado = ' '.join(palavras_finais)
        
        logger.info(f"   ✅ Termo otimizado: '{termo_otimizado}'")
        logger.info(f"   🔑 Palavras-chave: {palavras_finais}")
        
        return {
            'termo_otimizado': termo_otimizado,
            'palavras_chave': palavras_finais,
            'termo_original': termo_original
        }
    
    def calcular_score_relevancia(self, nome_produto, palavras_chave):
        """
        Calcula score de relevância do produto (0.0 a 1.0)
        
        Score baseado em:
        - Quantas palavras-chave aparecem no nome do produto
        - Ordem das palavras
        
        Args:
            nome_produto (str): Nome do produto encontrado
            palavras_chave (list): Lista de palavras-chave da busca
            
        Returns:
            float: Score de 0.0 (irrelevante) a 1.0 (muito relevante)
        """
        if not palavras_chave:
            return 0.0
        
        nome_lower = nome_produto.lower()
        palavras_encontradas = 0
        score_ordem = 0
        
        for i, palavra in enumerate(palavras_chave):
            if palavra in nome_lower:
                palavras_encontradas += 1
                # Bonus se aparecer na ordem correta
                if i == 0 or palavras_chave[i-1] in nome_lower:
                    score_ordem += 0.1
        
        # Score base: proporção de palavras encontradas
        score_base = palavras_encontradas / len(palavras_chave)
        
        # Bonus por ordem (até 0.2)
        score_final = min(1.0, score_base + score_ordem)
        
        return score_final
    
    def filtrar_produtos_relevantes(self, produtos, palavras_chave):
        """
        Filtra produtos mantendo apenas os relevantes
        
        Args:
            produtos (list): Lista de produtos encontrados
            palavras_chave (list): Palavras-chave da busca
            
        Returns:
            list: Produtos filtrados com score >= min_score_relevancia
        """
        produtos_relevantes = []
        
        for produto in produtos:
            score = self.calcular_score_relevancia(produto['nome'], palavras_chave)
            
            if score >= self.min_score_relevancia:
                produto['score_relevancia'] = score
                produtos_relevantes.append(produto)
        
        # Ordena por relevância (maior score primeiro)
        produtos_relevantes.sort(key=lambda x: x['score_relevancia'], reverse=True)
        
        logger.info(f"   🎯 Produtos filtrados: {len(produtos)} → {len(produtos_relevantes)} (score >= {self.min_score_relevancia})")
        
        return produtos_relevantes
    
    def buscar_produtos_material(self, nome_material):
        """
        Busca produtos para um material específico no Mercado Livre
        COM OTIMIZAÇÃO DE RELEVÂNCIA
        """
        logger.info(f"🔍 Buscando: {nome_material}")
        
        try:
            # Aplicar temporizador
            self.aplicar_temporizador()
            
            # OTIMIZAR TERMO DE BUSCA
            otimizacao = self.otimizar_termo_busca(nome_material)
            termo_busca = otimizacao['termo_otimizado']
            palavras_chave = otimizacao['palavras_chave']
            
            # URL de busca com termo otimizado
            url = f"{self.base_url}/{quote(termo_busca)}"
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            produtos_brutos = []
            
            # Encontrar produtos na página
            items = soup.find_all('li', class_='ui-search-layout__item')
            
            if not items:
                items = soup.find_all('div', class_='ui-search-result')
            
            for item in items[:30]:  # Busca mais produtos para depois filtrar
                produto = self.extrair_dados_produto(item, nome_material)
                if produto:
                    produtos_brutos.append(produto)
            
            logger.info(f"   📦 Produtos brutos encontrados: {len(produtos_brutos)}")
            
            # FILTRAR POR RELEVÂNCIA
            produtos = self.filtrar_produtos_relevantes(produtos_brutos, palavras_chave)
            
            # Log dos produtos filtrados
            if produtos:
                logger.info(f"   🏆 Top 3 produtos mais relevantes:")
                for i, p in enumerate(produtos[:3], 1):
                    logger.info(f"      {i}. [{p['score_relevancia']:.2f}] {p['nome'][:60]}...")
            
            # Calcular estatísticas
            if produtos:
                estatisticas = self.calcular_estatisticas(produtos)
                
                # Criar JSON com links dos produtos
                links_json = json.dumps([
                    {
                        'nome': p['nome'],
                        'preco': p['preco'],
                        'link': p['link'],
                        'score_relevancia': round(p.get('score_relevancia', 0), 2)
                    } for p in produtos
                ], ensure_ascii=False, indent=2)
                
                return {
                    'total_encontrado': len(produtos_brutos),
                    'total_relevante': len(produtos),
                    'termo_original': nome_material,
                    'termo_otimizado': termo_busca,
                    'palavras_chave': palavras_chave,
                    'estatisticas': estatisticas,
                    'links_produtos': links_json,
                    'produtos': produtos,
                    'status': 'sucesso'
                }
            else:
                logger.warning(f"❌ Nenhum produto relevante para: {nome_material}")
                return {
                    'total_encontrado': len(produtos_brutos),
                    'total_relevante': 0,
                    'termo_original': nome_material,
                    'termo_otimizado': termo_busca,
                    'palavras_chave': palavras_chave,
                    'estatisticas': None,
                    'links_produtos': json.dumps([], ensure_ascii=False),
                    'produtos': [],
                    'status': 'nenhum_produto_relevante'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro de requisição para '{nome_material}': {e}")
            return {
                'total_encontrado': 0,
                'total_relevante': 0,
                'termo_original': nome_material,
                'estatisticas': None,
                'links_produtos': json.dumps([], ensure_ascii=False),
                'produtos': [],
                'status': 'erro_requisicao',
                'erro': str(e)
            }
        except Exception as e:
            logger.error(f"❌ Erro geral para '{nome_material}': {e}")
            return {
                'total_encontrado': 0,
                'total_relevante': 0,
                'termo_original': nome_material,
                'estatisticas': None,
                'links_produtos': json.dumps([], ensure_ascii=False),
                'produtos': [],
                'status': 'erro_geral',
                'erro': str(e)
            }
    
    def extrair_dados_produto(self, item, nome_material):
        """Extrai dados de um produto específico"""
        try:
            # Nome do produto
            nome_element = item.find('h3', class_='poly-component__title')
            if not nome_element:
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
            
            # Preço
            preco_element = item.find('span', class_='andes-money-amount__fraction')
            if not preco_element:
                preco_element = item.find('span', class_='price-tag-fraction')
            if not preco_element:
                spans = item.find_all('span')
                for span in spans:
                    texto = span.get_text().strip()
                    if re.search(r'\d+', texto) and ('R$' in texto or re.search(r'\d+\.?\d*', texto)):
                        preco_element = span
                        break
            
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
            
            # Link
            link_element = item.find('a', class_='poly-component__title')
            if not link_element:
                link_element = item.find('a', class_='ui-search-link')
            if not link_element:
                link_element = item.find('a')
            
            link = link_element.get('href') if link_element else ''
            
            # Imagem
            img_element = item.find('img')
            imagem = ''
            if img_element:
                imagem = img_element.get('data-src') or img_element.get('src', '')
            
            # Loja
            loja_element = item.find('p', class_='ui-search-official-store-item__subtitle')
            if not loja_element:
                loja_element = item.find('span', class_='ui-search-item__group__element')
            if not loja_element:
                loja_element = item.find('p', class_='ui-search-item__location')
            
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
            logger.debug(f"Erro ao extrair produto: {e}")
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
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return None
    
    def aplicar_temporizador(self):
        """Aplica temporizador entre requisições"""
        self.contador_requisicoes += 1
        
        if self.contador_requisicoes % 100 == 0:
            logger.info(f"⏸️  Pausa longa após {self.contador_requisicoes} requisições")
            time.sleep(self.tempo_pausa_longa)
        else:
            time.sleep(self.tempo_base)
    
    def processar_planilha(self, arquivo_entrada, arquivo_saida=None):
        """Processa toda a planilha de materiais COM OTIMIZAÇÃO"""
        if arquivo_saida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"materiais_com_precos_otimizado_{timestamp}.xlsx"
        
        logger.info(f"📖 Lendo planilha: {arquivo_entrada}")
        
        try:
            df = pd.read_excel(arquivo_entrada)
            
            if 'Nome' not in df.columns:
                raise ValueError("Planilha deve ter uma coluna chamada 'Nome'")
            
            logger.info(f"📊 Total de materiais encontrados: {len(df)}")
            
            # Criar novas colunas
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
                
                # Buscar produtos (COM OTIMIZAÇÃO)
                resultado = self.buscar_produtos_material(nome_material)
                
                # Preencher dados na planilha
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
                    logger.info(f"✅ Progresso: {idx + 1}/{total_materiais} materiais processados")
            
            logger.info(f"💾 Salvando planilha: {arquivo_saida}")
            df.to_excel(arquivo_saida, index=False)
            
            logger.info(f"🎉 Processamento concluído!")
            logger.info(f"📁 Arquivo salvo: {arquivo_saida}")
            
            sucessos = len(df[df['Status_Busca'] == 'sucesso'])
            erros = len(df[df['Status_Busca'].str.contains('erro', na=False)])
            sem_produtos = len(df[df['Status_Busca'] == 'nenhum_produto_relevante'])
            
            logger.info(f"📈 Resumo final:")
            logger.info(f"   ✅ Sucessos: {sucessos}")
            logger.info(f"   ❌ Erros: {erros}")
            logger.info(f"   🔍 Sem produtos relevantes: {sem_produtos}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar planilha: {e}")
            raise

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Buscar preços de materiais no Mercado Livre (VERSÃO OTIMIZADA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Melhorias desta versão:
  ✅ Otimização automática de termos de busca
  ✅ Remoção de stopwords e palavras genéricas
  ✅ Priorização de conteúdo após hífen (mais específico)
  ✅ Filtro de relevância por score (0.0 a 1.0)
  ✅ Produtos ordenados por relevância
  ✅ Novas colunas: Termo_Otimizado, Palavras_Chave, Total_Produtos_Relevantes

Exemplo de uso:
  python3 busca_materiais_planilha_otimizado.py
  python3 busca_materiais_planilha_otimizado.py --entrada materiais.xlsx
  python3 busca_materiais_planilha_otimizado.py --min-score 0.4
        """
    )
    
    parser.add_argument('--entrada', default='materiais.xlsx', help='Arquivo de entrada (padrão: materiais.xlsx)')
    parser.add_argument('--saida', help='Arquivo de saída (opcional)')
    parser.add_argument('--min-score', type=float, default=0.3, help='Score mínimo de relevância 0.0-1.0 (padrão: 0.3)')
    
    args = parser.parse_args()
    
    logger.info("🚀 Iniciando busca de preços de materiais (VERSÃO OTIMIZADA)")
    logger.info(f"📖 Arquivo de entrada: {args.entrada}")
    logger.info(f"🎯 Score mínimo de relevância: {args.min_score}")
    
    buscador = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=args.min_score)
    
    try:
        buscador.processar_planilha(args.entrada, args.saida)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
