import requests
import pandas as pd
import json
import time


# ============================================================
# CONFIGURAÇÃO
# ============================================================

API_URL = "https://site.fastshop.com.br/api/graphql"

OPERATION_NAME = "ClientManyProductsQuery"

OPERATION_HASH = (
    "ed07b92d65116b99f0587c4e7299ac5f01bd9e6f"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0"
    ),
    "Accept": "application/json",
}


# ============================================================
# MODELOS
# ============================================================

MODELOS = [
    "galaxy s26",
    "galaxy s25",
    "galaxy s24",
    "galaxy s26 ultra",
    "galaxy s26+",
    "galaxy z fold8",
    "galaxy z fold8 ultra",
    "galaxy z flip8",
    "galaxy a57",
    "galaxy a37",
]
TERMOS_EXCLUIR = [
    "capa",
    "fone",
    "buds",
    "carregador",
    "película",
    "case",
    "adaptador",
    "cabo",
    "suporte",
]


# ============================================================
# BUSCAR PÁGINA
# ============================================================

def buscar_pagina(
    keyword,
    after=None,
    first=100
):

    variables = {
        "first": first,
        "after": after,
        "sort": "score_desc",
        "term": keyword,
        "selectedFacets": [],
        "sponsoredCount": 0
    }

    params = {
        "operationName": OPERATION_NAME,
        "operationHash": OPERATION_HASH,
        "variables": json.dumps(
            variables,
            separators=(",", ":")
        )
    }

    resposta = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    resposta.raise_for_status()

    return resposta.json()


# ============================================================
# EXTRAIR PRODUTO
# ============================================================

def extrair_produto(
    node,
    keyword
):

    # --------------------------------------------------------
    # PREÇO
    # --------------------------------------------------------

    offers = node.get("offers") or {}

    preco_minimo = offers.get(
        "lowPrice"
    )

    ofertas = offers.get(
        "offers"
    ) or []

    preco = None
    preco_lista = None
    estoque = None
    vendedor = None

    if ofertas:

        primeira_oferta = ofertas[0]

        preco = primeira_oferta.get(
            "price"
        )

        preco_lista = primeira_oferta.get(
            "listPrice"
        )

        estoque = primeira_oferta.get(
            "availability"
        )

        seller_data = primeira_oferta.get(
            "seller"
        ) or {}

        vendedor = seller_data.get(
            "identifier"
        )

    # --------------------------------------------------------
    # MARCA
    # --------------------------------------------------------

    brand = node.get("brand") or {}

    fabricante = (
        brand.get("brandName")
        or brand.get("name")
    )

    # --------------------------------------------------------
    # IMAGEM
    # --------------------------------------------------------

    imagens = node.get("image") or []

    imagem = None

    if imagens:

        imagem = imagens[0].get(
            "url"
        )

    # --------------------------------------------------------
    # ESPECIFICAÇÕES
    # --------------------------------------------------------

    especificacoes = {}

    for propriedade in (
        node.get("additionalProperty")
        or []
    ):

        nome = propriedade.get(
            "name"
        )

        valor = propriedade.get(
            "value"
        )

        if nome:

            especificacoes[nome] = valor

    # --------------------------------------------------------
    # PRODUTO
    # --------------------------------------------------------

    return {

        "termo_busca": keyword,

        "id": node.get(
            "id"
        ),

        "sku": node.get(
            "sku"
        ),

        "nome": node.get(
            "name"
        ),

        "produto_grupo": (
            node.get("isVariantOf")
            or {}
        ).get("name"),

        "product_group_id": (
            node.get("isVariantOf")
            or {}
        ).get("productGroupID"),

        "fabricante": fabricante,

        "gtin": node.get(
            "gtin"
        ),

        "preco": preco,

        "preco_lista": preco_lista,

        "preco_minimo": preco_minimo,

        "estoque": estoque,

        "vendedor": vendedor,

        "imagem": imagem,

        "slug": node.get(
            "slug"
        ),

        "voltagem": especificacoes.get(
            "Voltagem"
        ),

        "cor": (
            especificacoes.get("CORES")
            or especificacoes.get("Cor")
        ),

    }

def produto_valido(produto, keyword):

    fabricante = str(
        produto.get("fabricante", "")
    ).lower()

    nome = str(
        produto.get("nome", "")
    ).lower()

    keyword = keyword.lower()

    # Precisa ser Samsung
    if "samsung" not in fabricante:
        return False

    # Precisa ser Galaxy
    if "galaxy" not in nome:
        return False

    # O modelo pesquisado precisa aparecer no nome
    modelo = keyword.replace("galaxy ", "")

    if modelo not in nome:
        return False

    return True

# ============================================================
# BUSCAR TODOS OS PRODUTOS DE UM TERMO
# ============================================================

def buscar_todos(keyword):

    print()
    print("=" * 70)
    print("BUSCANDO:", keyword)
    print("=" * 70)

    primeiro_resultado = buscar_pagina(keyword)

    products = (
        primeiro_resultado
        ["data"]
        ["search"]
        ["products"]
    )

    total = products["pageInfo"]["totalCount"]

    print("Total informado pela API:",total)
    produtos = []
    after = None

    while True:

        resultado = (
            primeiro_resultado
            if after is None
            else buscar_pagina(
                keyword,
                after=after
            )
        )

        products = (
            resultado
            ["data"]
            ["search"]
            ["products"]
        )

        edges = products.get(
            "edges",
            []
        )

        print(
            f"Offset {after or 0}/{total}:"
            f"{len(edges)} produtos"
        )

        for edge in edges:
            node = edge.get("node")

            if node:
                produto = extrair_produto(node, keyword)
                if produto_valido(produto, keyword):
                    produtos.append(produto)

        # Se retornou menos que 100,
        # provavelmente chegamos ao fim.
        if len(edges) < 100:
            break

        # Próximo offset
        if after is None:
            after = "100"
        else:
            after = str(int(after) + 100)

        # Segurança
        if int(after) >= total:
            break

        time.sleep(0.5)

    print("Total coletado:",len(produtos))

    return produtos


# ============================================================
# COLETA
# ============================================================

todos_produtos = []


for modelo in MODELOS:

    try:

        produtos = buscar_todos(
            modelo
        )

        todos_produtos.extend(
            produtos
        )

    except Exception as erro:

        print(
            f"Erro em '{modelo}':",
            erro
        )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    todos_produtos
)


# ============================================================
# REMOVER DUPLICADOS
# ============================================================

if not df.empty:

    # Primeiro tenta pelo SKU
    if "sku" in df.columns:

        df = df.drop_duplicates(
            subset=["sku"],
            keep="first"
        )

    else:

        df = df.drop_duplicates(
            subset=["id"],
            keep="first"
        )

    df = df.reset_index(
        drop=True
    )


# ============================================================
# RESUMO
# ============================================================

print()
print("=" * 70)
print("RESUMO FINAL")
print("=" * 70)

print(
    "Produtos coletados:",
    len(df)
)

print(
    "Colunas:",
    len(df.columns)
)

print()

print(
    df[
        [
            "nome",
            "sku",
            "fabricante",
            "preco",
            "preco_lista",
            "estoque",
            "vendedor"
        ]
    ].to_string(
        index=False
    )
)


# ============================================================
# CSV
# ============================================================

df.to_csv(
    "fastshop_produtos.csv",
    index=False,
    encoding="utf-8-sig"
)



print()
print("Arquivos gerados:")
print("fastshop_produtos.csv")