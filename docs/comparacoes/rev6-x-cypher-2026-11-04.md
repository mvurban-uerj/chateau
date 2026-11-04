# Modelo rev_6 × Cypher da carga de 03/11/2026

## Fontes e verificação

- Referência: `chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json`, commit Data `2f20d84`.
- Saída do pipeline: `chateau-data/data/out/20261103-114032/arrows/domain.json` e `cypher/chateau-consolidado.cypher` (não versionados; podem conter dados pessoais). SHA-256 do Cypher: `29e0f9d432df2e7a9768df9efa92806652b7ee5757aebee6ae8b8a414865729c`; do `domain.json`: `4d8dd5b09b975cbae6cfbcbe1b297aa65732b10b975e95fd85e614d73a2370b2`.
- Reproduzir, da raiz: `python3 docs/comparacoes/comparar_rev6_cypher.py chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json chateau-data/data/out/20261103-114032/arrows/domain.json chateau-data/data/out/20261103-114032/cypher/chateau-consolidado.cypher`.

O script lê diretamente os `MERGE` e `SET` do Cypher, confere cada nó, rótulo, valor, tipo e relação da camada de domínio com `domain.json`, e compara sua estrutura com o JSON rev_6. Não imprime valores nem consulta o servidor. A camada técnica de proveniência (`SourceDocument`, `ExtractedRecord`, `HAS_EXTRACTED_RECORD`) é externa ao modelo acadêmico e fica fora das contagens de domínio.

## Resultado estrutural

**Resultado para nomes, tipos e direções:** nenhuma divergência nos elementos de domínio que o Cypher materializa. O arquivo é uma **carga de dados**, não uma declaração exaustiva de todos os campos e relações possíveis no JSON. Por isso, as contagens de rótulos, campos e padrões abaixo medem somente a cobertura dos dados capturados; **não são diferenças de estrutura** a corrigir no modelo ou no gerador.

| Item | Modelo rev_6 | Cypher gerado | Leitura |
|---|---:|---:|---|
| Nós de domínio | Modelo, sem instâncias | 488 | Iguais ao `domain.json` |
| Relações de domínio | Modelo, sem instâncias | 603 | Iguais ao `domain.json`, inclusive direção |
| Rótulos principais com nós | 25 possíveis | 13 | Cobertura da carga: 12 sem dados capturados; não é divergência de esquema |
| Pares rótulo–campo com valor em ao menos um nó | 131 possíveis | 46 | Cobertura da carga: 85 sem valor; não é divergência de esquema |
| Campo de nó com nome ou tipo fora do JSON | — | 0 | Nenhum; `DATE` é emitido como `date(...)`, `INTEGER` como inteiro |
| Padrões dirigidos de relação com instâncias | 49 possíveis | 13 | Cobertura da carga: 36 sem arestas; nenhum padrão extra ou invertido |
| Relações com propriedade preenchida | 8 tipos do modelo declaram propriedades | 0 | Ausência de dados de propriedades nas arestas; não é divergência de esquema |
| Campos `IS KEY` | 19 | 19 constraints `IS UNIQUE` | Unicidade declarada; não equivale a existência obrigatória |
| Campos `NOT NULL` | 48 | 0 constraints de existência | 14 pares rótulo–campo obrigatórios faltam em pelo menos um nó; 808 ausências ao somar nós afetados |

Um **padrão de relação** é a tripla `(rótulo de origem, tipo da aresta, rótulo de destino)`. Por exemplo, `(:Person)-[:IS_AUTHOR_OF]->(:Article)` é um dos 49 padrões admitidos pelo rev_6; ele está entre os 13 para os quais o Cypher contém ao menos uma aresta concreta. Os outros 36 continuam válidos no modelo, apenas não têm ocorrências nesta carga.

Os 12 rótulos sem nós são `AcademicWork`, `Acknowledgment`, `Campus`, `Course`, `CourseInstance`, `Job`, `JobPosting`, `Role`, `Service`, `Syllabus`, `Topic` e `WorkPlace`. A ausência de instância não significa que o Cypher declare um esquema diferente: **o arquivo de carga só materializa rótulos, campos e padrões que têm dados**, além de constraints de unicidade.

Entre os campos obrigatórios sem preenchimento estão `Article.abstract` (337/337 ausentes), `Article.keywords` (337/337), `ResearchProject.description` (87/87), `ResearchProject.startDate` (9/87) e `Biography.date` (5/5). Isso é limitação dos dados capturados. O efeito estrutural relevante é que o Cypher não cria constraints de existência para `NOT NULL`. O script confirma que os nomes e tipos dos campos presentes coincidem com o JSON.

## O Cypher é exatamente a estrutura do Neo4j?

**Não há equivalência automática entre esses três objetos:** o JSON descreve a estrutura permitida; o Cypher é uma carga de instâncias e de constraints; o Neo4j guarda o resultado efetivo da execução. O pipeline gera `MERGE`/`SET` a partir do `domain.json` e serializa valores conforme os tipos do modelo. A conferência local encontrou correspondência exata entre esse domínio exportado e o Cypher gerado.

O script `chateau-data/scripts/publicar_producao.sh` apaga os **nós e relações** antes de executar a carga e confere contagens depois. Ele **não remove constraints/índices antigos**. Além disso, Neo4j Community não impõe tipos ou existência de propriedade no schema, e `IS KEY` foi traduzido para `IS UNIQUE` porque `NODE KEY`/existência exigem Enterprise. Assim, mesmo após uma carga concluída, o banco pode reter constraints anteriores e pode ser modificado por outra operação. A igualdade atual entre arquivo e banco exige inventário somente leitura do Neo4j, com rótulos, propriedades, tipos, padrões de relação e constraints. A tentativa de SSH sem senha em 04/11 retornou `Permission denied (publickey,password)`; não foi feita leitura ao vivo. A documentação registra que a carga de 03/11 terminou com 488 nós e 603 relações de domínio e amostras de tipos conferidas, mas isso não substitui o inventário completo.
