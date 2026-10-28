O modelo orquestrador recebe a pergunta com as úlitmas perguntas e respostas. O modelo orquestrador reescreve a pergunta antes de submeter para o modelo que responde a pergunta.
Caso 1 (A IA pode nos ajudar a criar vários casos)
Pergunta 1: Liste as pessoas do PPGMC
Resposta 1: Ivan ...; Hermes ...; Verona .....
Pergunta 2: Quantos atigos essas pessoas publicaram em 2024?

Problema: Enviar a Pergunta 2 dreto para modelo cypher irá retornar uma resposta vazia.
Teste isso!

O modelo orquestrador recebe a Pergunta 1 e a Resposta 1. Um prompt com pedido para reescrever a Pergunta 2.
A Pergunta 2 reescrita pelo modelo orquestrador segue para o modelo cypher.

Objetivo: Definir o prompt para o orquestrador. (A IA pode nos ajudar a decidir isso)
Vai ser um prompt fixo?
Vai ser definido de acordo com o contexto?