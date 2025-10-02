#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador de preços no Mercado Livre
Busca produtos e retorna JSON com estatísticas de preços
"""

import requests
from bs4 import BeautifulSoup
import json
import statistics
import re
import time
import argparse
from urllib.parse import quote


class BuscadorMercadoLivre:
    """Classe para buscar produtos no Mercado Livre"""
    
    def __init__(self):
        self.base_url = "https://lista.mercadolivre.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.max_paginas = 3
    
    def buscar_produtos(self, termo_busca):
        """
        Busca produtos no Mercado Livre
        
        Args:
            termo_busca (str): Termo de busca
            
        Returns:
            dict: Dicionário com produtos e estatísticas
        """
        print(f"🔍 Buscando produtos para: '{termo_busca}'")
        
        produtos = []
        
        # Busca apenas na primeira página (melhores resultados do ML)
        url = f"{self.base_url}/{quote(termo_busca)}"
        print(f"📄 Buscando primeira página (melhores resultados do Mercado Livre)...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            produtos = self._extrair_produtos_pagina(soup)
            
            if not produtos:
                print(f"   ❌ Nenhum produto encontrado")
                return {
                    'produtos': [],
                    'estatisticas': None,
                    'termo': termo_busca,
                    'total_encontrado': 0,
                    'total_filtrado': 0
                }
            
            print(f"   ✅ {len(produtos)} produtos encontrados na primeira página")
            
        except requests.RequestException as e:
            print(f"   ❌ Erro ao buscar: {e}")
            return {
                'produtos': [],
                'estatisticas': None,
                'termo': termo_busca,
                'total_encontrado': 0,
                'total_filtrado': 0
            }
        
        # Aplica filtro de outliers (mediana ± 1 desvio padrão)
        produtos_filtrados = self._filtrar_outliers(produtos)
        
        print(f"🎯 Produtos encontrados: {len(produtos)}")
        print(f"🎯 Produtos após filtro de outliers: {len(produtos_filtrados)}")
        
        # Calcula estatísticas dos produtos filtrados
        estatisticas = self._calcular_estatisticas(produtos_filtrados)
        
        return {
            'produtos': produtos_filtrados,
            'estatisticas': estatisticas,
            'termo': termo_busca,
            'total_encontrado': len(produtos),
            'total_filtrado': len(produtos_filtrados)
        }
    
    def _extrair_produtos_pagina(self, soup):
        """Extrai produtos de uma página HTML"""
        produtos = []
        
        # Busca por itens de produto no Mercado Livre
        items = soup.find_all('li', class_='ui-search-layout__item')
        
        for item in items:
            try:
                # Nome do produto - procura no alt da imagem ou title
                nome = "Produto sem nome"
                
                # Tenta encontrar o nome no alt da imagem
                img_element = item.find('img')
                if img_element and img_element.get('alt'):
                    nome = img_element.get('alt').strip()
                else:
                    # Tenta encontrar em elementos com title
                    title_element = item.find(attrs={'title': True})
                    if title_element and title_element.get('title'):
                        nome = title_element.get('title').strip()
                    else:
                        # Tenta encontrar em texto visível
                        texto_elements = item.find_all(string=True)
                        for texto in texto_elements:
                            texto_limpo = texto.strip()
                            if len(texto_limpo) > 10 and len(texto_limpo) < 100:
                                nome = texto_limpo
                                break
                
                # Preço - procura o preço principal (não o parcelado)
                preco = None
                
                # Primeiro tenta pegar o preço completo (R$68,50)
                preco_completo = item.find('span', class_='andes-money-amount')
                if preco_completo and 'andes-money-amount--cents-superscript' in preco_completo.get('class', []):
                    preco_texto = preco_completo.get_text(strip=True)
                    preco = self._extrair_preco(preco_texto)
                else:
                    # Se não encontrar o preço completo, tenta pegar apenas a parte inteira
                    # mas evita pegar o preço parcelado
                    preco_elements = item.find_all('span', class_='andes-money-amount__fraction')
                    for preco_element in preco_elements:
                        # Verifica se não é parte de um preço parcelado
                        parent = preco_element.parent
                        if parent and 'poly-phrase-price' not in parent.get('class', []):
                            preco_texto = preco_element.get_text(strip=True)
                            preco = self._extrair_preco(preco_texto)
                            break
                    
                    # Fallback para outros seletores
                    if preco is None:
                        preco_element = item.find('span', class_='price-tag-fraction')
                        if preco_element:
                            preco_texto = preco_element.get_text(strip=True)
                            preco = self._extrair_preco(preco_texto)
                
                # Link do produto
                link_element = item.find('a')
                link = link_element.get('href') if link_element else None
                
                # Loja
                loja_element = item.find('p', class_='ui-search-official-store-item__title')
                if not loja_element:
                    loja_element = item.find('span', class_='ui-search-item__group__element')
                loja = loja_element.get_text(strip=True) if loja_element else "Vendedor não identificado"
                
                # Imagem
                img_element = item.find('img')
                imagem = img_element.get('data-src') or img_element.get('src') if img_element else None
                
                if preco is not None:
                    produtos.append({
                        'nome': nome,
                        'preco': preco,
                        'loja': loja,
                        'link': link,
                        'imagem': imagem
                    })
                    
            except Exception as e:
                continue
        
        return produtos
    
    def _extrair_preco(self, preco_texto):
        """Extrai valor numérico do preço"""
        if not preco_texto:
            return None
        
        # Remove caracteres não numéricos exceto vírgula e ponto
        preco_limpo = re.sub(r'[^\d,.]', '', preco_texto)
        
        if not preco_limpo:
            return None
        
        # Se tem vírgula E ponto, trata como formato brasileiro (ex: 1.299,90)
        if ',' in preco_limpo and '.' in preco_limpo:
            # Remove pontos (milhares) e mantém vírgula como decimal
            partes = preco_limpo.split(',')
            if len(partes) == 2:
                parte_inteira = partes[0].replace('.', '')
                parte_decimal = partes[1]
                preco_limpo = parte_inteira + '.' + parte_decimal
        
        # Se só tem vírgula, trata como decimal brasileiro (ex: 1299,90)
        elif ',' in preco_limpo and '.' not in preco_limpo:
            preco_limpo = preco_limpo.replace(',', '.')
        
        # Se só tem ponto, precisa analisar se é decimal ou milhares
        elif '.' in preco_limpo and ',' not in preco_limpo:
            partes = preco_limpo.split('.')
            # Se tem mais de 2 dígitos após o ponto, é formato de milhares
            if len(partes) == 2 and len(partes[1]) > 2:
                # É formato de milhares (ex: 1.299), remove o ponto
                preco_limpo = preco_limpo.replace('.', '')
            # Senão mantém como decimal (ex: 129.90)
        
        # Se não tem vírgula nem ponto, adiciona vírgula antes dos últimos 2 dígitos
        elif ',' not in preco_limpo and '.' not in preco_limpo:
            if len(preco_limpo) >= 2:
                preco_limpo = preco_limpo[:-2] + '.' + preco_limpo[-2:]
        
        try:
            valor = float(preco_limpo)
            # Se o valor parece muito baixo para um preço (menor que 10), 
            # pode ser que esteja faltando zeros
            if valor < 10 and len(preco_texto.replace(',', '').replace('.', '').replace('R$', '').replace('reais', '').strip()) > 2:
                # Tenta interpretar como centavos (multiplica por 100)
                valor = valor * 100
            return valor
        except ValueError:
            return None
    
    def _filtrar_produtos_pelo_menos_2_palavras(self, produtos, termo_busca):
        """Filtra produtos que contenham pelo menos 2 palavras da busca (após o hífen)"""
        # Remove conectivos e extrai palavras-chave
        conectivos = ['de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 
                     'para', 'com', 'por', 'sobre', 'entre', 'até', 'a', 'o', 'e', 'ou', 
                     'mas', 'que', 'se', 'um', 'uma']
        
        # Separa o termo por hífen e pega apenas a parte após o hífen
        if '-' in termo_busca:
            parte_apos_hifen = termo_busca.split('-', 1)[1].strip()
            print(f"🔍 Filtrando por palavras após o hífen: '{parte_apos_hifen}'")
        else:
            # Se não há hífen, usa todo o termo
            parte_apos_hifen = termo_busca
            print(f"🔍 Nenhum hífen encontrado, usando todo o termo: '{parte_apos_hifen}'")
        
        palavras_busca = [palavra.lower() for palavra in parte_apos_hifen.lower().split() 
                         if palavra not in conectivos and len(palavra) > 2]
        
        print(f"📝 Palavras-chave para filtro: {palavras_busca}")
        
        produtos_filtrados = []
        
        for produto in produtos:
            nome_produto = produto.get('nome', '').lower()
            
            # Conta quantas palavras da busca estão presentes no nome do produto
            palavras_encontradas = sum(1 for palavra in palavras_busca if palavra in nome_produto)
            
            # Aceita se pelo menos 2 palavras foram encontradas (ou todas se for menos que 2)
            min_palavras = min(2, len(palavras_busca))
            if palavras_encontradas >= min_palavras and palavras_busca:
                produto['palavras_encontradas'] = palavras_encontradas
                produto['total_palavras'] = len(palavras_busca)
                produto['percentual_match'] = (palavras_encontradas / len(palavras_busca)) * 100
                produtos_filtrados.append(produto)
        
        print(f"🎯 Produtos filtrados (pelo menos {min_palavras} palavras): {len(produtos_filtrados)}")
        
        # Ordena por percentual de match (maior primeiro)
        produtos_filtrados.sort(key=lambda x: x['percentual_match'], reverse=True)
        
        return produtos_filtrados
    
    def _filtrar_outliers(self, produtos):
        """Filtra produtos removendo outliers baseado em mediana ± 1 desvio padrão"""
        if len(produtos) < 3:  # Precisa de pelo menos 3 produtos para calcular desvio padrão
            return produtos
        
        # Calcula estatísticas iniciais
        precos = [p['preco'] for p in produtos if p['preco'] is not None]
        if len(precos) < 3:
            return produtos
        
        mediana = statistics.median(precos)
        desvio_padrao = statistics.stdev(precos)
        
        # Define os limites do filtro
        limite_inferior = mediana - desvio_padrao
        limite_superior = mediana + desvio_padrao
        
        print(f"📊 Filtro de outliers:")
        print(f"   Mediana: R$ {mediana:.2f}")
        print(f"   Desvio padrão: R$ {desvio_padrao:.2f}")
        print(f"   Limite inferior: R$ {limite_inferior:.2f}")
        print(f"   Limite superior: R$ {limite_superior:.2f}")
        
        # Filtra produtos dentro do range
        produtos_filtrados = []
        produtos_removidos = 0
        
        for produto in produtos:
            preco = produto['preco']
            if preco is not None and limite_inferior <= preco <= limite_superior:
                produtos_filtrados.append(produto)
            else:
                produtos_removidos += 1
        
        print(f"   ✅ {len(produtos_filtrados)} produtos mantidos")
        print(f"   ❌ {produtos_removidos} outliers removidos")
        
        return produtos_filtrados

    def _calcular_estatisticas(self, produtos):
        """Calcula estatísticas dos preços"""
        if not produtos:
            return None
        
        precos = [produto['preco'] for produto in produtos if produto['preco'] is not None]
        
        if not precos:
            return None
        
        try:
            return {
                'media': round(statistics.mean(precos), 2),
                'mediana': round(statistics.median(precos), 2),
                'minimo': round(min(precos), 2),
                'maximo': round(max(precos), 2),
                'desvio_padrao': round(statistics.stdev(precos), 2) if len(precos) > 1 else 0,
                'quantidade': len(precos)
            }
        except statistics.StatisticsError:
            return None


def main():
    """Função principal para uso via linha de comando"""
    parser = argparse.ArgumentParser(description='Busca preços no Mercado Livre')
    parser.add_argument('termo', help='Termo de busca')
    parser.add_argument('-o', '--output', help='Arquivo de saída JSON')
    
    args = parser.parse_args()
    
    buscador = BuscadorMercadoLivre()
    resultado = buscador.buscar_produtos(args.termo)
    
    # Saída em JSON
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"💾 Resultado salvo em: {args.output}")
    else:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
