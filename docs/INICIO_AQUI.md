# 🚀 COMECE AQUI - Sistema de Busca de Preços

## ⚡ Teste Rápido (30 segundos)

```bash
python3 testar_paginas_estaticas.py -n 5
xdg-open teste_pagina_estatica.html
```

Isso vai:
1. Buscar preços de 5 materiais (~25 segundos)
2. Gerar uma página HTML com os resultados
3. Você poderá remover produtos e exportar para Excel

---

## 🎯 Opção A: Processar Uma Parte de Cada Vez ⭐ RECOMENDADO

### Modo Interativo (escolhe a parte):
```bash
python3 processar_parte.py
```

### Ou especifique a parte:
```bash
# Processar parte 1
python3 processar_parte.py -p 1

# Depois processar parte 2
python3 processar_parte.py -p 2

# ... e assim por diante
```

**Vantagens:**
- ✅ Processa e valida uma parte por vez
- ✅ Pode parar e continuar depois
- ✅ Menor risco de perda de dados
- ✅ ~40 minutos por parte (6 partes)

**Fluxo:**
1. Processa parte 1 → Valida → Exporta Excel
2. Processa parte 2 → Valida → Exporta Excel
3. ... (repete até parte 6)

---

## 🚀 Opção B: Processar Tudo de Uma Vez (3-4 horas)

```bash
python3 processar_completo.py
```

Isso vai:
1. Dividir `materiais.xlsx` em 6 partes
2. **Buscar preços** de todos os materiais (3-4 horas)
3. Gerar 6 páginas HTML estáticas
4. Criar página índice

Depois abra:
```bash
xdg-open paginas_html/index.html
```

---

## ⚠️ Como Funciona?

### Etapa 1: Script Python Busca Preços (DEMORA!)
- Script acessa Mercado Livre
- Busca produtos para cada material (~3 segundos/material)
- Filtra com modo inteligente
- **Tempo total: ~3-4 horas para 3306 materiais**

### Etapa 2: Script Gera Página HTML
- Salva todos os produtos no HTML
- Página funciona offline (dados embutidos)
- **Tempo: instantâneo**

### Etapa 3: Você Valida Manualmente
- Abre página HTML no navegador
- Vê todos os produtos já coletados
- Remove produtos irrelevantes com um clique
- Exporta Excel com dados filtrados

---

## 📚 Documentação

- 📖 **`README_FLUXO.md`** - Entenda o fluxo completo
- 📖 **`docs/GUIA_USO_RAPIDO.md`** - Guia prático
- 📖 **`docs/README_PAGINAS_ESTATICAS.md`** - Documentação técnica
- 📖 **`README.md`** - Visão geral do sistema

---

## 🎯 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `testar_paginas_estaticas.py` | Teste rápido com N materiais |
| `processar_completo.py` | Processa tudo automaticamente |
| `dividir_planilha.py` | Divide materiais.xlsx em partes |
| `gerar_paginas_estaticas.py` | Busca preços + Gera HTML |

---

## ✅ Estrutura do Resultado

```
paginas_html/
├── index.html              ← Abra este
├── pagina_parte_1.html     ← Dados da parte 1
├── pagina_parte_2.html     ← Dados da parte 2
└── ... (até parte 6)
```

Cada página permite:
- ✅ Ver todos os produtos já buscados
- ✅ Buscar/filtrar materiais
- ✅ Remover produtos irrelevantes
- ✅ Exportar para Excel

---

## 🎬 Comandos Principais

### 1️⃣ Teste Rápido (5 materiais, ~25 segundos):
```bash
python3 testar_paginas_estaticas.py -n 5
```

### 2️⃣ Dividir em Partes:
```bash
python3 dividir_planilha.py -n 6
```

### 3️⃣ Processar Parte por Parte (RECOMENDADO):
```bash
# Modo interativo
python3 processar_parte.py

# Ou especifique a parte
python3 processar_parte.py -p 1  # Processa parte 1
python3 processar_parte.py -p 2  # Processa parte 2
# ... até parte 6
```

### 4️⃣ Gerar Página Índice:
```bash
python3 gerar_indice.py
```

### 5️⃣ OU Processar Tudo de Uma Vez (~3-4 horas):
```bash
python3 processar_completo.py
```

---

## ❓ Dúvidas Comuns

### "A busca é em tempo real na página?"
❌ **NÃO!** O script Python busca tudo **antes** de gerar o HTML. A página já tem todos os dados embutidos.

### "Quanto tempo demora?"
- Teste (5 materiais): ~25 segundos
- Completo (3306 materiais): ~3-4 horas

### "Preciso de servidor para abrir as páginas?"
❌ **NÃO!** As páginas funcionam offline. Basta abrir o arquivo `.html` no navegador.

### "Posso compartilhar as páginas?"
✅ **SIM!** Copie a pasta `paginas_html/` e envie. As páginas funcionam em qualquer computador.

---

## 🚀 Pronto para Começar?

**Execute agora:**

```bash
python3 testar_paginas_estaticas.py -n 5
```

ou leia a documentação completa:

```bash
cat README_FLUXO.md
```

---

**Boa busca de preços! 🎯**

