#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizador de Materiais - Interface Web
Exibe dados da planilha gerada por busca_materiais_planilha.py
"""

import pandas as pd
import json
import argparse
from flask import Flask, render_template, jsonify
from datetime import datetime
import sys
import os

app = Flask(__name__)

# Variável global para armazenar os dados
dados_planilha = None
nome_arquivo = None

class VisualizadorMateriais:
    """Classe para processar e servir dados da planilha"""
    
    def __init__(self, arquivo_xlsx):
        self.arquivo = arquivo_xlsx
        self.df = None
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados da planilha Excel"""
        try:
            print(f"📖 Carregando planilha: {self.arquivo}")
            self.df = pd.read_excel(self.arquivo)
            
            # Aceita tanto 'Nome' quanto 'Nome_Original'
            if 'Nome_Original' in self.df.columns and 'Nome' not in self.df.columns:
                print(f"   📝 Renomeando coluna 'Nome_Original' para 'Nome'")
                self.df['Nome'] = self.df['Nome_Original']
            
            # Verifica se tem as colunas necessárias
            colunas_necessarias = ['Nome', 'Total_Produtos_Encontrados', 'Links_Produtos_JSON']
            for coluna in colunas_necessarias:
                if coluna not in self.df.columns:
                    raise ValueError(f"Coluna '{coluna}' não encontrada na planilha")
            
            # Aceita tanto 'Total_Produtos_Relevantes' quanto sem ela
            if 'Total_Produtos_Relevantes' in self.df.columns:
                print(f"   ✅ Planilha otimizada detectada (com coluna Total_Produtos_Relevantes)")
            
            # Adiciona colunas que podem estar faltando (para compatibilidade)
            colunas_padrao = {
                'Preco_Mediana': None,
                'Desvio_Padrao': None, 
                'Outliers_Removidos': 0,
                'Data_Hora_Busca': None
            }
            
            for coluna, valor_padrao in colunas_padrao.items():
                if coluna not in self.df.columns:
                    self.df[coluna] = valor_padrao
                    print(f"   📝 Adicionando coluna padrão: {coluna}")
            
            print(f"✅ Planilha carregada com sucesso!")
            print(f"📊 Total de materiais: {len(self.df)}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar planilha: {e}")
            raise
    
    def obter_resumo(self):
        """Obtém resumo estatístico dos dados"""
        if self.df is None:
            return None
        
        total_materiais = len(self.df)
        materiais_com_produtos = len(self.df[self.df['Total_Produtos_Encontrados'] > 0])
        materiais_sem_produtos = len(self.df[self.df['Total_Produtos_Encontrados'] == 0])
        
        # Estatísticas de preços
        df_com_precos = self.df[self.df['Preco_Medio'].notna()]
        
        resumo = {
            'total_materiais': int(total_materiais),
            'materiais_com_produtos': int(materiais_com_produtos),
            'materiais_sem_produtos': int(materiais_sem_produtos),
            'total_produtos_encontrados': int(self.df['Total_Produtos_Encontrados'].sum()),
            'preco_medio_geral': float(df_com_precos['Preco_Medio'].mean()) if len(df_com_precos) > 0 else 0,
            'preco_minimo_geral': float(df_com_precos['Preco_Minimo'].min()) if len(df_com_precos) > 0 else 0,
            'preco_maximo_geral': float(df_com_precos['Preco_Maximo'].max()) if len(df_com_precos) > 0 else 0,
        }
        
        return resumo
    
    def obter_materiais(self, filtro=None, ordenar_por='Nome', ordem='asc'):
        """Obtém lista de materiais com filtros e ordenação"""
        if self.df is None:
            return []
        
        df_filtrado = self.df.copy()
        
        # Aplica filtro de busca
        if filtro and filtro.strip():
            df_filtrado = df_filtrado[
                df_filtrado['Nome'].str.contains(filtro, case=False, na=False)
            ]
        
        # Ordena
        if ordenar_por in df_filtrado.columns:
            ascending = (ordem == 'asc')
            df_filtrado = df_filtrado.sort_values(by=ordenar_por, ascending=ascending)
        
        # Converte para lista de dicionários
        materiais = []
        for idx, row in df_filtrado.iterrows():
            material = {
                'nome': row['Nome'],
                'total_produtos': int(row['Total_Produtos_Encontrados']) if pd.notna(row['Total_Produtos_Encontrados']) else 0,
                'preco_minimo': float(row['Preco_Minimo']) if pd.notna(row['Preco_Minimo']) else None,
                'preco_maximo': float(row['Preco_Maximo']) if pd.notna(row['Preco_Maximo']) else None,
                'preco_medio': float(row['Preco_Medio']) if pd.notna(row['Preco_Medio']) else None,
                'preco_mediana': float(row['Preco_Mediana']) if pd.notna(row['Preco_Mediana']) else None,
                'desvio_padrao': float(row['Desvio_Padrao']) if pd.notna(row['Desvio_Padrao']) else None,
                'outliers_removidos': int(row['Outliers_Removidos']) if pd.notna(row['Outliers_Removidos']) else 0,
                'status': row['Status_Busca'] if pd.notna(row['Status_Busca']) else 'desconhecido',
                'data_busca': row['Data_Hora_Busca'] if pd.notna(row['Data_Hora_Busca']) else None,
                'produtos_json': self._parse_json(row['Links_Produtos_JSON']) if pd.notna(row['Links_Produtos_JSON']) else []
            }
            materiais.append(material)
        
        return materiais
    
    def _parse_json(self, json_str):
        """Parse string JSON para lista de produtos"""
        try:
            if isinstance(json_str, str) and json_str.strip():
                produtos = json.loads(json_str)
                return produtos if isinstance(produtos, list) else []
            return []
        except json.JSONDecodeError:
            return []

# Instância global do visualizador
visualizador = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('visualizador.html', nome_arquivo=nome_arquivo)

@app.route('/api/resumo')
def api_resumo():
    """API: Retorna resumo estatístico"""
    if visualizador is None:
        return jsonify({'erro': 'Dados não carregados'}), 500
    
    resumo = visualizador.obter_resumo()
    return jsonify(resumo)

@app.route('/api/materiais')
def api_materiais():
    """API: Retorna lista de materiais"""
    if visualizador is None:
        return jsonify({'erro': 'Dados não carregados'}), 500
    
    from flask import request
    filtro = request.args.get('filtro', '')
    ordenar_por = request.args.get('ordenar_por', 'Nome')
    ordem = request.args.get('ordem', 'asc')
    
    materiais = visualizador.obter_materiais(filtro, ordenar_por, ordem)
    return jsonify({
        'materiais': materiais,
        'total': len(materiais)
    })

def main():
    """Função principal"""
    global visualizador, nome_arquivo
    
    parser = argparse.ArgumentParser(
        description='Visualizador de materiais com preços',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python3 visualizador_materiais.py materiais_com_precos.xlsx
  python3 visualizador_materiais.py teste_materiais_precos.xlsx
  python3 visualizador_materiais.py materiais_com_precos.xlsx --port 8080
        """
    )
    
    parser.add_argument('arquivo', help='Arquivo XLSX com dados dos materiais')
    parser.add_argument('--port', type=int, default=5001, help='Porta do servidor (padrão: 5001)')
    parser.add_argument('--host', default='0.0.0.0', help='Host do servidor (padrão: 0.0.0.0)')
    
    args = parser.parse_args()
    
    # Verifica se o arquivo existe
    if not os.path.exists(args.arquivo):
        print(f"❌ Erro: Arquivo '{args.arquivo}' não encontrado")
        return 1
    
    # Carrega dados
    try:
        visualizador = VisualizadorMateriais(args.arquivo)
        nome_arquivo = os.path.basename(args.arquivo)
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return 1
    
    # Inicia servidor
    print("\n" + "="*60)
    print("🚀 Visualizador de Materiais - Servidor iniciado!")
    print("="*60)
    print(f"📁 Arquivo: {args.arquivo}")
    print(f"🌐 Acesse: http://localhost:{args.port}")
    print(f"🌐 Ou: http://{args.host}:{args.port}")
    print("="*60)
    print("\n⌨️  Pressione Ctrl+C para parar o servidor\n")
    
    try:
        app.run(debug=True, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor encerrado pelo usuário")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

