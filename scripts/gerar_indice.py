#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera página índice (index.html) para as páginas HTML já criadas
"""

import os
import sys
from datetime import datetime

def gerar_pagina_indice(pasta_saida='output/paginas_html'):
    """Gera página índice com links para todas as páginas HTML"""
    
    print("\n" + "="*80)
    print("📋 GERANDO PÁGINA ÍNDICE")
    print("="*80 + "\n")
    
    if not os.path.exists(pasta_saida):
        print(f"❌ Pasta '{pasta_saida}/' não encontrada")
        return 1
    
    # Encontrar páginas HTML
    arquivos_html = sorted([
        f for f in os.listdir(pasta_saida)
        if f.startswith('pagina_parte_') and f.endswith('.html')
    ])
    
    if not arquivos_html:
        print(f"❌ Nenhuma página HTML encontrada em '{pasta_saida}/'")
        print(f"\n💡 Processe ao menos uma parte primeiro:")
        print(f"   python3 processar_parte.py -p 1")
        return 1
    
    print(f"📦 Páginas encontradas: {len(arquivos_html)}")
    for arquivo in arquivos_html:
        print(f"   • {arquivo}")
    print()
    
    # Gerar HTML do índice
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
        
        .info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .info p {
            margin: 5px 0;
            color: #666;
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
        
        .instrucoes {
            background: #e7f3ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }
        
        .instrucoes h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .instrucoes ul {
            margin-left: 20px;
            color: #555;
        }
        
        .instrucoes li {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Busca de Preços</h1>
        <div class="subtitle">
            Sistema Inteligente de Busca de Materiais
        </div>
        
        <div class="info">
            <p><strong>📊 Total de partes processadas: """ + str(len(arquivos_html)) + """</strong></p>
            <p>📅 Índice gerado em: """ + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + """</p>
        </div>
        
        <div class="instrucoes">
            <h3>📝 Como usar cada página:</h3>
            <ul>
                <li>✅ Visualize todos os produtos já coletados</li>
                <li>✅ Use a busca para filtrar materiais</li>
                <li>✅ Remova produtos irrelevantes (botão "✕ Remover")</li>
                <li>✅ Exporte para Excel (botão "📊 Exportar para Excel")</li>
                <li>✅ Restaure produtos removidos (botão "🗑️ Limpar Removidos")</li>
            </ul>
        </div>
        
        <div class="parts-list">
"""
    
    # Adicionar links para cada parte
    for i, arquivo in enumerate(arquivos_html, 1):
        numero_parte = arquivo.replace('pagina_parte_', '').replace('.html', '')
        html_indice += f"""
            <a href="{arquivo}" class="part-card">
                <div class="part-info">
                    <h2>Parte {numero_parte}</h2>
                    <p>Clique para visualizar os materiais desta parte</p>
                </div>
                <div class="arrow">→</div>
            </a>
"""
    
    html_indice += """
        </div>
        
        <div class="footer">
            <p>Sistema de Busca Inteligente de Preços</p>
            <p>Modo Inteligente: Palavras específicas são obrigatórias</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Salvar arquivo
    arquivo_indice = os.path.join(pasta_saida, 'index.html')
    with open(arquivo_indice, 'w', encoding='utf-8') as f:
        f.write(html_indice)
    
    print(f"✅ Página índice gerada: {arquivo_indice}")
    
    caminho_absoluto = os.path.abspath(arquivo_indice)
    print(f"\n🌐 Para visualizar:")
    print(f"   xdg-open {arquivo_indice}")
    print(f"   \nOu abra: file://{caminho_absoluto}\n")
    
    return 0

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Gera página índice para as páginas HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Gera index.html com links para todas as páginas HTML disponíveis.

Exemplos:
  python3 gerar_indice.py
  python3 gerar_indice.py --pasta paginas_html
        """
    )
    
    parser.add_argument('--pasta', default='output/paginas_html',
                        help='Pasta com as páginas HTML (padrão: output/paginas_html)')
    
    args = parser.parse_args()
    
    return gerar_pagina_indice(args.pasta)

if __name__ == "__main__":
    sys.exit(main())

