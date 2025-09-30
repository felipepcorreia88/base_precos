# Consulta de materiais esportivos

Este repositório contém um script em Python para consultar a API pública do
Governo Federal (`dadosabertos.compras.gov.br`) em busca de materiais
esportivos. A ferramenta recebe uma descrição textual, remove conectivos em
português e calcula a média e a mediana dos valores disponíveis para os itens
retornados pela API.

## Requisitos

- Python 3.9 ou superior
- Biblioteca [`requests`](https://docs.python-requests.org/)

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Uso

Execute o script `material_stats.py` passando a descrição do material esportivo
como argumento. Conectivos como "de", "como", "para" são ignorados durante a
busca.

```bash
python material_stats.py "bola de futebol"
```

Saída esperada:

```
Termos pesquisados: bola futebol
Itens considerados: 42
Média: 150.35
Mediana: 139.90
```

Caso deseje visualizar mensagens de depuração, utilize a flag `--debug`:

```bash
python material_stats.py "rede de vôlei" --debug
```

## Observações

- O script realiza paginação automaticamente caso a API retorne múltiplas
  páginas de resultados.
- Apenas itens cuja descrição contém todas as palavras informadas (após a
  remoção dos conectivos) são considerados no cálculo das estatísticas.
- Alguns ambientes podem exigir configuração de proxy para acessar a API.
