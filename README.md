# 🛒 Sistema de Busca de Preços

Sistema completo de web scraping para busca de preços em múltiplas plataformas com análise estatística avançada.

## 🚀 Funcionalidades

- **Web Scraping Inteligente**: Busca produtos no Mercado Livre e BuscaPé
- **Análise Estatística**: Calcula média, mediana, desvio padrão e outliers
- **Interface Web**: Aplicação Flask com interface HTML moderna em tabela
- **Filtro de Outliers**: Remove preços extremos automaticamente (mediana ± 1 desvio padrão)
- **Múltiplas Fontes**: Escolha entre Mercado Livre ou BuscaPé
- **Estatísticas Completas**: Preço mínimo, máximo, média, mediana e desvio padrão

## 📁 Estrutura do Projeto

```
projeto/
├── app_web.py                    # Aplicação Flask principal
├── busca_mercadolivre.py         # Scraper do Mercado Livre
├── busca_buscape.py              # Scraper do BuscaPé
├── templates/
│   └── index.html               # Interface web (tabela responsiva)
├── requirements.txt              # Dependências Python
└── README.md                    # Este arquivo
```

## 🚀 Como usar

### 1. Instalação das dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação web

```bash
# Executar aplicação web
python3 app_web.py

# Acessar no navegador: http://localhost:5000
```

### 3. Usar via linha de comando

```bash
# Mercado Livre
python3 busca_mercadolivre.py "termo de busca"

# BuscaPé
python3 busca_buscape.py "termo de busca"

# Exemplos
python3 busca_mercadolivre.py "mouse gamer"
python3 busca_buscape.py "notebook dell"
```

## 🌐 Interface Web

### Como usar:
1. Execute `python3 app_web.py`
2. Acesse `http://localhost:5000`
3. Digite o termo de busca
4. Escolha a base de dados (Mercado Livre ou BuscaPé)
5. Clique em "Buscar"
6. Visualize os resultados na tabela organizada

### Recursos da interface:
- ✅ **Tabela responsiva**: Organizada por colunas (Imagem, Produto, Preço, Ação)
- ✅ **Filtro de outliers**: Remove preços extremos automaticamente
- ✅ **Estatísticas visuais**: Cards com média, mediana, min, max, desvio padrão
- ✅ **Links diretos**: Acesso direto aos produtos nas plataformas
- ✅ **Imagens dos produtos**: Visualização das fotos dos produtos
- ✅ **Design moderno**: Interface limpa e profissional

## 📊 Informações exibidas

Para cada produto encontrado, o sistema mostra:
- **Imagem**: Foto do produto
- **Nome**: Nome completo do produto
- **Preço**: Valor atual
- **Loja**: Vendedor/loja
- **Link**: Acesso direto à plataforma

### Estatísticas gerais:
- **Quantidade**: Total de produtos
- **Preço mínimo**: Menor preço encontrado
- **Preço máximo**: Maior preço encontrado
- **Média**: Preço médio
- **Mediana**: Valor mediano
- **Desvio padrão**: Dispersão dos preços

## 🔍 Filtro de Outliers

O sistema aplica automaticamente um filtro estatístico:
- **Fórmula**: Mediana ± 1 Desvio Padrão
- **Objetivo**: Remove preços extremos que podem distorcer a análise
- **Resultado**: Mostra apenas produtos com preços dentro do range estatisticamente relevante

## 🛠️ Tecnologias utilizadas

- **Python 3.6+**
- **Flask** - Framework web
- **requests** - Requisições HTTP
- **beautifulsoup4** - Parsing HTML
- **lxml** - Parser XML/HTML rápido
- **HTML5/CSS3/JavaScript** - Interface web moderna

## 📡 Fontes de Dados

- **Mercado Livre**: https://lista.mercadolivre.com.br/
- **BuscaPé**: https://www.buscape.com.br/
- **Método**: Web Scraping com BeautifulSoup

## 💡 Dicas para melhor busca

- Use termos específicos para resultados mais precisos
- Combine palavras-chave relevantes
- Evite termos muito genéricos
- Exemplos: "mouse gamer", "notebook dell", "smartphone samsung"

## ⚠️ Observações

- Os preços mostrados são de lojas online reais
- O filtro de outliers remove automaticamente preços extremos
- Requer conexão com a internet
- O web scraping respeita os limites dos sites
- A busca é otimizada para primeira página (melhores resultados)

## 🎯 Exemplos de uso

```bash
# Buscar mouses gamer
python3 busca_mercadolivre.py "mouse gamer"

# Buscar notebooks
python3 busca_buscape.py "notebook dell"

# Buscar smartphones
python3 busca_mercadolivre.py "smartphone samsung"
```

## 📈 Resultado típico

```json
{
  "produtos": [...],
  "estatisticas": {
    "quantidade": 25,
    "minimo": 45.50,
    "maximo": 299.99,
    "media": 125.75,
    "mediana": 120.00,
    "desvio_padrao": 45.30
  },
  "fonte": "Mercado Livre"
}
```