# Fontes de dados e pipeline

**Implementado em `chateau-data`.** O pipeline local extrai dados de currículos Lattes, certificados e Sucupira/CAPES para um grafo rastreável. Há três extratores no `run_all`: `general` (documentos gerais), `sucupira_api` e `sucupira_pdf`. A extração usa regras determinísticas, sem LLM. `data/in/dev` guarda amostras de desenvolvimento; `data/out` é saída gerada, não versionada.

## Regras atuais de consolidação

- Todos os extratores usam o mesmo modelo Arrows e seus dicionários. O padrão atual é `rev_6_training`, mas `--model` aceita outro modelo compatível.
- Na fusão de propriedades conflitantes, prevalece o primeiro valor; a ordem atual é `general`, `sucupira_api`, `sucupira_pdf`. Para o conflito típico entre as duas fontes Sucupira, a **API precede o PDF**. Campo ausente ainda pode ser preenchido pela fonte seguinte.
- Identificadores reais da API são preservados. Para propriedades `IS KEY` ainda sem valor após a fusão, um sequencial por caption é gerado **de novo a cada execução**; portanto, esse número não é identidade estável entre cargas.
- Cada execução grava JSON do grafo, Cypher e relatórios de normalização, proveniência (inclusive hash dos documentos), qualidade e problemas. A saída permite rastrear a origem dos valores.

## Limites conhecidos

- O PDF Sucupira distingue capítulo de livro inteiro pelo tipo de contribuição; a listagem da API não fornece esse detalhe. Na comparação das fontes, agrupar `Book` + `Chapter` do PDF antes de confrontar com `Book` da API. Nunca inferir capítulo quando a fonte não sustenta.
- A extração de produções dos PDFs Sucupira ainda perde registros. O teste `test_producoes_extracao_pdf.py`, executado nesta revisão, falhou em **20 PDFs**; por exemplo, Ivan/2016 contém 23 produções segundo a leitura independente do PDF e o pipeline extrai 2. Não tratar contagens do grafo como cobertura completa dessa fonte.
- PDF escaneado sem texto precisa de OCR. Ausência de resumo, palavras-chave ou identificador numa fonte não deve virar valor inventado.
- A investigação de `rev_5` encontrou vínculo de `ShortCourseInstance` não criado pelo extrator Lattes por falta de decisão sobre datas da oferta. Confirmar no pipeline atual antes de tratá-lo como resolvido.
- O [catálogo de cargos](../../chateau-data/model/instancias/cargos_uerj_catalogo.json) e o [banco-modelo](../../chateau-data/model/instancias/banco-modelo.json) são artefatos de modelagem/amostra; não são automaticamente o grafo de produção.

Fontes: [run_all](../../chateau-data/scripts/chateau-extract/run_all/cli.py), [modelo e dicionários](../../chateau-data/scripts/chateau-extract/common/model.py), [identificadores](../../chateau-data/scripts/chateau-extract/common/identifiers.py), [investigação PDF/API](../../chateau-data/docs/sucupira-pdf-vs-api/README.md), [levantamento do banco-modelo](../../chateau-data/docs/levantamento-campos.md). Guias antigos em `chateau-data/scripts/README.md` e `docs/knowledge-graph-pipeline.md` ainda mencionam versões/caminhos anteriores; usar código e README raiz do Data para execução atual.
