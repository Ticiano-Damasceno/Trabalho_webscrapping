"""
Configuração central do projeto F105 — Comparação de preços Samsung.

Este módulo concentra tudo que pode mudar sem mexer na lógica do pipeline:
lojas candidatas, modelos-alvo e critérios de elegibilidade definidos no
escopo do projeto. Ajuste aqui, não espalhe "números mágicos" pelo código.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Lojas candidatas (ver README do projeto — "Fontes candidatas")
# ---------------------------------------------------------------------------
# status:
#   "planejado"  -> ainda não implementado / não validado
#   "implementado" -> coletor funcional (mesmo que só teste em algumas páginas)
LOJAS = {
    "magazine_luiza": {"nome_exibicao": "Magazine Luiza", "status": "planejado"},
    "kabum": {"nome_exibicao": "KaBuM!", "status": "planejado"},
    "samsung": {"nome_exibicao": "Samsung", "status": "planejado"},
    "casas_bahia": {"nome_exibicao": "Casas Bahia", "status": "planejado"},
    "amazon": {"nome_exibicao": "Amazon Brasil", "status": "planejado"},
    "compra_rapida": {"nome_exibicao": "Compra Rápida", "status": "planejado"},
}


@dataclass
class ModeloAlvo:
    """Um modelo/configuração que o time decidiu comparar entre lojas."""
    modelo: str          # ex: "Galaxy A15"
    ram_gb: int          # ex: 4
    armazenamento_gb: int  # ex: 128
    conectividade: str = "5G"  # distinguir 4G/5G explicitamente
    termos_busca: list = field(default_factory=list)  # variações de texto para buscar em cada loja


# ---------------------------------------------------------------------------
# Modelos-alvo (~10 configurações, conforme meta inicial do escopo).
# Ajuste esta lista depois de confirmar disponibilidade em mais de uma loja.
# ---------------------------------------------------------------------------
MODELOS_ALVO = [
    ModeloAlvo("Galaxy A15", 4, 128, termos_busca=["Galaxy A15 128GB", "Galaxy A15 5G 128GB"]),
    ModeloAlvo("Galaxy A25", 6, 128, termos_busca=["Galaxy A25 128GB"]),
    ModeloAlvo("Galaxy A35", 6, 128, termos_busca=["Galaxy A35 128GB"]),
    ModeloAlvo("Galaxy A35", 8, 256, termos_busca=["Galaxy A35 256GB"]),
    ModeloAlvo("Galaxy A55", 8, 256, termos_busca=["Galaxy A55 256GB"]),
    ModeloAlvo("Galaxy S23", 8, 128, termos_busca=["Galaxy S23 128GB"]),
    ModeloAlvo("Galaxy S23 FE", 8, 128, termos_busca=["Galaxy S23 FE 128GB"]),
    ModeloAlvo("Galaxy S24", 8, 256, termos_busca=["Galaxy S24 128GB", "Galaxy S24 256GB"]),
    ModeloAlvo("Galaxy S24 FE", 8, 256, termos_busca=["Galaxy S24 FE 256GB"]),
    ModeloAlvo("Galaxy S24 Ultra", 12, 256, termos_busca=["Galaxy S24 Ultra 256GB"]),
]


# ---------------------------------------------------------------------------
# Critérios de elegibilidade (ver README — "Escopo definido")
# Uma oferta só entra na COMPARAÇÃO PRINCIPAL se passar em todas as regras.
# Isso é aplicado em src/eligibility.py — mantenha os dois arquivos em sincronia.
# ---------------------------------------------------------------------------
CRITERIOS_ELEGIBILIDADE_DOC = """
1. Vendedor confirmado E vendido pela própria loja (não por parceiro/marketplace).
2. Preço à vista no Pix confirmado (não cartão, não boleto, não "consulte").
3. Preço não pode depender de cupom, troca de aparelho ou outro benefício condicional.
4. Aparelho novo (não usado/recondicionado).
5. Oferta disponível (não esgotada).
6. Modelo, RAM e armazenamento identificados (para garantir equivalência).
7. "Entregue pela loja" NÃO conta como "vendido pela loja" — o campo vendedor
   precisa dizer explicitamente que é a própria loja.
"""

# Campos mínimos exigidos pela atividade (ver README — "Dados a coletar")
CAMPOS_MINIMOS = ["nome_produto", "preco", "loja", "url", "categoria_termo_pesquisado"]

VOLUME_MINIMO_OFERTAS_VALIDAS = 30
