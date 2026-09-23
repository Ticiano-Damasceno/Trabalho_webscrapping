"""
Aplica os critérios de elegibilidade do escopo do projeto (ver
config.CRITERIOS_ELEGIBILIDADE_DOC e o README) a um DataFrame já tratado
por src/cleaning.tratar(). Uma oferta só entra na comparação principal se
passar em TODAS as regras — caso contrário, é mantida em dados_tratados.csv
mas marcada como inválida, com o(s) motivo(s) de exclusão explicitados
(nada é descartado silenciosamente).
"""

import pandas as pd


def _motivos_exclusao(linha: pd.Series) -> list[str]:
    motivos = []

    preco = linha["preco_num"]
    if pd.isna(preco) or preco is None or preco <= 0:
        motivos.append("preço inválido/ausente")

    vendedor = str(linha["vendedor"]).strip().lower()
    if vendedor == "":
        motivos.append("vendedor não confirmado")
    elif "parceiro" in vendedor or "marketplace" in vendedor:
        motivos.append("vendido por parceiro de marketplace (não pela própria loja)")

    # if str(linha["forma_pagamento"]).strip().lower() != "pix":
    #     motivos.append("preço não é à vista no Pix")

    # beneficio = str(linha["beneficio_condicional"]).strip().lower()
    # if beneficio not in ("nenhum", ""):
    #     motivos.append("preço depende de cupom/benefício condicional")

    # if str(linha["condicao"]).strip().lower() != "novo":
    #     motivos.append("aparelho não é novo")

    # if str(linha["disponibilidade"]).strip().lower() == "esgotado":
    #     motivos.append("oferta esgotada")

    forma_pagamento = str(
        linha.get("forma_pagamento", "")
    ).strip().lower()

    if forma_pagamento not in ("", "pix"):
        motivos.append("preço não é à vista no Pix")


    beneficio = str(
        linha.get("beneficio_condicional", "")
    ).strip().lower()

    if beneficio not in ("", "nenhum"):
        motivos.append(
            "preço depende de cupom/benefício condicional"
        )


    condicao = str(
        linha.get("condicao", "")
    ).strip().lower()

    if condicao not in ("", "novo"):
        motivos.append("aparelho não é novo")


    disponibilidade = str(
        linha.get("disponibilidade", "")
    ).strip().lower()

    if disponibilidade == "esgotado":
        motivos.append("oferta esgotada")

    modelo = linha.get("modelo_norm")
    if pd.isna(modelo) or modelo is None:
        motivos.append("modelo não identificado")

    # ram = linha.get("ram_gb")
    # if pd.isna(ram) or ram is None:
    #     motivos.append("RAM não confirmada (equivalência não garantida)")

    # armazenamento = linha.get("armazenamento_gb")
    # if pd.isna(armazenamento) or armazenamento is None:
    #     motivos.append("armazenamento não confirmado (equivalência não garantida)")

    return motivos


def aplicar_elegibilidade(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona as colunas 'valida' (bool) e 'motivos_exclusao' (lista).
    Não remove nenhuma linha — quem decide o que exportar/analisar é quem
    chama esta função (normalmente: filtrar por df['valida'])."""
    df = df.copy()
    df["motivos_exclusao"] = df.apply(_motivos_exclusao, axis=1)
    df["valida"] = df["motivos_exclusao"].apply(lambda m: len(m) == 0)
    return df


def resumo_exclusoes(df: pd.DataFrame) -> pd.DataFrame:
    """Conta quantas ofertas caíram em cada motivo de exclusão — útil para
    o relatório (seção de pré-processamento) e para debugar coletores."""
    from collections import Counter
    contador = Counter()
    for motivos in df.loc[~df["valida"], "motivos_exclusao"]:
        for m in motivos:
            contador[m] += 1
    return (
        pd.DataFrame(contador.items(), columns=["motivo", "quantidade"])
        .sort_values("quantidade", ascending=False)
        .reset_index(drop=True)
    )
