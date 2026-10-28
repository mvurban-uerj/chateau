# Visão geral

O Chateau apoia a descoberta de especialistas no contexto acadêmico e a seleção/formação de equipes. A aplicação entregue combina conversa, busca no grafo acadêmico, API de negócio e administração. O foco institucional apresentado no produto é a UERJ; o [README do Expert](../../chateau-expert/README.md) também cita a UFF.

Há três responsabilidades distintas:

- **Dados e modelo:** `chateau-data/` define o grafo acadêmico e extrai documentos para gerar dados rastreáveis.
- **Aplicação:** `chateau-expert/web` apresenta o produto e `chateau-expert/backend` guarda contas, permissões, autorização de contexto, contexto do usuário, conversas e a API de busca.
- **Orquestração:** `chateau-expert/orchestration` transforma pergunta em Cypher e consulta o Neo4j em modo de leitura.

## Fluxo de ponta a ponta

Confirmado pelo Marcelo em 22/10/2026. As etapas são construídas **em paralelo** e cada uma depende do contrato da seguinte, não do seu estado pronto.

Antes da busca, o `chateau-data` extrai dados das fontes acadêmicas e gera o Cypher que popula o Neo4j. Durante uma busca com modelo disponível, o caminho é:

1. **Web → API Express:** o usuário escreve a pergunta no chat. O web envia a pergunta e o nome técnico do modelo escolhido (selecionado automaticamente quando há apenas um).
2. **API Express → orquestração Quarkus:** a API consulta o cadastro para obter a URL do servidor do modelo e envia à orquestração a pergunta, o nome técnico e essa URL.
3. **Orquestração → servidor do modelo de IA:** a orquestração envia a pergunta e o esquema do grafo. Para o Chateau, o servidor é uma caixa preta: descrevemos o que entra e o que sai, sem pressupor seu processamento interno, seus caminhos ou sua tecnologia.
4. **Servidor do modelo de IA → orquestração:** o servidor devolve uma resposta da qual a orquestração extrai o Cypher gerado.
5. **Orquestração → Neo4j:** a orquestração verifica que o Cypher é de leitura e executa a consulta.
6. **Neo4j → orquestração:** o Neo4j devolve os dados encontrados à orquestração. Ele não responde diretamente à API Express nem ao servidor do modelo.
7. **Orquestração → API Express:** a orquestração devolve os dados e o Cypher usado. Os dados não são reenviados ao servidor do modelo.
8. **API Express → web:** a API classifica o resultado; o web monta a resposta e, quando há pessoas, os cartões de perfil ([nova UI](../../docs/nova-ui/README.md#chat-livre--cartões-decidido-em-22102026)).

Consequência: tudo o que a resposta traz — inclusive instituição, área ou quantidade de artigos — vem do grafo, pelas colunas que o Cypher gerado escolheu. Não há regra de negócio no backend que complete ou ranqueie os dados. O que o grafo ainda não tem, ou que o modelo ainda não sabe consultar, não pode aparecer como dado real.

**Acesso ao grafo (decidido em 22/10/2026):** a API Express e o web não acessam o Neo4j; somente a orquestração executa o Cypher recebido do servidor do modelo. O que não vier da consulta fica simulado (mock) até o Edson decidir o rumo (decidido pelo Marcelo em 22/10/2026). Pode ser revisto no futuro; até lá, não se constrói caminho novo até o Neo4j para depois desfazer.

No código atual, a orquestração executa a consulta no Neo4j; o servidor do modelo devolve o Cypher e os dados seguem da orquestração para a API sem voltar ao servidor ([contrato técnico](../tech/contrato-de-busca.md)).

## Estado atual

Na evolução local ainda não publicada, a busca usa a orquestração quando há um modelo disponível selecionado; sem modelo, o backend devolve um mock. `ORCHESTRATION_URL` apenas substitui o endereço interno padrão do serviço. Exemplos e dados simulados não descrevem a cobertura real do grafo.

Fontes: [README do Expert](../../chateau-expert/README.md), [busca do backend](../../chateau-expert/backend/src/services/search.service.ts), [README do Data](../../chateau-data/README.md).
