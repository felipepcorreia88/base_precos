# 🧠 Sistema de Busca Inteligente de Preços

Sistema avançado para busca automatizada de preços de materiais com **filtro inteligente** que elimina produtos irrelevantes.

## 🎯 Funcionalidade Principal

**FILTRO FLEXÍVEL**: Confia no mecanismo de busca do Mercado Livre e pontua produtos por relevância ao invés de eliminá-los. Mais produtos, melhor cobertura, ainda ordenados por relevância!

## 🔄 Fluxo de Trabalho

```
materiais.xlsx → [DIVIDIR] → [BUSCAR preços] → [GERAR HTML] → [VALIDAR manualmente] → [EXPORTAR Excel]
```

⚠️ **IMPORTANTE:** A busca de preços **NÃO é em tempo real**! O script Python **primeiro busca** todos os produtos (~3-4 horas), **depois** gera páginas HTML com os dados já embutidos. O validador humano abre a página HTML, remove produtos irrelevantes e exporta para Excel.

📖 **Veja fluxo detalhado:** `docs/README_FLUXO.md` (se existir) ou use os scripts wrapper na raiz.

## 📁 Estrutura do Projeto (Reorganizada)

```
busca_precos/
├── 📄 ARQUIVOS PRINCIPAIS (RAIZ)
│   ├── README.md                    # Este arquivo
│   ├── materiais.xlsx               # Planilha original (3306 materiais)
│   ├── requirements.txt             # Dependências Python
│   └── *.sh                         # Scripts wrapper (facilitadores)
│
├── 📂 scripts/                      # Scripts Python
│   ├── dividir_planilha.py          # Divide em partes
│   ├── processar_parte.py           # Processa com scraping
│   ├── gerar_indice.py              # Gera página índice
│   ├── gerar_paginas_estaticas.py   # Motor geração HTML
│   ├── testar_paginas_estaticas.py  # Teste rápido
│   └── core/                        # Módulos principais
│       └── busca_materiais_planilha_inteligente.py
│
├── 📂 docs/                         # Documentação
│   ├── LEIA_PRIMEIRO.txt            # 🚀 Comece aqui
│   ├── INICIO_AQUI.md               # Guia rápido
│   ├── FLUXO_RECOMENDADO.md        # Fluxo parte por parte
│   ├── SOLUCAO_PROBLEMAS.md        # Soluções implementadas
│   ├── COMANDOS_RAPIDOS.md         # Referência rápida
│   └── RESUMO_SOLUCOES.txt         # Resumo visual
│
├── 📂 templates/                    # Templates HTML
│   └── pagina_estatica.html
│
├── 📂 output/                       # Arquivos gerados
│   ├── partes/                      # Planilhas divididas
│   ├── paginas_html/                # Páginas HTML geradas
│   └── logs/                        # Logs de execução
│
└── 📂 backup_antigo/                # Scripts antigos
```

## 🚀 Como Usar (Simplificado)

### 🧪 Teste Rápido

```bash
./dividir.sh                    # Dividir planilha em 6 partes (padrão)
./dividir.sh -n 3              # Ou dividir em 3 partes
./processar.sh -p 1            # Processar parte 1 com scraping
```

Ou use Python diretamente:
```bash
cd scripts
python3 dividir_planilha.py
python3 processar_parte_api.py -p 1
```

### 🎯 Divisão Configurável

```bash
# Escolha o número de partes ideal:
./dividir.sh                # 6 partes (padrão) - ~551 materiais/parte
./dividir.sh -n 3          # 3 partes - ~1102 materiais/parte (mais lento)
./dividir.sh -n 10         # 10 partes - ~330 materiais/parte (mais rápido)
./dividir.sh -n 20         # 20 partes - ~165 materiais/parte (muito rápido)

# Ou use Python diretamente:
cd scripts
python3 dividir_planilha.py -n 10
```

**Dica:** Mais partes = processamento mais rápido em paralelo, mas mais arquivos para gerenciar.

### 🎯 Processamento Completo

```bash
# 1. Dividir (escolha o número de partes)
./dividir.sh -n 10

# 2. Processar todas as partes
./processar.sh -p 1
./processar.sh -p 2
./processar.sh -p 3
# ... até parte 10

# 3. Gerar índice
./gerar_indice.sh

# 4. Visualizar
xdg-open output/paginas_html/index.html
```

## 📊 Sistema de Pontuação

O sistema pontua produtos de 0.3 a 1.0:
- **1.0** ⭐⭐⭐⭐⭐ - Tem todas as palavras buscadas
- **0.8** ⭐⭐⭐⭐ - Tem maioria das palavras
- **0.6** ⭐⭐⭐ - Tem algumas palavras
- **0.3** ⭐ - Mercado Livre achou relevante

**Todos os produtos são mantidos**, ordenados por score!

## ⏱️ Tempo de Execução

| Materiais | Tempo (Scraping) |
|-----------|------------------|
| 5         | ~25 segundos |
| 551 (1 parte) | ~40 minutos |
| 3306 (6 partes) | ~4 horas |

### 📊 Recomendações de Divisão (3306 materiais)
| Partes | Materiais/Parte | Sequencial (scraping) | Paralelo (scraping) |
|--------|-----------------|----------------------|---------------------|
| 20 ⚡  | ~165            | ~2h 20min            | ~7 min              |
| 10 ⭐  | ~330            | ~5h 30min            | ~14 min             |
| 6 📦   | ~551            | ~4h                  | ~40 min             |
| 3 🐢   | ~1102           | ~5h 30min            | ~1h 50min           |

**Dica:** Mais partes = processamento paralelo mais rápido + menor risco de bloqueio!

## 📋 Dependências

```bash
pip install -r requirements.txt
```

## 📚 Documentação

- `docs/LEIA_PRIMEIRO.txt` - 🚀 **Comece por aqui!**
- `docs/INICIO_AQUI.md` - Guia de início rápido
- `docs/SOLUCAO_PROBLEMAS.md` - Soluções para problemas comuns
- `docs/COMANDOS_RAPIDOS.md` - Referência de comandos

## 🗂️ Diretórios Importantes

- **`output/partes/`** - (gerado) Planilhas divididas (materiais_parte_1.xlsx, etc.)
- **`output/paginas_html/`** - (gerado) Páginas HTML estáticas com resultados
- **`output/logs/`** - Logs de execução para debug
- **`backup_antigo/`** - Scripts e documentação antiga (não necessários)

## ✨ Comandos Recomendados

### 🧪 Teste Rápido (5 materiais)
```bash
cd scripts
python3 testar_paginas_estaticas.py -n 5
```

### 🚀 Processamento Recomendado
```bash
# Da raiz
./dividir.sh -n 10
./processar.sh -p 1
./gerar_indice.sh

# Ou do diretório scripts
cd scripts
python3 dividir_planilha.py -n 10
python3 processar_parte.py -p 1
python3 gerar_indice.py
```

## 🆕 Sistema de Páginas Estáticas

**NOVO:** Agora você pode gerar **páginas HTML estáticas** que:
- ✅ Funcionam sem servidor (abra direto no navegador)
- ✅ Permitem remover produtos irrelevantes manualmente
- ✅ Exportam para Excel com os dados filtrados (1 material por linha + JSON)
- ✅ Mostram estatísticas completas (média, mediana, moda, desvio padrão)
- ✅ Totalmente portáveis e compartilháveis

📖 **Documentação completa:** `docs/SOLUCAO_PROBLEMAS.md`

---

**🎯 Resultado:** Sistema com **FILTRO FLEXÍVEL** - confia no Mercado Livre e dá mais opções de produtos!
