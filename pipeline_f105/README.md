# F105 — Pipeline de comparação de preços Samsung

Pipeline em Python para coletar, tratar e comparar preços de smartphones
Samsung (linhas Galaxy A e Galaxy S) entre lojas online, respondendo:
**quanto o preço varia entre lojas e qual a economia (R$ e %) ao escolher a
menor oferta?**

## Status atual

- ✅ Módulos de tratamento, elegibilidade, estatísticas e gráficos —
  **implementados e testados** (rodam ponta a ponta em modo `mock`).
- ⏳ Coletores reais (`src/collectors/*.py`) — **esqueletos**, ainda não
  validados contra os sites reais. Cada um lança `ColetorNaoImplementado`
  de propósito, com comentários do que falta investigar (ver cada arquivo).
- ⏳ `dados_brutos.csv` / `dados_tratados.csv` reais — ainda não existem;
  o que está em `dados/` agora é gerado a partir do dataset de exemplo
  (`dados_brutos_mock.csv`), só para validar o pipeline.

## Como rodar

```bash
pip install -r requirements.txt

# roda tudo com dados de exemplo, sem precisar de rede/coletores prontos
python pipeline.py --modo mock

# quando os coletores estiverem implementados:
python pipeline.py --modo coleta
```

Saídas em `dados/`: `dados_brutos.csv`, `dados_tratados.csv`,
`estatisticas_por_modelo.csv`, `estatisticas_por_loja.csv`.
Saídas em `graficos/`: 4 PNGs (preço médio por loja, menor vs. maior por
modelo, frequência de menor preço por loja, economia percentual).

## Estrutura

```
pipeline.py              # orquestra tudo (coleta -> limpeza -> elegibilidade -> análise -> gráficos)
src/
  config.py              # lojas candidatas, modelos-alvo, critérios de elegibilidade
  cleaning.py             # normaliza texto, parseia preço/RAM/armazenamento, remove duplicatas exatas
  eligibility.py          # aplica as regras do escopo (vendedor, Pix, sem cupom, novo, etc.)
  analysis.py             # estatísticas gerais, por modelo, economia, frequência de menor preço
  charts.py               # 4 gráficos matplotlib para o relatório PDF
  collectors/
    base.py               # schema comum (classe Oferta) e RateLimiter
    magazine_luiza.py      # esqueleto — requests+BeautifulSoup, seletores por mapear
    kabum.py                # esqueleto
    samsung.py               # esqueleto
    casas_bahia.py           # esqueleto
    amazon.py                 # esqueleto — decidir API Creators vs. scraping
    compra_rapida.py          # esqueleto — domínio ainda a confirmar
dados/
  dados_brutos_mock.csv    # dataset de exemplo (73 ofertas simuladas) usado no modo "mock"
```

## Próximos passos para tirar do "esqueleto"

1. Escolher **um** coletor por vez, inspecionar a página real (Network tab
   do navegador) e decidir: API documentada, JSON interno (cuidado: não é
   API pública autorizada) ou HTML puro (requests+BeautifulSoup) ou exige
   JS (Selenium).
2. Confirmar em cada site o campo que identifica o **vendedor real** (não
   "entregue pela loja") e o **preço no Pix** especificamente.
3. Implementar `_parsear_cards()` daquele coletor, testar com 1-2 termos de
   busca, comparar campos extraídos com o schema em `collectors/base.py`.
4. Repetir para as demais lojas até ter pelo menos 3 lojas funcionando e
   >= 30 ofertas válidas (ver `config.VOLUME_MINIMO_OFERTAS_VALIDAS`).
5. Rodar `python pipeline.py --modo coleta` e revisar
   `dados/dados_tratados.csv` + o resumo de exclusões impresso no console.

## Coleta responsável

Antes de implementar qualquer coletor: ler os termos de uso do site,
manter o `RateLimiter` (intervalo mínimo entre requisições) definido em
`collectors/base.py`, coletar somente os campos necessários ao estudo, e
nunca commitar credenciais/tokens de API no repositório.
