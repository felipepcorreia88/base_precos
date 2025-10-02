# 🎯 Fluxo Recomendado - Processar Partes Individualmente

## ⭐ Por que processar uma parte de cada vez?

- ✅ **Menor risco**: Se algo der errado, só perde uma parte
- ✅ **Valida enquanto processa**: Pode validar parte 1 enquanto processa parte 2
- ✅ **Flexibilidade**: Pode parar e continuar depois
- ✅ **Melhor organização**: Trabalha com um conjunto menor de materiais por vez

---

## 📋 Passo a Passo Completo

### **Passo 1: Dividir a Planilha**

```bash
python3 dividir_planilha.py -n 6
```

**Resultado:** Pasta `partes/` com 6 arquivos:
- `materiais_parte_1.xlsx` (~551 materiais)
- `materiais_parte_2.xlsx` (~551 materiais)
- ... até `materiais_parte_6.xlsx`

**Tempo:** Instantâneo

---

### **Passo 2: Processar Parte 1**

```bash
python3 processar_parte.py -p 1
```

**O que acontece:**
1. 🔍 Lê `partes/materiais_parte_1.xlsx`
2. 🌐 Busca preços no Mercado Livre (~551 requisições)
3. 🧠 Filtra com modo inteligente
4. 💾 Gera `paginas_html/pagina_parte_1.html`

**Tempo:** ~40 minutos

**Resultado:** Página HTML com dados da parte 1

---

### **Passo 3: Validar Parte 1**

Enquanto a parte 2 processa (ou depois), valide a parte 1:

```bash
xdg-open paginas_html/pagina_parte_1.html
```

**Na página HTML:**
1. 👀 Revise os produtos encontrados
2. ✕ Remova produtos irrelevantes (botão "Remover")
3. 📊 Exporte para Excel (botão "Exportar para Excel")
4. 💾 Salve como: `parte_1_validada.xlsx`

**Tempo:** 5-15 minutos (depende da revisão)

---

### **Passo 4: Processar Parte 2**

```bash
python3 processar_parte.py -p 2
```

**Tempo:** ~40 minutos

**Enquanto processa:** Você pode validar a parte 1 (passo 3)!

---

### **Passo 5: Repetir para Todas as Partes**

```bash
# Parte 3
python3 processar_parte.py -p 3

# Parte 4
python3 processar_parte.py -p 4

# Parte 5
python3 processar_parte.py -p 5

# Parte 6
python3 processar_parte.py -p 6
```

**Para cada parte:**
1. Processar (~40 minutos)
2. Validar (abrir HTML, remover produtos, exportar Excel)
3. Salvar Excel validado

---

### **Passo 6: Gerar Página Índice**

Depois de processar todas (ou algumas) partes:

```bash
python3 gerar_indice.py
```

**Resultado:** `paginas_html/index.html` com links para todas as partes

**Abrir:**
```bash
xdg-open paginas_html/index.html
```

---

## 🎯 Modo Interativo (Ainda Mais Fácil!)

### Comando único para escolher a parte:

```bash
python3 processar_parte.py
```

**O que acontece:**
1. ✅ Mostra todas as partes disponíveis
2. ✅ Mostra quais já foram processadas
3. ✅ Você escolhe qual processar
4. ✅ Processa automaticamente
5. ✅ Mostra progresso geral

**Exemplo de tela:**

```
📦 Partes disponíveis: 6
✅ Partes processadas: 2

Status de cada parte:
--------------------------------------------------
   1. materiais_parte_1.xlsx        ✅ Processada
   2. materiais_parte_2.xlsx        ✅ Processada
   3. materiais_parte_3.xlsx        ⏳ Pendente
   4. materiais_parte_4.xlsx        ⏳ Pendente
   5. materiais_parte_5.xlsx        ⏳ Pendente
   6. materiais_parte_6.xlsx        ⏳ Pendente
--------------------------------------------------

💡 Escolha uma parte para processar:
   Digite o número da parte (1-6)
   Ou 'q' para sair

➤ Parte: 3
```

---

## ⏱️ Cronograma Sugerido

### Dia 1 (Manhã):
```bash
python3 dividir_planilha.py
python3 processar_parte.py -p 1  # ~40 min
python3 processar_parte.py -p 2  # ~40 min
```
→ Durante o almoço: Valide partes 1 e 2

### Dia 1 (Tarde):
```bash
python3 processar_parte.py -p 3  # ~40 min
python3 processar_parte.py -p 4  # ~40 min
```
→ Valide partes 3 e 4

### Dia 2:
```bash
python3 processar_parte.py -p 5  # ~40 min
python3 processar_parte.py -p 6  # ~40 min
python3 gerar_indice.py
```
→ Valide partes 5 e 6

**Total:** ~4 horas de processamento + tempo de validação

---

## 🔄 Fluxo Paralelo (Avançado)

Se quiser acelerar, processe várias partes em paralelo:

### Terminal 1:
```bash
python3 processar_parte.py -p 1
```

### Terminal 2:
```bash
python3 processar_parte.py -p 2
```

### Terminal 3:
```bash
python3 processar_parte.py -p 3
```

**Vantagem:** Reduz tempo total de ~4 horas para ~40 minutos!

**Cuidado:** Pode sobrecarregar o servidor do Mercado Livre (risco de bloqueio)

---

## 📂 Estrutura Final

Depois de processar todas as partes:

```
busca_precos/
├── partes/
│   ├── materiais_parte_1.xlsx
│   ├── materiais_parte_2.xlsx
│   └── ... (até 6)
│
├── paginas_html/
│   ├── index.html              ← Página índice
│   ├── pagina_parte_1.html
│   ├── pagina_parte_2.html
│   └── ... (até 6)
│
└── validados/                   ← Crie esta pasta
    ├── parte_1_validada.xlsx    ← Exportado da página HTML
    ├── parte_2_validada.xlsx
    └── ... (até 6)
```

---

## 📊 Vantagens vs Processar Tudo de Uma Vez

| Característica | Uma Parte por Vez ⭐ | Tudo de Uma Vez |
|----------------|---------------------|-----------------|
| Tempo total | ~4 horas | ~3-4 horas |
| Risco de perda | Baixo (perde só 1 parte) | Alto (perde tudo) |
| Flexibilidade | Pode pausar | Não pode pausar |
| Validação | Paralela ao processamento | Só no final |
| Organização | Excelente | Regular |
| Complexidade | Muito simples | Simples |

---

## 💡 Dicas Importantes

### Para Pausar e Continuar:
1. Processe partes 1, 2 e 3
2. Pause (faça outra coisa)
3. Continue processando partes 4, 5 e 6 depois

### Para Verificar Progresso:
```bash
python3 processar_parte.py
```
(Modo interativo mostra quais partes já foram processadas)

### Para Reprocessar uma Parte:
```bash
python3 processar_parte.py -p 2
```
(Sobrescreve a página HTML anterior)

### Para Validar Todas as Páginas:
```bash
python3 gerar_indice.py
xdg-open paginas_html/index.html
```

---

## 🚀 Comando Recomendado para Começar

```bash
# 1. Dividir
python3 dividir_planilha.py

# 2. Processar parte por parte (modo interativo)
python3 processar_parte.py
```

**Pronto!** Agora é só escolher qual parte processar! 🎯

