"""
Coletor: Magazine Luiza.

STATUS: esqueleto, não validado (ver config.LOJAS["magazine_luiza"]["status"]).

Antes de implementar de verdade:
  - Inspecionar se a página de busca é renderizada no HTML inicial ou via
    JavaScript (nesse caso, requests+BeautifulSoup não basta).
  - Confirmar se existe endpoint JSON interno chamado pela página (Network
    tab do navegador) — mas lembre: um JSON interno encontrado por engenharia
    reversa NÃO é a mesma coisa que uma API pública autorizada para uso
    automatizado. Ler os Termos de Uso antes de decidir.
  - "Entregue pela loja" no card do produto não é o mesmo que "vendido pela
    loja" — o vendedor real geralmente aparece só na página do produto.
"""

import requests
from bs4 import BeautifulSoup

from .base import Oferta, RateLimiter, ColetorNaoImplementado

NOME_LOJA = "Magazine Luiza"
BASE_URL = "https://www.magazineluiza.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (projeto academico F105 - datamining/webscraping)"
}

_rate_limiter = RateLimiter(min_interval_seconds=2.0)


def _buscar_pagina(termo_busca: str) -> str:
    """Faz a requisição HTTP da página de busca. Isolado numa função própria
    para facilitar troca por Selenium depois, se a página exigir JS."""
    _rate_limiter.wait()
    url_busca = f"{BASE_URL}/busca/{requests.utils.quote(termo_busca)}/"
    resp = requests.get(url_busca, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def _parsear_cards(html: str, termo_busca: str) -> list[Oferta]:
    """TODO: mapear os seletores reais depois de inspecionar o HTML.
    Estrutura de exemplo (ilustrativa, NÃO confirmada):

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("[data-testid='product-card-container']")
        ofertas = []
        for card in cards:
            nome = card.select_one("[data-testid='product-title']")
            preco = card.select_one("[data-testid='price-value']")
            link = card.select_one("a")
            ...
        return ofertas
    """
    raise ColetorNaoImplementado(
        "Seletores do Magazine Luiza ainda não foram mapeados/validados. "
        "Inspecione o HTML real antes de implementar este método."
    )


def collect(termos_busca: list[str], categoria: str = "Smartphones") -> list[dict]:
    """Ponto de entrada usado pelo pipeline. Devolve lista de dicts prontos
    para virar linhas de dados_brutos.csv."""
    ofertas: list[Oferta] = []
    for termo in termos_busca:
        html = _buscar_pagina(termo)
        ofertas.extend(_parsear_cards(html, termo))
    return [o.to_dict() for o in ofertas]
