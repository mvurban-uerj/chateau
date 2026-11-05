atualmente temos o seguinte fluxo, confirme - a pergunta no chat chama a api que recupera o modelo e a url referenciada no admin, aciona o orquestrador que monta o prompt pro modelo que gera consulta no neo4j que entao retorna ao orquestrador que mostra a saída.

Precisamos criar um mecanismo intermediário que é ligado ou desligado pelo admin, ele se chama modelo orquestrador, tb é um modelo de ia que irá interpretar o contexto pra entao enviar ao modelo cypher que vai gerar a consulta.

Ou seja, hoje a pergunta: quais artigos o ivan publicou ele vai no modelo e recupera, mas se a proxima pergunta for, quantos destes artigos começam com A, ele vai pegar a lista inteira, sem passar pelo contexto que é os artigos do edson e não todos os artigos.
Então se o admin estiver com esta opção ligada, ele vai ao modelo orquestrado antes de ir ao modelo do cypher, se desligado ele se comporta como hoje, pergunta direta.

Aí vamos precisar estudar, como as IAs costumam fazer pra enviar esse contexto, pq podem ter várias perguntas e o modelo orquestrado (veja bem, não é o nosso orquestrador em quarkus, é um modelo de ia no servidor que fica junto com o modelo Cyper) O endereço é 27.0.0.1:11436. No admin, vc pode até colocar o ligado deseligado e um campo único com a url e deixar essa como padrão.

então quero que faça um plano pra introduzir esse novo modelo orquestrador que terá a função de interpretar o contexto passado pelo orquestrador quarkus pra ele. Objetivo é fazer funcionar da forma mais simples possível e evoluírmos gradualmente. No final do processo perguntas encadeadas devem ser interpretadas e conduzidas pelo modelo de forma a retornar o que foi pedido com base em todo o contexto daquela conversa.

Além de retornar a query, vou precisar que vc tb retorne qual foi o prompt que o modelo orquestrador gerou com base no contexto, isso será avaliado pelo coordenador pra aprimorar o modelo.