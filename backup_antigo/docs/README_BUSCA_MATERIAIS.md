# 🔍 Sistema de Busca de Preços de Materiais

Sistema especializado para buscar preços de materiais da planilha no Mercado Livre, gerando um novo dataset com estatísticas completas e links dos produtos.

## 🚀 Funcionalidades

- **Processamento em lote**: Processa todos os 3306 materiais da planilha
- **Análise estatística**: Calcula média, mediana, desvio padrão e outliers
- **Filtro inteligente**: Remove preços extremos automaticamente
- **Temporizadores**: Evita sobrecarga do sistema com pausas automáticas
- **Logs detalhados**: Acompanhe o progresso em tempo real
- **JSON com links**: Cada material tem um JSON com todos os produtos encontrados

## 📁 Arquivos Principais

- `busca_materiais_planilha.py` - Script principal para processar a planilha
- `teste_busca_pequena.py` - Script para testes com poucos materiais
- `exemplo_uso.py` - Interface interativa para diferentes tipos de processamento

## 🛠️ Como Usar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Teste Pequeno (Recomendado para começar)

```bash
# Testar com 5 materiais
python3 teste_busca_pequena.py 5
```

### 3. Interface Interativa

```bash
python3 exemplo_uso.py
```

### 4. Processamento Direto

```bash
# Processar toda a planilha
python3 busca_materiais_planilha.py

# Ou especificar arquivos
python3 busca_materiais_planilha.py --entrada materiais.xlsx --saida resultado.xlsx
```

## 📊 Colunas do Dataset de Saída

O sistema gera um novo arquivo Excel com as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| `Nome` | Nome original do material |
| `Total_Produtos_Encontrados` | Quantidade de produtos encontrados |
| `Preco_Minimo` | Menor preço encontrado |
| `Preco_Maximo` | Maior preço encontrado |
| `Preco_Medio` | Preço médio (após filtro de outliers) |
| `Preco_Mediana` | Preço mediano |
| `Desvio_Padrao` | Desvio padrão dos preços |
| `Outliers_Removidos` | Quantidade de preços extremos removidos |
| `Links_Produtos_JSON` | JSON com todos os produtos e links |
| `Status_Busca` | Status da busca (sucesso, erro, etc.) |
| `Data_Hora_Busca` | Data e hora da busca |

## ⏱️ Temporizadores

O sistema implementa temporizadores inteligentes:

- **2 segundos** entre cada requisição
- **30 segundos** de pausa a cada 100 requisições
- **Logs de progresso** a cada 50 materiais processados

## 🔍 Exemplo de JSON de Links

Cada material terá um JSON com os produtos encontrados:

```json
[
  {
    "nome": "Mouse Gamer Sem Fio Logitech G502 X PLUS",
    "preco": 999.90,
    "link": "https://produto.mercadolivre.com.br/MLB-..."
  },
  {
    "nome": "Mouse Gamer Redragon Cobra M711",
    "preco": 89.90,
    "link": "https://produto.mercadolivre.com.br/MLB-..."
  }
]
```

## 📈 Estatísticas Geradas

Para cada material, o sistema calcula:

- **Quantidade total** de produtos encontrados
- **Quantidade filtrada** (após remoção de outliers)
- **Preço mínimo e máximo**
- **Média e mediana** dos preços
- **Desvio padrão** para análise de dispersão
- **Quantidade de outliers** removidos

## 🎯 Filtro de Outliers

O sistema aplica automaticamente um filtro estatístico:

- **Fórmula**: Mediana ± 1 Desvio Padrão
- **Objetivo**: Remove preços extremos que distorcem a análise
- **Resultado**: Mostra apenas preços estatisticamente relevantes

## 📝 Logs e Monitoramento

O sistema gera logs detalhados:

- **Arquivo**: `busca_materiais.log`
- **Console**: Progresso em tempo real
- **Status**: Sucesso, erro, ou sem produtos para cada material

## ⚠️ Considerações Importantes

### Tempo de Processamento

- **5 materiais**: ~30 segundos
- **50 materiais**: ~5 minutos  
- **3306 materiais**: ~3-4 horas

### Recomendações

1. **Sempre teste primeiro** com poucos materiais
2. **Execute em horários de menor tráfego** (madrugada)
3. **Monitore os logs** durante o processamento
4. **Mantenha conexão estável** com a internet

## 🚨 Tratamento de Erros

O sistema trata automaticamente:

- **Erros de conexão**: Retry automático
- **Timeouts**: Continua com próximo material
- **Materiais sem produtos**: Registra como "nenhum_produto"
- **Erros de parsing**: Continua processamento

## 📊 Exemplo de Resultado

```
📈 Resumo final:
   ✅ Sucessos: 2800
   ❌ Erros: 50
   🔍 Sem produtos: 456
```

## 🔧 Personalização

Você pode ajustar os temporizadores editando:

```python
self.tempo_base = 2  # segundos entre requisições
self.tempo_pausa_longa = 30  # pausa a cada 100 itens
```

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs em `busca_materiais.log`
2. Teste com poucos materiais primeiro
3. Verifique sua conexão com a internet
4. Considere executar em horários de menor tráfego
