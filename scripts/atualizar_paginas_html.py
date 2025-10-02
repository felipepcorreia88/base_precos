#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar páginas HTML com localStorage e correção de bugs
"""

import os
import glob
import shutil
from datetime import datetime

def atualizar_pagina(arquivo):
    """Atualiza uma página HTML com o template mais recente"""
    print(f"🔄 Atualizando: {os.path.basename(arquivo)}")
    
    # Ler página antiga
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo_antigo = f.read()
    
    # Extrair os DADOS_JSON da página antiga
    import re
    match = re.search(r'const DADOS = (\[.*?\]);', conteudo_antigo, re.DOTALL)
    
    if not match:
        print(f"   ⚠️  Não foi possível extrair DADOS_JSON, pulando...")
        return False
    
    dados_json = match.group(1)
    
    # Extrair título
    match_titulo = re.search(r'<title>(.*?)</title>', conteudo_antigo)
    titulo = match_titulo.group(1) if match_titulo else "Busca de Preços"
    
    # Extrair data de geração
    match_data = re.search(r'Gerado em: (.*?)</p>', conteudo_antigo)
    data_geracao = match_data.group(1) if match_data else datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Extrair total de materiais
    match_total = re.search(r'Total de materiais processados: <strong id="total-materiais">(\d+)</strong>', conteudo_antigo)
    total_materiais = match_total.group(1) if match_total else "0"
    
    # Ler template atualizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    template_path = os.path.join(project_root, 'templates', 'pagina_estatica.html')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_novo = f.read()
    
    # Substituir placeholders
    html_atualizado = template_novo.replace('{{TITULO}}', titulo)
    html_atualizado = html_atualizado.replace('{{DATA_GERACAO}}', data_geracao)
    html_atualizado = html_atualizado.replace('{{TOTAL_MATERIAIS}}', total_materiais)
    html_atualizado = html_atualizado.replace('{{DADOS_JSON}}', dados_json)
    
    # Fazer backup
    backup_path = arquivo + '.backup'
    shutil.copy2(arquivo, backup_path)
    
    # Salvar página atualizada
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html_atualizado)
    
    print(f"   ✅ Atualizado! (backup: {os.path.basename(backup_path)})")
    return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pasta_html = os.path.join(project_root, 'output', 'paginas_html')
    
    # Encontrar todos os arquivos HTML (exceto index.html)
    arquivos = glob.glob(os.path.join(pasta_html, 'pagina_parte_*.html'))
    
    if not arquivos:
        print("❌ Nenhuma página HTML encontrada em", pasta_html)
        return
    
    print(f"\n{'='*80}")
    print(f"🔄 ATUALIZAÇÃO DE PÁGINAS HTML")
    print(f"{'='*80}\n")
    print(f"📋 Encontradas {len(arquivos)} páginas para atualizar\n")
    
    atualizadas = 0
    for arquivo in sorted(arquivos):
        if atualizar_pagina(arquivo):
            atualizadas += 1
    
    print(f"\n{'='*80}")
    print(f"✅ {atualizadas}/{len(arquivos)} páginas atualizadas com sucesso!")
    print(f"{'='*80}\n")
    
    print("🎯 Novas funcionalidades:")
    print("   ✅ Produtos removidos salvos no localStorage")
    print("   ✅ Ao reabrir página, remoções são mantidas")
    print("   ✅ Correção do bug de scroll")
    print("   ✅ Logs de debug adicionados")
    print()
    print("🗑️ Arquivos de backup criados (.backup)")
    print("   Se algo der errado, renomeie o .backup para .html")
    print()

if __name__ == "__main__":
    main()

