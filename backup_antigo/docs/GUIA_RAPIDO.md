# 🚀 Guia Rápido - Sistema de Busca de Preços

Este guia mostra como usar rapidamente todas as funcionalidades do sistema.

## 📋 Índice

1. [Instalação Inicial](#instalação-inicial)
2. [Busca Web Interativa](#busca-web-interativa)
3. [Processamento de Planilhas](#processamento-de-planilhas)
4. [Visualização de Dados](#visualização-de-dados)

---

## 🔧 Instalação Inicial

```bash
# 1. Clone ou entre no diretório do projeto
cd busca_precos

# 2. Instale as dependências
pip install -r requirements.txt

# Pronto! Sistema instalado ✅
```

---

## 🌐 Busca Web Interativa

### Uso Rápido

```bash
# Iniciar servidor web de busca
python3 app_web.py

# Acessar no navegador
# http://localhost:5000
```

### O que faz?

- ✅ Busca produtos no Mercado Livre, BuscaPé ou Zoom
- ✅ Mostra resultados em tempo real
- ✅ Exibe estatísticas de preços
- ✅ Interface moderna e responsiva

### Exemplo de Busca

1. Abra `http://localhost:5000`
2. Digite: "mouse gamer"
3. Escolha: "Mercado Livre"
4. Clique em "Buscar"
5. Veja produtos com preços e estatísticas!

---

## 📊 Processamento de Planilhas

### Teste Rápido (5 materiais)

```bash
# Processar apenas 5 materiais (RECOMENDADO para teste)
python3 teste_busca_pequena.py 5

# Resultado: teste_materiais_precos.xlsx
# Tempo: ~30 segundos
```

### Interface Interativa

```bash
# Menu interativo com opções
python3 exemplo_uso.py

# Escolha:
# 1. Teste pequeno (5 materiais)
# 2. Teste médio (50 materiais) 
# 3. Processar tudo (3306 materiais)
# 4. Busca individual
```

### Processamento Completo

```bash
# Processar toda a planilha materiais.xlsx
python3 busca_materiais_planilha.py

# ⚠️ ATENÇÃO:
# - 3306 materiais
# - Tempo estimado: 3-4 horas
# - Execute apenas se necessário!
```

### O que faz?

- ✅ Lê planilha Excel com lista de materiais
- ✅ Busca preços no Mercado Livre para cada um
- ✅ Calcula estatísticas completas
- ✅ Salva tudo em nova planilha com:
  - Preços (mín, máx, média, mediana)
  - Links para todos os produtos (formato JSON)
  - Status de cada busca
  - Data e hora

---

## 📈 Visualização de Dados

### Uso Rápido

```bash
# Visualizar planilha processada
python3 visualizador_materiais.py teste_materiais_precos.xlsx

# Acessar no navegador
# http://localhost:5001
```

### Ou use o atalho

```bash
# Script que encontra automaticamente a planilha
./visualizar_exemplo.sh
```

### O que faz?

- ✅ Dashboard com estatísticas gerais
- ✅ Lista todos os materiais processados
- ✅ Busca em tempo real
- ✅ Ordenação flexível
- ✅ Cards expansíveis com detalhes
- ✅ Links diretos para produtos

### Interface Web

1. **Dashboard Superior**: Estatísticas gerais
   - Total de materiais
   - Materiais com/sem produtos
   - Preços médios, mínimo, máximo

2. **Controles**: 
   - Busca por nome
   - Ordenação (nome, produtos, preços)
   - Ordem (crescente/decrescente)

3. **Lista de Materiais**:
   - Cada card mostra resumo
   - Clique para expandir
   - Veja todos os produtos e links

---

## 🎯 Fluxo Completo de Uso

### Cenário 1: Busca Rápida de um Produto

```bash
# Iniciar busca web
python3 app_web.py

# Abrir http://localhost:5000
# Buscar: "smartphone samsung"
# Ver resultados instantaneamente
```

**Tempo total**: ~10 segundos

---

### Cenário 2: Processar Lista de Materiais (Teste)

```bash
# Passo 1: Processar poucos materiais (teste)
python3 teste_busca_pequena.py 5

# Passo 2: Visualizar resultados
python3 visualizador_materiais.py teste_materiais_precos.xlsx

# Passo 3: Abrir http://localhost:5001
# Explorar dados coletados
```

**Tempo total**: ~1 minuto

---

### Cenário 3: Processamento Completo

```bash
# Passo 1: Processar planilha completa (DEMORA!)
python3 busca_materiais_planilha.py

# Passo 2: Aguardar 3-4 horas...
# (pode acompanhar progresso nos logs)

# Passo 3: Visualizar resultado
python3 visualizador_materiais.py materiais_com_precos_*.xlsx

# Passo 4: Abrir http://localhost:5001
# Explorar 3306 materiais processados
```

**Tempo total**: ~3-4 horas

---

## 📂 Arquivos Gerados

### Por `teste_busca_pequena.py`:
```
teste_materiais_precos.xlsx  (poucos materiais, teste)
```

### Por `busca_materiais_planilha.py`:
```
materiais_com_precos_20251002_143000.xlsx  (timestamp automático)
```

### Logs:
```
busca_materiais.log  (logs detalhados do processamento)
```

---

## 🔍 Comandos Úteis

### Listar arquivos processados

```bash
# Ver planilhas geradas
ls -lh *.xlsx

# Ver logs
tail -f busca_materiais.log
```

### Busca via CLI (sem interface)

```bash
# Mercado Livre
python3 busca_mercadolivre.py "notebook dell"

# BuscaPé
python3 busca_buscape.py "mouse gamer"

# Zoom
python3 busca_zoom.py "teclado mecânico"
```

### Servidores em portas diferentes

```bash
# Busca web na porta 5000
python3 app_web.py

# Visualizador na porta 5001 (padrão)
python3 visualizador_materiais.py arquivo.xlsx

# Ou especificar porta
python3 visualizador_materiais.py arquivo.xlsx --port 8080
```

---

## 💡 Dicas

### Para Testes
- ✅ Use `teste_busca_pequena.py 5` antes de processar tudo
- ✅ Verifique os logs em tempo real: `tail -f busca_materiais.log`
- ✅ Teste com diferentes termos de busca

### Para Produção
- ✅ Execute processamento completo em horário de baixo tráfego (madrugada)
- ✅ Monitore o progresso pelos logs
- ✅ Mantenha conexão estável com internet
- ✅ Não interrompa o processamento (pode retomar com --inicio)

### Para Análise
- ✅ Use o visualizador para explorar dados
- ✅ Ordene por diferentes campos para insights
- ✅ Use a busca para encontrar materiais específicos
- ✅ Clique nos links para ver produtos no site original

---

## 📚 Documentação Completa

- `README.md` - Sistema geral e busca web
- `README_BUSCA_MATERIAIS.md` - Processamento de planilhas
- `README_VISUALIZADOR.md` - Visualizador web de dados

---

## ❓ Problemas Comuns

### "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### "Arquivo não encontrado"
```bash
# Verificar se planilha existe
ls -lh materiais.xlsx

# Usar caminho completo
python3 visualizador_materiais.py /caminho/completo/arquivo.xlsx
```

### "Porta já em uso"
```bash
# Usar outra porta
python3 app_web.py  # usa porta 5000
python3 visualizador_materiais.py arquivo.xlsx --port 5002
```

### Processamento muito lento
```bash
# Ajustar temporizadores em busca_materiais_planilha.py:
# self.tempo_base = 2  # aumentar para 3 ou 4
# self.tempo_pausa_longa = 30  # aumentar para 60
```

---

## 🎓 Próximos Passos

1. ✅ Teste com busca web interativa
2. ✅ Processe poucos materiais (5)
3. ✅ Visualize os dados coletados
4. ✅ Explore a interface do visualizador
5. ✅ Se necessário, processe planilha completa
6. ✅ Analise estatísticas e tome decisões

---

**Pronto para começar? Execute o primeiro comando!** 🚀

