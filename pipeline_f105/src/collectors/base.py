"""
Contrato comum que todo coletor de loja deve seguir.

Cada coletor (magazine_luiza.py, kabum.py, etc.) implementa uma função
`collect(termos_busca: list[str]) -> list[dict]` que devolve uma lista de
dicionários no formato OFERTA_SCHEMA abaixo. Isso garante que o pipeline
principal (src/pipeline.py) não precisa saber nada sobre a estrutura de
cada site — só precisa da lista de dicts.

IMPORTANTE (status do projeto): nenhum coletor foi validado ainda contra o
site real (ver README, seção "Fontes candidatas"). As funções aqui lançam
NotImplementedError propositalmente até que:
  1. alguém confirme, inspecionando o site, se existe API pública/documentada
     ou se será scraping de HTML;
  2. os seletores/campos corretos sejam mapeados;
  3. os termos de uso do site permitam a coleta automatizada (ver
     src/etica.py e a seção "Coleta responsável" do README).
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import time


# Campos que TODA oferta coletada deve ter, mesmo que venha vazio/None.
# Mantenha alinhado com "Dados a coletar" do README do projeto.
OFERTA_CAMPOS = [
    "id_oferta", "nome_produto", "marca", "linha", "modelo", "ram",
    "armazenamento", "conectividade", "cor", "condicao", "loja", "vendedor",
    "preco", "moeda", "forma_pagamento", "disponibilidade",
    "beneficio_condicional", "url", "categoria", "termo_pesquisado",
    "data_coleta", "origem_dados",
]


@dataclass
class Oferta:
    """Uma linha de dados_brutos.csv. Preencha só o que a página realmente
    mostrar — não invente valor para campo ausente (ver README)."""
    id_oferta: str
    nome_produto: str
    loja: str
    url: str
    categoria: str
    termo_pesquisado: str
    preco: str = ""                 # texto ORIGINAL do preço, sem parsear ainda
    marca: str = ""
    linha: str = ""
    modelo: str = ""
    ram: str = ""
    armazenamento: str = ""
    conectividade: str = ""
    cor: str = ""
    condicao: str = ""
    vendedor: str = ""
    moeda: str = "BRL"
    forma_pagamento: str = ""
    disponibilidade: str = ""
    beneficio_condicional: str = "Nenhum"
    origem_dados: str = "SCRAPING"  # trocar para "API" quando aplicável

    def __post_init__(self):
        self.data_coleta = datetime.now(timezone.utc).astimezone().isoformat()

    def to_dict(self) -> dict:
        d = asdict(self)
        d["data_coleta"] = self.data_coleta
        return {campo: d.get(campo, "") for campo in OFERTA_CAMPOS}


class RateLimiter:
    """Espaçador simples de requisições — ver 'Coleta responsável' no README:
    limitar requisições, aplicar intervalos, evitar sobrecarregar o site."""

    def __init__(self, min_interval_seconds: float = 2.0):
        self.min_interval = min_interval_seconds
        self._last_call = 0.0

    def wait(self):
        elapsed = time.monotonic() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.monotonic()


class ColetorNaoImplementado(NotImplementedError):
    """Erro explícito para deixar claro, no log/relatório, que este coletor
    ainda é um esqueleto — e não uma falha silenciosa de rede."""
    pass
