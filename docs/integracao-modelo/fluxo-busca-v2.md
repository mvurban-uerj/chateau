# Fluxo de busca — versão 2 (28/10/2026)

**Proposta registrada em 28/10/2026, a partir de [talk-ia.md](../talk-ia.md). Não implementada.** O Edson sugere uma etapa de IA que chama de *modelo orquestrador* para reescrever perguntas que dependem de respostas anteriores. Essa função é diferente do serviço Quarkus, que coordena a busca, e precede a geração de Cypher. Não está definido se haverá um modelo separado, qual será o prompt nem como o histórico chegará à etapa de reformulação.

### Exemplo sugerido

1. Pergunta anterior: “Liste as pessoas do PPGMC”.
2. Resposta anterior: “Ivan; Hermes; Verona; ...”.
3. Pergunta atual: “Quantos artigos essas pessoas publicaram em 2024?”
4. Reformulação ilustrativa: “Quantos artigos Ivan, Hermes e Verona publicaram em 2024?”

A reformulação precisa substituir “essas pessoas” pelas pessoas da resposta anterior, preservar o ano de 2024 e não inventar identidades. Os nomes abreviados acima servem apenas para explicar a ideia; identificadores estáveis seriam preferíveis se estiverem disponíveis na resposta anterior. Ainda é preciso definir se a contagem pedida é total ou por pessoa.

### Pergunta do Edson: prompt fixo ou definido pelo contexto?

Neste exemplo, **contexto** significa as perguntas e respostas anteriores da conversa; não é o perfil da área “Meu contexto”. A pergunta do Edson não obriga a escolher entre duas opções exclusivas. **Hipótese para testar:** manter fixa a instrução de *como* reformular e preencher a cada busca os dados variáveis: pergunta atual e histórico da conversa. Assim, o texto completo enviado ao modelo muda com a conversa, mas a regra de reformulação permanece estável.

Um candidato de instrução fixa seria: “Reescreva a pergunta atual para que possa ser entendida isoladamente. Resolva referências usando apenas as perguntas e respostas fornecidas. Preserve nomes, restrições, datas e a intenção da pergunta. Não invente dados, não gere Cypher e sinalize quando faltar informação para resolver uma referência.” A forma de sinalizar falta de informação e o formato exato da resposta ainda precisam ser definidos.

Também é possível variar instruções conforme o tipo de pergunta, mas isso acrescenta decisões e testes. Primeiro seria preciso medir se o candidato acima resolve casos com referência, mantém perguntas já independentes e evita alterações indevidas. **Nenhum prompt foi aprovado ou testado com o modelo real.**

### Quanto histórico enviar? Proposta corrigida para testar

Para o primeiro teste da versão 2, enviar ao modelo orquestrador **a pergunta atual e todo o histórico da conversa**, incluindo perguntas e respostas. O backend pode recuperar e transportar esse histórico, mas não deve decidir sozinho quais trechos são semanticamente relevantes. É o modelo que precisa ler a conversa para entender a que se refere “essas pessoas”, inclusive quando o antecedente estiver várias trocas atrás. Enviar apenas a última troca sem outra forma de acesso pode ocultar a informação necessária.

O histórico transmitido deve preservar o conteúdo necessário das respostas estruturadas, como identificadores das pessoas retornadas e critérios da busca. No exemplo do PPGMC, o modelo pode decidir se a pergunta reformulada deve usar identificadores das pessoas efetivamente listadas ou os critérios “pessoas do PPGMC”. Essas opções podem representar conjuntos diferentes quando a resposta anterior foi truncada ou filtrada. Uma resposta simulada não serve como evidência de quem está no grafo. Se o antecedente não puder ser recuperado com segurança, o modelo deve pedir esclarecimento em vez de inventar pessoas.

Para conversas que excedam a janela de contexto do modelo, será necessária outra estratégia. A alternativa de resumo acumulado está descrita abaixo. Um resumo ou corte que esconda o antecedente impediria o modelo de decidir corretamente. Também será preciso garantir que a resposta anterior esteja disponível antes da busca seguinte, porque hoje o web grava a conversa após receber a resposta. Nada disso está implementado ou aprovado.

### Ida e volta proposta — primeiro teste com histórico completo

| Passo | De → para | Informação proposta |
|---|---|---|
| 1 | Web → backend | Pergunta atual, modelo escolhido e identificação da conversa para localizar as mensagens anteriores. O contrato atual da busca ainda não envia essa identificação. |
| 2 | Backend → Quarkus | Pergunta atual, histórico completo da conversa, nome técnico e URL do servidor do modelo que gera Cypher. **Hipótese de desenho:** o backend recupera o histórico persistido; a origem e o formato exatos ainda serão definidos. |
| 3 | Quarkus → modelo orquestrador (servidor a definir) | Pergunta atual, histórico da conversa e instrução para produzir uma pergunta independente do contexto anterior. O modelo decide quais partes do histórico resolvem a referência; o prompt dessa etapa ainda não foi definido. |
| 4 | Modelo orquestrador → Quarkus | Pergunta reformulada em texto. |
| 5 | Quarkus → servidor do modelo de IA que gera Cypher | Pergunta reformulada, nome técnico do modelo escolhido e schema do grafo. |
| 6 | Servidor do modelo de IA que gera Cypher → Quarkus | Consulta Cypher gerada. |
| 7 | Quarkus → Neo4j → Quarkus | Verificação de leitura, execução da consulta e retorno das colunas e linhas. |
| 8 | Quarkus → backend → web | Resultado, Cypher e estado da busca para apresentação, como na versão 1. |

### Alternativa proposta: resumo acumulado da conversa

Em vez de reenviar todas as mensagens em cada busca, o backend poderia guardar, por conversa, um **resumo atualizado pelo modelo de IA**. A cada nova pergunta, o Quarkus enviaria ao modelo orquestrador o resumo anterior, a pergunta atual e as trocas recentes ainda não incorporadas. O modelo usaria esse contexto para reformular a pergunta. Depois da resposta real do Neo4j, o Quarkus pediria ao modelo para atualizar o resumo com a pergunta e o resultado; o backend guardaria o novo resumo para a próxima busca.

O backend armazenaria e transportaria o resumo, sem decidir o significado das perguntas. O Quarkus coordenaria as chamadas. O modelo de IA produziria e atualizaria o contexto em linguagem natural. Ainda não está decidido se a mesma instância fará reformulação e resumo, nem qual será o formato do resumo.

**Avaliação:** a alternativa reduz o tamanho do contexto transmitido nas conversas longas, mas o resumo pode omitir uma pessoa, filtro ou identificador necessário para uma referência futura. Por isso, as mensagens e resultados originais precisam continuar disponíveis para consulta quando o resumo não bastar. Respostas simuladas ou com falha não devem virar fatos do grafo no resumo. A atualização do resumo também precisa terminar ou ter uma regra de ordenação antes da próxima pergunta; caso contrário, o modelo pode receber contexto atrasado. Cada atualização acrescenta trabalho do modelo e pode aumentar o tempo da busca.

Para comparar as alternativas, testar as mesmas conversas com histórico completo e com resumo acumulado, incluindo referências a respostas antigas, listas grandes, resultados truncados e mudança de assunto. Esta alternativa permanece hipótese de documentação; não substitui o primeiro teste com histórico completo nem define implementação.

### Avaliação e decisões pendentes

- A proposta pode resolver referências como “essas pessoas”, porque a pergunta enviada ao modelo de Cypher passaria a conter o antecedente. **Ainda não há teste com o modelo real** que comprove a afirmação de que a pergunta direta retornaria vazio, nem que a reformulação produziria a consulta correta.
- O fluxo atual envia ao Quarkus somente pergunta, usuário, nome técnico e URL do servidor do modelo. O histórico existe na conversa do web/backend, mas não entra na busca. A versão 2 exige um contrato novo para transmitir ou recuperar o histórico.
- É preciso testar o envio do histórico completo e a alternativa de resumo acumulado, medir o limite de tamanho e decidir como o modelo alcança mensagens antigas que o resumo omitiu, além de tratar respostas simuladas, incompletas ou com falha.
- É preciso definir se a reformulação ocorre em toda pergunta ou só quando houver referência ao contexto e qual modelo a fará. A hipótese de instrução fixa com histórico variável está descrita acima; continua aberta à avaliação com o Edson.
- A reformulação acrescenta uma chamada ao servidor de modelo antes da geração de Cypher. Deve ser avaliada quanto a tempo de resposta, falhas e preservação da intenção original (por exemplo, o ano e a diferença entre total e contagem por pessoa).

**Próxima validação, antes de qualquer implementação:** testar a pergunta 2 diretamente no modelo de Cypher com o grafo apropriado; depois comparar com reformulações candidatas e conferir o Cypher e o resultado no Neo4j. Esta proposta não altera o [fluxo da versão 1](fluxo-busca-v1.md).
