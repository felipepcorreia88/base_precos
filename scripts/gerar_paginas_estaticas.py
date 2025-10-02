#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa partes da planilha e gera páginas HTML estáticas
"""

import pandas as pd
import json
import os
import argparse
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from busca_materiais_planilha_inteligente import BuscadorInteligente

def gerar_pagina_estatica(arquivo_entrada, arquivo_saida_html, numero_parte=None):
    """
    Processa planilha e gera página HTML estática com dados embutidos
    """
    print(f"\n{'='*80}")
    print(f"🔄 Processando: {arquivo_entrada}")
    print(f"{'='*80}\n")
    
    # Ler planilha
    df = pd.read_excel(arquivo_entrada)
    
    if 'Nome' not in df.columns:
        raise ValueError("Planilha deve ter coluna 'Nome'")
    
    # Criar buscador
    buscador = BuscadorInteligente()
    
    # Processar cada material
    materiais_dados = []
    
    for idx, row in df.iterrows():
        nome_material = str(row['Nome']).strip()
        
        print(f"🔍 [{idx+1}/{len(df)}] {nome_material}")
        
        # Buscar produtos
        resultado = buscador.buscar_produtos_material(nome_material)
        
        # Preparar dados
        produtos = []
        if resultado.get('produtos'):
            for p in resultado['produtos']:
                produtos.append({
                    'nome': p['nome'],
                    'preco': p['preco'],
                    'link': p.get('link', ''),
                    'score_relevancia': p.get('score_relevancia', 0)
                })
        
        # Calcular preço médio
        preco_medio = None
        if produtos:
            precos = [p['preco'] for p in produtos if p['preco']]
            if precos:
                preco_medio = sum(precos) / len(precos)
        
        material_info = {
            'nome': nome_material,
            'total_produtos': len(produtos),
            'preco_medio': preco_medio,
            'produtos': produtos
        }
        
        materiais_dados.append(material_info)
        
        print(f"   ✅ {len(produtos)} produtos encontrados\n")
    
    # Ler template HTML
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'pagina_estatica.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_html = f.read()
    
    # Preparar dados JSON
    dados_json = json.dumps(materiais_dados, ensure_ascii=False, indent=2)
    
    # Substituir placeholders
    titulo = f"Busca de Preços - Parte {numero_parte}" if numero_parte else "Busca de Preços"
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    html_final = template_html.replace('{{TITULO}}', titulo)
    html_final = html_final.replace('{{DATA_GERACAO}}', data_geracao)
    html_final = html_final.replace('{{TOTAL_MATERIAIS}}', str(len(materiais_dados)))
    html_final = html_final.replace('{{DADOS_JSON}}', dados_json)
    
    # Salvar HTML
    with open(arquivo_saida_html, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"\n{'='*80}")
    print(f"✅ Página gerada: {arquivo_saida_html}")
    print(f"{'='*80}\n")
    
    return arquivo_saida_html

def processar_todas_partes(pasta_partes='output/partes', pasta_saida='output/paginas_html'):
    """
    Processa todas as partes e gera páginas HTML
    """
    print(f"\n{'='*80}")
    print(f"🚀 PROCESSAMENTO DE TODAS AS PARTES")
    print(f"{'='*80}\n")
    
    # Criar pasta de saída
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"📁 Pasta criada: {pasta_saida}\n")
    
    # Encontrar arquivos de partes
    arquivos_partes = sorted([
        f for f in os.listdir(pasta_partes) 
        if f.startswith('materiais_parte_') and f.endswith('.xlsx')
    ])
    
    if not arquivos_partes:
        print(f"❌ Nenhum arquivo encontrado em '{pasta_partes}/'")
        print(f"   Execute primeiro: python3 dividir_planilha.py")
        return
    
    print(f"📦 Encontradas {len(arquivos_partes)} partes:\n")
    for f in arquivos_partes:
        print(f"   • {f}")
    print()
    
    # Processar cada parte
    paginas_geradas = []
    
    for arquivo in arquivos_partes:
        # Extrair número da parte
        numero_parte = arquivo.replace('materiais_parte_', '').replace('.xlsx', '')
        
        arquivo_entrada = os.path.join(pasta_partes, arquivo)
        arquivo_saida = os.path.join(pasta_saida, f'pagina_parte_{numero_parte}.html')
        
        try:
            gerar_pagina_estatica(arquivo_entrada, arquivo_saida, numero_parte)
            paginas_geradas.append(arquivo_saida)
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}\n")
            import traceback
            traceback.print_exc()
    
    # Gerar página índice
    gerar_pagina_indice(paginas_geradas, pasta_saida)
    
    print(f"\n{'='*80}")
    print(f"🎉 PROCESSAMENTO CONCLUÍDO!")
    print(f"{'='*80}")
    print(f"\n📊 {len(paginas_geradas)} páginas geradas em '{pasta_saida}/':\n")
    for p in paginas_geradas:
        print(f"   ✅ {os.path.basename(p)}")
    print(f"\n🌐 Abra qualquer página HTML no navegador!")
    print(f"   Exemplo: file://{os.path.abspath(paginas_geradas[0])}")
    print()

def gerar_pagina_indice(paginas, pasta_saida):
    """Gera página índice com links para todas as partes"""
    
    html_indice = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Busca de Preços - Índice</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .parts-list {
            display: grid;
            gap: 20px;
        }
        
        .part-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            color: white;
        }
        
        .part-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .part-info h2 {
            margin-bottom: 8px;
            font-size: 1.5em;
        }
        
        .part-info p {
            opacity: 0.9;
            font-size: 0.95em;
        }
        
        .arrow {
            font-size: 2em;
            opacity: 0.8;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Busca de Preços</h1>
        <div class="subtitle">
            Sistema Inteligente de Busca de Materiais
        </div>
        
        <div class="parts-list">
"""
    
    for i, pagina in enumerate(paginas, 1):
        nome_arquivo = os.path.basename(pagina)
        html_indice += f"""
            <a href="{nome_arquivo}" class="part-card">
                <div class="part-info">
                    <h2>Parte {i}</h2>
                    <p>Clique para visualizar os materiais desta parte</p>
                </div>
                <div class="arrow">→</div>
            </a>
"""
    
    html_indice += """
        </div>
        
        <div class="footer">
            <p>Gerado em """ + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + """</p>
            <p>Sistema de Busca Inteligente de Preços</p>
        </div>
    </div>
</body>
</html>
"""
    
    arquivo_indice = os.path.join(pasta_saida, 'index.html')
    with open(arquivo_indice, 'w', encoding='utf-8') as f:
        f.write(html_indice)
    
    print(f"📋 Página índice gerada: {arquivo_indice}")

def main():
    parser = argparse.ArgumentParser(
        description='Gera páginas HTML estáticas com busca de preços',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Processar uma parte específica
  python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o pagina1.html
  
  # Processar todas as partes automaticamente
  python3 gerar_paginas_estaticas.py --todas
        """
    )
    
    parser.add_argument('-i', '--entrada', help='Arquivo de entrada (uma parte)')
    parser.add_argument('-o', '--saida', help='Arquivo de saída HTML')
    parser.add_argument('-n', '--numero', type=int, help='Número da parte')
    parser.add_argument('--todas', action='store_true', 
                        help='Processar todas as partes da pasta "partes/"')
    parser.add_argument('--pasta-partes', default='output/partes',
                        help='Pasta com as partes (padrão: output/partes)')
    parser.add_argument('--pasta-saida', default='output/paginas_html',
                        help='Pasta de saída (padrão: output/paginas_html)')
    
    args = parser.parse_args()
    
    try:
        if args.todas:
            # Processar todas as partes
            processar_todas_partes(args.pasta_partes, args.pasta_saida)
        elif args.entrada and args.saida:
            # Processar uma parte específica
            gerar_pagina_estatica(args.entrada, args.saida, args.numero)
        else:
            print("❌ Erro: Especifique --todas ou forneça -i e -o")
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

