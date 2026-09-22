import requests
import pandas as pd
import json
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURAÇÃO
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0"
    )
}


# ============================================================
# TERMOS DE BUSCA
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


# ============================================================
# VALIDAR PRODUTO
# ============================================================

def produto_valido(produto, keyword):

    fabricante = str(produto.get("fabricante", "")).lower()
    nome = str(produto.get("nome", "")).lower()
    keyword = keyword.lower()

    if "samsung" not in fabricante:
        return False

    modelo = keyword.replace("galaxy ","")

    if modelo not in nome:
        return False

    return True


# ============================================================
# BUSCAR PÁGINA
# ============================================================

def buscar_pagina(url):

    resposta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    script = soup.find("script",id="__NEXT_DATA__")

    if not script:
        raise Exception("__NEXT_DATA__ não encontrado")

    return json.loads(
        script.string
    )


# ============================================================
# EXTRAIR PRODUTOS
# ============================================================

def extrair_produtos(
    dados,
    termo_busca
):

    catalog = (
        dados["props"]
        ["pageProps"]
        ["data"]
        ["catalogServer"]
    )

    produtos = catalog["data"]

    resultado = []

    for produto in produtos:

        produto_extraido = {

            "termo_busca": termo_busca,

            "id": produto.get(
                "code"
            ),

            "nome": produto.get(
                "name"
            ),

            "modelo": produto.get(
                "friendlyName"
            ),

            "fabricante": (
                produto.get(
                    "manufacturer",
                    {}
                )
                .get("name")
            ),

            "categoria": produto.get(
                "category"
            ),

            "vendedor": produto.get(
                "sellerName"
            ),

            "seller_id": produto.get(
                "sellerId"
            ),

            "preco_original": produto.get(
                "oldPrice"
            ),

            "preco_venda": produto.get(
                "priceWithDiscount"
            ),

            "desconto": produto.get(
                "discountPercentage"
            ),

            "quantidade": produto.get(
                "quantity"
            ),

            "avaliacao": produto.get(
                "averageRating"
            ),

            "qtd_avaliacoes": produto.get(
                "ratingCount"
            ),

            "disponivel": produto.get(
                "available"
            ),

            "marketplace": (
                produto.get(
                    "flags",
                    {}
                )
                .get("isMarketplace")
            ),

            "oferta": (
                produto.get(
                    "flags",
                    {}
                )
                .get("isOffer")
            ),

            "frete_gratis": (
                produto.get(
                    "flags",
                    {}
                )
                .get("isFreeShipping")
            ),

            "imagem": produto.get(
                "image"
            ),

            "thumbnail": produto.get(
                "thumbnail"
            ),

            "produto_url": (
                "https://www.kabum.com.br"
                "/produto/"
                + str(
                    produto.get("code")
                )
            ),
        }

        # Adiciona apenas produtos válidos
        if produto_valido(
            produto_extraido,
            termo_busca
        ):

            resultado.append(
                produto_extraido
            )

    return resultado


# ============================================================
# BUSCAR TODOS OS PRODUTOS
# ============================================================

def buscar_todos(keyword):

    primeira_url = (
        "https://www.kabum.com.br/busca/"
        + keyword.replace(
            " ",
            "-"
        )
    )

    print("=" * 70)
    print(
        "BUSCANDO:",
        keyword
    )
    print("=" * 70)

    dados = buscar_pagina(
        primeira_url
    )

    catalog = (
        dados["props"]
        ["pageProps"]
        ["data"]
        ["catalogServer"]
    )

    meta = catalog["meta"]

    total_produtos = meta[
        "totalItemsCount"
    ]

    total_paginas = meta[
        "totalPagesCount"
    ]

    tamanho_pagina = meta[
        "page"
    ]["size"]

    print(
        "Total de produtos:",
        total_produtos
    )

    print(
        "Total de páginas:",
        total_paginas
    )

    print(
        "Produtos por página:",
        tamanho_pagina
    )

    produtos = []

    # Primeira página
    produtos.extend(
        extrair_produtos(
            dados,
            keyword
        )
    )

    # Demais páginas
    for pagina in range(
        2,
        total_paginas + 1
    ):

        url = (
            primeira_url
            + f"?page_number={pagina}"
        )

        print(
            f"\nConsultando página "
            f"{pagina}/{total_paginas}"
        )

        dados_pagina = buscar_pagina(
            url
        )

        produtos.extend(
            extrair_produtos(
                dados_pagina,
                keyword
            )
        )

    print(
        "Produtos válidos:",
        len(produtos)
    )

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
            f"Erro em {modelo}: "
            f"{erro}"
        )


# ============================================================
# REMOVER DUPLICADOS
# ============================================================

df = pd.DataFrame(
    todos_produtos
)

if not df.empty:

    df = df.drop_duplicates(
        subset=["id"],
        keep="first"
    )

    df = df.reset_index(
        drop=True
    )


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 70)
print("RESUMO FINAL")
print("=" * 70)

print(
    "Produtos encontrados:",
    len(df)
)

print(
    "Colunas:",
    len(df.columns)
)

# ============================================================
# CSV
# ============================================================

df.to_csv(
    "kabum_produtos.csv",
    index=False,
    encoding="utf-8-sig"
)


print()
print("Arquivos gerados:")
print("kabum_produtos.csv")