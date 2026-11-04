# Cypher gerado × Neo4j de produção — inventário de 04/11/2026

## Fontes

- Cypher local da carga de 03/11: `chateau-data/data/out/20261103-114032/cypher/chateau-consolidado.cypher` (SHA-256 `29e0f9d432df2e7a9768df9efa92806652b7ee5757aebee6ae8b8a414865729c`), com o `arrows/domain.json` da mesma execução (SHA-256 `4d8dd5b09b975cbae6cfbcbe1b297aa65732b10b975e95fd85e614d73a2370b2`). Arquivos não versionados, com dados pessoais; não copiá-los para `docs/`.
- Inventário de produção enviado pelo usuário em [talk-ia.md](../talk-ia.md), atualizado em 04/11 às 10:33 -03, obtido do Neo4j Kernel 5.26.29. A saída não contém valores de propriedades.

As combinações de rótulos foram comparadas como conjuntos, porque a ordem devolvida por `labels()` não é garantida. Os tipos da procedure do Neo4j foram normalizados: `String` ↔ `STRING`, `Long` ↔ `INTEGER`, `Date` ↔ `DATE`. Contagens de relações foram agrupadas por combinações de rótulos de origem e destino e nome da aresta. O `domain.json` já foi conferido nó a nó e relação a relação contra o Cypher no [levantamento anterior](rev6-x-cypher-2026-11-04.md).

## Resultado

| Verificação | Resultado |
|---|---:|
| Rótulos de domínio divergentes | **0** |
| Campos de domínio ausentes, extras ou com nome diferente | **0** |
| Campos de domínio com tipo diferente | **0** |
| Relações com nome ou direção diferente | **0** |
| Contagens de nós e relações de domínio diferentes | **0** (488 nós; 603 relações em cada fonte) |
| Propriedades de relação divergentes | **0** (nenhuma gerada ou observada) |
| Constraints ausentes ou extras | **0** (21 esperadas e presentes) |
| Índices independentes extras | **0** (além de 2 índices `LOOKUP` do Neo4j) |

**Conclusão:** para a estrutura e as contagens da camada de domínio, o Neo4j observado corresponde ao Cypher gerado. As 21 constraints também correspondem. Os dois índices `LOOKUP` são da infraestrutura do Neo4j e não representam campo ou relação extra do domínio.

## Limites desta evidência

- A consulta de propriedades excluiu `SourceDocument` e `ExtractedRecord`, e as contagens excluíram a camada técnica de proveniência. A saída mostra suas duas constraints, mas não comprova suas contagens, propriedades e relações contra o Cypher.
- O inventário agrega nomes, tipos e contagens; não compara `uid` e valores de cada nó ou as extremidades de cada relação individualmente. Portanto, ele **não prova igualdade registro a registro**. Para a pergunta de estrutura, a evidência é suficiente na camada de domínio.
- O Neo4j Community usa `IS UNIQUE` para as chaves, sem impor existência de propriedade; isso continua sendo uma diferença semântica em relação a `IS KEY`/`NOT NULL` do JSON rev_6, já documentada em [rev6-x-cypher-2026-11-04.md](rev6-x-cypher-2026-11-04.md).
