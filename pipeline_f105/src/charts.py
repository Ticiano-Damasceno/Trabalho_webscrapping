"""
Gera os gráficos exigidos pela atividade (>=3 tipos diferentes, com título,
eixos identificados e legenda quando fizer sentido) como arquivos PNG, para
serem inseridos no relatório PDF. Usa Matplotlib puro — sem estilo custom
elaborado, priorizando clareza e reprodutibilidade.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd


def _salvar(fig, caminho_saida: str):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    plt.close(fig)


def grafico_preco_medio_por_loja(df_loja: pd.DataFrame, caminho_saida: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(df_loja["loja"], df_loja["preco_medio"], color="#1450d1")
    ax.set_title("Preço médio por loja (ofertas válidas)")
    ax.set_xlabel("Loja")
    ax.set_ylabel("Preço médio (R$)")
    ax.tick_params(axis="x", rotation=30)
    _salvar(fig, caminho_saida)


# def grafico_menor_vs_maior_por_modelo(df_modelo: pd.DataFrame, caminho_saida: str):
#     fig, ax = plt.subplots(figsize=(9, 5))
#     x = range(len(df_modelo))
#     largura = 0.38
#     ax.bar([i - largura / 2 for i in x], df_modelo["menor_preco"], width=largura,
#            label="Menor preço", color="#17a673")
#     ax.bar([i + largura / 2 for i in x], df_modelo["maior_preco"], width=largura,
#            label="Maior preço", color="#d1841f")
#     ax.set_xticks(list(x))
#     ax.set_xticklabels(df_modelo["config"], rotation=45, ha="right")
#     ax.set_title("Menor vs. maior preço por modelo/configuração")
#     ax.set_xlabel("Modelo / configuração")
#     ax.set_ylabel("Preço (R$)")
#     ax.legend()
#     _salvar(fig, caminho_saida)

def grafico_menor_vs_maior_por_modelo(df_modelo, caminho_saida):

    # Apenas configurações com diferença de preço
    df_plot = df_modelo[
        df_modelo["menor_preco"] < df_modelo["maior_preco"]
    ].copy()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(df_plot))
    largura = 0.38

    ax.bar(
        [i - largura / 2 for i in x],
        df_plot["menor_preco"],
        width=largura,
        label="Menor preço"
    )

    ax.bar(
        [i + largura / 2 for i in x],
        df_plot["maior_preco"],
        width=largura,
        label="Maior preço"
    )

    ax.set_xticks(list(x))

    ax.set_xticklabels(
        df_plot["config"],
        rotation=45,
        ha="right"
    )

    ax.set_title(
        "Menor vs. maior preço por modelo/configuração"
    )

    ax.set_xlabel("Modelo / configuração")
    ax.set_ylabel("Preço (R$)")
    ax.legend()

    _salvar(fig, caminho_saida)

def grafico_frequencia_menor_preco(df_freq: pd.DataFrame, caminho_saida: str):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df_freq["vezes_menor_preco"], labels=df_freq["loja"], autopct="%1.0f%%",
           startangle=90)
    ax.set_title("Frequência de menor preço por loja")
    ax.axis("equal")
    _salvar(fig, caminho_saida)


# def grafico_economia_percentual(df_modelo: pd.DataFrame, caminho_saida: str):
#     df_ord = df_modelo.sort_values("economia_percentual")
#     fig, ax = plt.subplots(figsize=(7, 5.5))
#     ax.barh(df_ord["config"], df_ord["economia_percentual"], color="#a13ed1")
#     ax.set_title("Economia percentual por modelo (menor preço vs. maior preço)")
#     ax.set_xlabel("Economia (%)")
#     ax.set_ylabel("Modelo / configuração")
#     _salvar(fig, caminho_saida)

def grafico_economia_percentual(df_modelo, caminho_saida):

    df_plot = df_modelo[
        df_modelo["economia_percentual"] > 0
    ].copy()

    df_plot = df_plot.sort_values(
        "economia_percentual"
    )

    # Altura aumenta conforme o número de modelos
    altura = max(
        5,
        len(df_plot) * 0.4
    )

    fig, ax = plt.subplots(
        figsize=(9, altura)
    )

    ax.barh(
        df_plot["config"],
        df_plot["economia_percentual"]
    )

    ax.set_title(
        "Economia percentual por modelo"
    )

    ax.set_xlabel("Economia (%)")
    ax.set_ylabel("Modelo / configuração")

    _salvar(fig, caminho_saida)

def gerar_todos_os_graficos(df_loja, df_modelo, df_freq, pasta_saida: str = "graficos"):
    grafico_preco_medio_por_loja(df_loja, f"{pasta_saida}/01_preco_medio_por_loja.png")
    grafico_menor_vs_maior_por_modelo(df_modelo, f"{pasta_saida}/02_menor_vs_maior_por_modelo.png")
    grafico_frequencia_menor_preco(df_freq, f"{pasta_saida}/03_frequencia_menor_preco.png")
    grafico_economia_percentual(df_modelo, f"{pasta_saida}/04_economia_percentual.png")
