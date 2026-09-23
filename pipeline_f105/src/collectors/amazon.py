"""
Coletor: Amazon Brasil.

STATUS: esqueleto, não validado.
Pendência mais importante desta loja: confirmar elegibilidade e adequação da
Amazon Creators API ao objetivo do projeto ANTES de fazer scraping de
páginas — a Amazon é conhecida por bloquear/limitar scraping agressivamente,
e a Creators API pode ser a via correta (ver README — "Introdução à API
Amazon Creators"). Se nem API nem scraping forem viáveis dentro dos termos de
uso, documentar essa decisão no relatório em vez de forçar a coleta.
"""

import requests
from .base import Oferta, RateLimiter, ColetorNaoImplementado

NOME_LOJA = "Amazon Brasil"
BASE_URL = "https://www.amazon.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0 (projeto academico F105 - datamining/webscraping)"}
_rate_limiter = RateLimiter(min_interval_seconds=3.0)  # intervalo maior: loja mais sensível a bloqueio


def _via_api(termos_busca: list[str]) -> list[Oferta]:
    """Caminho preferencial, se a Creators API for elegível para o projeto."""
    raise ColetorNaoImplementado(
        "Elegibilidade da Amazon Creators API ainda não foi confirmada."
    )


def _via_scraping(termos_busca: list[str]) -> list[Oferta]:
    """Caminho alternativo, só se a API não for viável. Ver aviso acima."""
    raise ColetorNaoImplementado(
        "Scraping da Amazon ainda não foi avaliado/validado (risco de "
        "bloqueio e de violar termos de uso é maior aqui que nas outras lojas)."
    )


def collect(termos_busca: list[str], categoria: str = "Smartphones") -> list[dict]:
    try:
        ofertas = _via_api(termos_busca)
    except ColetorNaoImplementado:
        ofertas = _via_scraping(termos_busca)
    return [o.to_dict() for o in ofertas]
