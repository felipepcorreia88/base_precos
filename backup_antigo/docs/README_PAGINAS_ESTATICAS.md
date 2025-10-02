# 📊 Sistema de Páginas HTML Estáticas

Sistema para gerar **páginas HTML estáticas interativas** com resultados da busca de preços.

## 🎯 Características

### ✨ Páginas Estáticas Interativas
- ✅ **Nenhum servidor necessário** - abra direto no navegador
- ✅ **Dados embutidos** - tudo em um único arquivo HTML
- ✅ **JavaScript puro** - sem dependências externas
- ✅ **Totalmente funcional offline**

### 🛠️ Funcionalidades

1. **Visualização de Materiais**
   - Lista todos os materiais com produtos encontrados
   - Cards expansíveis com detalhes
   - Estatísticas em tempo real

2. **Busca em Tempo Real**
   - Filtra materiais enquanto você digita
   - Busca case-insensitive
   - Atualiza estatísticas automaticamente

3. **Remoção Manual de Produtos** ⭐
   - Remova produtos irrelevantes com um clique
   - Botão de restaurar tudo
   - Estado mantido na memória (temporário)

4. **Exportação para Excel** ⭐
   - Exporta dados filtrados
   - Remove produtos que você marcou
   - Usa biblioteca SheetJS (CDN)
   - Gera arquivo `.xlsx` pronto

## 📂 Estrutura de Arquivos

```
busca_precos/
├── dividir_planilha.py              # Divide materiais.xlsx em partes
├── gerar_paginas_estaticas.py       # Processa e gera HTML
├── processar_completo.py            # Script MASTER (tudo de uma vez)
├── templates/
│   └── pagina_estatica.html         # Template HTML
├── partes/                          # Planilhas divididas (geradas)
│   ├── materiais_parte_1.xlsx
│   ├── materiais_parte_2.xlsx
│   └── ...
└── paginas_html/                    # Páginas geradas (saída)
    ├── index.html                   # Página índice
    ├── pagina_parte_1.html
    ├── pagina_parte_2.html
    └── ...
```

## 🚀 Como Usar

### Opção 1: Processamento Completo (RECOMENDADO)

Execute tudo de uma vez:

```bash
python3 processar_completo.py
```

Isso vai:
1. ✅ Dividir `materiais.xlsx` em 6 partes
2. ✅ Buscar preços para cada material
3. ✅ Gerar 6 páginas HTML estáticas
4. ✅ Criar página índice

**Tempo estimado:** 3-4 horas para 3306 materiais

---

### Opção 2: Passo a Passo

#### Passo 1: Dividir Planilha

```bash
python3 dividir_planilha.py
```

Opções:
```bash
# Dividir em 4 partes
python3 dividir_planilha.py -n 4

# Arquivo customizado
python3 dividir_planilha.py -i dados.xlsx -n 10
```

**Resultado:** Pasta `partes/` com arquivos `materiais_parte_1.xlsx`, etc.

---

#### Passo 2: Gerar Páginas HTML

##### 2a) Processar TODAS as partes:

```bash
python3 gerar_paginas_estaticas.py --todas
```

##### 2b) Processar UMA parte específica:

```bash
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o pagina1.html -n 1
```

**Resultado:** Pasta `paginas_html/` com páginas HTML estáticas

---

## 🌐 Visualizando as Páginas

### Método 1: Abrir Diretamente

```bash
# Linux/Mac
xdg-open paginas_html/index.html

# Windows
start paginas_html/index.html

# Ou arraste o arquivo para o navegador
```

### Método 2: Caminho Absoluto

```bash
file:///home/usuario/projeto/busca_precos/paginas_html/index.html
```

## 📖 Usando a Interface

### Dashboard Superior
- **Total de Materiais**: Quantidade visível
- **Total de Produtos**: Produtos não removidos
- **Preço Médio**: Calculado dinamicamente

### Busca
Digite no campo de busca para filtrar materiais em tempo real.

### Remover Produtos
1. Clique no botão **"✕ Remover"** em qualquer produto
2. O produto desaparece da lista
3. Estatísticas são atualizadas automaticamente

### Restaurar Produtos Removidos
Clique em **"🗑️ Limpar Removidos"** para restaurar tudo.

### Exportar para Excel
1. Remova produtos irrelevantes (opcional)
2. Clique em **"📊 Exportar para Excel"**
3. Arquivo `.xlsx` será baixado
4. Contém apenas produtos não removidos

## 🎨 Customização

### Alterar Número de Partes

```bash
python3 processar_completo.py -n 10  # Divide em 10 partes
```

### Customizar Pastas

```bash
python3 processar_completo.py \
  --pasta-partes minhas_partes \
  --pasta-saida meus_htmls
```

### Template HTML

Edite `templates/pagina_estatica.html` para customizar:
- Cores e estilos (CSS)
- Layout e estrutura
- Funcionalidades JavaScript

## ⚙️ Parâmetros dos Scripts

### dividir_planilha.py

```bash
python3 dividir_planilha.py --help
```

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `-i, --entrada` | `materiais.xlsx` | Arquivo de entrada |
| `-n, --num-partes` | `6` | Número de partes |
| `-o, --pasta-saida` | `partes` | Pasta de saída |

### gerar_paginas_estaticas.py

```bash
python3 gerar_paginas_estaticas.py --help
```

| Parâmetro | Descrição |
|-----------|-----------|
| `--todas` | Processar todas as partes |
| `-i, --entrada` | Arquivo de entrada (uma parte) |
| `-o, --saida` | Arquivo HTML de saída |
| `-n, --numero` | Número da parte |
| `--pasta-partes` | Pasta com as partes (padrão: `partes`) |
| `--pasta-saida` | Pasta de saída (padrão: `paginas_html`) |

### processar_completo.py

```bash
python3 processar_completo.py --help
```

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `-i, --entrada` | `materiais.xlsx` | Arquivo de entrada |
| `-n, --num-partes` | `6` | Número de partes |
| `--pasta-partes` | `partes` | Pasta para as partes |
| `-o, --pasta-saida` | `paginas_html` | Pasta de saída |

## 📊 Exemplos de Uso

### Teste Rápido (5 materiais)

```bash
# 1. Criar planilha de teste
head -n 6 materiais.xlsx > teste_pequeno.xlsx  # Cabeçalho + 5 linhas

# 2. Dividir em 2 partes
python3 dividir_planilha.py -i teste_pequeno.xlsx -n 2

# 3. Gerar páginas
python3 gerar_paginas_estaticas.py --todas

# 4. Abrir
xdg-open paginas_html/index.html
```

### Processamento Paralelo

Você pode processar várias partes em paralelo (terminais diferentes):

```bash
# Terminal 1
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_1.xlsx -o paginas_html/pagina_parte_1.html -n 1

# Terminal 2
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_2.xlsx -o paginas_html/pagina_parte_2.html -n 2

# Terminal 3
python3 gerar_paginas_estaticas.py -i partes/materiais_parte_3.xlsx -o paginas_html/pagina_parte_3.html -n 3
```

## 🔧 Requisitos

- Python 3.6+
- Dependências (já instaladas):
  ```bash
  pip install pandas openpyxl requests beautifulsoup4
  ```
- Navegador moderno (Chrome, Firefox, Edge, Safari)

## 💡 Dicas

### Para Processamento Longo
- ✅ Execute em horário de baixo tráfego
- ✅ Use `nohup` para deixar rodando em segundo plano:
  ```bash
  nohup python3 processar_completo.py > processamento.log 2>&1 &
  ```
- ✅ Monitore o progresso:
  ```bash
  tail -f processamento.log
  ```

### Para Testes
- ✅ Comece com poucas linhas
- ✅ Teste com 1-2 partes primeiro
- ✅ Verifique o resultado antes de processar tudo

### Para Produção
- ✅ Faça backup de `materiais.xlsx`
- ✅ Mantenha as páginas em pasta separada
- ✅ Compartilhe os arquivos HTML (funcionam offline!)

## 🎯 Vantagens das Páginas Estáticas

| Característica | Páginas Estáticas | Flask (visualizador_materiais.py) |
|----------------|-------------------|-------------------------------------|
| Servidor necessário | ❌ Não | ✅ Sim |
| Portabilidade | ✅ Total | ❌ Limitada |
| Compartilhamento | ✅ Fácil | ❌ Difícil |
| Funciona offline | ✅ Sim | ❌ Não |
| Edição manual | ✅ Sim (remover produtos) | ❌ Não |
| Exportar editado | ✅ Sim | ❌ Não |

## ❓ Problemas Comuns

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Arquivo não encontrado"
Verifique se executou o passo de dividir planilha primeiro:
```bash
python3 dividir_planilha.py
ls -la partes/
```

### Processamento muito lento
Normal! Cada material leva ~3 segundos devido aos temporizadores (evita bloqueio).

### Navegador não abre HTML
Use caminho absoluto ou mova os arquivos para pasta acessível.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs: `logs/busca_materiais_inteligente.log`
2. Execute com verbose: `python3 script.py -v`
3. Teste com arquivo pequeno primeiro

---

## 🎉 Resultado Final

Você terá:
- ✅ 6 páginas HTML independentes
- ✅ Página índice para navegação
- ✅ Cada página funciona offline
- ✅ Remova produtos irrelevantes manualmente
- ✅ Exporte para Excel com filtros aplicados
- ✅ Compartilhe facilmente (só enviar os HTMLs!)

**Pronto para começar?**

```bash
python3 processar_completo.py
```

🚀 **Boa busca de preços!**

