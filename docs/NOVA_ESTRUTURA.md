# 📂 Nova Estrutura do Projeto

## ✅ Reorganização Completa

O projeto foi reorganizado em uma estrutura profissional com subdiretórios claros e separação de responsabilidades.

---

## 📁 Estrutura Completa

```
busca_precos/
│
├── 📄 RAIZ (Apenas arquivos principais)
│   ├── README.md                    # Documentação principal
│   ├── materiais.xlsx               # Planilha de dados (3306 materiais)
│   ├── requirements.txt             # Dependências Python
│   ├── .gitignore                   # Arquivos ignorados pelo Git
│   │
│   └── 🔧 Scripts Wrapper (facilitam execução)
│       ├── dividir.sh               # ./dividir.sh
│       ├── processar.sh             # ./processar.sh -p 1
│       ├── processar_api.sh         # ./processar_api.sh -p 1
│       └── gerar_indice.sh          # ./gerar_indice.sh
│
├── 📂 scripts/                      # Todos os scripts Python
│   ├── dividir_planilha.py
│   ├── processar_parte.py
│   ├── processar_parte_api.py       # ⭐ Recomendado
│   ├── gerar_indice.py
│   ├── gerar_paginas_estaticas.py
│   ├── gerar_paginas_estaticas_api.py
│   ├── testar_paginas_estaticas.py
│   │
│   └── core/                        # Módulos principais
│       ├── busca_materiais_planilha_inteligente.py
│       └── busca_materiais_api_ml.py
│
├── 📂 docs/                         # Toda a documentação
│   ├── LEIA_PRIMEIRO.txt            # 🚀 Comece aqui
│   ├── INICIO_AQUI.md
│   ├── FLUXO_RECOMENDADO.md
│   ├── SOLUCAO_PROBLEMAS.md
│   ├── COMANDOS_RAPIDOS.md
│   ├── ESTRUTURA.md
│   ├── RESUMO_SOLUCOES.txt
│   └── NOVA_ESTRUTURA.md            # Este arquivo
│
├── 📂 templates/                    # Templates HTML
│   └── pagina_estatica.html
│
├── 📂 output/                       # Tudo que é gerado
│   ├── partes/                      # Planilhas divididas
│   │   ├── materiais_parte_1.xlsx
│   │   └── ... (até 6)
│   │
│   ├── paginas_html/                # Páginas geradas
│   │   ├── index.html
│   │   ├── pagina_parte_1.html
│   │   └── ... (até 6)
│   │
│   └── logs/                        # Logs de execução
│       ├── busca_materiais_inteligente.log
│       └── busca_materiais_api_ml.log
│
└── 📂 backup_antigo/                # Scripts antigos (não usar)
```

---

## 🎯 Como Usar a Nova Estrutura

### Opção 1: Scripts Wrapper (Mais Fácil)

Execute da **raiz** do projeto:

```bash
# Dividir planilha
./dividir.sh

# Processar parte com API
./processar_api.sh -p 1

# Gerar índice
./gerar_indice.sh

# Visualizar
xdg-open output/paginas_html/index.html
```

---

### Opção 2: Python Direto

Execute do diretório **scripts/**:

```bash
cd scripts

# Dividir
python3 dividir_planilha.py

# Processar
python3 processar_parte_api.py -p 1

# Gerar índice
python3 gerar_indice.py

# Voltar à raiz
cd ..
xdg-open output/paginas_html/index.html
```

---

## 📊 Caminhos Atualizados

Todos os scripts foram ajustados para usar os novos caminhos:

| Tipo | Caminho Antigo | Caminho Novo |
|------|----------------|--------------|
| Partes | `partes/` | `output/partes/` |
| HTML | `paginas_html/` | `output/paginas_html/` |
| Logs | `logs/` | `output/logs/` |
| Scripts | Raiz | `scripts/` |
| Módulos | Raiz | `scripts/core/` |
| Docs | Raiz | `docs/` |

---

## 🔧 Ajustes Realizados

### 1. Scripts Python
- ✅ Movidos para `scripts/`
- ✅ Módulos principais em `scripts/core/`
- ✅ Imports ajustados (`sys.path.insert`)
- ✅ Caminhos de templates ajustados (`../templates/`)
- ✅ Caminhos de output ajustados (`output/`)

### 2. Logs
- ✅ Agora salvam em `output/logs/`
- ✅ Logging configurado nos módulos core

### 3. Templates
- ✅ Mantidos em `templates/` (raiz relativa)
- ✅ Scripts acessam via caminho relativo

### 4. Documentação
- ✅ Toda em `docs/`
- ✅ Organizada por tópico

### 5. Scripts Wrapper
- ✅ Criados na raiz (`.sh`)
- ✅ Executáveis (`chmod +x`)
- ✅ Facilitam uso sem navegar pastas

---

## 📋 Vantagens da Nova Estrutura

### ✅ Organização
- Raiz limpa (apenas arquivos essenciais)
- Separação clara de responsabilidades
- Fácil navegação

### ✅ Manutenção
- Scripts agrupados em `scripts/`
- Módulos core isolados
- Documentação centralizada

### ✅ Uso
- Scripts wrapper facilitam execução
- Caminhos relativos funcionam de qualquer lugar
- Output separado do código fonte

### ✅ Versionamento
- `.gitignore` atualizado
- Output não versionado
- Código limpo no Git

---

## 🧪 Teste Rápido

Verifique se tudo funciona:

```bash
# Da raiz
./dividir.sh

# Deve criar: output/partes/materiais_parte_1.xlsx, etc.

# Processar uma parte
./processar_api.sh -p 1

# Deve criar: output/paginas_html/pagina_parte_1_api.html

# Gerar índice
./gerar_indice.sh

# Deve criar: output/paginas_html/index.html

# Visualizar
xdg-open output/paginas_html/index.html
```

---

## 🔄 Migração

Se você tinha arquivos na estrutura antiga:

```bash
# Já foi feito automaticamente, mas para referência:

# Partes antigas -> nova localização
# mv partes/* output/partes/

# Páginas antigas -> nova localização
# mv paginas_html/* output/paginas_html/

# Logs antigos -> nova localização  
# mv logs/* output/logs/
```

---

## 📚 Documentação Relacionada

- `docs/LEIA_PRIMEIRO.txt` - Início rápido
- `docs/COMANDOS_RAPIDOS.md` - Referência de comandos
- `docs/SOLUCAO_PROBLEMAS.md` - Soluções implementadas
- `README.md` (raiz) - Visão geral atualizada

---

## ⚠️ Importante

### Scripts Wrapper
Os scripts `.sh` na raiz são **wrappers** que:
- Navegam para o diretório correto
- Executam o Python correspondente
- Passam todos os argumentos

**Exemplo:**
```bash
./processar_api.sh -p 1
# Equivale a:
# cd <raiz> && python3 scripts/processar_parte_api.py -p 1
```

### Caminhos Relativos
Todos os scripts funcionam com caminhos relativos:
- `output/partes/` ao invés de `partes/`
- `output/paginas_html/` ao invés de `paginas_html/`
- `output/logs/` ao invés de `logs/`

### Imports
Módulos core são importados dinamicamente:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from busca_materiais_api_ml import BuscadorAPIML
```

---

## ✅ Checklist

Após reorganização, verifique:

- [ ] Scripts `.sh` são executáveis (`chmod +x *.sh`)
- [ ] Pasta `output/` existe com subpastas
- [ ] Pasta `scripts/core/` tem os módulos
- [ ] Pasta `docs/` tem toda documentação
- [ ] Pasta `templates/` tem o HTML
- [ ] `.gitignore` atualizado
- [ ] README.md atualizado
- [ ] Teste rápido funciona

---

**✅ Estrutura reorganizada com sucesso!**

```bash
./dividir.sh
./processar_api.sh -p 1
./gerar_indice.sh
```

