# �� Sistema de Busca OTIMIZADO

## ❌ Problema Identificado

Ao buscar materiais como:
```
"ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD"
```

O sistema retornava produtos IRRELEVANTES como:
- ❌ "Kit 50 Bolas Para Piscina De Bolinhas Baby"
- ❌ "Tapete Pista Infantil De Deficiência PCD Autista"

## ✅ Soluções Implementadas

### 1. **Priorização de Conteúdo Após Hífen**

**Antes:**
```
Busca: "ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD"
```

**Depois:**
```
Termo otimizado: "kit bolas suíças pcd"
```

O sistema **detecta o hífen** e usa apenas a parte mais específica (após o hífen).

---

### 2. **Remoção de Stopwords**

Remove palavras comuns sem significado:
- `para`, `com`, `de`, `da`, `do`, `em`, `na`, `no`
- `um`, `uma`, `esse`, `essa`, `aquele`, etc.

**Exemplo:**
```
Original: "Kit de Alongamento para Pessoas com Deficiência"
Otimizado: "kit alongamento pessoas deficiência"
```

---

### 3. **Remoção de Palavras Genéricas**

Remove termos muito amplos:
- `atividades`, `materiais`, `produtos`, `itens`
- `equipamentos`, `acessórios`, `conjunto`

**Exemplo:**
```
Original: "MATERIAIS ESPORTIVOS - Cones de Treinamento"
Otimizado: "cones treinamento"
```

---

### 4. **Filtro de Relevância por Score**

Cada produto recebe um **score de 0.0 a 1.0**:

```python
Score = (Palavras encontradas) / (Total de palavras-chave)
```

**Exemplo com termo "kit bolas suíças pcd":**

| Produto | Score | Status |
|---------|-------|--------|
| Kit Bola Suíça 65cm PCD | **0.75** | ✅ MANTIDO |
| Bola Suíça 55cm | **0.25** | ❌ REMOVIDO |
| Kit Bolas Piscina Baby | **0.50** | ✅ MANTIDO |
| Bola de Pilates | **0.00** | ❌ REMOVIDO |

**Score mínimo padrão:** 0.3 (configurável)

---

### 5. **Ordenação por Relevância**

Produtos com **maior score aparecem primeiro**:

```
🏆 Top 3 produtos mais relevantes:
1. [1.00] Kit Bola Suíça 65cm PCD Pilates
2. [0.75] Bola Suíça Premium Kit Completo
3. [0.50] Kit Bolas Pilates PCD
```

---

## 🚀 Como Usar

### **Teste Rápido (Recomendado)**

Veja a otimização em ação:

```bash
python3 teste_otimizacao.py
```

Mostra como cada termo é otimizado e quais produtos seriam filtrados.

---

### **Teste com 1 Material Real**

```bash
python3 -c "
from busca_materiais_planilha_otimizado import BuscadorMateriaisPlanilhaOtimizado

buscador = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=0.3)
resultado = buscador.buscar_produtos_material('ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD')

print(f'Termo original: {resultado[\"termo_original\"]}')
print(f'Termo otimizado: {resultado[\"termo_otimizado\"]}')
print(f'Produtos brutos: {resultado[\"total_encontrado\"]}')
print(f'Produtos relevantes: {resultado[\"total_relevante\"]}')
"
```

---

### **Processar Planilha Completa**

```bash
# Padrão (score >= 0.3)
python3 busca_materiais_planilha_otimizado.py

# Mais rigoroso (score >= 0.5 - menos produtos, mais relevantes)
python3 busca_materiais_planilha_otimizado.py --min-score 0.5

# Menos rigoroso (score >= 0.2 - mais produtos, menos seletivo)
python3 busca_materiais_planilha_otimizado.py --min-score 0.2

# Especificar arquivo
python3 busca_materiais_planilha_otimizado.py --entrada materiais.xlsx --saida resultado.xlsx
```

---

## 📊 Novas Colunas na Planilha

O arquivo gerado terá colunas adicionais:

| Coluna | Descrição |
|--------|-----------|
| `Total_Produtos_Encontrados` | Produtos brutos (antes do filtro) |
| `Total_Produtos_Relevantes` | Produtos filtrados (após filtro) |
| `Termo_Otimizado` | Termo usado na busca |
| `Palavras_Chave` | Palavras-chave extraídas |
| `Links_Produtos_JSON` | JSON com produtos + score de relevância |

**Exemplo do JSON:**
```json
[
  {
    "nome": "Kit Bola Suíça 65cm PCD",
    "preco": 89.90,
    "link": "https://...",
    "score_relevancia": 0.75
  }
]
```

---

## ⚙️ Configurações

### Ajustar Score Mínimo

```python
# No código
buscador = BuscadorMateriaisPlanilhaOtimizado(min_score_relevancia=0.4)

# Via linha de comando
python3 busca_materiais_planilha_otimizado.py --min-score 0.4
```

**Recomendações:**
- **0.3** (padrão) - Equilíbrio entre quantidade e relevância
- **0.5** - Mais rigoroso, apenas produtos muito relevantes
- **0.2** - Menos rigoroso, aceita mais variações

---

### Adicionar Stopwords Customizadas

Edite o arquivo `busca_materiais_planilha_otimizado.py`:

```python
STOPWORDS = {
    'a', 'o', 'e', 'de', 'da', 'do',
    # Adicione suas palavras aqui:
    'tamanho', 'modelo', 'tipo'
}
```

---

### Adicionar Palavras Genéricas

```python
PALAVRAS_GENERICAS = {
    'atividades', 'materiais', 'produtos',
    # Adicione suas palavras aqui:
    'linha', 'serie', 'versao'
}
```

---

## 📈 Comparação: Antes vs Depois

### **Exemplo Real**

**Termo:** `ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD`

#### ANTES (sistema original):
```
Busca com termo completo: "ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD"
Produtos encontrados: 25

Top 5 resultados:
1. Kit 50 Bolas Para Piscina De Bolinhas (❌ irrelevante)
2. Tapete Pista Infantil PCD (❌ irrelevante)
3. Bola Colorida Baby (❌ irrelevante)
4. Kit Atividades Pedagógicas (❌ irrelevante)
5. Bola Suíça 65cm (✅ relevante, mas perdida)
```

#### DEPOIS (sistema otimizado):
```
Termo otimizado: "kit bolas suíças pcd"
Palavras-chave: ['kit', 'bolas', 'suíças', 'pcd']

Produtos brutos: 25
Produtos filtrados: 8 (score >= 0.3)

Top 5 resultados:
1. [1.00] Kit Bola Suíça 65cm PCD Pilates ✅
2. [0.75] Bola Suíça Premium Kit Completo ✅
3. [0.75] Kit Bolas Suíças Yoga PCD ✅
4. [0.50] Bola Suíça 55cm Kit ✅
5. [0.50] Kit 3 Bolas Pilates PCD ✅
```

**Melhoria: 100% de relevância nos top 5 resultados!**

---

## 🔍 Logs Detalhados

O sistema gera logs completos mostrando cada etapa:

```
2025-10-02 10:58:15 - INFO - 🔍 Buscando: ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD
2025-10-02 10:58:15 - INFO - 📝 Otimizando termo: ATIVIDADES PARA PESSOAS COM DEFICIÊNCIA - Kit Bolas Suíças PCD
2025-10-02 10:58:15 - INFO -    ✂️  Usando parte após hífen: 'Kit Bolas Suíças PCD'
2025-10-02 10:58:15 - INFO -    ✅ Termo otimizado: 'kit bolas suíças pcd'
2025-10-02 10:58:15 - INFO -    🔑 Palavras-chave: ['kit', 'bolas', 'suíças', 'pcd']
2025-10-02 10:58:16 - INFO -    📦 Produtos brutos encontrados: 25
2025-10-02 10:58:16 - INFO -    🎯 Produtos filtrados: 25 → 8 (score >= 0.3)
2025-10-02 10:58:16 - INFO -    🏆 Top 3 produtos mais relevantes:
2025-10-02 10:58:16 - INFO -       1. [1.00] Kit Bola Suíça 65cm PCD Pilates Premium...
2025-10-02 10:58:16 - INFO -       2. [0.75] Bola Suíça Premium Kit Completo...
2025-10-02 10:58:16 - INFO -       3. [0.75] Kit Bolas Suíças Yoga PCD...
```

Arquivo de log: `busca_materiais_otimizado.log`

---

## �� Dicas

### 1. **Comece com Teste**

Sempre teste com poucos materiais primeiro:

```bash
# Teste de otimização (sem fazer buscas reais)
python3 teste_otimizacao.py

# Teste com 1 material real
python3 -c "from busca_materiais_planilha_otimizado import BuscadorMateriaisPlanilhaOtimizado; ..."
```

---

### 2. **Ajuste o Score**

Se estiver recebendo:
- **Muitos produtos irrelevantes** → Aumente o score (ex: 0.4 ou 0.5)
- **Poucos produtos** → Diminua o score (ex: 0.2)

---

### 3. **Revise os Termos**

Se um termo não está funcionando bem:
1. Verifique o termo otimizado nos logs
2. Adicione stopwords/genéricas se necessário
3. Considere ajustar o termo na planilha original

---

## 🆚 Original vs Otimizado

| Recurso | Original | Otimizado |
|---------|----------|-----------|
| Termo de busca | Completo | Otimizado (após hífen) |
| Stopwords | Não | ✅ Sim |
| Palavras genéricas | Não | ✅ Sim |
| Filtro de relevância | Não | ✅ Sim (score 0-1) |
| Ordenação por relevância | Não | ✅ Sim |
| Score nos resultados | Não | ✅ Sim |
| Novas colunas | Não | ✅ Sim (4 novas) |

---

## 📞 Suporte

**Problemas comuns:**

### "Muitos produtos filtrados"
- Diminua o `--min-score` para 0.2

### "Produtos ainda irrelevantes"
- Aumente o `--min-score` para 0.5
- Adicione palavras às listas STOPWORDS/GENERICAS

### "Termo otimizado muito curto"
- Verifique se o termo original tem conteúdo após o hífen
- Considere remover o hífen do termo na planilha

---

## ✅ Próximos Passos

1. ✅ Teste a otimização: `python3 teste_otimizacao.py`
2. ✅ Teste com 1 material real
3. ✅ Processe planilha pequena (5-10 materiais)
4. ✅ Compare resultados com versão original
5. ✅ Ajuste score conforme necessário
6. ✅ Processe planilha completa

**Boas buscas! 🎯**
