"""
Coletor: Samsung — loja oficial.

STATUS: esqueleto, não validado.
Pendência: inspecionar página de compra e como o preço é carregado (pode ser
renderizado via JS, exigindo Selenium em vez de requests+BeautifulSoup —
ver README, "Web scraping, a validar").
Vantagem deste site: como é a loja oficial, o "vendedor" tende a ser sempre
a própria Samsung — mas confirme mesmo assim, sem assumir.
"""

import requests
from .base import Oferta, RateLimiter, ColetorNaoImplementado

NOME_LOJA = "Samsung"
BASE_URL = "https://www.samsung.com/br"
HEADERS = {"User-Agent": "Mozilla/5.0 (projeto academico F105 - datamining/webscraping)"}
_rate_limiter = RateLimiter(min_interval_seconds=2.0)


def _buscar_pagina(termo_busca: str) -> str:
    _rate_limiter.wait()
    url_busca = f"{BASE_URL}/search/?searchvalue={requests.utils.quote(termo_busca)}"
    resp = requests.get(url_busca, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def _parsear_cards(html: str, termo_busca: str) -> list[Oferta]:
    raise ColetorNaoImplementado(
        "Seletores da Samsung.com ainda não foram mapeados/validados."
    )


def collect(termos_busca: list[str], categoria: str = "Smartphones") -> list[dict]:
    ofertas: list[Oferta] = []
    for termo in termos_busca:
        html = _buscar_pagina(termo)
        ofertas.extend(_parsear_cards(html, termo))
    return [o.to_dict() for o in ofertas]
