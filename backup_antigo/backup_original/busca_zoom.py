#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador de preços no Zoom
Busca produtos e retorna JSON com estatísticas de preços
"""

import requests
from bs4 import BeautifulSoup
import json
import statistics
import re
import time
import argparse
from urllib.parse import quote_plus


class BuscadorZoom:
    """Classe para buscar produtos no Zoom"""
    
    def __init__(self):
        self.base_url = "https://www.zoom.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.google.com/'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.max_paginas = 3
    
    def buscar_produtos(self, termo_busca):
        """
        Busca produtos no Zoom
        
        Args:
            termo_busca (str): Termo de busca
            
        Returns:
            dict: Dicionário com produtos e estatísticas
        """
        print(f"🔍 Buscando produtos para: '{termo_busca}'")
        
        produtos = []
        
        # Busca apenas na primeira página (melhores resultados do Zoom)
        url = f"{self.base_url}/search?q={quote_plus(termo_busca)}"
        print(f"📄 Buscando primeira página (melhores resultados do Zoom)...")
        
        try:
            print(f"   🔄 Buscando produtos...")
            response = self.session.get(url, timeout=15)
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
            print(f"   ❌ Erro ao buscar no Zoom: {e}")
            return {
                'produtos': [],
                'estatisticas': None,
                'termo': termo_busca,
                'total_encontrado': 0,
                'total_filtrado': 0,
                'erro': f'Erro ao acessar Zoom: {str(e)}'
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
            'total_filtrado': len(produtos_filtrados),
            'fonte': 'Zoom'
        }
    
    def _extrair_produtos_pagina(self, soup):
        """Extrai produtos de uma página HTML"""
        produtos = []
        
        # Busca por itens de produto no Zoom
        # Tenta diferentes seletores possíveis
        seletores = [
            'div[data-testid="product-card"]',
            'div.product-card',
            'div[class*="product"]',
            'article[data-testid="product"]',
            'div.card-product',
            'div[class*="card"]',
            'div[class*="item"]',
            '.product',
            '.card',
            '.item'
        ]
        
        items = []
        for seletor in seletores:
            items = soup.select(seletor)
            if items:
                print(f"   ✅ Encontrados {len(items)} produtos com seletor: {seletor}")
                break
        
        if not items:
            print(f"   ⚠️ Nenhum produto específico encontrado, tentando busca alternativa...")
            # Procura por elementos que contenham preços
            elementos_com_preco = []
            for elem in soup.find_all(['div', 'li', 'article', 'section']):
                texto = elem.get_text()
                if 'R$' in texto and any(c.isdigit() for c in texto):
                    # Verifica se tem características de produto (nome + preço)
                    if len(texto) > 50 and len(texto) < 500:
                        elementos_com_preco.append(elem)
            
            items = elementos_com_preco[:20]  # Limita a 20 elementos
            if items:
                print(f"   ✅ Encontrados {len(items)} elementos com preços")
        
        for item in items:
            try:
                # Nome do produto
                nome = self._extrair_nome(item)
                
                # Preço
                preco = self._extrair_preco(item)
                
                # Link do produto
                link = self._extrair_link(item)
                
                # Imagem
                imagem = self._extrair_imagem(item)
                
                # Loja
                loja = self._extrair_loja(item)
                
                if preco is not None and preco > 0:
                    produtos.append({
                        'nome': nome,
                        'preco': preco,
                        'loja': loja,
                        'link': link,
                        'imagem': imagem
                    })
                    
            except Exception as e:
                # print(f"Erro ao extrair produto: {e}")  # Descomente para debug
                continue
        
        return produtos
    
    def _extrair_nome(self, item):
        """Extrai nome do produto"""
        # Tenta diferentes seletores para nome
        seletores_nome = [
            'h2', 'h3', 'h4',
            '[data-testid="product-title"]',
            '.product-title',
            '.product-name',
            'a[title]',
            '[class*="title"]',
            '[class*="name"]'
        ]
        
        for seletor in seletores_nome:
            elemento = item.select_one(seletor)
            if elemento:
                nome = elemento.get_text(strip=True)
                if nome and len(nome) > 3:
                    return nome
        
        # Se não encontrar, tenta pegar do title de um link
        link = item.find('a')
        if link and link.get('title'):
            return link.get('title')
        
        # Último recurso: pega o primeiro texto longo encontrado
        textos = item.find_all(string=True)
        for texto in textos:
            texto_limpo = texto.strip()
            if len(texto_limpo) > 10 and len(texto_limpo) < 100:
                return texto_limpo
        
        return "Produto sem nome"
    
    def _extrair_preco(self, item):
        """Extrai preço do produto"""
        # Procura por elementos que contenham preços
        precos = item.find_all(string=re.compile(r'R\$\s*\d+'))
        
        for preco_texto in precos:
            if preco_texto:
                valor = self._extrair_preco_numerico(preco_texto.strip())
                if valor:
                    return valor
        
        # Tenta seletores específicos de preço
        seletores_preco = [
            '[class*="price"]',
            '[class*="preco"]',
            '[data-testid*="price"]',
            '.price',
            '.preco'
        ]
        
        for seletor in seletores_preco:
            elemento = item.select_one(seletor)
            if elemento:
                preco_texto = elemento.get_text(strip=True)
                valor = self._extrair_preco_numerico(preco_texto)
                if valor:
                    return valor
        
        return None
    
    def _extrair_preco_numerico(self, preco_texto):
        """Extrai valor numérico do preço"""
        if not preco_texto:
            return None
        
        # Remove caracteres não numéricos exceto vírgula e ponto
        preco_limpo = re.sub(r'[^\d,.]', '', preco_texto)
        
        if not preco_limpo:
            return None
        
        # Substitui vírgula por ponto (formato brasileiro -> formato numérico)
        if '.' in preco_limpo and ',' in preco_limpo:
            preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
        elif ',' in preco_limpo:
            preco_limpo = preco_limpo.replace(',', '.')
        
        try:
            valor = float(preco_limpo)
            return valor
        except ValueError:
            return None
    
    def _extrair_link(self, item):
        """Extrai link do produto"""
        link_element = item.find('a')
        if link_element and link_element.get('href'):
            href = link_element.get('href')
            if href.startswith('/'):
                return f"{self.base_url}{href}"
            elif href.startswith('http'):
                return href
        return None
    
    def _extrair_imagem(self, item):
        """Extrai imagem do produto"""
        img_element = item.find('img')
        if img_element:
            imagem = img_element.get('src') or img_element.get('data-src')
            if imagem and imagem.startswith('/'):
                return f"{self.base_url}{imagem}"
            return imagem
        return None
    
    def _extrair_loja(self, item):
        """Extrai loja do produto"""
        # Procura por informações de loja
        seletores_loja = [
            '[class*="store"]',
            '[class*="loja"]',
            '[class*="seller"]',
            '[data-testid*="store"]'
        ]
        
        for seletor in seletores_loja:
            elemento = item.select_one(seletor)
            if elemento:
                loja = elemento.get_text(strip=True)
                if loja:
                    return loja
        
        return "Loja não identificada"
    
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
    parser = argparse.ArgumentParser(description='Busca preços no Zoom')
    parser.add_argument('termo', help='Termo de busca')
    parser.add_argument('-o', '--output', help='Arquivo de saída JSON')
    
    args = parser.parse_args()
    
    buscador = BuscadorZoom()
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
