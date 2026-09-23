"""
Coletor: Casas Bahia.

STATUS: esqueleto, não validado.
Pendência: verificar páginas e alternativas de API do Portal de
Desenvolvedores do Grupo Casas Bahia antes de decidir por scraping puro
(ver README — referências externas).
"""

import requests
from .base import Oferta, RateLimiter, ColetorNaoImplementado

NOME_LOJA = "Casas Bahia"
BASE_URL = "https://www.casasbahia.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0 (projeto academico F105 - datamining/webscraping)"}
_rate_limiter = RateLimiter(min_interval_seconds=2.0)


def _buscar_pagina(termo_busca: str) -> str:
    _rate_limiter.wait()
    url_busca = f"{BASE_URL}/busca/{requests.utils.quote(termo_busca)}"
    resp = requests.get(url_busca, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def _parsear_cards(html: str, termo_busca: str) -> list[Oferta]:
    raise ColetorNaoImplementado(
        "Seletores da Casas Bahia ainda não foram mapeados/validados, e a "
        "API do portal de desenvolvedores ainda não foi avaliada."
    )


def collect(termos_busca: list[str], categoria: str = "Smartphones") -> list[dict]:
    ofertas: list[Oferta] = []
    for termo in termos_busca:
        html = _buscar_pagina(termo)
        ofertas.extend(_parsear_cards(html, termo))
    return [o.to_dict() for o in ofertas]
