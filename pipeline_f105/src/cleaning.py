"""
Tratamento/limpeza de dados_brutos.csv (etapas 4-6 do "Plano de gasoduto"):
investigar ausências/duplicidades, limpar nomes, converter preços em
números, normalizar RAM/armazenamento.

Este módulo NÃO decide o que é elegível para a comparação principal —
isso é responsabilidade de src/eligibility.py, para manter cada etapa do
pipeline com uma responsabilidade clara.
"""

import re
import pandas as pd


def carregar_bruto(caminho_csv: str, separador: str = ",") -> pd.DataFrame:
    df = pd.read_csv(caminho_csv, sep=separador, dtype=str, keep_default_na=False, na_values=[])
    df.columns = [c.strip() for c in df.columns]
    return df


def normalizar_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços duplicados e nas pontas de todas as colunas de texto."""
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].astype(str).apply(lambda x: re.sub(r"\s+", " ", x.strip()))
    return df

def remover_duplicatas_exatas(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    antes = len(df)
    df2 = df.drop_duplicates().reset_index(drop=True)
    return df2, antes - len(df2)

def parsear_preco(texto_preco: str) -> float | None:
    """Converte texto de preço em número. Aceita formatos como:
    'R$ 1.234,56', '1234.56', '1.234,56 no Pix', '962,90'.
    Retorna None se não conseguir converter (ex.: 'Consulte', vazio)."""
    if texto_preco is None:
        return None
    p = str(texto_preco).strip()
    if p == "" or p.lower() == "consulte":
        return None
    p = p.replace("R$", "").strip()
    p = re.sub(r"no\s*pix", "", p, flags=re.IGNORECASE).strip()
    if "," in p and "." in p:
        p = p.replace(".", "").replace(",", ".")
    elif "," in p:
        p = p.replace(",", ".")
    try:
        return float(p)
    except ValueError:
        return None

def normalizar_gb(texto: str) -> int | None:
    """Extrai o número de GB de textos como '128 GB', '6', '8GB'."""
    if texto is None or str(texto).strip() == "":
        return None
    m = re.search(r"(\d+)", str(texto).upper().replace(" ", ""))
    return int(m.group(1)) if m else None

def tratar(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline de limpeza completo: normaliza espaços, remove duplicatas
    exatas e cria colunas numéricas/normalizadas a partir dos textos brutos.
    Preserva as colunas originais (preco, ram, armazenamento) para
    rastreabilidade — ver README, campo 'texto original do preço'."""
    df = normalizar_espacos(df)
    df, n_dup = remover_duplicatas_exatas(df)

    # df["preco_num"] = df["preco_venda"].apply(parsear_preco)
    # df["ram_gb"] = df["ram"].apply(normalizar_gb)
    # df["armazenamento_gb"] = df["armazenamento"].apply(normalizar_gb)

    df["preco_num"] = (df["preco_venda"].apply(parsear_preco))

    # Texto que será utilizado para procurar
    # características do aparelho
    texto_produto = (df["nome"].fillna("") + " " + df["modelo"].fillna(""))

    df["ram_gb"] = (texto_produto.apply(extrair_ram))

    df["armazenamento_gb"] = (texto_produto.apply(extrair_armazenamento))

    df["modelo_norm"] = texto_produto.apply(extrair_modelo)
    
    df.attrs["duplicatas_exatas_removidas"] = n_dup
    return df

def extrair_armazenamento(texto: str) -> int | None:

    if texto is None:
        return None

    texto = str(texto).upper()

    # Procura capacidades típicas de armazenamento
    padrao = r"\b(64|128|256|512|1024)\s*GB\b"

    resultados = re.findall(
        padrao,
        texto
    )

    if resultados:
        return int(resultados[-1])

    return None

def extrair_ram(texto: str) -> int | None:

    if texto is None:
        return None

    texto = str(texto).upper()

    # Casos como:
    # 8GB RAM
    # 12 GB RAM
    padrao = r"\b(\d{1,2})\s*GB\s*(?:DE\s*)?RAM\b"

    resultado = re.search(
        padrao,
        texto
    )

    if resultado:
        return int(
            resultado.group(1)
        )

    return None

def extrair_modelo(texto: str) -> str | None:

    if texto is None:
        return None

    texto = str(texto).upper()

    padroes = [
        (r"\bGALAXY\s+Z\s+FOLD\s*8\s+ULTRA\b", "Galaxy Z Fold8 Ultra"),
        (r"\bGALAXY\s+Z\s+FOLD\s*8\b", "Galaxy Z Fold8"),
        (r"\bGALAXY\s+Z\s+FLIP\s*8\b", "Galaxy Z Flip8"),

        (r"\bGALAXY\s+S26\s+ULTRA\b", "Galaxy S26 Ultra"),
        (r"\bGALAXY\s+S26\+\b", "Galaxy S26+"),
        (r"\bGALAXY\s+S26\b", "Galaxy S26"),

        (r"\bGALAXY\s+S25\b", "Galaxy S25"),
        (r"\bGALAXY\s+S24\b", "Galaxy S24"),

        (r"\bGALAXY\s+A57\b", "Galaxy A57"),
        (r"\bGALAXY\s+A37\b", "Galaxy A37"),
    ]

    for padrao, modelo in padroes:
        if re.search(padrao, texto):
            return modelo

    return None