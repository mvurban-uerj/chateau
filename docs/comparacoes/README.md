# Comparações de esquemas

Este diretório reúne conferências entre três fontes distintas:

1. **Modelo de referência:** JSON Arrows `rev_6_training` do `chateau-data`.
2. **Esquema recebido pelo modelo `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234`:** seção `Schema` do template no pacote cliente `/mnt/c/temp/chateau/model/chateau-cypher-cliente-31b-rev6-v1.0.0`.
3. **Neo4j de produção:** estrutura e valores efetivamente carregados. Deve ser inventariado de novo após cada carga; o relatório do pacote, datado de 29/10, retrata a carga anterior à de 03/11.

| Etapa | Registro | Situação |
|---|---|---|
| JSON rev_6 × esquema do modelo `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` | [rev6-x-prompt-31b-2026-11-04.md](rev6-x-prompt-31b-2026-11-04.md) | Concluída; restrições de campo ausentes do esquema fornecido |
| JSON rev_6 × Cypher gerado em 03/11 | [rev6-x-cypher-2026-11-04.md](rev6-x-cypher-2026-11-04.md) | Concluída para o arquivo local; nomes, tipos e relações presentes coincidem; ausência de instâncias é cobertura dos dados |
| Cypher gerado em 03/11 × esquema do modelo 31B | [cypher-x-modelo-31b-2026-11-04.md](cypher-x-modelo-31b-2026-11-04.md) | Concluída; nenhuma diferença de nome, tipo ou direção nos dados de domínio gerados |
| Cypher gerado em 03/11 × Neo4j de produção | [cypher-x-neo4j-2026-11-04.md](cypher-x-neo4j-2026-11-04.md) | Domínio e constraints conferidos com inventário enviado em `talk-ia.md`; camada técnica e valores individuais fora do escopo dessa evidência |
| JSON rev_6 × esquema do modelo 31B × Neo4j de produção | Ver as quatro comparações acima | Estrutura de domínio triangulada; validação de consultas reais do modelo ainda pendente |

O script [comparar_rev6_prompt.py](comparar_rev6_prompt.py) reproduz a primeira etapa. Ele exige os dois caminhos como argumentos e falha se o formato do prompt não puder ser interpretado. O pacote externo não é copiado para este repositório.

O inventário somente leitura da carga atual chegou em `talk-ia.md` em 04/11. Ele conferiu combinações de rótulos, campos e tipos de domínio, padrões dirigidos e constraints/índices; não incluiu valores individuais nem a estrutura completa da camada de proveniência. Ausência de dados em rótulos ou campos do JSON não é divergência estrutural. Para nova carga, repetir o inventário; não usar a fotografia antiga `schema_producao.txt` como substituta do banco atual.

O relatório pré-carga [esquema-prompt-31b-x-banco-chateau.md](/mnt/c/temp/chateau/model/chateau-cypher-cliente-31b-rev6-v1.0.0/esquema-prompt-31b-x-banco-chateau.md) serve como histórico, não como resultado da conferência de 04/11.

## Inventário do pacote em `C:\temp` (04/11/2026)

Foi examinado `/mnt/c/temp/chateau/model/chateau-cypher-cliente-31b-rev6-v1.0.0` e procurado outro arquivo de schema em `/mnt/c/temp`, excluindo dependências da UI e o ambiente virtual. O **único arquivo do pacote com a definição completa de rótulos, propriedades, tipos e padrões dirigidos de relação** é `prompt/prompt_formato_a_rev_6.txt`. `README.md` (seção 5) descreve o formato e traz apenas um exemplo abreviado para outro banco; `cliente/chateau_cypher_31b.py` carrega o template como fonte padrão; `cliente/perguntar_31b.py` aceita um esquema externo para outro banco, mas nenhum é fornecido; `LICENCAS.md` aponta a origem do template em `chateau-data-generation/esquemas/prompt_formato_a_rev_6_training.txt`. O relatório `esquema-prompt-31b-x-banco-chateau.md` analisa esse mesmo template, não define um schema independente. O pacote não inclui os pesos do modelo de IA nem um JSON/TTL de schema separado. Todos os oito arquivos listados em `SHA256SUMS` passaram na verificação de hash.
