"""
Estatísticas e comparações exigidas pela atividade (ver README —
"Análises previstas"): quantidade de registros, preço médio/mínimo/
máximo/mediano, menor/maior preço por modelo, economia em R$ e em %,
frequência de menor preço por loja.
"""

import pandas as pd


def estatisticas_gerais(df_validas: pd.DataFrame) -> dict:
    """df_validas = subconjunto onde valida == True."""
    n_modelos = df_validas.groupby(["modelo_norm", "armazenamento_gb", "ram_gb"]).ngroups
    return {
        "n_ofertas_validas": len(df_validas),
        "n_modelos_configuracoes_unicas": n_modelos,
        "preco_medio": round(df_validas["preco_num"].mean(), 2),
        "preco_minimo": df_validas["preco_num"].min(),
        "preco_maximo": df_validas["preco_num"].max(),
        "preco_mediano": round(df_validas["preco_num"].median(), 2),
    }


# def _rotulo_config(row) -> str:
#     return f"{row['modelo_norm']} {int(row['armazenamento_gb'])}GB"

def _rotulo_config(row):

    modelo = row["modelo_norm"]
    armazenamento = row["armazenamento_gb"]

    if pd.notna(armazenamento):
        return f"{modelo} {int(armazenamento)}GB"

    return str(modelo)

def estatisticas_por_modelo(df_validas: pd.DataFrame) -> pd.DataFrame:
    """Menor/maior/média por modelo+armazenamento, com economia em R$ e %.

    economia_reais = maior_preco - menor_preco
    economia_percentual = (maior_preco - menor_preco) / maior_preco * 100
    (fórmulas exatamente como definidas no escopo do projeto)
    """
    df = df_validas.copy()
    df["config"] = df.apply(_rotulo_config, axis=1)

    linhas = []
    for config, grupo in df.groupby("config"):
        menor = grupo["preco_num"].min()
        maior = grupo["preco_num"].max()
        loja_menor = grupo.loc[grupo["preco_num"].idxmin(), "loja"]
        loja_maior = grupo.loc[grupo["preco_num"].idxmax(), "loja"]
        economia_reais = maior - menor
        economia_percentual = (economia_reais / maior * 100) if maior else 0
        linhas.append({
            "config": config,
            "menor_preco": round(menor, 2),
            "loja_menor_preco": loja_menor,
            "maior_preco": round(maior, 2),
            "loja_maior_preco": loja_maior,
            "preco_medio": round(grupo["preco_num"].mean(), 2),
            "preco_mediano": round(grupo["preco_num"].median(), 2),
            "qtd_ofertas": len(grupo),
            "economia_reais": round(economia_reais, 2),
            "economia_percentual": round(economia_percentual, 2),
        })
    return pd.DataFrame(linhas).sort_values("economia_percentual", ascending=False).reset_index(drop=True)


def preco_medio_por_loja(df_validas: pd.DataFrame) -> pd.DataFrame:
    return (
        df_validas.groupby("loja")["preco_num"]
        .agg(preco_medio="mean", preco_minimo="min", preco_maximo="max", qtd_ofertas="count")
        .round(2)
        .sort_values("preco_medio")
        .reset_index()
    )


def frequencia_menor_preco_por_loja(df_por_modelo: pd.DataFrame) -> pd.DataFrame:
    """Quantas vezes cada loja teve o menor preço, entre os modelos
    comparáveis (ou seja, considerando cobertura: só entram modelos com
    mais de uma loja ofertando)."""
    contagem = df_por_modelo["loja_menor_preco"].value_counts().reset_index()
    contagem.columns = ["loja", "vezes_menor_preco"]
    return contagem
