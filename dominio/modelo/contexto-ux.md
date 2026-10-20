# Contexto do usuário e modelo de UX

**Modelo conceitual definido; implementação parcial no protótipo.** O [Chateau-UX.json](../../chateau-data/model/diagramas/Chateau-UX.json) define `Context` composto de `Profile`, `Objective`, `Interest`, `Document`, `Instruction`, `Availability`, `Chat` e `Consent`. `Chat` contém `Prompt`; `Instruction` aplica `Filter`. Entre filtros o modelo prevê `AND` e `OR`.

- `Interest`, `Document` e `Instruction` têm seleção; `Availability` tem habilitação.
- `Document` prevê nome, resumo e referência por arquivo, DOI ou URL.
- `Filter` prevê variável do modelo de domínio, operador (`=`, `<`, `>` ou `!=`) e valor.
- `Consent` modela nome, unidade, localização, e-mail, cookies e revogação.

O protótipo Vite guarda contexto e consentimento no `localStorage` e implementa só parte desse desenho. Em especial, documentos são armazenados mas não entram na busca; sua interface está desativada. O protótipo oferece apenas `=` e `!=` para filtros e trata consentimento localmente. Nada disso está integrado às tabelas, APIs ou termos do Expert atual.

Fontes: [modelo de UX](../../chateau-data/model/diagramas/Chateau-UX.json) e, no protótipo local, `src/context.ts`, `src/features.ts` e `src/consent.ts`. O caminho do protótipo deverá ser substituído por uma fonte versionada quando houver integração.
