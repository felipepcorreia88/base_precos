#!/bin/bash
# Script de exemplo para visualizar dados da planilha

echo "======================================"
echo "📊 Visualizador de Materiais"
echo "======================================"
echo ""

# Verifica se existe algum arquivo de teste
if [ -f "teste_materiais_precos.xlsx" ]; then
    echo "✅ Arquivo de teste encontrado: teste_materiais_precos.xlsx"
    echo ""
    echo "🚀 Iniciando visualizador..."
    echo "🌐 Acesse: http://localhost:5001"
    echo ""
    python3 visualizador_materiais.py teste_materiais_precos.xlsx
elif [ -f "materiais_com_precos.xlsx" ]; then
    echo "✅ Arquivo encontrado: materiais_com_precos.xlsx"
    echo ""
    echo "🚀 Iniciando visualizador..."
    echo "🌐 Acesse: http://localhost:5001"
    echo ""
    python3 visualizador_materiais.py materiais_com_precos.xlsx
else
    echo "❌ Nenhum arquivo de dados encontrado!"
    echo ""
    echo "📋 Arquivos XLSX disponíveis:"
    ls -lh *.xlsx 2>/dev/null || echo "   Nenhum arquivo .xlsx encontrado"
    echo ""
    echo "💡 Para gerar dados, execute primeiro:"
    echo "   python3 teste_busca_pequena.py 5"
    echo ""
    echo "💡 Ou para processar a planilha completa:"
    echo "   python3 busca_materiais_planilha.py"
    echo ""
    echo "💡 Depois execute:"
    echo "   python3 visualizador_materiais.py ARQUIVO.xlsx"
fi

