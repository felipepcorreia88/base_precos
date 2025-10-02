# 📊 Visualizador de Materiais - Interface Web

Interface web moderna para visualizar os dados coletados pelo `busca_materiais_planilha.py`.

## 🚀 Funcionalidades

- ✅ **Dashboard Estatístico**: Resumo completo com estatísticas gerais
- ✅ **Lista Interativa**: Todos os materiais da planilha em cards expansíveis
- ✅ **Busca em Tempo Real**: Filtre materiais por nome
- ✅ **Ordenação Flexível**: Ordene por nome, quantidade de produtos ou preços
- ✅ **Detalhes Completos**: Veja todos os produtos e links para cada material
- ✅ **Design Responsivo**: Funciona perfeitamente em desktop e mobile
- ✅ **Interface Moderna**: Cards expansíveis com animações suaves

## 📋 Pré-requisitos

```bash
# Certifique-se de ter as dependências instaladas
pip install -r requirements.txt
```

## 🛠️ Como Usar

### 1. Uso Básico

```bash
# Visualizar planilha gerada pelo busca_materiais_planilha.py
python3 visualizador_materiais.py teste_materiais_precos.xlsx
```

### 2. Especificar Porta

```bash
# Usar porta personalizada (padrão: 5001)
python3 visualizador_materiais.py materiais_com_precos.xlsx --port 8080
```

### 3. Especificar Host

```bash
# Permitir acesso externo
python3 visualizador_materiais.py dados.xlsx --host 0.0.0.0 --port 5001
```

## 🌐 Acessando a Interface

Após iniciar o servidor, acesse no navegador:

```
http://localhost:5001
```

Ou se estiver em outra máquina na rede:

```
http://IP_DO_SERVIDOR:5001
```

## 📊 Interface do Usuário

### Dashboard Estatístico

No topo da página você encontra cards com:
- **Total de Materiais**: Quantidade total processada
- **Com Produtos**: Materiais que tiveram produtos encontrados
- **Sem Produtos**: Materiais sem resultados
- **Total de Produtos**: Soma de todos os produtos encontrados
- **Preço Médio Geral**: Média de todos os preços
- **Preço Mínimo/Máximo**: Range de preços encontrados

### Controles

- **🔍 Busca**: Digite para filtrar materiais por nome em tempo real
- **Ordenar por**: Nome, Produtos, Preço Médio, Preço Mínimo
- **Ordem**: Crescente ou Decrescente

### Cards de Materiais

Cada material é exibido em um card que mostra:
- **Nome do Material**
- **Quantidade de Produtos** encontrados
- **Preço Médio** (se disponível)
- **Status da Busca** (sucesso, erro, sem produtos)

**Clique no card** para expandir e ver:
- **Resumo de Preços**: Média, Mediana, Mínimo, Máximo, Desvio Padrão, Outliers
- **Lista de Produtos**: Todos os produtos com nome, preço e link direto

## 📁 Estrutura de Dados Esperada

O visualizador espera uma planilha Excel (`.xlsx`) com as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Nome` | String | Nome do material |
| `Total_Produtos_Encontrados` | Integer | Quantidade de produtos encontrados |
| `Preco_Minimo` | Float | Menor preço encontrado |
| `Preco_Maximo` | Float | Maior preço encontrado |
| `Preco_Medio` | Float | Preço médio (após filtro) |
| `Preco_Mediana` | Float | Preço mediano |
| `Desvio_Padrao` | Float | Desvio padrão dos preços |
| `Outliers_Removidos` | Integer | Quantidade de outliers removidos |
| `Links_Produtos_JSON` | String (JSON) | Array JSON com produtos |
| `Status_Busca` | String | Status da busca |
| `Data_Hora_Busca` | String | Data e hora da busca |

### Formato do JSON em Links_Produtos_JSON

```json
[
  {
    "nome": "Nome do Produto",
    "preco": 99.90,
    "link": "https://produto.mercadolivre.com.br/..."
  },
  {
    "nome": "Outro Produto",
    "preco": 149.90,
    "link": "https://produto.mercadolivre.com.br/..."
  }
]
```

## 🔧 API Endpoints

O visualizador expõe APIs REST para integração:

### GET /api/resumo

Retorna estatísticas gerais:

```json
{
  "total_materiais": 100,
  "materiais_com_produtos": 85,
  "materiais_sem_produtos": 15,
  "total_produtos_encontrados": 2500,
  "preco_medio_geral": 125.50,
  "preco_minimo_geral": 10.00,
  "preco_maximo_geral": 999.90
}
```

### GET /api/materiais

Retorna lista de materiais com filtros:

**Parâmetros de Query:**
- `filtro` (string): Termo para filtrar por nome
- `ordenar_por` (string): Campo para ordenar (Nome, Total_Produtos_Encontrados, Preco_Medio, etc.)
- `ordem` (string): `asc` ou `desc`

**Resposta:**

```json
{
  "materiais": [
    {
      "nome": "Material 1",
      "total_produtos": 25,
      "preco_minimo": 45.50,
      "preco_maximo": 299.99,
      "preco_medio": 125.75,
      "preco_mediana": 120.00,
      "desvio_padrao": 45.30,
      "outliers_removidos": 3,
      "status": "sucesso",
      "data_busca": "2025-10-02 10:30:00",
      "produtos_json": [...]
    }
  ],
  "total": 100
}
```

## 🎨 Recursos da Interface

- **Cards Expansíveis**: Clique para ver detalhes de cada material
- **Busca Instantânea**: Filtro em tempo real enquanto você digita
- **Ordenação Dinâmica**: Mude a ordenação sem recarregar a página
- **Links Diretos**: Acesse produtos diretamente no Mercado Livre
- **Status Coloridos**: Verde (sucesso), Vermelho (erro), Amarelo (sem produtos)
- **Animações Suaves**: Transições elegantes ao expandir/recolher
- **Design Responsivo**: Adapta-se a qualquer tamanho de tela

## 💡 Exemplos de Uso

### Exemplo 1: Visualizar Teste Pequeno

```bash
# Primeiro execute uma busca pequena
python3 teste_busca_pequena.py 5

# Depois visualize o resultado
python3 visualizador_materiais.py teste_materiais_precos.xlsx
```

### Exemplo 2: Visualizar Processamento Completo

```bash
# Visualizar arquivo completo com 3306 materiais
python3 visualizador_materiais.py materiais_com_precos_20251002_143000.xlsx
```

### Exemplo 3: Servidor em Produção

```bash
# Executar em servidor com acesso externo
python3 visualizador_materiais.py dados.xlsx --host 0.0.0.0 --port 80
```

## ⚠️ Observações

- O servidor roda em modo debug por padrão (ideal para desenvolvimento)
- Para produção, considere usar Gunicorn ou uWSGI
- O arquivo Excel deve estar no formato correto (gerado por `busca_materiais_planilha.py`)
- Arquivos grandes podem levar alguns segundos para carregar
- A interface carrega dados via API REST de forma assíncrona

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"

```bash
# Verifique se o arquivo existe
ls -lh *.xlsx

# Use caminho absoluto se necessário
python3 visualizador_materiais.py /caminho/completo/arquivo.xlsx
```

### Erro: "Coluna não encontrada"

Certifique-se de que a planilha foi gerada por `busca_materiais_planilha.py` e contém todas as colunas necessárias.

### Porta já em uso

```bash
# Use outra porta
python3 visualizador_materiais.py arquivo.xlsx --port 5002
```

## 🔗 Integração com Outros Scripts

Este visualizador é projetado para trabalhar com:

- ✅ `busca_materiais_planilha.py` - Gerador dos dados
- ✅ `teste_busca_pequena.py` - Testes pequenos
- ✅ `exemplo_uso.py` - Interface CLI

## 📞 Suporte

Para mais informações sobre o sistema completo, veja:
- `README.md` - Sistema de busca web
- `README_BUSCA_MATERIAIS.md` - Sistema de processamento de planilhas

