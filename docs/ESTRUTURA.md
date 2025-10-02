# 📂 Estrutura do Projeto

Última atualização: $(date '+%Y-%m-%d')

## 🎯 Arquivos Essenciais

### Scripts Python (Ordem de Uso)

```
1. dividir_planilha.py           - Divide materiais.xlsx em 6 partes
2. processar_parte.py            - ⭐ Processa uma parte de cada vez
3. gerar_indice.py               - Gera index.html com links
4. testar_paginas_estaticas.py   - Teste rápido (5 materiais)
```

### Scripts de Suporte

```
busca_materiais_planilha_inteligente.py  - Motor de busca (usado internamente)
gerar_paginas_estaticas.py               - Motor de geração HTML (usado internamente)
```

### Dados

```
materiais.xlsx                   - Planilha original (3306 materiais)
```

### Documentação

```
README.md                        - Visão geral do sistema
INICIO_AQUI.md                   - 🚀 Comece por aqui!
FLUXO_RECOMENDADO.md            - Fluxo detalhado parte por parte
ESTRUTURA.md                     - Este arquivo
```

### Infraestrutura

```
templates/
  └── pagina_estatica.html       - Template para páginas geradas

requirements.txt                 - Dependências Python

logs/                            - Logs de execução
  ├── busca_materiais_inteligente.log
  ├── busca_materiais_otimizado.log
  └── ...

.gitignore                       - Arquivos ignorados pelo Git
```

---

## 📦 Pastas Geradas (não versionadas)

Estas pastas são criadas automaticamente quando você executa os scripts:

```
partes/                          - Planilhas divididas (gerado por dividir_planilha.py)
  ├── materiais_parte_1.xlsx
  ├── materiais_parte_2.xlsx
  └── ... (até 6)

paginas_html/                    - Páginas HTML (gerado por processar_parte.py)
  ├── index.html
  ├── pagina_parte_1.html
  ├── pagina_parte_2.html
  └── ... (até 6)
```

---

## 🗂️ Backup de Arquivos Antigos

```
backup_antigo/                   - Scripts e documentação antiga
  ├── README_BACKUP.md           - Informações sobre o backup
  ├── processar_completo.py      - (alternativa não recomendada)
  ├── visualizador_materiais.py  - (Flask - não necessário)
  ├── backup_original/           - Módulos antigos
  ├── testes_antigos/            - Scripts de teste anteriores
  └── docs/                      - Documentação antiga
```

**Nota:** Arquivos em `backup_antigo/` NÃO são necessários para funcionamento.

---

## 🎯 Tamanho dos Arquivos

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `busca_materiais_planilha_inteligente.py` | ~16 KB | Motor de busca |
| `gerar_paginas_estaticas.py` | ~11 KB | Gerador de HTML |
| `processar_parte.py` | ~8 KB | Script principal |
| `gerar_indice.py` | ~7 KB | Gerador de índice |
| `FLUXO_RECOMENDADO.md` | ~6 KB | Documentação |
| `README.md` | ~5 KB | Visão geral |
| `INICIO_AQUI.md` | ~4 KB | Guia rápido |
| `testar_paginas_estaticas.py` | ~4 KB | Script de teste |
| `dividir_planilha.py` | ~3 KB | Divisor de planilha |
| `materiais.xlsx` | ~72 KB | Dados (3306 linhas) |

---

## 📊 Fluxo de Arquivos

```
materiais.xlsx
    ↓
[dividir_planilha.py]
    ↓
partes/materiais_parte_X.xlsx
    ↓
[processar_parte.py]
    ↓
paginas_html/pagina_parte_X.html
    ↓
[gerar_indice.py]
    ↓
paginas_html/index.html
```

---

## 🔧 Dependências (requirements.txt)

```
requests>=2.25.1       - Requisições HTTP
beautifulsoup4>=4.9.3  - Parse HTML
lxml>=4.6.3            - Parser XML/HTML
flask>=2.0.1           - (não usado no fluxo principal)
pandas>=1.3.0          - Manipulação de dados
openpyxl>=3.0.0        - Leitura/escrita Excel
```

---

## 📁 Estrutura Visual

```
busca_precos/
│
├── 📝 SCRIPTS
│   ├── dividir_planilha.py               (3 KB)
│   ├── processar_parte.py                (8 KB) ⭐
│   ├── gerar_indice.py                   (7 KB)
│   ├── gerar_paginas_estaticas.py        (11 KB)
│   ├── testar_paginas_estaticas.py       (4 KB)
│   └── busca_materiais_planilha_inteligente.py (16 KB)
│
├── 📊 DADOS
│   └── materiais.xlsx                    (72 KB)
│
├── 📖 DOCS
│   ├── README.md                         (5 KB)
│   ├── INICIO_AQUI.md                    (4 KB)
│   ├── FLUXO_RECOMENDADO.md             (6 KB)
│   └── ESTRUTURA.md                      (este arquivo)
│
├── 🛠️ INFRA
│   ├── templates/
│   │   └── pagina_estatica.html
│   ├── requirements.txt
│   ├── .gitignore
│   └── logs/
│
├── 📦 GERADOS (não versionados)
│   ├── partes/
│   └── paginas_html/
│
└── 🗄️ BACKUP
    └── backup_antigo/
```

---

## 🎯 Total de Arquivos

**Essenciais:** 14 arquivos
- 6 scripts Python
- 3 documentos Markdown
- 1 planilha de dados
- 1 template HTML
- 1 arquivo de dependências
- 1 .gitignore
- 1 arquivo de estrutura

**Pastas:** 4
- templates/ (1 arquivo)
- logs/ (vazia/limpa)
- backup_antigo/ (arquivos antigos)
- .git/ (controle de versão)

---

## ✅ Checklist de Arquivos Necessários

Verifique se você tem todos estes arquivos:

- [ ] `dividir_planilha.py`
- [ ] `processar_parte.py`
- [ ] `gerar_indice.py`
- [ ] `gerar_paginas_estaticas.py`
- [ ] `testar_paginas_estaticas.py`
- [ ] `busca_materiais_planilha_inteligente.py`
- [ ] `materiais.xlsx`
- [ ] `templates/pagina_estatica.html`
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] `INICIO_AQUI.md`
- [ ] `FLUXO_RECOMENDADO.md`

Se algum arquivo estiver faltando, verifique em `backup_antigo/`.

---

**Última limpeza:** $(date '+%Y-%m-%d %H:%M:%S')
**Arquivos movidos para backup:** Ver `backup_antigo/README_BACKUP.md`

