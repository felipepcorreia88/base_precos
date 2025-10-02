#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir páginas HTML já geradas
Atualiza as funções JavaScript para não causar scroll ao remover produtos
"""

import os
import re
import glob

def corrigir_pagina_html(arquivo):
    """Corrige uma página HTML"""
    print(f"📝 Corrigindo: {arquivo}")
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Padrão da função antiga removerProduto
    padrao_antigo = r'// Remover produto\s+function removerProduto\(materialIdx, nomeProduto\) \{[^}]+\{[^}]+\}[^}]+\}'
    
    # Nova implementação
    nova_funcao = '''// Remover produto
        function removerProduto(materialIdx, nomeProduto) {
            const chave = `${materialIdx}-${nomeProduto}`;
            produtosRemovidos.add(chave);
            
            // Remover visualmente o elemento DOM (sem re-renderizar tudo)
            // O ID é gerado da mesma forma que no criarCardMaterial
            const baseId = `${materialIdx}-${nomeProduto}`;
            const produtoId = `produto-${baseId.replace(/[^a-zA-Z0-9]/g, '_')}`;
            const produtoElement = document.getElementById(produtoId);
            
            if (produtoElement) {
                // Animação de fade out
                produtoElement.style.transition = 'opacity 0.3s, transform 0.3s';
                produtoElement.style.opacity = '0';
                produtoElement.style.transform = 'translateX(-20px)';
                
                // Remover após animação
                setTimeout(() => {
                    produtoElement.remove();
                    
                    // Atualizar estatísticas do material e badge
                    atualizarMaterialVisual(materialIdx);
                    atualizarEstatisticas();
                }, 300);
            }
        }
        
        // Atualizar visual do material (estatísticas e badge)
        function atualizarMaterialVisual(materialIdx) {
            const material = DADOS[materialIdx];
            if (!material) return;
            
            const produtos = material.produtos || [];
            const produtosVisiveis = produtos.filter(p => 
                !produtosRemovidos.has(`${materialIdx}-${p.nome}`)
            );
            
            // Atualizar badge e contador
            const materialCard = document.getElementById(`material-${materialIdx}`);
            if (!materialCard) return;
            
            const materialInfo = materialCard.querySelector('.material-info');
            if (!materialInfo) return;
            
            // Atualizar badge
            let statusBadge = '';
            if (produtosVisiveis.length === 0) {
                statusBadge = '<span class="badge badge-danger">Sem produtos</span>';
            } else if (produtosVisiveis.length < 5) {
                statusBadge = '<span class="badge badge-warning">Poucos produtos</span>';
            } else {
                statusBadge = '<span class="badge badge-success">Com produtos</span>';
            }
            
            // Calcular novas estatísticas
            let statsHTML = '';
            if (produtosVisiveis.length > 0) {
                const precos = produtosVisiveis.map(p => p.preco).filter(p => p);
                if (precos.length > 0) {
                    const stats = calcularEstatisticas(precos);
                    statsHTML = `
                        <span>📊 Min: <strong>R$ ${stats.minimo.toFixed(2)}</strong></span>
                        <span>📊 Máx: <strong>R$ ${stats.maximo.toFixed(2)}</strong></span>
                        <span>📊 Média: <strong>R$ ${stats.media.toFixed(2)}</strong></span>
                        <span>📊 Mediana: <strong>R$ ${stats.mediana.toFixed(2)}</strong></span>
                        <span>📊 DP: <strong>R$ ${stats.desvioPadrao.toFixed(2)}</strong></span>
                    `;
                }
            }
            
            // Atualizar o HTML
            materialInfo.innerHTML = `
                ${statusBadge}
                <span>📦 <strong>${produtosVisiveis.length}</strong> produto(s)</span>
                ${statsHTML}
            `;
        }'''
    
    # Substituir a função antiga
    conteudo_novo = re.sub(padrao_antigo, nova_funcao, conteudo, flags=re.DOTALL)
    
    # Corrigir também a função limparRemovidos
    padrao_limpar = r'// Limpar produtos removidos\s+function limparRemovidos\(\) \{[^}]+if \(confirm[^}]+\}[^}]+\}'
    
    nova_limpar = '''// Limpar produtos removidos
        function limparRemovidos() {
            if (produtosRemovidos.size === 0) {
                alert('Nenhum produto foi removido!');
                return;
            }
            
            if (confirm(`Restaurar ${produtosRemovidos.size} produto(s) removido(s)?`)) {
                // Salvar posição do scroll
                const scrollPos = window.scrollY;
                
                produtosRemovidos.clear();
                const filtro = document.getElementById('search-box').value.toLowerCase();
                renderizarMateriais(filtro);
                atualizarEstatisticas();
                
                // Restaurar posição do scroll após um pequeno delay
                setTimeout(() => {
                    window.scrollTo(0, scrollPos);
                }, 50);
            }
        }'''
    
    conteudo_novo = re.sub(padrao_limpar, nova_limpar, conteudo_novo, flags=re.DOTALL)
    
    # Salvar arquivo corrigido
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo_novo)
    
    print(f"   ✅ Corrigido!")

def main():
    pasta_html = '../output/paginas_html'
    
    # Encontrar todos os arquivos HTML
    arquivos = glob.glob(os.path.join(pasta_html, 'pagina_parte_*.html'))
    
    if not arquivos:
        print("❌ Nenhuma página HTML encontrada em", pasta_html)
        return
    
    print(f"\n📋 Encontradas {len(arquivos)} páginas HTML para corrigir:\n")
    
    for arquivo in sorted(arquivos):
        corrigir_pagina_html(arquivo)
    
    print(f"\n✅ {len(arquivos)} páginas HTML corrigidas!")
    print("\n🎯 Agora ao remover um produto, a página mantém a posição do scroll.")

if __name__ == "__main__":
    main()

