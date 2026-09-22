import pandas as pd


# ============================================================
# ARQUIVOS
# ============================================================

ARQUIVOS = {
    "Kabum": "kabum_produtos.csv",
    "Samsung": "samsung_produtos.csv",
    "FastShop": "fastshop_produtos.csv",
}


# ============================================================
# CARREGAR CSV
# ============================================================

def carregar_csv(arquivo):

    # sep=None tenta detectar automaticamente
    # se o arquivo usa "," ou ";"
    return pd.read_csv(
        arquivo,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )


# ============================================================
# PADRONIZAR KABUM
# ============================================================

def padronizar_kabum(df):

    resultado = pd.DataFrame(index=df.index)
    resultado["loja"] = "Kabum"
    resultado["termo_busca"] = df["termo_busca"]
    resultado["id"] = df["id"]
    resultado["sku"] = None
    resultado["nome"] = df["nome"]
    resultado["modelo"] = df["modelo"]
    resultado["fabricante"] = df["fabricante"]
    resultado["preco_original"] = df["preco_original"]
    resultado["preco_venda"] = df["preco_venda"]
    resultado["desconto"] = df["desconto"]
    resultado["estoque"] = df["quantidade"]
    resultado["disponivel"] = df["disponivel"]
    resultado["vendedor"] = df["vendedor"]
    resultado["avaliacao"] = df["avaliacao"]
    resultado["qtd_avaliacoes"] = df["qtd_avaliacoes"]
    resultado["url"] = df["produto_url"]
    resultado["imagem"] = df["imagem"]

    return resultado


# ============================================================
# PADRONIZAR SAMSUNG
# ============================================================

def padronizar_samsung(df):

    resultado = pd.DataFrame(index=df.index)
    resultado["loja"] = "Samsung"
    resultado["termo_busca"] = df["termo_busca"]
    resultado["id"] = df["id"]
    resultado["sku"] = None
    resultado["nome"] = df["nome"]
    resultado["modelo"] = df["modelo"]
    resultado["fabricante"] = "Samsung"
    resultado["preco_original"] = df["preco_original"]
    resultado["preco_venda"] = df["preco_venda"]
    resultado["desconto"] = df["desconto"]
    resultado["estoque"] = df["estoque"]
    resultado["disponivel"] = None
    resultado["vendedor"] = "Samsung"
    resultado["avaliacao"] = df["avaliacao"]
    resultado["qtd_avaliacoes"] = df["qtd_avaliacoes"]
    resultado["url"] = df["url"]
    resultado["imagem"] = df["imagem"]

    return resultado


# ============================================================
# PADRONIZAR FASTSHOP
# ============================================================

def padronizar_fastshop(df):

    resultado = pd.DataFrame(index=df.index)
    resultado["loja"] = "FastShop"
    resultado["termo_busca"] = df["termo_busca"]
    resultado["id"] = df["id"]
    resultado["sku"] = df["sku"]
    resultado["nome"] = df["nome"]
    resultado["modelo"] = df["produto_grupo"]
    resultado["fabricante"] = df["fabricante"]
    resultado["preco_original"] = df["preco_lista"]
    resultado["preco_venda"] = df["preco"]
    resultado["desconto"] = None
    resultado["estoque"] = df["estoque"]
    resultado["disponivel"] = None
    resultado["vendedor"] = df["vendedor"]
    resultado["avaliacao"] = None
    resultado["qtd_avaliacoes"] = None

    resultado["url"] = df["slug"]
    resultado["imagem"] = df["imagem"]

    return resultado


# ============================================================
# CARREGAR DADOS
# ============================================================

kabum = carregar_csv(
    ARQUIVOS["Kabum"]
)

samsung = carregar_csv(
    ARQUIVOS["Samsung"]
)

fastshop = carregar_csv(
    ARQUIVOS["FastShop"]
)


# ============================================================
# PADRONIZAR
# ============================================================

kabum = padronizar_kabum(kabum)

samsung = padronizar_samsung(samsung)

fastshop = padronizar_fastshop(fastshop)


# ============================================================
# CONSOLIDAR
# ============================================================

df = pd.concat(
    [
        kabum,
        samsung,
        fastshop
    ],
    ignore_index=True
)


# ============================================================
# RESUMO
# ============================================================

print()
print("=" * 70)
print("DATA HARVEST")
print("=" * 70)

print(
    "Total de registros:",
    len(df)
)

print()

print(
    df["loja"].value_counts()
)

print()

print(
    df[
        [
            "loja",
            "nome",
            "modelo",
            "preco_venda"
        ]
    ].head(20)
)


# ============================================================
# SALVAR
# ============================================================

df.to_csv(
    "produtos_consolidados.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print(
    "Arquivo gerado: produtos_consolidados.csv"
)