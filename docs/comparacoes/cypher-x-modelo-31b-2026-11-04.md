# Cypher gerado × esquema do modelo `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234`

Comparação direta de 04/11/2026 entre a **camada de domínio** do Cypher de `chateau-data/data/out/20261103-114032/cypher/chateau-consolidado.cypher` e a seção de esquema de `/mnt/c/temp/chateau/model/chateau-cypher-cliente-31b-rev6-v1.0.0/prompt/prompt_formato_a_rev_6.txt`.

| Verificação | Resultado |
|---|---:|
| Rótulos de domínio divergentes | **0** |
| Campos ausentes no esquema ou com nome diferente | **0** |
| Campos com tipo diferente | **0** |
| Relações com nome ou direção diferente | **0** |
| Rótulos adicionais divergentes | **0** |

**Leitura correta:** tudo o que o Cypher gerou para o domínio é compatível com o esquema fornecido ao modelo. Rótulos, campos e relações definidos no esquema mas sem dados nesta carga não entram como diferenças. Nenhuma propriedade de relação foi preenchida nesta carga; por isso não há valores desse tipo para comparar.

O Cypher inclui ainda `uid` como identificador interno e a camada técnica de proveniência (`SourceDocument`, `ExtractedRecord` e `HAS_EXTRACTED_RECORD`). Esses elementos não pertencem ao domínio acadêmico apresentado ao modelo. O arquivo Cypher também cria 19 constraints `IS UNIQUE`; o esquema enviado ao modelo não declara restrições de unicidade ou obrigatoriedade, portanto não há comparação direta dessas marcações entre os dois arquivos.

Reproduzir a conferência, da raiz do projeto, com `python3 -B docs/comparacoes/comparar_rev6_cypher.py chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json chateau-data/data/out/20261103-114032/arrows/domain.json chateau-data/data/out/20261103-114032/cypher/chateau-consolidado.cypher --prompt /mnt/c/temp/chateau/model/chateau-cypher-cliente-31b-rev6-v1.0.0/prompt/prompt_formato_a_rev_6.txt`. O script lê diretamente o Cypher gerado e não consulta o Neo4j.
