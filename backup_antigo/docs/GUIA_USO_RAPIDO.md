# ⚡ Guia de Uso Rápido - Páginas HTML Estáticas

## 🎯 O que você vai fazer

Dividir sua planilha de materiais em 6 partes, buscar preços e gerar 6 páginas HTML interativas.

---

## 🚀 Opção 1: Tudo de Uma Vez (RECOMENDADO)

### Comando Único:

```bash
python3 processar_completo.py
```

**Isso vai:**
1. ✅ Dividir `materiais.xlsx` em 6 partes
2. ✅ Buscar preços no Mercado Livre
3. ✅ Gerar 6 páginas HTML estáticas
4. ✅ Criar página índice

**Tempo:** ~3-4 horas para 3306 materiais

**Resultado:**
- 📂 `partes/` - 6 planilhas divididas
- 📂 `paginas_html/` - 6 páginas HTML + índice

### Abrir no navegador:

```bash
xdg-open paginas_html/index.html
```

Ou arraste `paginas_html/index.html` para seu navegador.

---

## 🧪 Opção 2: Teste Primeiro (RECOMENDADO para iniciantes)

### Teste com 5 materiais:

```bash
python3 testar_paginas_estaticas.py -n 5
```

**Tempo:** ~25 segundos

**Resultado:** `teste_pagina_estatica.html`

### Abrir:

```bash
xdg-open teste_pagina_estatica.html
```

---

## 📋 Opção 3: Passo a Passo Manual

### Passo 1: Dividir a planilha

```bash
python3 dividir_planilha.py
```

**Resultado:** Pasta `partes/` com 6 arquivos:
- `materiais_parte_1.xlsx`
- `materiais_parte_2.xlsx`
- ... até parte 6

---

### Passo 2: Gerar páginas HTML

#### Opção A: Todas de uma vez
```bash
python3 gerar_paginas_estaticas.py --todas
```

#### Opção B: Uma por uma (pode processar em paralelo!)
```bash
# Terminal 1
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o paginas_html/pagina_parte_1.html -n 1

# Terminal 2
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_2.xlsx -o paginas_html/pagina_parte_2.html -n 2

# ... e assim por diante
```

**Resultado:** Pasta `paginas_html/` com:
- `index.html` (página índice)
- `pagina_parte_1.html`
- `pagina_parte_2.html`
- ... até parte 6

---

## 🌐 Usando as Páginas

### 1. Abrir
Arraste qualquer arquivo `.html` para o navegador ou use:
```bash
xdg-open paginas_html/index.html
```

### 2. Buscar Materiais
Digite no campo de busca no topo da página.

### 3. Remover Produtos Irrelevantes
Clique no botão **"✕ Remover"** em qualquer produto.

### 4. Restaurar Produtos
Clique em **"🗑️ Limpar Removidos"** para restaurar tudo.

### 5. Exportar para Excel
1. Remova produtos indesejados (opcional)
2. Clique em **"📊 Exportar para Excel"**
3. Arquivo `.xlsx` será baixado automaticamente

---

## 📊 Personalização

### Dividir em mais/menos partes:

```bash
python3 processar_completo.py -n 10  # 10 partes
python3 processar_completo.py -n 4   # 4 partes
```

### Usar arquivo diferente:

```bash
python3 processar_completo.py -i meus_dados.xlsx
```

### Customizar pastas:

```bash
python3 processar_completo.py --pasta-partes divisoes --pasta-saida htmls
```

---

## ⏱️ Tempos Estimados

| Materiais | Tempo Aproximado |
|-----------|------------------|
| 5         | ~25 segundos     |
| 50        | ~4 minutos       |
| 500       | ~40 minutos      |
| 3306      | ~3-4 horas       |

---

## 💡 Dicas Importantes

### Para processamento longo:
```bash
# Rodar em segundo plano
nohup python3 processar_completo.py > processamento.log 2>&1 &

# Monitorar progresso
tail -f processamento.log
```

### Para compartilhar resultados:
As páginas HTML funcionam **offline**! Basta:
1. Copiar a pasta `paginas_html/`
2. Enviar para quem quiser
3. Abrir `index.html` no navegador

### Para editar visualmente:
Todas as páginas permitem:
- ✅ Remover produtos
- ✅ Buscar/filtrar
- ✅ Exportar versão editada para Excel

---

## ❓ Problemas Comuns

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Arquivo não encontrado"
Verifique se `materiais.xlsx` existe:
```bash
ls -la materiais.xlsx
```

### Páginas não abrem
Use caminho completo:
```bash
# Linux/Mac
realpath paginas_html/index.html

# Copie o caminho e adicione file:// no início
# Exemplo: file:///home/user/projeto/paginas_html/index.html
```

---

## 🎯 Fluxo Recomendado

### Para iniciantes:
1. ✅ Teste com 5 materiais: `python3 testar_paginas_estaticas.py -n 5`
2. ✅ Veja se funcionou: `xdg-open teste_pagina_estatica.html`
3. ✅ Teste remover produtos e exportar
4. ✅ Se estiver bom, processe tudo: `python3 processar_completo.py`

### Para usuários experientes:
1. ✅ Divida: `python3 dividir_planilha.py -n 6`
2. ✅ Processe partes em paralelo (vários terminais)
3. ✅ Abra e edite cada página conforme necessário

---

## 📁 Estrutura Final

```
busca_precos/
├── materiais.xlsx              # Planilha original
├── partes/                     # Gerado pelo dividir_planilha.py
│   ├── materiais_parte_1.xlsx
│   ├── materiais_parte_2.xlsx
│   └── ... (até 6)
└── paginas_html/               # Gerado pelo gerar_paginas_estaticas.py
    ├── index.html              # Página índice
    ├── pagina_parte_1.html
    ├── pagina_parte_2.html
    └── ... (até 6)
```

---

## 🎉 Pronto!

Agora você tem um sistema completo para:
- ✅ Buscar preços automaticamente
- ✅ Visualizar em páginas HTML bonitas
- ✅ Remover produtos irrelevantes manualmente
- ✅ Exportar tudo para Excel
- ✅ Compartilhar facilmente (páginas funcionam offline!)

**Comece agora:**

```bash
python3 testar_paginas_estaticas.py -n 5
```

ou

```bash
python3 processar_completo.py
```

🚀 **Boa busca de preços!**

