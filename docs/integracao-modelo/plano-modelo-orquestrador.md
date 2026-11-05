# Plano — modelo orquestrador (contexto da conversa)

**05/11/2026. Plano aprovado pelo usuário ([talk-ia.md](../talk-ia.md), [reunião de 05/11](../reunioes/2026-11-05.md)). Fase 1 implementada no Expert em 05/11 (`e6f4add`, enviado a `main`; deploy pendente); fases 0 e 2 pendentes.** Retoma a [versão 2 do fluxo](fluxo-busca-v2.md) com as decisões de 05/11: o modelo orquestrador é um modelo de IA, `gemma4:31b`, no mesmo servidor do modelo Cypher, porta `11436`; o Admin liga e desliga a etapa; desligada, a busca é a de hoje.

Verificado contra `chateau-expert` `ef20311` (árvore com `testar_modelo.sh` alterado e sem commit).

## 1. Fluxo atual (conferido no código)

1. O chat (`ConversaAoVivo.tsx`) envia `POST /api/search` com `{pergunta, modelId, modelName}`. **Nenhuma pergunta ou resposta anterior é enviada.**
2. A rota Next.js repassa à API (backend), que busca no PostgreSQL o cadastro do Admin pelo ID: nome técnico e URLs ordenadas. O formato do prompt (`e4b` ou `rev6_31b`) é escolhido pelo nome técnico no código.
3. A API chama `POST /search` na orquestração Quarkus com pergunta, usuário, modelo, URLs e `prompt_contract`.
4. O Quarkus monta o prompt (schema ou template rev_6 + pergunta) e chama `/api/generate` do servidor do modelo, com failover entre as URLs.
5. O modelo devolve **o texto do Cypher**; ele não acessa o Neo4j. O Quarkus confere com `EXPLAIN` que a consulta só lê e a executa no Neo4j em transação somente leitura.
6. O Quarkus devolve Cypher e linhas à API, que classifica o desfecho (`ok`, `sem_resultado`, `fora_escopo`...) e devolve ao web.

Por isso “Quais destes começam com A?” chega ao modelo Cypher sem saber quais são “estes” e é respondida sobre todos os artigos.

## 2. Fluxo proposto

```
web ──pergunta + histórico──▶ API ──(Admin: orquestrador ligado? URL, modelo)──▶ Quarkus
Quarkus ──prompt de reescrita (instrução fixa + histórico + pergunta)──▶ modelo orquestrador (gemma4:31b)
modelo orquestrador ──pergunta independente──▶ Quarkus
Quarkus ──pergunta independente──▶ modelo Cypher ──Cypher──▶ Quarkus ──▶ Neo4j ──▶ Quarkus ──▶ API ──▶ web
```

- **Ligado:** havendo histórico, o Quarkus pede ao modelo orquestrador uma pergunta independente (que se entende sem a conversa) e a envia ao modelo Cypher no lugar da original.
- **Desligado:** a API não envia histórico nem dados do orquestrador; o Quarkus segue exatamente o caminho de hoje.
- **Primeira pergunta da conversa:** não há contexto; o Quarkus não chama o modelo orquestrador e registra `sem_historico` no fluxo.
- **Falha do modelo orquestrador** (conexão, timeout, resposta vazia): segue com a pergunta original e um aviso no fluxo. A busca não é bloqueada.

É a técnica usual dos assistentes com busca em base de dados (*question condensation* ou *query rewriting*): um passo de modelo transforma “pergunta + conversa” numa pergunta autossuficiente, e só ela vai ao gerador de consulta, que continua sem estado. Começamos pela variante mais simples, uma janela com as últimas trocas. Resumo acumulado e memória de entidades ficam para a fase 3.

## 3. Fase 0 — infraestrutura e prova manual (antes de codificar)

Depende do aviso do Edson de que o `gemma4:31b` subiu.

1. **Alcance do container.** `127.0.0.1:11436` é o túnel no host; o container `chateau_orchestration` não o alcança. Criar a ponte `chateau_ollama_ponte_11436` (socat em `172.17.0.1:11436`, como a de `11434`). A URL usada pelo Quarkus será `http://host.docker.internal:11436`. Conferir `GET /api/tags` de dentro do container e se `gemma4:31b` aparece.
2. **Prova com `curl`.** Executar as duas perguntas do exemplo da seção 5 com o prompt da seção 5: anotar pergunta reescrita, tempo e `prompt_eval_count`. Depois enviar a reescrita ao modelo Cypher e conferir Cypher e resultado no Neo4j.
3. **Janela de contexto.** O servidor está com 16k. Medir os tokens do prompt real. O Quarkus pode pedir `num_ctx` menor por requisição (ex.: 4096), mas um valor diferente do carregado faz o Ollama **recarregar o modelo**, o que custa tempo e memória. Combinar com o Edson se fixa o valor no servidor (`Modelfile` ou `OLLAMA_CONTEXT_LENGTH`) ou se o Quarkus o envia.

## 4. Fase 1 — MVP (mais simples que funcione)

### Admin
- Nova seção “Modelo orquestrador” na página de modelos: **Ligado/Desligado**, **URL** (padrão `http://host.docker.internal:11436`) e **nome do modelo** (padrão `gemma4:31b`). O pedido citou só URL; o nome técnico é necessário na chamada ao Ollama e fica com padrão para trocar sem deploy.
- Prisma: registro único `OrchestratorSettings {enabled=false, url, modelName, updatedAt}`; rota `GET/PUT /api/admin/orchestrator`, só administrador. Começa **desligado**: o deploy não muda o comportamento atual.
- Textos fixos internacionalizados, como exige a regra de interface.

### Web → API
- `POST /api/search` passa a aceitar `historico` opcional: as últimas **4 trocas** da conversa em memória, mais antigas primeiro, cada uma com `pergunta` (original), `perguntaReescrita?`, `cypher?`, `status`, `colunas` e até **15 linhas**, com textos cortados em 120 caracteres.
- Trocas com `simulado: true` ou com falha vão **só com a pergunta**: dado simulado não pode virar fato para o modelo.
- O histórico vem do navegador porque a conversa é gravada no PostgreSQL depois da resposta, e a pergunta seguinte pode chegar antes. O risco aceito é que um usuário que adultere o histórico afete só a própria busca; o Cypher continua limitado a leitura. Ler a conversa do banco pelo `chatId` fica para a fase 3.

### API → Quarkus
- Ligado: acrescenta ao corpo `orquestrador: {url, modelo}` e `historico` (com teto de ~8.000 caracteres, descartando as trocas mais antigas primeiro). Desligado: corpo igual ao de hoje.
- `ORCHESTRATION_TIMEOUT_MS` sobe de 60 s para 80 s quando ligado; ver prazos abaixo.

### Quarkus
- Classe nova `ReescritorContexto`: monta o prompt da seção 5 e chama `POST {url}/api/generate` com `think: false`, `stream: false`, `temperature: 0`; usa a primeira linha não vazia da resposta.
- Prazo próprio de **20 s** (`CHATEAU_ORQUESTRADOR_TIMEOUT_S`), separado dos 55 s do modelo Cypher. Sem failover no MVP: uma única URL.
- A pergunta reescrita substitui a original **só** na chamada ao modelo Cypher; log e resposta guardam ambas.
- A resposta ganha `orquestrador`, sempre presente quando ligado:

```json
"orquestrador": {
  "desfecho": "reescreveu | sem_historico | falhou",
  "modelo": "gemma4:31b",
  "url": "http://host.docker.internal:11436",
  "prompt_enviado": "<prompt completo enviado ao modelo orquestrador>",
  "pergunta_original": "Desses artigos quais começam com A?",
  "pergunta_gerada": "<prompt gerado pelo modelo orquestrador e enviado ao modelo Cypher>",
  "tempo_ms": 0, "tokens_prompt": 0, "tokens_resposta": 0, "erro": null
}
```

- O registro JSONL de buscas (`RegistroConsultas`) grava o mesmo bloco, para o coordenador avaliar sem depender da tela.
- Python (reserva de comparação) **não** recebe a etapa no MVP: ignora os campos novos e se comporta como desligado. Divergência registrada; paridade na fase 3 se o Python continuar em uso.

### API → web e tela
- `SearchResult` ganha `fluxo` (o bloco acima) e o persiste com a mensagem no histórico da conversa.
- Abaixo da consulta gerada, um bloco recolhível **“Fluxo da resposta”** mostra: pergunta do usuário → prompt enviado ao modelo orquestrador → pergunta gerada (enviada ao modelo Cypher) → Cypher → nº de linhas e tempos. É o pedido de “mostrar o fluxo total das respostas”.

### Testes do MVP
- Backend: toggle desligado mantém o corpo atual (regressão); histórico cortado no teto; trocas simuladas sem linhas.
- Quarkus: servidor HTTP simulado para reescrita normal, sem histórico, timeout e resposta vazia (as duas últimas seguem com a pergunta original).
- Web: o bloco “Fluxo da resposta” aparece só quando há `fluxo`; mensagens antigas sem o campo continuam abrindo.

### Estado da fase 1 (05/11/2026)

Implementada como descrita acima, com dois ajustes:
- O web não envia trocas sem resposta (`indisponivel` não simulado). Sem isso, o “Tentar de novo” mandaria como contexto a própria pergunta que falhou.
- O bloco `orquestrador` traz também `versao_instrucao` (`2026-11-05`), para comparar no log as mudanças de instrução.

Testes: API 95 (com Postgres de teste), Quarkus 39 (com Neo4j via Dev Services e Ollama simulado), web 175, mais `tsc` e lint do web. Nenhum teste com o `gemma4:31b` real.

## 5. Prompt inicial do modelo orquestrador (a validar na fase 0)

Instrução fixa, conversa variável (hipótese já registrada na versão 2):

```
Você reescreve perguntas de um chat sobre uma base acadêmica (pessoas, artigos, projetos, orientações).
Reescreva a PERGUNTA ATUAL para que ela possa ser entendida sozinha, sem a conversa.
- Resolva referências como "desses", "eles", "esse professor" usando apenas a CONVERSA abaixo.
- Prefira repetir o critério da pergunta anterior (ex.: "artigos publicados por Ivan") a listar resultados.
- Preserve nomes, anos, filtros e o que está sendo pedido (lista, contagem, por pessoa).
- Se a pergunta atual já for independente ou mudar de assunto, devolva-a sem alterações.
- Não invente dados. Não gere Cypher. Responda somente com a pergunta reescrita, em uma linha.

CONVERSA:
[1] Usuário: Quais os artigos que o Ivan publicou?
    Consulta: MATCH (p:Person)-[:AUTHORED]->(a:Article) WHERE p.name CONTAINS 'Ivan' RETURN a.title
    Resultado: 12 linhas; colunas: a.title; primeiras: "...", "..."

PERGUNTA ATUAL: Desses artigos quais começam com A?
```

Saída esperada: `Quais artigos publicados por Ivan têm título começando com a letra A?` A consulta acima é ilustrativa; os nomes reais de rótulos e relações vêm do Cypher efetivamente gerado na troca anterior.

Enviar o Cypher anterior ajuda o modelo a manter o critério (“publicados por Ivan”), em vez de copiar uma lista que pode estar truncada em 50 linhas.

## 6. Fase 2 — avaliação e ajuste

- Arquivo `orchestration/teste_modelo/conversas.jsonl` com conversas encadeadas e a reescrita esperada: referência à troca anterior, referência a duas trocas atrás, mudança de assunto, pergunta já independente, contagem vs. lista, ano preservado, resultado anterior vazio ou simulado.
- Script no estilo de `testar_modelo.sh`/`avaliar.py`: roda as conversas com o orquestrador ligado e desligado e compara a reescrita, o Cypher e o resultado no Neo4j de produção.
- O coordenador avalia `prompt_enviado` e `pergunta_gerada` (tela e JSONL); os ajustes de instrução são versionados com data e hash no log, como o `schema_sha256`.
- Reduzir a janela: medir tokens reais e diminuir trocas, linhas e `num_ctx` enquanto os casos de teste continuarem passando.

## 7. Fase 3 — evoluções (só após a fase 2)

- Pedido de esclarecimento: saída JSON `{pergunta, precisa_esclarecer, motivo}` e mensagem própria na tela quando a referência for ambígua.
- Pular a chamada quando a pergunta não tiver marcador de referência, para economizar tempo (decidido pelo modelo ou por heurística medida).
- Resumo acumulado por conversa, avaliado na [versão 2](fluxo-busca-v2.md), para conversas longas.
- Histórico lido do PostgreSQL pelo `chatId` em vez de vir do navegador.
- Failover de URLs e paridade no Python, se necessários.

## 8. Confirmações e pendências

Confirmado pelo usuário em 05/11: a URL é `127.0.0.1:11436` (no container, `http://host.docker.internal:11436` via ponte); o exemplo é todo sobre o Ivan; o “Fluxo da resposta” é visível para todos os usuários.

Pendentes:
1. **Janela de contexto:** quem fixa o `num_ctx` (servidor ou requisição) — Edson.
2. **Disponibilidade e capacidade:** o `gemma4:31b` e o modelo Cypher no mesmo servidor disputam GPU; medir se duas chamadas seguidas cabem no tempo aceitável (logs de latência já existem).
