# 🔄 Fluxo de Trabalho - Sistema de Busca de Preços

## 📋 Resumo do Fluxo

```
materiais.xlsx
    ↓
[1. DIVIDIR em 6 partes]
    ↓
partes/materiais_parte_X.xlsx
    ↓
[2. BUSCAR preços (demora!)]
    ↓
[3. GERAR página HTML com dados]
    ↓
paginas_html/pagina_parte_X.html
    ↓
[4. VALIDADOR HUMANO abre página]
    ↓
[5. Remove produtos irrelevantes]
    ↓
[6. EXPORTA para Excel filtrado]
    ↓
resultado_final.xlsx ✅
```

---

## ⚠️ IMPORTANTE: Busca NÃO é em Tempo Real!

**O script PRIMEIRO busca todos os produtos, DEPOIS gera a página HTML.**

### Etapas:

1. **Script Python busca preços** (~3-4 horas para 3306 materiais)
   - Acessa Mercado Livre
   - Coleta produtos
   - Filtra com modo inteligente
   
2. **Script gera página HTML** com dados já embutidos
   - Todos os produtos ficam salvos no HTML
   - Página funciona offline
   
3. **Validador humano** abre a página no navegador
   - Vê todos os produtos já coletados
   - Remove manualmente os irrelevantes
   - Exporta Excel com dados filtrados

---

## 🚀 Comandos Principais

### Para Teste (5 materiais, ~25 segundos):

```bash
python3 testar_paginas_estaticas.py -n 5
```

**Resultado:** `teste_pagina_estatica.html` com dados já incluídos

**Abrir:**
```bash
xdg-open teste_pagina_estatica.html
```

---

### Para Processamento Completo (3306 materiais, ~3-4 horas):

```bash
python3 processar_completo.py
```

**O que acontece:**
1. ✅ Divide `materiais.xlsx` em 6 partes
2. ✅ **BUSCA preços** de todos os materiais (DEMORA!)
3. ✅ Gera 6 páginas HTML com dados embutidos
4. ✅ Cria página índice

**Resultado:** Pasta `paginas_html/` com 6 páginas prontas

**Abrir:**
```bash
xdg-open paginas_html/index.html
```

---

## 📝 Estrutura dos Scripts

### `dividir_planilha.py`
**O que faz:** Divide materiais.xlsx em N partes
**Tempo:** Instantâneo

```bash
python3 dividir_planilha.py -n 6
```

---

### `gerar_paginas_estaticas.py` ⭐
**O que faz:**
1. Lê planilha de materiais
2. **BUSCA produtos no Mercado Livre** (uma requisição por material)
3. Filtra com modo inteligente
4. Gera página HTML com **TODOS os dados embutidos**

**Tempo:** ~3 segundos por material

**Uso individual:**
```bash
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o pagina1.html -n 1
```

**Uso todas as partes:**
```bash
python3 gerar_paginas_estaticas.py --todas
```

---

### `processar_completo.py`
**O que faz:** Executa tudo automaticamente
1. Chama `dividir_planilha.py`
2. Chama `gerar_paginas_estaticas.py --todas`

```bash
python3 processar_completo.py
```

---

### `testar_paginas_estaticas.py`
**O que faz:** Teste rápido com poucos materiais

```bash
python3 testar_paginas_estaticas.py -n 5  # Teste com 5 materiais
```

---

## 🌐 Usando a Página HTML Gerada

### A página HTML contém:
- ✅ **Todos os produtos já buscados** (dados embutidos no HTML)
- ✅ Interface de busca (filtra localmente)
- ✅ Botão para remover produtos
- ✅ Botão para exportar Excel
- ✅ Estatísticas dinâmicas

### Funcionalidades:

#### 1. Buscar Material
Digite no campo de busca para filtrar a lista (busca local, instantânea)

#### 2. Remover Produto Irrelevante
Clique em **"✕ Remover"** no produto indesejado

#### 3. Restaurar Produtos
Clique em **"🗑️ Limpar Removidos"**

#### 4. Exportar para Excel
1. Remova todos os produtos irrelevantes
2. Clique em **"📊 Exportar para Excel"**
3. Arquivo `.xlsx` é baixado com apenas produtos não removidos

---

## 📂 Estrutura de Diretórios

```
busca_precos/
├── 📊 ARQUIVOS PRINCIPAIS
│   ├── materiais.xlsx                      # Planilha original
│   ├── dividir_planilha.py                 # Divide em partes
│   ├── gerar_paginas_estaticas.py          # Busca + Gera HTML
│   ├── processar_completo.py               # Faz tudo
│   └── testar_paginas_estaticas.py         # Teste rápido
│
├── 📂 GERADOS AUTOMATICAMENTE
│   ├── partes/                             # Planilhas divididas
│   │   ├── materiais_parte_1.xlsx
│   │   └── ... (até 6)
│   │
│   └── paginas_html/                       # Páginas geradas
│       ├── index.html                      # Índice
│       ├── pagina_parte_1.html             # Parte 1
│       └── ... (até 6)
│
├── 📖 DOCUMENTAÇÃO
│   └── docs/
│       ├── GUIA_USO_RAPIDO.md
│       ├── README_PAGINAS_ESTATICAS.md
│       └── ...
│
├── 🛠️ SISTEMA BASE
│   ├── busca_materiais_planilha_inteligente.py  # Motor de busca
│   ├── templates/pagina_estatica.html           # Template HTML
│   └── requirements.txt
│
└── 📁 ORGANIZAÇÃO
    ├── backup/                             # Scripts antigos
    ├── logs/                               # Logs de execução
    └── testes_antigos/                     # Testes anteriores
```

---

## ⏱️ Tempos de Processamento

| Etapa | Tempo |
|-------|-------|
| Dividir planilha | Instantâneo |
| **Buscar 1 material** | **~3 segundos** |
| **Buscar 100 materiais** | **~5 minutos** |
| **Buscar 3306 materiais** | **~3-4 horas** |
| Gerar HTML (após busca) | Instantâneo |
| Abrir página HTML | Instantâneo |
| Editar/remover produtos | Instantâneo |
| Exportar Excel | Instantâneo |

---

## 💡 Cenários de Uso

### Cenário 1: Teste Rápido
```bash
# 1. Teste com 5 materiais (~25 segundos)
python3 testar_paginas_estaticas.py -n 5

# 2. Abrir página
xdg-open teste_pagina_estatica.html

# 3. Remover produtos irrelevantes
# 4. Exportar Excel
```

---

### Cenário 2: Processar Tudo
```bash
# 1. Processar tudo (~3-4 horas)
python3 processar_completo.py

# 2. Aguardar finalização (pode deixar rodando)

# 3. Abrir página índice
xdg-open paginas_html/index.html

# 4. Para cada parte:
#    - Abrir página
#    - Remover produtos irrelevantes
#    - Exportar Excel
#    - Salvar como: parte_1_validado.xlsx, etc.
```

---

### Cenário 3: Processar em Paralelo (Avançado)
```bash
# 1. Dividir planilha
python3 dividir_planilha.py -n 6

# 2. Processar cada parte em terminal diferente (PARALELO!)
# Terminal 1:
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o paginas_html/pagina_parte_1.html -n 1

# Terminal 2:
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_2.xlsx -o paginas_html/pagina_parte_2.html -n 2

# ... e assim por diante (6 terminais)

# 3. Cada parte levará ~40 minutos (551 materiais * 3s)
# 4. Total: ~40 minutos (vs 3-4 horas sequencial)
```

---

## 🎯 Resumo Final

**Fluxo completo:**
1. ✅ Execute: `python3 processar_completo.py`
2. ✅ Aguarde 3-4 horas (deixe rodando)
3. ✅ Abra: `paginas_html/index.html`
4. ✅ Para cada parte:
   - Abra a página
   - Remova produtos irrelevantes
   - Exporte Excel
5. ✅ Pronto! 6 arquivos Excel validados

**A página HTML:**
- ❌ **NÃO** busca em tempo real
- ✅ **JÁ TEM** todos os produtos embutidos
- ✅ Funciona 100% offline
- ✅ Permite edição manual
- ✅ Exporta Excel filtrado

---

**Pronto para começar? Execute:**

```bash
python3 testar_paginas_estaticas.py -n 5
```

ou

```bash
python3 processar_completo.py
```

