# Visão geral

O Chateau apoia a descoberta de especialistas no contexto acadêmico e a seleção/formação de equipes. A aplicação entregue combina conversa, busca no grafo acadêmico, API de negócio e administração. O foco institucional apresentado no produto é a UERJ; o [README do Expert](../../chateau-expert/README.md) também cita a UFF.

Há três responsabilidades distintas:

- **Dados e modelo:** `chateau-data/` define o grafo acadêmico e extrai documentos para gerar dados rastreáveis.
- **Aplicação:** `chateau-expert/web` apresenta o produto e `chateau-expert/backend` guarda contas, permissões, autorização de contexto, contexto do usuário, conversas e a API de busca.
- **Orquestração:** `chateau-expert/orchestration` transforma pergunta em Cypher e consulta o Neo4j em modo de leitura.

## Fluxo de ponta a ponta

Confirmado pelo Marcelo em 22/10/2026. As etapas são construídas **em paralelo** e cada uma depende do contrato da seguinte, não do seu estado pronto.

1. **Dados → grafo** (`chateau-data`): lê documentos, currículos Lattes, Sucupira e outras fontes; extrai segundo o modelo acadêmico vigente (rev_6 training) e gera o Cypher que popula o Neo4j.
2. **Pergunta** (web): o usuário escreve em linguagem natural no chat; o web envia à API, que encaminha à orquestração.
3. **Interpretação** (modelo treinado): o modelo texto→Cypher interpreta a pergunta e gera a consulta Cypher.
4. **Consulta** (orquestração → Neo4j): a consulta gerada roda no grafo, somente leitura, e os dados voltam pelo mesmo caminho (orquestração → API → web), com o Cypher usado.
5. **Apresentação** (web): com os dados devolvidos, a interface monta a resposta; quando são pessoas, cartões de perfil ([nova UI](../../docs/nova-ui/README.md#chat-livre--cartões-decidido-em-22102026)).

Consequência: tudo o que a resposta traz — inclusive instituição, área ou quantidade de artigos — vem do grafo, pelas colunas que o Cypher gerado escolheu. Não há regra de negócio no backend que complete ou ranqueie os dados. O que o grafo ainda não tem, ou que o modelo ainda não sabe consultar, não pode aparecer como dado real.

**Acesso ao grafo (decidido em 22/10/2026):** o backend e a web não ganham acesso ao Neo4j; o grafo só é alcançado pelo modelo, via orquestração. O que não vier do modelo fica simulado (mock) até o Edson decidir o rumo (decidido pelo Marcelo em 22/10/2026). Pode ser revisto no futuro; até lá, não se constrói caminho novo até o Neo4j para depois desfazer.

No código atual, quem executa a consulta no Neo4j é o serviço de orquestração, não o modelo: o modelo só gera o Cypher, e os dados seguem da orquestração para a API sem voltar ao modelo ([contrato](../tech/contrato-de-busca.md)).

## Estado atual

A busca do web atual usa o serviço real **somente quando** `ORCHESTRATION_URL` está preenchida; caso contrário, o backend devolve um mock. O [protótipo da nova interface](../../docs/analises/ui-prototipo-2026-10-20.md) é outra aplicação, ainda isolada. Exemplos e dados simulados não descrevem a cobertura real do grafo.

Fontes: [README do Expert](../../chateau-expert/README.md), [busca do backend](../../chateau-expert/backend/src/services/search.service.ts), [README do Data](../../chateau-data/README.md).
