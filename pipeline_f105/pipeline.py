"""
Pipeline principal do projeto F105 — Comparação de preços Samsung.

Uso:
    python pipeline.py --modo mock      # roda tudo com dados de exemplo (sem rede)
    python pipeline.py --modo coleta    # roda a coleta real (precisa dos coletores prontos)

O modo "mock" existe para o time poder testar e validar TODO o resto do
pipeline (limpeza, elegibilidade, estatísticas, gráficos) sem depender dos
coletores reais estarem prontos — troque para "coleta" quando os coletores
de src/collectors/*.py estiverem implementados e validados.
"""

import argparse
import sys
from datetime import datetime

import pandas as pd

sys.path.insert(0, "pipeline_f105")
from src import config, cleaning, eligibility, analysis, charts  # noqa: E402
from src.collectors import COLETORES  # noqa: E402


def coletar_dados_reais() -> pd.DataFrame:
    """Chama todos os coletores registrados em src/collectors/__init__.py.
    Cada coletor ainda é um esqueleto (ColetorNaoImplementado) — isso vai
    lançar erro até que pelo menos um coletor seja implementado de verdade."""
    todas_ofertas = []
    for nome_loja, modulo in COLETORES.items():
        print(f"[coleta] {nome_loja}...")
        for m in config.MODELOS_ALVO:
            ofertas = modulo.collect(m.termos_busca, categoria="Smartphones")
            todas_ofertas.extend(ofertas)
    return pd.DataFrame(todas_ofertas)


def carregar_dados_mock(caminho: str = "dados_brutos.csv") -> pd.DataFrame:
    """Carrega o CSV de exemplo (mock) já usado para prototipar o painel.
    Substitua pelo dados_brutos.csv real assim que a coleta estiver pronta."""
    return cleaning.carregar_bruto(caminho)


def rodar_pipeline(modo: str):
    print(f"=== Pipeline F105 — modo: {modo} ===")

    # 1-3. Coletar e salvar dados_brutos.csv
    if modo == "mock":
        bruto = carregar_dados_mock()
    elif modo == "coleta":
        bruto = coletar_dados_reais()
    else:
        raise ValueError("modo deve ser 'mock' ou 'coleta'")

    bruto.to_csv("./pipeline_f105/dados/dados_brutos.csv", sep=",", index=False)
    print(f"[ok] dados_brutos.csv salvo ({len(bruto)} linhas)")

    # 4-6. Tratar: normalizar espaços, remover duplicatas exatas, parsear preço/RAM/armazenamento
    print(bruto["loja"].value_counts())
    tratado = cleaning.tratar(bruto)
    print(f"[ok] duplicatas exatas removidas: {tratado.attrs.get('duplicatas_exatas_removidas', 0)}")

    # Aplicar critérios de elegibilidade (marca válida/inválida, não descarta)
    tratado = eligibility.aplicar_elegibilidade(tratado)
    n_validas = int(tratado["valida"].sum())
    print(f"[ok] ofertas válidas para comparação principal: {n_validas} / {len(tratado)}")

    if n_validas < config.VOLUME_MINIMO_OFERTAS_VALIDAS:
        print(
            f"[atenção] volume mínimo exigido é {config.VOLUME_MINIMO_OFERTAS_VALIDAS} "
            f"ofertas válidas — está em {n_validas}. Revisar cobertura de lojas/modelos."
        )

    resumo = eligibility.resumo_exclusoes(tratado)
    if len(resumo):
        print("[info] motivos de exclusão:")
        print(resumo.to_string(index=False))

    # 7. Exportar dados_tratados.csv (com todas as linhas, válidas e não válidas,
    # e a coluna 'valida'/'motivos_exclusao' explicando cada exclusão)
    tratado_export = tratado.copy()
    tratado_export["motivos_exclusao"] = tratado_export["motivos_exclusao"].apply(
        lambda lst: "; ".join(lst)
    )
    tratado_export.to_csv("./pipeline_f105/dados/dados_tratados.csv", index=False)
    print("[ok] dados_tratados.csv salvo")

    # 8. Estatísticas e comparações
    validas = tratado[tratado["valida"]].copy()
    if validas.empty:
        print("[erro] nenhuma oferta válida — não é possível gerar estatísticas/gráficos.")
        return

    gerais = analysis.estatisticas_gerais(validas)
    por_modelo = analysis.estatisticas_por_modelo(validas)
    por_loja = analysis.preco_medio_por_loja(validas)
    freq_menor_preco = analysis.frequencia_menor_preco_por_loja(por_modelo)

    print("\n=== Estatísticas gerais ===")
    for k, v in gerais.items():
        print(f"  {k}: {v}")

    por_modelo.to_csv("./pipeline_f105/dados/estatisticas_por_modelo.csv", index=False)
    por_loja.to_csv("./pipeline_f105/dados/estatisticas_por_loja.csv", index=False)

    # 9. Gráficos para o relatório
    charts.gerar_todos_os_graficos(por_loja, por_modelo, freq_menor_preco, pasta_saida="graficos")
    print("[ok] gráficos salvos em graficos/")

    print(f"\nConcluído em {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline F105 — Comparação de preços Samsung")
    parser.add_argument("--modo", choices=["mock", "coleta"], default="mock")
    args = parser.parse_args()
    rodar_pipeline(args.modo)
