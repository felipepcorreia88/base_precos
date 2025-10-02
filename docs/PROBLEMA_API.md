# ⚠️ Problema com API do Mercado Livre

## Situação

A API oficial do Mercado Livre (`api.mercadolivre.com`) não está acessível neste ambiente devido a:

- ❌ DNS não resolve o domínio
- ❌ `curl` retorna "Could not resolve host"
- ❌ Possível bloqueio de firewall/proxy/ISP

## ✅ Solução: Usar Scraping

O método de **scraping** (acesso direto ao site) **estava funcionando perfeitamente**!

### Vantagens do Scraping:
- ✅ Funciona com sua configuração de rede
- ✅ Não depende de API externa
- ✅ Já testado e aprovado
- ✅ Resultados comprovados

### Desvantagens:
- ⏱️ Um pouco mais lento (~3s por material vs ~0.5s)
- ⚠️ Risco de bloqueio se fizer muitas requisições rápidas

---

## 🚀 Use o Scraping

```bash
# Método recomendado para seu ambiente
./processar.sh -p 1

# OU
cd scripts
python3 processar_parte.py -p 1
```

**NÃO use:**
```bash
# ❌ Não funciona no seu ambiente
./processar_api.sh -p 1
```

---

## 🔧 Ajustes para Evitar Bloqueio

Se o scraping for bloqueado novamente:

### 1. Aumentar Temporizadores

Edite `scripts/core/busca_materiais_planilha_inteligente.py`:

```python
# Linha ~52
self.tempo_base = 5  # Aumentar de 2 para 5 segundos
```

### 2. Processar Menos de Cada Vez

```bash
# Processar apenas 100 materiais por vez
# (crie partes menores)
./dividir.sh -n 20  # 20 partes de ~165 materiais cada
```

### 3. Rodar em Horários de Baixo Tráfego

Execute o processamento de madrugada (2h-6h) quando há menos tráfego.

---

## 📊 Tempos Esperados (Scraping)

| Materiais | Tempo |
|-----------|-------|
| 5 | ~25 segundos |
| 50 | ~2.5 minutos |
| 551 (1 parte de 6) | ~40 minutos |
| 3306 (total) | ~4 horas |

---

## ✅ Comando Recomendado

```bash
# Dividir
./dividir.sh

# Processar COM SCRAPING (funciona!)
./processar.sh -p 1
./processar.sh -p 2
# ... até parte 6

# Gerar índice
./gerar_indice.sh

# Visualizar
xdg-open output/paginas_html/index.html
```

---

## 🆘 Se o Scraping for Bloqueado

1. **Aguarde 30 minutos** antes de tentar novamente
2. **Aumente o temporizador** para 5 segundos
3. **Use VPN** se disponível
4. **Processe em lotes menores** (dividir em mais partes)

---

**Resumo:** Use `./processar.sh` (scraping) ao invés de `./processar_api.sh` (API).

