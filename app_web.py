#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Web para Busca de Preços
Interface HTML com busca em múltiplas bases (Mercado Livre, BuscaPé e Zoom)
"""

from flask import Flask, render_template, request, jsonify
from busca_mercadolivre import BuscadorMercadoLivre
from busca_buscape import BuscadorBuscaPe
from busca_zoom import BuscadorZoom

app = Flask(__name__)

class BuscadorPrecosWeb:
    """Gerenciador de buscas em múltiplas fontes"""
    
    def __init__(self):
        self.buscadores = {
            'mercadolivre': BuscadorMercadoLivre(),
            'buscape': BuscadorBuscaPe(),
            'zoom': BuscadorZoom()
        }
    
    def buscar_produtos(self, termo_busca, fonte='mercadolivre'):
        """
        Busca produtos na fonte especificada
        
        Args:
            termo_busca (str): Termo de busca
            fonte (str): 'mercadolivre', 'buscape' ou 'zoom'
            
        Returns:
            dict: Resultado da busca com produtos e estatísticas
        """
        buscador = self.buscadores.get(fonte.lower())
        
        if not buscador:
            return {
                'erro': f'Fonte "{fonte}" não suportada. Use: mercadolivre, buscape ou zoom'
            }
        
        resultado = buscador.buscar_produtos(termo_busca)
        
        # Define o nome da fonte
        if fonte == 'mercadolivre':
            resultado['fonte'] = 'Mercado Livre'
        elif fonte == 'buscape':
            resultado['fonte'] = 'BuscaPé'
        elif fonte == 'zoom':
            resultado['fonte'] = 'Zoom'
        
        return resultado

# Instância global do buscador
buscador = BuscadorPrecosWeb()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    """Endpoint para buscar produtos"""
    try:
        data = request.get_json()
        termo = data.get('termo', '').strip()
        fonte = data.get('fonte', 'mercadolivre').strip().lower()
        
        if not termo:
            return jsonify({
                'erro': 'Termo de busca não pode estar vazio'
            }), 400
        
        # Busca produtos na fonte especificada
        resultado = buscador.buscar_produtos(termo, fonte)
        
        if 'erro' in resultado:
            return jsonify(resultado), 400
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'erro': f'Erro interno: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("🌐 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)