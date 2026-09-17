Comparação de preços de smartphones Samsung

Projeto acadêmico da disciplina F105 — Datamining e Webscraping.

Status: planejamento. O escopo foi definido; os coletores, a base de dados e as análises ainda não foram implementados. As fontes listadas são candidatas, sem garantia de viabilidade da coleta.

Objetivo e pergunta de negócio

Construir um pipeline em Python para coletar, tratar e comparar preços de smartphones Samsung entre lojas online, apoiando um estudo de posicionamento de preços no mercado.

Pergunta central: quanto varia o preço do mesmo smartphone Samsung entre lojas e qual a economia em reais e percentual ao escolher a menor oferta?

Escopo definido

Critério

Definição

Marca

Samsung

Linhas

Galaxy A e Galaxy S

Condição

Aparelhos novos

Vendedor

Somente ofertas vendidas pela própria loja; excluir parceiros de marketplace

Pagamento

À vista no Pix

Frete

Não incluído na comparação

Benefícios condicionais

Excluir preços dependentes de cupons, troca de aparelho ou benefícios exclusivos

Equivalência

Comparar o mesmo modelo, memória RAM e armazenamento; distinguir versões como 4G/5G, FE, Plus e Ultra

Volume mínimo

Pelo menos 30 ofertas válidas, conforme o enunciado

Modelos específicos

Selecionar após verificar disponibilidade em mais de uma loja

“Entregue pela loja” não comprova que o produto é vendido por ela. O campo vendido por deverá ser verificado. Se o vendedor ou o preço no Pix não puderem ser confirmados, a oferta não deverá entrar na comparação principal.

A meta inicial discutida foi buscar aproximadamente 10 modelos/configurações em pelo menos 3 lojas. Essa distribuição é uma proposta, não uma exigência: poderá mudar conforme os testes, preservando o mínimo de 30 ofertas válidas. Não é necessário encontrar todos os modelos em todas as lojas.

Fontes candidatas e estratégia preliminar

Fonte

Método previsto

Situação

Magazine Luiza

Web scraping

Testar páginas públicas; API de integração voltada a vendedores não equivale a acesso aberto ao catálogo inteiro

KaBuM!

Web scraping

Validar extração de preço, especificações e vendedor

Samsung — loja oficial

Web scraping, a validar

Inspecionar páginas de compra e carregamento dos preços

Casas Bahia

Web scraping, a validar

Verificar páginas e alternativas de API adequadas ao objetivo

Amazon Brasil

API se houver acesso elegível; scraping a avaliar

Verificar elegibilidade e adequação da Creators API, além das condições de acesso às páginas

Fast Shop

Web scraping, a validar

Inspecionar estrutura das páginas; API pública adequada ainda não confirmada

A escolha definitiva depende de acesso, regras de uso, disponibilidade dos campos e quantidade de ofertas comparáveis. Nenhum coletor foi testado até esta etapa.

Avaliaremos APIs documentadas quando disponíveis. Para páginas com dados no HTML, a proposta é utilizar Requests e Beautiful Soup. Selenium será considerado apenas se necessário. Encontrar uma resposta JSON interna não comprova a existência de uma API pública autorizada.

Dados a coletar

Campos mínimos exigidos pela atividade:

Nome do produto.

Preço.

Loja ou fonte.

URL.

Categoria ou termo pesquisado.

Campos adicionais propostos para garantir comparabilidade e rastreabilidade:

Vendedor identificado na página.

Modelo, linha, RAM, armazenamento e conectividade.

Condição do aparelho e disponibilidade.

Forma de pagamento e texto original do preço.

Data e hora da coleta.

Cor e código do fabricante, quando disponíveis.

A regra para comparar cores diferentes ainda será definida. Informações ausentes não serão inventadas.

Pipeline planejado

Identificar fontes e modelos comparáveis.

Coletar automaticamente múltiplas ofertas, com paginação quando necessária.

Salvar os dados originais em dados_brutos.csv antes do tratamento.

Investigar ausências, duplicidades e inconsistências.

Limpar nomes e converter preços textuais em valores numéricos, tratando moeda e separadores.

Aplicar os filtros de elegibilidade e padronizar as configurações.

Exportar dados_tratados.csv.

Calcular estatísticas e comparar ofertas equivalentes.

Produzir gráficos, painel e conclusões baseadas nos resultados.

O relatório deverá incluir um pequeno diagrama do pipeline e uma proposta de execução automatizada. Não é obrigatório colocar o processo em produção.

Análises previstas

A atividade exige quantidade de registros, preço médio, mínimo, máximo e mediana, além de pelo menos três padrões ou insights.

Propostas de análise para este projeto:

Menor e maior preço por modelo/configuração entre lojas.

Diferença em reais e economia percentual entre essas ofertas.

Frequência com que cada loja apresenta o menor preço, considerando a cobertura de modelos comparáveis.

Para a economia entre a maior e a menor oferta, propõe-se:

economia_reais = maior_preco - menor_preco

economia_percentual = (maior_preco - menor_preco) / maior_preco * 100

A comparação principal será por modelo equivalente. A média geral de uma loja pode refletir um conjunto de aparelhos mais caros e não comprova, isoladamente, que ela cobra mais pelo mesmo produto. As conclusões deverão se limitar à amostra e ao momento da coleta. A economia calculada não inclui frete.

Não é obrigatório utilizar algoritmos complexos de Machine Learning.

Visualizações e painel

Requisitos da atividade:

Pelo menos três gráficos diferentes, com título, identificação dos eixos, legenda quando necessária e interpretação.

Painel simples com quantidade de produtos, preço médio, menor preço, maior preço e pelo menos dois gráficos.

Não é necessário publicar o painel na internet.

Os gráficos específicos ainda serão escolhidos conforme os dados. Python com Matplotlib é uma opção indicada no enunciado. Convém distinguir no painel a quantidade de ofertas e a quantidade de modelos/configurações únicos.

Coleta responsável

O relatório deverá discutir acesso público, alternativas de API, dados pessoais, risco de sobrecarga e cuidados para uso contínuo. Boas práticas propostas:

Verificar termos de uso e orientações de acesso automatizado das fontes.

Limitar requisições, aplicar intervalos e evitar downloads repetidos.

Respeitar restrições de acesso, sem contornar autenticação ou bloqueios.

Coletar apenas os campos necessários ao estudo e não publicar credenciais no repositório.

Entregáveis acadêmicos

Entregável

Requisito

Relatório em PDF

De 5 a 8 páginas, incluindo capa com nomes completos e matrículas

Código-fonte

Notebook .ipynb ou arquivos .py, com comentários sobre as etapas principais

Bases de dados

dados_brutos.csv e dados_tratados.csv

Vídeo

De 5 a 8 minutos, com participação de todos os integrantes e demonstração do processo

O relatório deverá abordar problema, objetivo, fonte, coleta, pré-processamento, análise, gráficos, painel, aspectos éticos e legais e conclusão. A coleta automática não poderá ser substituída por transcrição manual.

Prazo informado no enunciado: 25/09/2026 — Módulo B.

Nomes e matrículas devem constar na entrega acadêmica; não precisam ser expostos em um repositório público.

Base de estudo e referências externas

Materiais fornecidos para orientar o projeto:

Arquivo Base Atividade Final (Prática): enunciado e critérios de avaliação.

PA 1: fundamentos, processos e ferramentas de Data Mining e Web Scraping.

PA 2: técnicas de coleta, APIs, automação e aspectos éticos e legais.

PA 3: tratamento, transformação e caracterização dos dados.

PA 4: integração do pipeline, dashboards e insights de mercado.

O projeto deverá complementar os materiais das aulas com fontes externas, priorizando documentação oficial. Referências identificadas na etapa de planejamento:

Integração com APIs do Magalu

Documentação de produtos do Magalu

Portal de desenvolvedores do Grupo Casas Bahia

Introdução à Amazon Creators API

Essas referências não comprovam acesso liberado para o projeto. Requisitos e permissões deverão ser verificados na implementação.

Próximas decisões e etapas

Definir marca e linhas: Samsung Galaxy A e S.

Definir comparação de preços entre lojas.

Selecionar seis fontes candidatas.

Restringir às ofertas vendidas pela própria loja.

Adotar preço no Pix, sem frete.

Escolher ambiente: Jupyter no VS Code, Google Colab ou scripts Python.

Testar acesso, seletores, paginação, APIs e filtros das fontes.

Selecionar modelos/configurações e definir tratamento das cores.

Implementar coleta e obter pelo menos 30 ofertas válidas.

Tratar os dados, analisar e construir as visualizações.

Produzir relatório e roteiro do vídeo.

Este README registra o planejamento e deverá ser atualizado com instruções de execução e resultados após a implementação.
