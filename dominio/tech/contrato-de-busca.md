# Contrato da busca

**Implementado no Expert.** Fluxo: web `POST /api/search` com `{pergunta}` → rota Next.js acrescenta e-mail da sessão → backend `POST /api/search` → mock ou serviço de orquestração → classificação para o web. O backend limita pergunta a 1.000 caracteres. O resultado da API inclui `status`, `mensagem`, `cypher`, `avisos`, `colunas`, `linhas`, `truncado` e `tempoMs`.

`ORCHESTRATION_URL` vazia seleciona mock; preenchida, o backend chama `POST /search` com pergunta original e usuário. O serviço responde com todas as chaves do contrato (`cypher`, `avisos`, `tokens_prompt`, `segundos`, `resultado`, `recusada`, `erro`), inclusive nas falhas do modelo/banco; transporte/HTTP inválido vira indisponibilidade. O limite padrão devolvido pelo serviço é 50 linhas, máximo aceito 500.

Antes de executar Cypher gerado, Python e Quarkus conferem o tipo da consulta com `EXPLAIN` e só aceitam leitura; a transação de execução também é aberta em modo de leitura e tem timeout. A recusa é mostrada como `recusada`. Erro do modelo/serviço vira `indisponivel`; erro no Neo4j vira `erro_consulta`; resultado vazio ou só com células vazias vira `sem_resultado`.

O schema enviado ao modelo é o arquivo configurado em `CHATEAU_SCHEMA_ARQUIVO`, geralmente a fotografia [schema_producao.txt](../../chateau-expert/orchestration/schema/schema_producao.txt). Ele pode divergir do [modelo acadêmico rev_6](../modelo/grafo-academico.md). Não atribuir ao modelo capacidades ou entidades apenas porque existem no JSON Arrows.

Fontes: [rota web](../../chateau-expert/web/src/app/api/search/route.ts), [serviço backend](../../chateau-expert/backend/src/services/search.service.ts), [cliente HTTP](../../chateau-expert/backend/src/lib/orchestration.ts), [contrato da orquestração](../../chateau-expert/orchestration/README.md), [executor Quarkus](../../chateau-expert/orchestration/quarkus/src/main/java/br/uerj/chateau/orchestration/ExecutorLeitura.java).
