# Failover entre URLs do mesmo modelo — 04/11/2026

## Contexto e decisão

A [reunião de 29/10](../reunioes/2026-10-29.md) pediu várias URLs/túneis por modelo para posterior balanceamento. O Admin já guarda uma lista ordenada. Nesta conversa foi autorizado o primeiro passo: tentar a primeira URL e avançar para a seguinte quando houver falha técnica clara. A política de distribuir buscas normais entre servidores e a troca por lentidão permanecem pendentes.

O backend resolve o cadastro pelo ID, envia à orquestração `modelo`, `prompt_contract`, `ollama_urls` na ordem do Admin e `ollama_url` com o primeiro elemento para compatibilidade. Quarkus e Python tentam as URLs em sequência antes de consultar o Neo4j. Avançam após conexão recusada, HTTP 503 ou resposta técnica vazia do gerador. Uma geração com Cypher válido encerra as tentativas; também encerram a recusa explícita do 31B, consulta sem resultados, falha no Neo4j, outro erro HTTP e timeout durante a geração. Se nenhuma tentativa produzir Cypher, vale a resposta simulada já definida para falha do modelo. O prompt continua determinado pelo nome técnico, sem campo de prompt no Admin.

O Quarkus inclui `tentativas_modelo` no log da consulta quando recebe mais de uma URL, com URL, tempo em milissegundos e desfecho. O Python registra as tentativas no stderr; seus clientes existentes também gravam o log próprio de cada chamada. A resposta HTTP da busca conserva o contrato anterior. Com uma URL, o comportamento permanece equivalente ao anterior.

## Limite de tempo

O timeout atual do modelo é 55 s e o backend espera 60 s pela orquestração. Todas as tentativas de modelo na mesma busca compartilham o prazo de 55 s; cada URL recebe apenas o tempo restante. Uma troca após o timeout da primeira geração não caberia com segurança nessa janela; além disso, não sabemos se a geração anterior continuaria ocupando a GPU. O cliente usa `stream: false`, sem progresso parcial. Por isso, **lentidão isolada não aciona failover nesta etapa**. O limiar e a política de tentativas após timeout dependem de medidas com o 31B real e das respostas do Edson.

## Conferência do domínio

Foram corrigidos trechos que ainda apresentavam decisões substituídas como vigentes: seletor de modelo demonstrativo, formato de prompt por cadastro, URL única e exigência de termo aceito na busca. [Administração](../../dominio/negocio/administracao.md), [contrato da busca](../../dominio/tech/contrato-de-busca.md) e [índice do domínio](../../dominio/indice.md) agora descrevem a regra atual; análises datadas preservam as decisões anteriores. A [lista de divergências de 20/10](divergencias-2026-10-20.md) é histórica e ainda contém fotografias anteriores à implementação da nova UI, não uma regra vigente.

## Verificação e pendências

Implementação publicada em `chateau-expert/main` no commit `e52bd79`. Passaram 81 testes do backend, 164 do web, 29 do Python e 21 do Quarkus com Neo4j de teste; o build de produção do web também passou. Os casos cobrem envio ordenado da lista, conexão recusada, HTTP 503, resposta vazia, recusa do 31B e contrato antigo de uma URL. A execução com múltiplos túneis, o 31B real e o Neo4j de produção não foi feita. Ainda faltam decisão sobre capacidade, distribuição, afinidade, saúde, timeout, limites de tentativa, configuração dos túneis e observabilidade em produção. [Perguntas ao Edson](../duvidas-edson/README.md).
