# 📊 Guia de Divisão da Planilha

## 🎯 Como Escolher o Número de Partes

O script `dividir_planilha.py` permite dividir a planilha `materiais.xlsx` (3306 materiais) em **qualquer número de partes**.

### 🚀 Uso Rápido

```bash
# Da raiz do projeto
./dividir.sh -n NUMERO        # Dividir em N partes

# Do diretório scripts
cd scripts
python3 dividir_planilha.py -n NUMERO
```

### 📋 Parâmetros Disponíveis

```bash
python3 dividir_planilha.py [opções]

Opções:
  -n, --num-partes NUMERO    Número de partes (padrão: 6)
  -i, --entrada ARQUIVO      Arquivo de entrada (padrão: materiais.xlsx)
  -o, --pasta-saida PASTA    Pasta de saída (padrão: output/partes)
  -h, --help                 Mostrar ajuda
```

---

## 💡 Recomendações por Cenário

### 🐢 **3 Partes** - Processamento Sequencial Moderado
```bash
./dividir.sh -n 3
```
- **~1102 materiais** por parte
- **Tempo sequencial:** ~5h 30min (scraping)
- **Tempo paralelo:** ~1h 50min (scraping)
- **Ideal para:** Processamento em máquina com poucos recursos

---

### 📦 **6 Partes** - Padrão Balanceado (RECOMENDADO)
```bash
./dividir.sh             # ou ./dividir.sh -n 6
```
- **~551 materiais** por parte
- **Tempo sequencial:** ~4h (scraping)
- **Tempo paralelo:** ~40 min (scraping)
- **Ideal para:** Uso geral, bom equilíbrio

---

### ⭐ **10 Partes** - Processamento Rápido
```bash
./dividir.sh -n 10
```
- **~330 materiais** por parte
- **Tempo sequencial:** ~5h 30min (scraping)
- **Tempo paralelo:** ~14 min (scraping)
- **Ideal para:** Processamento paralelo em várias abas do terminal

---

### ⚡ **20 Partes** - Processamento Ultra Rápido
```bash
./dividir.sh -n 20
```
- **~165 materiais** por parte
- **Tempo sequencial:** ~2h 20min (scraping)
- **Tempo paralelo:** ~7 min (scraping)
- **Ideal para:** Máximo paralelismo, menor risco de bloqueio

---

## 🔥 Processamento em Paralelo

### Exemplo com 10 Partes

Abra **10 terminais** e execute simultaneamente:

```bash
# Terminal 1
./processar.sh -p 1

# Terminal 2
./processar.sh -p 2

# Terminal 3
./processar.sh -p 3

# ... e assim por diante até Terminal 10
./processar.sh -p 10
```

**Tempo total:** ~14 minutos (ao invés de ~5h 30min sequencial)!

---

## 📊 Tabela Comparativa

| Partes | Mat./Parte | Arquivos | Tempo Seq. | Tempo Par. | Gerenciamento |
|--------|------------|----------|-----------|-----------|---------------|
| 3      | ~1102      | 3        | 5h 30min  | 1h 50min  | ⭐⭐⭐⭐⭐ Fácil |
| 6      | ~551       | 6        | 4h        | 40 min    | ⭐⭐⭐⭐ Fácil   |
| 10     | ~330       | 10       | 5h 30min  | 14 min    | ⭐⭐⭐ Médio    |
| 20     | ~165       | 20       | 2h 20min  | 7 min     | ⭐⭐ Difícil    |

---

## 🎯 Qual Escolher?

### ✅ Use **3-6 partes** se:
- Vai processar sequencialmente (uma parte por vez)
- Prefere menos arquivos para gerenciar
- Não tem pressa
- Computador com poucos recursos

### ✅ Use **10-20 partes** se:
- Vai processar em paralelo (múltiplas abas/terminais)
- Quer terminar o mais rápido possível
- Tem computador potente
- Quer minimizar risco de bloqueio do Mercado Livre

---

## 📝 Exemplos Práticos

### Teste Rápido (5 materiais)
```bash
cd scripts
python3 dividir_planilha.py -i ../materiais.xlsx -n 1 -o ../output/teste
# Edite a planilha resultante para ter apenas 5 linhas
python3 processar_parte.py -i ../output/teste/materiais_parte_1.xlsx
```

### Divisão Personalizada
```bash
# 15 partes
./dividir.sh -n 15

# Processar apenas as partes 1, 5 e 10
./processar.sh -p 1
./processar.sh -p 5
./processar.sh -p 10
```

### Redividir com Outro Número
```bash
# Se já dividiu em 6 e quer mudar para 10:
rm -rf output/partes/*        # Limpar divisão antiga
./dividir.sh -n 10           # Nova divisão
```

---

## 🚨 Importante

1. **Sempre divida primeiro** antes de processar:
   ```bash
   ./dividir.sh -n 10
   ```

2. **Aguarde a conclusão** da divisão antes de processar

3. **Não misture** partes de divisões diferentes

4. **Backup:** Os arquivos originais são preservados

---

## 🆘 Troubleshooting

### "Arquivo não encontrado"
```bash
# Certifique-se de que materiais.xlsx existe na raiz
ls materiais.xlsx

# Ou especifique o caminho completo
cd scripts
python3 dividir_planilha.py -i /caminho/completo/materiais.xlsx
```

### "Pasta já existe"
Os arquivos serão sobrescritos. Isso é seguro e esperado.

### Quantas partes devo usar?
- **Primeiro teste:** Use 6 partes (padrão)
- **Se for lento:** Aumente para 10-20 partes
- **Se for rápido:** Mantenha 6 partes

---

## 📚 Ver Também

- `COMANDOS_RAPIDOS.md` - Referência de comandos
- `FLUXO_RECOMENDADO.md` - Fluxo completo de trabalho
- `SOLUCAO_PROBLEMAS.md` - Soluções para problemas comuns

---

**🎯 Dica Final:** Para a primeira execução, use o padrão (6 partes). Se quiser mais velocidade na próxima vez, use 10-20 partes com processamento paralelo!

