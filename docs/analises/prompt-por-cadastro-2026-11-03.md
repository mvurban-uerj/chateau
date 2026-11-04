# Formato de prompt por cadastro de modelo — 03/11/2026

**Substituída em 04/11/2026:** o usuário corrigiu a regra: o formato do prompt é definido pelo nome técnico do modelo, em de-para no código, e não pelo cadastro do Admin. Ver [contrato da busca](../../dominio/tech/contrato-de-busca.md). O texto abaixo preserva o histórico da decisão anterior.

O pacote `chateau-cypher-cliente-31b-rev6-v1.0.0` em `/mnt/c/temp/chateau/model` exige um prompt único no formato A, sem `system` e com `think: false`. O modelo e4b usa `system` e `prompt` separados. O schema do formato A foi conferido contra o JSON rev_6: 25 rótulos, 131 propriedades de nó, 49 padrões de relação, 8 tipos de propriedades de relação e os rótulos adicionais coincidem.

O Admin já permite cadastros com o mesmo nome técnico e URLs diferentes, identificados por ID. Escolher o formato a partir do nome técnico faria duas versões compartilharem o mesmo prompt indevidamente. O usuário confirmou que o conteúdo enviado pode variar por versão. Por isso, cada `AiModel` passa a guardar `promptContract` (`e4b` ou `rev6_31b`); a migração atribui `e4b` aos registros existentes. O backend resolve o cadastro por ID e envia `prompt_contract` à orquestração junto com nome técnico e URL. Quarkus e Python selecionam o formato por esse campo.

No formato `rev6_31b`, `RETURN null AS sem_resposta` significa recusa do modelo por falta de caminho no schema e não é executado no Neo4j. O backend mostra `fora_escopo`, distinto da recusa de consulta de escrita. O arquivo `schema_producao.txt` continua sendo a fotografia compacta usada pelo e4b; o 31B usa o template integral do pacote, inclusive entidades sem registros.

Implementação e testes foram preparados em `chateau-expert`. A confirmação do deploy e os testes com o modelo 31B real e o grafo de produção ainda estão pendentes. O servidor do modelo não estava acessível no ambiente local durante esta revisão.
