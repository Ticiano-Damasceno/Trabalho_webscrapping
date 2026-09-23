"""
Gera os gráficos exigidos pela atividade (>=3 tipos diferentes, com título,
eixos identificados e legenda quando fizer sentido) como arquivos PNG, para
serem inseridos no relatório PDF. Usa Matplotlib puro — sem estilo custom
elaborado, priorizando clareza e reprodutibilidade.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import re

def _rotulo_bonito(texto):
    if texto is None:
        return ""
    texto = str(texto).replace("-", " ").strip()
    return texto.title()

def extrair_modelo_base(texto):

    if pd.isna(texto):
        return None

    texto = str(texto).lower()

    padroes = [
        (r"\bs26\b", "S26"),
        (r"\bs25\b", "S25"),
        (r"\bs24\b", "S24"),
        (r"\ba57\b", "A57"),
        (r"\ba37\b", "A37"),
        (r"z\s*fold\s*8|fold8|fold\s*8", "Z Fold8"),
        (r"z\s*flip\s*8|flip8|flip\s*8", "Z Flip8"),
    ]

    for padrao, modelo in padroes:

        if re.search(
            padrao,
            texto
        ):
            return modelo

    return None

def _salvar(fig, caminho_saida: str):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    plt.close(fig)

# def grafico_preco_medio_por_loja(df_loja: pd.DataFrame, caminho_saida: str):
#     fig, ax = plt.subplots(figsize=(7, 4.5))
#     ax.bar(df_loja["loja"], df_loja["preco_medio"], color="#1450d1")
#     ax.set_title("Preço médio por loja (ofertas válidas)")
#     ax.set_xlabel("Loja")
#     ax.set_ylabel("Preço médio (R$)")
#     ax.tick_params(axis="x", rotation=30)
#     _salvar(fig, caminho_saida)

def grafico_preco_medio_por_loja(df_loja: pd.DataFrame, caminho_saida: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    barras = ax.bar(df_loja["loja"],df_loja["preco_medio"])
    ax.set_title("Preço médio por loja (ofertas válidas)")
    ax.set_xlabel("Loja")
    ax.set_ylabel("Preço médio (R$)")
    ax.tick_params(axis="x", rotation=30)
    ax.bar_label(barras,fmt="R$ %.2f",padding=3)
    _salvar(fig, caminho_saida)

def grafico_menor_vs_maior_por_modelo(df_modelo: pd.DataFrame,caminho_saida: str):

    df_plot = df_modelo.copy()
    
    # Identifica o modelo base
    df_plot["modelo_base"] = df_plot["config"].apply(extrair_modelo_base)

    # Remove apenas registros cujo modelo não foi identificado
    df_plot = df_plot[df_plot["modelo_base"].notna()]

    # Agrupa todas as configurações do mesmo modelo
    df_plot = df_plot.groupby("modelo_base",as_index=False).agg(
            menor_preco=("menor_preco", "min"),
            maior_preco=("maior_preco", "max")
        )

    # Ordem desejada no gráfico
    ordem = [
        "A37",
        "A57",
        "S24",
        "S25",
        "S26",
        "Z Flip8",
        "Z Fold8"
    ]

    df_plot["ordem"] = df_plot["modelo_base"].apply(
            lambda x:
            ordem.index(x)
            if x in ordem
            else 999
        )
    df_plot = (df_plot.sort_values("ordem").drop(columns="ordem"))

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(df_plot))
    largura = 0.38

    barras_menor = ax.bar([i - largura / 2 for i in x],df_plot["menor_preco"],width=largura,label="Menor preço")
    barras_maior = ax.bar([i + largura / 2 for i in x],df_plot["maior_preco"],width=largura,label="Maior preço")

    ax.set_xticks(list(x))
    ax.set_xticklabels(df_plot["modelo_base"],fontsize=10)
    ax.set_title("Menor vs. maior preço por modelo")
    ax.set_xlabel("Modelo")
    ax.set_ylabel("Preço (R$)")
    ax.bar_label(barras_menor,fmt="R$ %.0f",padding=3,fontsize=8)
    ax.bar_label(barras_maior,fmt="R$ %.0f",padding=3,fontsize=8)
    ax.legend()
    _salvar(fig,caminho_saida)

def grafico_frequencia_menor_preco(df_freq: pd.DataFrame, caminho_saida: str):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df_freq["vezes_menor_preco"], labels=df_freq["loja"], autopct="%1.0f%%",startangle=90)
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

def grafico_economia_percentual(df_modelo: pd.DataFrame,caminho_saida: str):

    df_plot = df_modelo.copy()

    # Identificar modelo base
    df_plot["modelo_base"] = (df_plot["config"].apply(extrair_modelo_base))
    df_plot = df_plot[df_plot["modelo_base"].notna()]

    # Mesmo agrupamento do gráfico
    # menor vs. maior preço
    df_plot = df_plot.groupby("modelo_base",as_index=False).agg(
            menor_preco=("menor_preco", "min"),
            maior_preco=("maior_preco", "max")
        )

    # Calcular economia percentual
    df_plot["economia_percentual"] = (df_plot["maior_preco"]- df_plot["menor_preco"])/ df_plot["maior_preco"] * 100

    # Mesma ordem
    ordem = [
        "A37",
        "A57",
        "S24",
        "S25",
        "S26",
        "Z Flip8",
        "Z Fold8"
    ]

    df_plot["ordem"] = df_plot["modelo_base"].apply(lambda x:ordem.index(x)if x in ordem else 999)
    df_plot = (df_plot.sort_values("ordem").drop(columns="ordem"))
    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.bar(df_plot["modelo_base"],df_plot["economia_percentual"])
    ax.set_title("Economia percentual por modelo")
    ax.set_xlabel("Modelo")
    ax.set_ylabel("Economia (%)")
    ax.bar_label(barras,fmt="%.1f%%",padding=3)

    _salvar(fig,caminho_saida)

def gerar_todos_os_graficos(df_loja, df_modelo, df_freq, pasta_saida: str = "graficos"):
    grafico_preco_medio_por_loja(df_loja, f"{pasta_saida}/01_preco_medio_por_loja.png")
    grafico_menor_vs_maior_por_modelo(df_modelo, f"{pasta_saida}/02_menor_vs_maior_por_modelo.png")
    grafico_frequencia_menor_preco(df_freq, f"{pasta_saida}/03_frequencia_menor_preco.png")
    grafico_economia_percentual(df_modelo, f"{pasta_saida}/04_economia_percentual.png")
