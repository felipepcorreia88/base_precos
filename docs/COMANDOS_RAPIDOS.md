# ⚡ Comandos Rápidos

Referência rápida dos comandos mais usados.

---

## 🧪 1. Testar Sistema (PRIMEIRO PASSO)

```bash
python3 testar_paginas_estaticas.py -n 5
xdg-open teste_pagina_estatica.html
```

**Tempo:** ~25 segundos  
**Resultado:** Página de teste com 5 materiais

---

## 🎯 2. Fluxo Principal (Processar Partes)

### A. Dividir Planilha

```bash
python3 dividir_planilha.py
```

**Resultado:** Pasta `partes/` com 6 arquivos xlsx

---

### B. Processar Partes (Modo Interativo)

```bash
python3 processar_parte.py
```

**Escolha a parte** (1-6) quando solicitado.

---

### C. OU Processar Parte Específica

```bash
# Processar parte 1
python3 processar_parte.py -p 1

# Processar parte 2
python3 processar_parte.py -p 2

# ... até parte 6
python3 processar_parte.py -p 6
```

**Tempo:** ~40 minutos por parte

---

### D. Gerar Página Índice

```bash
python3 gerar_indice.py
xdg-open paginas_html/index.html
```

---

## 📊 3. Visualizar Resultados

### Abrir Página Índice

```bash
xdg-open paginas_html/index.html
```

### Abrir Parte Específica

```bash
xdg-open paginas_html/pagina_parte_1.html
```

---

## 🔧 4. Utilidades

### Ver Progresso

```bash
python3 processar_parte.py
# Modo interativo mostra status de cada parte
```

### Listar Arquivos

```bash
# Ver partes divididas
ls -lh partes/

# Ver páginas geradas
ls -lh paginas_html/

# Ver logs
ls -lh logs/
```

### Limpar Logs

```bash
find logs/ -name "*.log" -exec truncate -s 0 {} \;
```

---

## 📦 5. Instalação

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Verificar Instalação

```bash
python3 -c "import requests, bs4, pandas, openpyxl; print('✅ OK')"
```

---

## 🆘 6. Problemas Comuns

### "Module not found"

```bash
pip install -r requirements.txt
```

### "Arquivo não encontrado"

```bash
# Verificar se materiais.xlsx existe
ls -lh materiais.xlsx

# Verificar se partes foram criadas
ls -lh partes/
```

### Reprocessar uma Parte

```bash
python3 processar_parte.py -p 1
# Sobrescreve a página anterior
```

---

## 📋 7. Sequência Completa (Copie e Cole)

```bash
# 1. Testar
python3 testar_paginas_estaticas.py -n 5

# 2. Dividir
python3 dividir_planilha.py

# 3. Processar partes (uma de cada vez)
python3 processar_parte.py -p 1  # ~40 min
python3 processar_parte.py -p 2  # ~40 min
python3 processar_parte.py -p 3  # ~40 min
python3 processar_parte.py -p 4  # ~40 min
python3 processar_parte.py -p 5  # ~40 min
python3 processar_parte.py -p 6  # ~40 min

# 4. Gerar índice
python3 gerar_indice.py

# 5. Abrir
xdg-open paginas_html/index.html
```

---

## ⏱️ 8. Estimativas de Tempo

| Ação | Tempo |
|------|-------|
| Teste (5 materiais) | ~25 segundos |
| Dividir planilha | Instantâneo |
| Processar 1 parte (~551 materiais) | ~40 minutos |
| Processar 6 partes (sequencial) | ~4 horas |
| Gerar índice | Instantâneo |
| Validar uma parte | 5-15 minutos |

---

## 💡 9. Dicas

### Processar em Paralelo (Avançado)

Abra 6 terminais e execute simultaneamente:

```bash
# Terminal 1
python3 processar_parte.py -p 1

# Terminal 2
python3 processar_parte.py -p 2

# ... (até 6)
```

**Reduz tempo total para ~40 minutos!**

### Pausar e Continuar

Você pode processar partes 1-3 hoje e 4-6 amanhã.  
O sistema rastreia o que já foi processado.

---

## 📖 10. Mais Informações

- **Início rápido:** `INICIO_AQUI.md`
- **Fluxo detalhado:** `FLUXO_RECOMENDADO.md`
- **Visão geral:** `README.md`
- **Estrutura:** `ESTRUTURA.md`

---

**Última atualização:** $(date '+%Y-%m-%d')

