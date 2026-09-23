"""
Coletor: KaBuM!

STATUS: esqueleto, não validado.
Pendências antes de implementar: confirmar separação clara entre preço,
especificações técnicas (RAM/armazenamento) e vendedor no HTML do card/página
do produto (ver README — "Validar separação de preço, especificações e
vendedor").
"""

import requests
from .base import Oferta, RateLimiter, ColetorNaoImplementado

NOME_LOJA = "KaBuM!"
BASE_URL = "https://www.kabum.com.br"
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
        "Seletores do KaBuM! ainda não foram mapeados/validados."
    )


def collect(termos_busca: list[str], categoria: str = "Smartphones") -> list[dict]:
    ofertas: list[Oferta] = []
    for termo in termos_busca:
        html = _buscar_pagina(termo)
        ofertas.extend(_parsear_cards(html, termo))
    return [o.to_dict() for o in ofertas]
