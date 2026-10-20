# Visão geral

O Chateau apoia a descoberta de especialistas no contexto acadêmico e a seleção/formação de equipes. A aplicação entregue combina conversa, busca no grafo acadêmico, API de negócio e administração. O foco institucional apresentado no produto é a UERJ; o [README do Expert](../../chateau-expert/README.md) também cita a UFF.

Há três responsabilidades distintas:

- **Dados e modelo:** `chateau-data/` define o grafo acadêmico e extrai documentos para gerar dados rastreáveis.
- **Aplicação:** `chateau-expert/web` apresenta o produto e `chateau-expert/backend` guarda contas, permissões, termos, conversas e a API de busca.
- **Orquestração:** `chateau-expert/orchestration` transforma pergunta em Cypher e consulta o Neo4j em modo de leitura.

A busca do web atual usa o serviço real **somente quando** `ORCHESTRATION_URL` está preenchida; caso contrário, o backend devolve um mock. O [protótipo da nova interface](../../docs/analises/ui-prototipo-2026-10-20.md) é outra aplicação, ainda isolada. Exemplos e dados simulados não descrevem a cobertura real do grafo.

Fontes: [README do Expert](../../chateau-expert/README.md), [busca do backend](../../chateau-expert/backend/src/services/search.service.ts), [README do Data](../../chateau-data/README.md).
