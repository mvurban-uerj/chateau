# Campos da nova UI × grafo rev_6 — 27/10/2026

Mapeamento estático conferido contra `chateau-data` `fea4635` (JSON Arrows rev_6) e `chateau-expert` `dc77c53` (`web/src/lib/chateau/cartoes.ts`, gavetas e comparação). É uma análise para a integração, **não** uma regra nova de produto. O `orchestration/schema/schema_producao.txt` versionado é uma fotografia antiga do grafo, não uma leitura do banco ao vivo; sem acesso ao Neo4j não há confirmação de contagens nem de valores carregados hoje. A carga rev_6 e a reextração desse schema seguem pendentes no [TODO](../todo.md).

O web transforma linhas da busca em cartões quando identifica pessoas. Só mapeia colunas diretas de e-mail, Lattes, ORCID, unidade, área, cargo, vínculo e campus. Nome vem do `Person` ou de uma coluna reconhecida. As demais colunas escalares ficam em `evidencias`; relações e listas não preenchem automaticamente os campos do cartão. Qualquer campo ausente recebe valor simulado em vermelho. Uma resposta inteira de mock é marcada como simulada, inclusive nome e campos que vierem na linha do mock.

| Campo na UI | Caminho possível no rev_6 | Schema de produção versionado | Web atual |
|---|---|---|---|
| Nome | `Person.name` | `Person.name` consta | Pode vir da linha/nó; mock em vermelho |
| E-mail | `Person.email` | Consta | Aceita `email` da linha; se ausente, simula e não oferece link |
| Lattes / ORCID | `Person.identifierLattes` / `identifierORCID` | Constam | Aceita identificadores da linha; simulados não viram link |
| Área / linha | `Person -[:CONTRIBUTES_TO]-> LineOfResearch.name` | Relação e nó constam | Aceita alias escalar `area`, `linha` ou `linhaDePesquisa`; não percorre a relação |
| Unidade | `Person -[:WORKS_AT]-> WorkPlace -[:PART_OF]-> OrganizationalUnit.name` | `OrganizationalUnit` consta, mas não o caminho desde `Person` | Aceita alias `unidade`, `instituicao`, `departamento` ou `lotacao`; caso contrário simula |
| Cargo | `Person -[:WORKS]-> Job.jobTitle` | `Job`/`WORKS` ausentes | Aceita alias `cargo`; caso contrário simula |
| Vínculo | `Person -[:HAS_ROLE]-> Role.roleName` (dicionário: `tipoVinculo`) | `Role`/`HAS_ROLE` ausentes | Aceita alias `vinculo`; caso contrário simula. Confirmar se esse conceito cobre todo o texto mostrado na UI |
| Campus | `Person -[:WORKS_AT]-> WorkPlace -[:PART_OF]-> OrganizationalUnit -[:PART_OF]-> Campus.name` | `WorkPlace`/`Campus` e esse caminho ausentes | Aceita alias `campus`; caso contrário simula |
| Biografia | `Person -[:WROTE]-> Biography.abstract` | Caminho e nó constam | Sempre simulada; o construtor não lê bio da resposta |
| Ensino / disciplinas | `Person -[:TAUGHT]-> CourseInstance -[:OF]-> Course.name` (também `ShortCourseInstance`/`ShortCourse`) | `TAUGHT`, `CourseInstance` e `Course` ausentes; há `ShortCourse`, mas só `ATTENDED` | Sempre simulado |
| Reconhecimentos | `Person -[:RECEIVED]-> Acknowledgment.description` | Ausentes | Sempre simulados |
| Desde / tempo de casa | `WORKS.jobStartDate`; a regra de "primeiro vínculo no lugar atual" exige decidir como agregar vínculos | `WORKS` ausente | Sempre simulado |
| Projeto ativo | `Person -[:IS_MEMBER_OF]-> ResearchProject` com `startDate`/`endDate` | Caminho e nó constam | Sempre simulado; não há regra confirmada para transformar datas em booleano |
| Disponibilidade | `UserContext.available` no PostgreSQL do usuário; não é propriedade do grafo acadêmico | Não se aplica | No cartão de terceiros é sempre simulada; a disponibilidade de "Meu contexto" é real, mas ainda não entra na busca |
| Aderência, justificativa e caminho exibido | Exigem cálculo, explicação ou caminho da busca; não são propriedades diretas do rev_6 | Não há contrato estruturado para esses campos | Sempre simulados, mesmo com resposta real do grafo; o caminho fake usa rótulos de aresta apenas como demonstração |
| Cobertura e equipe | Contagens e composição dependem do escopo, dos critérios e de contrato do modelo; não são propriedades diretas | Não há contrato | `escopo` e `comCurriculo` simulados; `atendem` é a quantidade de linhas de pessoas e só deixa de ser simulado quando a resposta inteira é real. Montar equipe permanece desabilitado |

## O que precisa ser confirmado antes de usar dados reais

1. No Neo4j de produção, confirmar a versão carregada, a existência das relações acima e a quantidade de pessoas com cada propriedade/caminho. O schema versionado não prova preenchimento.
2. Na orquestração, registrar exemplos reais de `colunas` e `linhas` para perguntas sobre pessoas. O modelo gera Cypher livre; uma relação existente no grafo não garante que sua resposta venha como alias reconhecido pelo web.
3. Definir com o Edson um contrato de resposta para aderência, justificativa, caminho, cobertura e equipe, e o significado de vínculo, projeto ativo e disponibilidade de terceiros. O construtor atual não extrai esses conceitos.
4. Após a carga rev_6, atualizar `schema_producao.txt` e o schema usado pelo modelo; só então escolher consultas/enriquecimento sem simular que o backend ou a web têm acesso direto ao Neo4j.

Fontes: [modelo e dicionário](../../chateau-data/model/diagramas/training/), [schema de produção](../../chateau-expert/orchestration/schema/schema_producao.txt), [construtor dos cartões](../../chateau-expert/web/src/lib/chateau/cartoes.ts), [dados simulados](../../chateau-expert/web/src/lib/chateau/simulados.ts), [contrato de busca](../../dominio/tech/contrato-de-busca.md).
