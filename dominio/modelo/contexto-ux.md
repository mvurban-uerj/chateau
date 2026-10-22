# Contexto do usuário e modelo de UX

**Modelo conceitual definido; implementação parcial no protótipo.** O [Chateau-UX.json](../../chateau-data/model/diagramas/Chateau-UX.json) define `Context` composto de `Profile`, `Objective`, `Interest`, `Document`, `Instruction`, `Availability`, `Chat` e `Consent`. `Chat` contém `Prompt`; `Instruction` aplica `Filter`. Entre filtros o modelo prevê `AND` e `OR`.

- `Interest`, `Document` e `Instruction` têm seleção; `Availability` tem habilitação.
- `Document` prevê nome, resumo e referência por arquivo, DOI ou URL.
- `Filter` prevê variável do modelo de domínio, operador (`=`, `<`, `>` ou `!=`) e valor.
- `Consent` modela nome, unidade, localização, e-mail, cookies e revogação.

**Decidido na [reunião de 20/10/2026](../../docs/reunioes/2026-10-20.md)** (substitui a decisão anterior do mesmo dia de manter o contexto no `localStorage`): o contexto do usuário — filtros, interesses, instruções e demais itens — fica no PostgreSQL, ligado ao usuário do site (conta Google). Por enquanto **não entra no envio da pesquisa**; o modelo ainda não recebe contexto. A disponibilidade começa como "disponível". O consentimento vira uma autorização de contexto, também no PostgreSQL ([termos](../negocio/termos-e-privacidade.md)).

- **Opções de filtro:** o destino é vir do grafo acadêmico, com cache e sem cópia no PostgreSQL. Por enquanto ficam **simuladas**: o backend e a web não ganham acesso ao Neo4j; o grafo só é alcançado pelo modelo, via orquestração. O que não vier do modelo fica simulado (mock) até o Edson decidir o rumo (decidido pelo Marcelo em 22/10/2026). A fonte definitiva depende do Edson.
- **Perguntas guiadas:** geradas uma vez a partir do grafo rev_6 ([`Expert-Finding-in-academia_rev_6_training.json`](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json)) e gravadas no PostgreSQL. Na interface, o campo de pesquisa monta o texto aos poucos e termina com tab, que abre um modal com as perguntas. Se um administrador poderá editá-las não foi definido.

No branch `feat/nova-ui` (`a96b322`, ainda não em `main`) estão implementados a autorização de contexto (`ContextAuthorization`, ver [termos e privacidade](../negocio/termos-e-privacidade.md)) e o contexto do usuário: `UserContext` (perfil, objetivo, disponibilidade, interesses) e `ContextInstruction` com `ContextFilter` (E entre filtros), por `GET`/`PUT /api/context`, na exportação de privacidade e apagados com a conta. Documentos ficam de fora (a busca não os lê). As opções de interesse e de condição são simuladas até a fonte ser definida. Perguntas guiadas ainda não têm tabelas.

O protótipo Vite guarda contexto e consentimento no `localStorage` e implementa só parte desse desenho. Em especial, documentos são armazenados mas não entram na busca; sua interface está desativada. O protótipo oferece apenas `=` e `!=` para filtros e trata consentimento localmente. Nada disso está integrado às tabelas, APIs ou termos do Expert atual.

Fontes: [modelo de UX](../../chateau-data/model/diagramas/Chateau-UX.json) e, no protótipo local, `src/context.ts`, `src/features.ts` e `src/consent.ts`. O caminho do protótipo deverá ser substituído por uma fonte versionada quando houver integração.
