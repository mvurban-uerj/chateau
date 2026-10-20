# Grafo acadêmico

**Modelo definido, não inventário de dados carregados.** O padrão do pipeline desde 28/09/2026 é [Expert-Finding-in-academia_rev_6_training.json](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json), acompanhado dos [dicionários de campos](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training_dic_fields.json) e [valores](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training_dic_values.json). O JSON é a referência detalhada de propriedades, tipos, obrigatoriedade, rótulos e direção das arestas. A [ontologia OWL e validação SHACL](../../chateau-data/model/diagramas/training/ontologia/) são artefatos derivados desse modelo.

## Núcleos do modelo rev_6

| Área | Nós principais | Relações exemplares |
|---|---|---|
| Pessoas e vínculos | `Person`, `Job`, `Role`, `JobPosting`, `Service` | `WORKS`, `HAS_ROLE`, `ADMITTED_THROUGH`, `PERFORMED` |
| Produção e reconhecimento | `Article`, `Book`, `Chapter`, `AcademicWork`, `Presentation`, `Biography`, `Acknowledgment` | `IS_AUTHOR_OF`, `WROTE`, `RECEIVED`, `SUPERVISED_BY`, `IS_ABOUT` |
| Pesquisa | `ResearchProject`, `LineOfResearch`, `ConcentrationArea`, `Topic` | `COORDINATES`, `IS_MEMBER_OF`, `CONTRIBUTES_TO`, `GROUPS`, `BROADER` |
| Ensino | `Course`, `CourseInstance`, `ShortCourse`, `ShortCourseInstance`, `Syllabus` | `TAUGHT`, `ATTENDED`, `OF`, `DESCRIBED_BY` |
| Instituição | `OrganizationalUnit`, `PostGraduateProgram`, `Campus`, `WorkPlace` | `HAS`, `DEFINES`, `PART_OF`, `WORKS_AT`, `BELONGS_TO` |

Produção intelectual pode portar o rótulo comum `IntellectualProduction`; os subtipos continuam nós/captions distintos. Curso e oferta/instância do curso são conceitos separados. O modelo define mais propriedades e relações do que as fontes atuais conseguem preencher.

## Versões e fronteiras

- [rev_5_evaluation](../../chateau-data/model/diagramas/evaluation/Expert-Finding-in-academia_rev_5_evaluation.json) é referência da fase de avaliação e da investigação [PDF versus API](../../chateau-data/docs/sucupira-pdf-vs-api/campos-do-modelo-rev5.md). Não é mais o padrão do extrator.
- **Dados da aplicação:** os campos de perfil exibidos pela nova UI virão do Cypher gerado pelo `chateau-data` no modelo rev_6 (decisão de 20/10/2026). O Neo4j de produção ainda não foi recarregado com esse Cypher.
- O [schema de produção extraído](../../chateau-expert/orchestration/schema/schema_producao.txt) é uma fotografia dos dados carregados no Neo4j; pode diferir do modelo rev_6. O modelo texto→Cypher usa o schema fornecido ao serviço, não lê automaticamente o JSON Arrows.
- [chateau-db-schema.json](../../chateau-data/model/schema/chateau-db-schema.json) descreve um **modelo alvo relacional** elaborado em outro trabalho de modelagem, com entidades como `pessoa`, `cargo`, `atribuicao` e `userJobs`. Não corresponde ao schema Prisma operacional do Expert e não substitui o JSON Arrows rev_6.
- Versões históricas em `model/diagramas/` documentam a evolução. Ao criar regra nova, declarar a versão do modelo a que ela se refere.

Fonte do padrão em execução: [DEFAULT_MODEL_PATH](../../chateau-data/scripts/chateau-extract/common/model.py) e [run_all](../../chateau-data/scripts/chateau-extract/run_all/cli.py).
