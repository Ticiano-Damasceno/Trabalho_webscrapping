import requests
import pandas as pd
import time


# ============================================================
# CONFIGURAÇÃO
# ============================================================

API_URL = "https://sribsrch.ecom.samsung.com/estoresearch-api/v1/scom/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0"
    ),
    "Origin": "https://www.samsung.com",
    "Referer": "https://www.samsung.com/",
    "Content-Type": "application/x-www-form-urlencoded",
}


# ============================================================
# MODELOS / TERMOS DE BUSCA
# ============================================================

MODELOS = [
    "Galaxy S26",
    "Galaxy S25",
    "Galaxy S24",

    "Galaxy S26 Ultra",
    "Galaxy S26+",

    "Galaxy Z Fold8",
    "Galaxy Z Fold8 Ultra",
    "Galaxy Z Flip8",

    "Galaxy A57",
    "Galaxy A37",
]


# Quantidade de produtos por requisição
REQUEST_COUNT = 14


# ============================================================
# FUNÇÃO PARA CONSULTAR A API
# ============================================================

def buscar_pagina(keyword, start_index):

    dados = {
        "clientCode": "b2c",
        "storeID": "br",
        "countryCode": "br",
        "startIndex": str(start_index),
        "requestCount": str(REQUEST_COUNT),
        "clientName": "scom",
        "projection": '["*"]',
        "keyword": keyword,
        "siteCd": "br",
        "version": "v2",
        "inVokeAISummary": "false",
        "firstSearchYN": "true",
    }

    resposta = requests.post(
        API_URL,
        headers=HEADERS,
        data=dados,
        timeout=30
    )

    resposta.raise_for_status()

    return resposta.json()


# ============================================================
# EXTRAIR PRODUTOS
# ============================================================

def extrair_produtos(resultado, termo_busca):

    produtos = []

    for produto in resultado.get("searchResults", []):

        produtos.append({

            "termo_busca": termo_busca,

            "id": produto.get("id"),

            "nome": produto.get(
                "productDisplayName"
            ),

            "modelo": produto.get(
                "modelCode"
            ),

            "categoria": produto.get(
                "category"
            ),

            "sub_categoria": produto.get(
                "sub_category"
            ),

            "familia": produto.get(
                "familyMktName"
            ),

            "preco_original": produto.get(
                "msrp_price"
            ),

            "preco_venda": produto.get(
                "sale_price"
            ),

            "desconto": produto.get(
                "discount"
            ),

            "moeda": produto.get(
                "sale_price_currency_code"
            ),

            "estoque": produto.get(
                "stockStatus"
            ),

            "avaliacao": produto.get(
                "reviewRating"
            ),

            "qtd_avaliacoes": produto.get(
                "numberOfReviews"
            ),

            "data_lancamento": produto.get(
                "productLaunchDate"
            ),

            "url": produto.get(
                "pdpURL"
            ),

            "imagem": (
                produto.get("images")[0]
                if produto.get("images")
                and isinstance(produto.get("images"), list)
                else None
            ),
        })

    return produtos


# ============================================================
# BUSCAR TODAS AS PÁGINAS DE UM MODELO
# ============================================================

def buscar_todos(keyword):

    todos_produtos = []

    start_index = 0

    print("\n" + "=" * 70)
    print(f"BUSCANDO: {keyword}")
    print("=" * 70)

    while True:

        print(
            f"Consultando produtos "
            f"{start_index + 1}..."
        )

        resultado = buscar_pagina(
            keyword,
            start_index
        )

        produtos = extrair_produtos(
            resultado,
            keyword
        )

        todos_produtos.extend(produtos)

        total = resultado.get(
            "searchTotalCount",
            0
        )

        tem_mais = resultado.get(
            "hasMoreResults",
            False
        )

        print(
            f"Encontrados nesta página: "
            f"{len(produtos)}"
        )

        print(
            f"Total informado pela API: "
            f"{total}"
        )

        # Se não existem mais resultados,
        # terminamos a paginação
        if not tem_mais:

            break

        # Próxima página
        start_index += REQUEST_COUNT

        # Pequena pausa para não fazer
        # muitas requisições seguidas
        time.sleep(1)

    print(
        f"Total coletado para "
        f"'{keyword}': {len(todos_produtos)}"
    )

    return todos_produtos


# ============================================================
# EXECUTAR SCRAPER
# ============================================================

todos_produtos = []


for modelo in MODELOS:

    try:

        produtos = buscar_todos(modelo)

        todos_produtos.extend(produtos)

    except requests.RequestException as erro:

        print(
            f"Erro ao consultar "
            f"'{modelo}': {erro}"
        )

# ============================================================
# TRATANDO OS DUPLICADOS
# ============================================================

df = pd.DataFrame(
    todos_produtos
)

if not df.empty:
    df = df.drop_duplicates(
        subset=["id"]
    )

    df = df.reset_index(
        drop=True
    )

# ============================================================
# MOSTRAR RESULTADO
# ============================================================

print("\n")
print("=" * 70)
print("RESUMO FINAL")
print("=" * 70)

print(
    f"Produtos coletados: {len(df)}"
)

print(
    f"Colunas: {len(df.columns)}"
)

# ============================================================
# SALVAR CSV
# ============================================================

arquivo_csv = "samsung_produtos.csv"

df.to_csv(
    arquivo_csv,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nCSV salvo em: {arquivo_csv}"
)