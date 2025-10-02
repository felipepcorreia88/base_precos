#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar preços de materiais da planilha no Mercado Livre
Cria novo dataset com estatísticas e links dos produtos
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
        logging.FileHandler('busca_materiais.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BuscadorMateriaisPlanilha:
    """Classe para buscar preços de materiais da planilha no Mercado Livre"""
    
    def __init__(self):
        self.base_url = "https://lista.mercadolivre.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Contadores para temporizadores
        self.contador_requisicoes = 0
        self.tempo_base = 2  # segundos entre requisições
        self.tempo_pausa_longa = 30  # pausa a cada 100 itens
        
    def buscar_produtos_material(self, nome_material):
        """
        Busca produtos para um material específico no Mercado Livre
        
        Args:
            nome_material (str): Nome do material a ser buscado
            
        Returns:
            dict: Resultado da busca com produtos e estatísticas
        """
        logger.info(f"🔍 Buscando: {nome_material}")
        
        try:
            # Aplicar temporizador
            self.aplicar_temporizador()
            
            # URL de busca
            url = f"{self.base_url}/{quote(nome_material)}"
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            produtos = []
            
            # Encontrar produtos na página
            items = soup.find_all('li', class_='ui-search-layout__item')
            
            if not items:
                # Tentar outro seletor se o primeiro não funcionar
                items = soup.find_all('div', class_='ui-search-result')
            
            for item in items[:20]:  # Limitar a 20 produtos por material
                produto = self.extrair_dados_produto(item, nome_material)
                if produto:
                    produtos.append(produto)
            
            # Calcular estatísticas
            if produtos:
                estatisticas = self.calcular_estatisticas(produtos)
                
                # Criar JSON com links dos produtos
                links_json = json.dumps([
                    {
                        'nome': p['nome'],
                        'preco': p['preco'],
                        'link': p['link']
                    } for p in produtos
                ], ensure_ascii=False, indent=2)
                
                return {
                    'total_encontrado': len(produtos),
                    'estatisticas': estatisticas,
                    'links_produtos': links_json,
                    'produtos': produtos,
                    'status': 'sucesso'
                }
            else:
                logger.warning(f"❌ Nenhum produto encontrado para: {nome_material}")
                return {
                    'total_encontrado': 0,
                    'estatisticas': None,
                    'links_produtos': json.dumps([], ensure_ascii=False),
                    'produtos': [],
                    'status': 'nenhum_produto'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro de requisição para '{nome_material}': {e}")
            return {
                'total_encontrado': 0,
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
                'estatisticas': None,
                'links_produtos': json.dumps([], ensure_ascii=False),
                'produtos': [],
                'status': 'erro_geral',
                'erro': str(e)
            }
    
    def extrair_dados_produto(self, item, nome_material):
        """Extrai dados de um produto específico"""
        try:
            # Nome do produto - nova estrutura HTML
            nome_element = item.find('h3', class_='poly-component__title')
            if not nome_element:
                nome_element = item.find('h2', class_='ui-search-item__title')
            if not nome_element:
                nome_element = item.find('h2')
            if not nome_element:
                nome_element = item.find('h3')
            if not nome_element:
                nome_element = item.find('a', class_='ui-search-item__group__element')
            if not nome_element:
                return None
                
            nome = nome_element.get_text().strip()
            if not nome:
                return None
            
            # Preço - nova estrutura HTML
            preco_element = item.find('span', class_='andes-money-amount__fraction')
            if not preco_element:
                preco_element = item.find('span', class_='price-tag-fraction')
            if not preco_element:
                preco_element = item.find('span', class_='andes-money-amount__cents')
            if not preco_element:
                # Procurar por qualquer span que contenha números
                spans = item.find_all('span')
                for span in spans:
                    texto = span.get_text().strip()
                    if re.search(r'\d+', texto) and ('R$' in texto or re.search(r'\d+\.?\d*', texto)):
                        preco_element = span
                        break
            
            if not preco_element:
                return None
                
            # Extrair preço do texto
            preco_texto = preco_element.get_text().strip()
            # Remover R$, pontos e espaços, substituir vírgula por ponto
            preco_texto = preco_texto.replace('R$', '').replace('.', '').replace(' ', '').replace(',', '.')
            # Encontrar primeiro número
            numeros = re.findall(r'\d+\.?\d*', preco_texto)
            if not numeros:
                return None
                
            preco = float(numeros[0])
            if preco <= 0:
                return None
            
            # Link - nova estrutura HTML
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
            
            # Loja - tentar diferentes seletores
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
            # Aplicar filtro de outliers (mediana ± 1 desvio padrão)
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
            logger.info(f"⏸️ Pausa longa após {self.contador_requisicoes} requisições")
            time.sleep(self.tempo_pausa_longa)
        else:
            time.sleep(self.tempo_base)
    
    def processar_planilha(self, arquivo_entrada, arquivo_saida=None):
        """
        Processa toda a planilha de materiais
        
        Args:
            arquivo_entrada (str): Caminho da planilha de entrada
            arquivo_saida (str): Caminho da planilha de saída (opcional)
        """
        if arquivo_saida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"materiais_com_precos_{timestamp}.xlsx"
        
        logger.info(f"📖 Lendo planilha: {arquivo_entrada}")
        
        try:
            # Ler planilha
            df = pd.read_excel(arquivo_entrada)
            
            # Verificar se tem a coluna 'Nome'
            if 'Nome' not in df.columns:
                raise ValueError("Planilha deve ter uma coluna chamada 'Nome'")
            
            logger.info(f"📊 Total de materiais encontrados: {len(df)}")
            
            # Criar novas colunas
            df['Total_Produtos_Encontrados'] = 0
            df['Preco_Minimo'] = None
            df['Preco_Maximo'] = None
            df['Preco_Medio'] = None
            df['Preco_Mediana'] = None
            df['Desvio_Padrao'] = None
            df['Outliers_Removidos'] = 0
            df['Links_Produtos_JSON'] = ''
            df['Status_Busca'] = ''
            df['Data_Hora_Busca'] = ''
            
            # Processar cada material
            total_materiais = len(df)
            
            for idx, row in df.iterrows():
                nome_material = str(row['Nome']).strip()
                
                logger.info(f"🔄 Processando {idx + 1}/{total_materiais}: {nome_material}")
                
                # Buscar produtos
                resultado = self.buscar_produtos_material(nome_material)
                
                # Preencher dados na planilha
                df.at[idx, 'Total_Produtos_Encontrados'] = resultado['total_encontrado']
                df.at[idx, 'Links_Produtos_JSON'] = resultado['links_produtos']
                df.at[idx, 'Status_Busca'] = resultado['status']
                df.at[idx, 'Data_Hora_Busca'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if resultado['estatisticas']:
                    stats = resultado['estatisticas']
                    df.at[idx, 'Preco_Minimo'] = stats['preco_minimo']
                    df.at[idx, 'Preco_Maximo'] = stats['preco_maximo']
                    df.at[idx, 'Preco_Medio'] = stats['preco_medio']
                    df.at[idx, 'Preco_Mediana'] = stats['preco_mediana']
                    df.at[idx, 'Desvio_Padrao'] = stats['desvio_padrao']
                    df.at[idx, 'Outliers_Removidos'] = stats['outliers_removidos']
                
                # Log de progresso a cada 50 itens
                if (idx + 1) % 50 == 0:
                    logger.info(f"✅ Progresso: {idx + 1}/{total_materiais} materiais processados")
            
            # Salvar planilha
            logger.info(f"💾 Salvando planilha: {arquivo_saida}")
            df.to_excel(arquivo_saida, index=False)
            
            logger.info(f"🎉 Processamento concluído!")
            logger.info(f"📁 Arquivo salvo: {arquivo_saida}")
            logger.info(f"📊 Total de requisições feitas: {self.contador_requisicoes}")
            
            # Estatísticas finais
            sucessos = len(df[df['Status_Busca'] == 'sucesso'])
            erros = len(df[df['Status_Busca'].str.contains('erro', na=False)])
            sem_produtos = len(df[df['Status_Busca'] == 'nenhum_produto'])
            
            logger.info(f"📈 Resumo final:")
            logger.info(f"   ✅ Sucessos: {sucessos}")
            logger.info(f"   ❌ Erros: {erros}")
            logger.info(f"   🔍 Sem produtos: {sem_produtos}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar planilha: {e}")
            raise

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Buscar preços de materiais no Mercado Livre')
    parser.add_argument('--entrada', default='materiais.xlsx', help='Arquivo de entrada (padrão: materiais.xlsx)')
    parser.add_argument('--saida', help='Arquivo de saída (opcional)')
    parser.add_argument('--inicio', type=int, default=0, help='Índice de início (para retomar processamento)')
    parser.add_argument('--fim', type=int, help='Índice de fim (opcional)')
    
    args = parser.parse_args()
    
    logger.info("🚀 Iniciando busca de preços de materiais")
    logger.info(f"📖 Arquivo de entrada: {args.entrada}")
    logger.info(f"📁 Arquivo de saída: {args.saida or 'auto-gerado'}")
    
    buscador = BuscadorMateriaisPlanilha()
    
    try:
        buscador.processar_planilha(args.entrada, args.saida)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
