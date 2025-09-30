#!/usr/bin/env python3
"""Ferramenta para calcular média e mediana de preços de materiais esportivos.

O script consulta a API de materiais do Governo Federal e filtra os itens
cuja descrição contenha as palavras relevantes fornecidas pelo usuário.
"""
from __future__ import annotations

import argparse
import logging
import re
import statistics
import sys
from typing import Dict, Iterable, Iterator, List, Optional
from urllib.parse import urljoin

import requests

API_URL = "https://dadosabertos.compras.gov.br/materiais/v1/material.json"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "base_precos_material_stats/1.0",
}

# Conectivos e palavras de parada em português que devem ser desconsideradas.
STOP_WORDS = {
    "a",
    "ao",
    "aos",
    "as",
    "como",
    "com",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "entre",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "para",
    "por",
    "sem",
    "sob",
    "sobre",
    "um",
    "uma",
    "uns",
    "umas",
}

PRICE_FIELDS = (
    "valor_medio",
    "preco_medio",
    "valor",
    "preco",
    "valor_unitario",
    "valor_unitario_medio",
    "preco_unitario",
)

DESCRIPTION_FIELDS = (
    "descricao",
    "descricao_material",
    "descricao_item",
    "descricao_detalhada",
    "ds_material",
    "descricao_resumida",
)


class APIError(RuntimeError):
    """Erro genérico para problemas de integração com a API."""


def sanitize_terms(raw_text: str) -> List[str]:
    """Normaliza a string de entrada removendo conectivos e sinais de pontuação."""
    tokens = re.findall(r"[\wÀ-ÖØ-öø-ÿ]+", raw_text.lower())
    filtered = [token for token in tokens if token not in STOP_WORDS]
    if not filtered:
        raise ValueError(
            "A consulta não contém termos válidos após a remoção dos conectivos."
        )
    return filtered


def extract_price(record: Dict[str, object]) -> Optional[float]:
    """Extrai o valor numérico do registro, se disponível."""
    for field in PRICE_FIELDS:
        if field not in record:
            continue
        value = record[field]
        if value in (None, ""):
            continue
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                continue
            # Remove símbolo monetário e espaços.
            cleaned = cleaned.replace("R$", "").strip()
            # Substitui separadores de milhar e decimal comuns no Brasil.
            cleaned = cleaned.replace(".", "").replace(",", ".")
            try:
                return float(cleaned)
            except ValueError:
                continue
    return None


def record_matches(record: Dict[str, object], terms: Iterable[str]) -> bool:
    """Verifica se o registro possui todas as palavras relevantes na descrição."""
    descriptions: List[str] = []
    for field in DESCRIPTION_FIELDS:
        value = record.get(field)
        if isinstance(value, str):
            descriptions.append(value.lower())
    if not descriptions:
        return False
    combined = " ".join(descriptions)
    return all(term in combined for term in terms)


def iter_records(url: str, params: Dict[str, str]) -> Iterator[Dict[str, object]]:
    """Percorre todas as páginas de resultados da API."""
    session = requests.Session()
    session.headers.update(HEADERS)

    next_url: Optional[str] = url
    next_params: Optional[Dict[str, str]] = dict(params)

    while next_url:
        try:
            response = session.get(next_url, params=next_params, timeout=30)
        except requests.RequestException as exc:  # pragma: no cover - robustez de rede
            raise APIError(f"Erro ao se comunicar com a API: {exc}") from exc

        if response.status_code == 403:
            raise APIError(
                "A API retornou 403 (Forbidden). Verifique se o serviço está acessível."
            )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise APIError(f"Erro HTTP ao consultar a API: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise APIError("Não foi possível interpretar a resposta JSON da API.") from exc

        records: List[Dict[str, object]] = []

        request_url = response.url

        if isinstance(payload, dict):
            if "_embedded" in payload and isinstance(payload["_embedded"], dict):
                embedded = payload["_embedded"]
                # Assume que a lista de materiais é o primeiro valor de lista em _embedded.
                for value in embedded.values():
                    if isinstance(value, list):
                        records = [item for item in value if isinstance(item, dict)]
                        break
            elif "results" in payload and isinstance(payload["results"], list):
                records = [item for item in payload["results"] if isinstance(item, dict)]
            elif "items" in payload and isinstance(payload["items"], list):
                records = [item for item in payload["items"] if isinstance(item, dict)]

            links = payload.get("_links") or payload.get("links")
            next_url = None
            if isinstance(links, dict):
                next_entry = links.get("next")
                if isinstance(next_entry, dict):
                    next_url = next_entry.get("href")
                elif isinstance(next_entry, str):
                    next_url = next_entry
            elif isinstance(links, list):
                for entry in links:
                    if (
                        isinstance(entry, dict)
                        and entry.get("rel") == "next"
                        and isinstance(entry.get("href"), str)
                    ):
                        next_url = entry["href"]
                        break
        elif isinstance(payload, list):
            records = [item for item in payload if isinstance(item, dict)]
            next_url = None
        else:
            records = []
            next_url = None

        for record in records:
            yield record

        # Após a primeira requisição, os parâmetros são embutidos na URL de paginação.
        next_params = None

        if next_url:
            next_url = urljoin(request_url, next_url)
        else:
            break


def compute_statistics(prices: List[float]) -> Dict[str, float]:
    """Calcula média e mediana para a lista de preços."""
    if not prices:
        raise ValueError("Não há preços suficientes para calcular estatísticas.")
    return {
        "media": statistics.mean(prices),
        "mediana": statistics.median(prices),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Consulta a API de materiais do Governo Federal e calcula média e mediana "
            "dos preços dos materiais esportivos cujo nome contenha as palavras "
            "informadas, desconsiderando conectivos."
        )
    )
    parser.add_argument("descricao", help="Descrição do material esportivo a ser pesquisado.")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Mostra mensagens de depuração durante a execução.",
    )

    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    try:
        terms = sanitize_terms(args.descricao)
    except ValueError as exc:
        logging.error(str(exc))
        return 1

    logging.debug("Termos filtrados para busca: %s", terms)

    params = {"descricao_material": " ".join(terms)}

    prices: List[float] = []
    for record in iter_records(API_URL, params):
        if not record_matches(record, terms):
            continue
        price = extract_price(record)
        if price is None:
            continue
        prices.append(price)

    if not prices:
        logging.error(
            "Nenhum preço foi encontrado para os termos informados. "
            "Tente refinar a descrição."
        )
        return 1

    stats = compute_statistics(prices)

    print(f"Termos pesquisados: {' '.join(terms)}")
    print(f"Itens considerados: {len(prices)}")
    print(f"Média: {stats['media']:.2f}")
    print(f"Mediana: {stats['mediana']:.2f}")

    return 0


if __name__ == "__main__":  # pragma: no cover - ponto de entrada de script
    sys.exit(main())
