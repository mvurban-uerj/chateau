# Integração do modelo de IA (texto → Cypher) com a interface

Plano de trabalho para trocar o mock do chat pela busca real: pergunta do usuário
→ modelo gera Cypher → consulta no Neo4j → resultado na interface.

> **Para quem retoma este trabalho com contexto limpo:** este documento é
> autossuficiente. Leia na ordem: seção 1 (contexto), 2 (fatos verificados no
> pacote do Edson), 3 (decisões), 4 (revisão da arquitetura) e então a fase em
> andamento na seção 8. Estado de cada fase: checkboxes na seção 8.

Criado em 2026-09-28.

---

## 1. Contexto

### Projeto e repositórios

Chateau: *expert finding* no domínio acadêmico (UERJ/IPRJ, PROINTEC 2025).
Coordenador: Edson. Desenvolvedor: Marcelo (mvurban).

| repo | caminho local | papel |
|---|---|---|
| `chateau` | `~/projetos/chateau` | raiz: `docs/`, notas de reunião |
| `chateau-expert` | `~/projetos/chateau/chateau-expert` | a aplicação: `web/` (Next.js), `backend/` (Express + Prisma + Postgres), `orchestration/` (vazio, reservado para a camada de IA) |
| `chateau-data` | `~/projetos/chateau/chateau-data` | extração de dados (Lattes, Sucupira...) → `.cypher` no modelo rev_5, carregado no Neo4j de produção |

Servidor de produção: `prointec@152.92.2.63` (`/opt/apps/chateau-expert`), atrás
do firewall da faculdade; serviços internos escutam só em `127.0.0.1` e são
acessados por túnel SSH. O Neo4j (`chateau_neo4j`, `neo4j:5-community`, APOC)
existe **só** no `docker-compose.prod.yml`, na rede `backend_net`, portas
`127.0.0.1:7474/7687`. Detalhes: `docs/neo4j/README.md`. Ele contém os dados
reais do `chateau-data` (rev_5), não o banco de exemplo do Edson.

### Origem da tarefa

- Reunião de 2026-09-23 (`docs/reunioes/2026-09-23.md`), itens 2 e 3: a interface
  deve chamar o modelo; o modelo devolve Cypher; executar no banco e devolver ao
  usuário; **mostrar também a query gerada** (o Edson quer ver). Pergunta fora do
  domínio ("quantas bananas numa penca") "retorna null ou zero" e tem de ser tratada.
- `docs/talk-ia.md`: deixar tudo pronto para que, quando o modelo estiver
  disponível, **uma troca de configuração** passe do mock para o modelo real.
  Tratar: sem achados, pergunta fora do projeto, null/zero.
- Mensagem do Edson: "liberei a primeira versão do modelo... material em
  `prointec@chateau:~/chateau/model`... Aloquei, para **quarta-quinta-sexta**
  (2026-09-30 a 2026-10-02), uma máquina com GPU... disponibilizar o modelo via
  tunnel e testarmos."
- Diretriz do Edson para o `chateau-orchestration`: **Quarkus + LangChain4j +
  extensão Neo4j** (https://quarkus.io). Evoluir para o diagrama do Drive
  (link na `docs/talk-ia.md`; não acessível daqui — pedir PNG).

### Estado atual do código (o mock)

- `chateau-expert/web/src/app/chat/page.tsx`
  - `mockProfessionals` / `mockResponse()` (linhas 32–45): profissionais
    sorteados, prefixo `__PROFESSIONALS__:` + JSON no `content` da mensagem.
  - `send()` (linha 339): cria o chat (`POST /api/chats`), registra o contador
    (`POST /api/chat-query` com `responseTimeMs` **aleatório** 1,5–9 s),
    espera com `setTimeout` e chama `mockResponse()`; persiste as mensagens
    (`PATCH /api/chats/:id`). 403 → `/pending`.
  - Renderização: `ProfessionalsList` para `__PROFESSIONALS__:`, texto para o resto.
- Padrão web → backend: Route Handler em `web/src/app/api/*/route.ts` pega o
  e-mail da sessão NextAuth e repassa ao backend (`API_URL`) no body/query.
  O backend valida com o middleware `authorizeUser` (e-mail → autorizado? 401/403).
- Backend: Routes → Services → Prisma; erros via `AppError`; testes com Vitest
  em `backend/tests/{unit,integration}`. Imagem `node:20-slim`.
- `docs/diagrams/chateau-web-api-map.drawio` já previa uma caixa
  "chateau-orchestration (a criar — LangChain)" com `search(query): Specialist[]`
  e `rankingScore`. **Essa interface está desatualizada**: o modelo devolve
  Cypher e linhas do banco, não especialistas ranqueados.

---

## 2. Fatos verificados no pacote do Edson

Pacote `chateau-cypher-orquestrador-v1.0.1` (cópia local em
`~/projetos/chateau/chateau-cypher-orquestrador-v1.0.1/`, ignorada pelo git;
original no servidor em `~/chateau/model/`). README também em
`docs/orquestrador/README.md`. Tudo abaixo foi lido no código, não inferido.

### As três peças

| peça | onde roda | faz |
|---|---|---|
| **Modelo** `chateau-gemma4-e4b-cypher` (Gemma 4 E4B + LoRA, GGUF 5 GB, pacote separado de 4,9 GB) | **Ollama** na máquina com GPU | só pergunta + schema → **texto de uma query Cypher**. Não valida, não explica, não corrige, não devolve erro estruturado. |
| **Orquestrador** (`cliente/chateau_cypher.py`, `cliente/perguntar.py`, `mcp/servidor_mcp.py`) | a máquina da interface | monta o prompt, chama o Ollama, gera avisos, confere se é leitura, executa no Neo4j, grava log |
| **Cliente** | nós | a interface |

**Ollama** = o servidor que carrega o arquivo do modelo na GPU e expõe uma API
HTTP em `:11434` (`POST /api/generate`). Chega-se nele por túnel SSH; do lado da
interface ele aparece em `http://127.0.0.1:11434`.

### O contrato do prompt (não pode mudar nem um caractere)

```
system = "You are a Neo4j Cypher expert. Using the graph schema below, translate the user's question into a single Cypher query. Return only the query, with no explanation and no markdown fences." + "\n\nSchema:\n" + schema
prompt = a pergunta, como o usuário escreveu (pt ou en, sem traduzir)
POST {OLLAMA_URL}/api/generate  {model, system, prompt, stream:false, options:{temperature:0, num_predict:512}}
```

- Schema: remover a quebra de linha final do arquivo (`rstrip("\n")`).
- `/api/generate` foi verificado byte a byte; `/api/chat` **não** foi.
- Contexto 4.096 tokens; o Ollama corta o **início** (a instrução) se estourar.

### O que cada arquivo faz

- `cliente/exemplo_http.sh` — o comando citado na reunião. `jq` monta o JSON,
  `curl` no Ollama, imprime **só** `.response`. **Não** valida, **não** executa,
  **não** loga. Se o Ollama responder `{"error": ...}`, o `jq -r '.response'`
  imprime **`null`**.
- `cliente/chateau_cypher.py` — biblioteca (só stdlib para o Ollama; `neo4j` e
  `neo4j_graphrag` sob demanda):
  - `gerar_cypher(pergunta, schema, usuario=...)` → `Resultado{cypher, avisos,
    tokens_prompt, tokens_resposta, segundos, bruto}`; grava uma linha no log
    JSONL (`CHATEAU_LOG`, padrão `~/.chateau-cypher/consultas.jsonl`) com
    quando, usuario, idioma, pergunta, cypher, modelo, schema_sha256, avisos,
    tokens, segundos (ou `erro`). Levanta `RuntimeError` se o Ollama falhar.
  - Avisos: schema > 11.058 caracteres; schema vazio; prompt ≥ 4.088 tokens
    (início cortado); prompt > 3.328 tokens; `done_reason == "length"`
    (resposta incompleta).
  - `limpar_resposta`: tira `<turn|>` e cercas de markdown.
  - `obter_schema(driver)`: extrai o schema do banco no formato do treino
    (enhanced; cai para **compacto** se passar de 7.618 caracteres).
  - `executar_somente_leitura(driver, cypher, limite=50, timeout_s=30)`:
    `EXPLAIN` → só aceita `query_type == "r"`, senão `PermissionError`;
    executa em `execute_read` com timeout; devolve
    `{colunas, linhas, truncado}` (linhas via `record.data()`).
- `cliente/perguntar.py --json [--executar]` — CLI que junta tudo. Saída:
  `{cypher, avisos, tokens_prompt, segundos, resultado?:{colunas,linhas,truncado}, recusada?}`.
  Código de saída: 0 ok, 1 erro do Ollama/Neo4j (mensagem em stderr), 2 recusada.
- `mcp/servidor_mcp.py` — as mesmas funções como ferramentas MCP (para
  assistente conversacional). Não usaremos agora.
- `exemplo/` — banco acadêmico fictício (`criar_banco.cypher`, 71 nós),
  `schema_compacto.txt` (recomendado, 15/20 acertos), `schema_rev5.txt`
  (13/20), `perguntas.jsonl` (20 perguntas com gabarito e resultado esperado).
- `avaliacao/avaliar.py` — compara consulta gerada × gabarito **por resultado**
  no banco (ignora nome de coluna e ordem das linhas).

### O "null ou zero" das bananas

**Nenhum código do pacote trata pergunta fora do domínio.** O modelo sempre
tenta gerar uma query. Hipóteses (a confirmar no teste real, seção 8, Fase 5):

- **zero**: o modelo gera algo como `MATCH (b:Banana) RETURN count(b)` → o banco
  devolve `[{count: 0}]`, ou uma query que devolve zero linhas;
- **null**: o `exemplo_http.sh` imprime `null` quando o Ollama devolve erro
  (modelo ausente, fora do ar) — ou seja, falha de infraestrutura, não resposta.

O README (seção 9) também avisa: **resultado vazio/zero/nulo é o sintoma de todos
os erros de fato do modelo**. Não dá para distinguir "fora do domínio" de "query
errada" — os dois viram "não encontrei resultados", sempre mostrando a query.

---

## 3. Decisões tomadas

| # | decisão | por quê |
|---|---|---|
| D1 | O tratamento da volta (sem resultado, recusada, erro) é **nosso**. | O modelo só gera texto; o pacote não trata fora-do-domínio. |
| D2 | **Não reescrever em TypeScript.** Primeiro usar o código Python do Edson como está. | Aproveitar o que ele entregou e validou. |
| D3 | Duas implementações do `chateau-orchestration`, **em sequência**: Python (ponte, agora) e **Quarkus** (definitiva, pedida pelo Edson). A Quarkus tem de dar **o mesmo resultado** da Python. | Python funciona já para o teste com GPU; Quarkus é a diretriz do coordenador; a Python vira gabarito. |
| D4 | Tudo em `chateau-expert/orchestration/`, em pastas separadas (`python/`, `quarkus/`). Ao final: apaga `python/`, move `quarkus/` para a raiz de `orchestration/`. | Uma pasta só para a camada de IA, como previsto no README dela. |
| D5 | O orchestration é um **serviço HTTP** com um **contrato único** (seção 6), implementado igual pelas duas versões. O backend fala com ele por HTTP. | A troca Python → Quarkus não muda nada no backend nem no web. (Chamar o `.py` como subprocesso do backend obrigaria a mexer no backend na troca.) |
| D6 | O pacote do Edson entra **intacto** em `orchestration/python/edson/`; nosso código só importa dele. | Versão nova do pacote = substituir a pasta. |
| D7 | O **mock fica no backend**, escolhido por variável de ambiente: `ORCHESTRATION_URL` vazia → mock; preenchida → serviço real. Esta é a "troca de uma linha". | O web e o backend funcionam em dev sem Ollama, sem Neo4j e sem Python. |
| D8 | A **classificação** da resposta (ok / sem resultado / recusada / erro) fica no **backend** (TypeScript, testada), não no orchestration. | O orchestration fica como porte fiel do código do Edson (mais fácil de comparar Python × Quarkus); a regra de negócio da volta tem uma implementação só. |
| D9 | A query gerada sempre acompanha a resposta na interface, em todos os status. | Pedido do Edson; e zero linhas é suspeito, o usuário precisa ver a query. |

---

## 4. Revisão da arquitetura — pontos encontrados

A arquitetura (web → backend → orchestration → Ollama/Neo4j) está correta e bate
com o diagrama de implantação do Edson (`figuras/chateau-deploy.png`:
chateau-client → chateau-orchestration → Local LLM Runner). Ajustes e riscos
encontrados na revisão:

1. **Schema de produção ≠ schema de exemplo.** O `schema_compacto.txt` descreve o
   banco fictício do Edson. O Neo4j de produção tem os dados reais do
   `chateau-data`, com rótulos, propriedades e relações próprios. Enviar o schema
   do exemplo contra o banco real faz o modelo gerar queries com nomes que não
   existem. **Ação:** extrair o schema do banco de produção com
   `chateau_cypher.obter_schema(driver)` (sai compacto neste domínio), revisar e
   **fixar em arquivo** (`orchestration/schema/schema_producao.txt`), como o
   README recomenda. O arquivo é compartilhado pelas duas implementações. Medir
   tamanho/tokens (limite de contexto).
2. **Container → túnel do Ollama.** O túnel (provavelmente reverso, partindo da
   máquina com GPU, porque a interface está atrás do firewall) escuta em
   `127.0.0.1:11434` **do host**. Um container na `backend_net` não enxerga o
   loopback do host. Opções, a decidir na Fase 5:
   - (a) túnel escutando no IP do gateway da rede Docker (`-R <gw>:11434:...`),
     o que exige `GatewayPorts clientspecified` no `sshd` do servidor (sudo);
   - (b) um repassador `socat` no host (ou container com `network_mode: host`)
     do IP do gateway para `127.0.0.1:11434`, sem mexer no `sshd`;
   - (c) orchestration com `network_mode: host` (alcança Ollama e Neo4j em
     `127.0.0.1`), mas aí o backend precisa alcançá-lo pelo gateway — mesmo
     problema invertido.
   Recomendação: (a) se houver sudo; senão (b). No container, `OLLAMA_URL=http://host.docker.internal:11434`
   com `extra_hosts: ["host.docker.internal:host-gateway"]`.
3. **Neo4j Community não tem usuário só-leitura.** O README recomenda conectar
   com um usuário sem permissão de escrita, mas controle de acesso por papéis é
   recurso da edição Enterprise. As travas que sobram são as do código do Edson
   (`EXPLAIN` só aceita `r` + `execute_read`), e são suficientes como defesa;
   registrar a limitação.
4. **LangChain4j usa `/api/chat`, o contrato foi verificado em `/api/generate`.**
   O `OllamaChatModel` do LangChain4j fala com `/api/chat` (mensagens
   system/user). Pode renderizar o mesmo template, mas não foi verificado. Além
   disso, o LangChain4j tem recursos prontos de "text-to-Cypher" com **prompt
   próprio** — proibido usar (quebra o contrato em silêncio). Na Fase 6: ou
   chamar `/api/generate` (REST client do Quarkus) ou provar pela comparação
   (Fase 7) que `/api/chat` gera o mesmo texto nas 20 perguntas.
5. **Serialização das linhas precisa ser idêntica nas duas versões.** O Python
   usa `record.data()` e `json.dumps(default=str)`. **Medido contra um Neo4j 5
   real (2026-09-28)** — a regra que estava aqui ("relações viram mapas de
   propriedades") estava errada: nó → mapa de propriedades; relação →
   `[propsInício, tipo, propsFim]`; caminho → lista achatada; `date`/`datetime`
   → string ISO (com nanossegundos); `duration` → `[meses, dias, segundos,
   nanos]`; `point` → lista de coordenadas. Tabela completa no
   `orchestration/README.md`. A Quarkus tem de reproduzir.
6. **Banco de exemplo para teste.** Neo4j Community tem **um banco de usuário
   só** por instância; não dá para criar o banco de exemplo ao lado do de
   produção. Para rodar as 20 perguntas com gabarito é preciso **outra
   instância** (`neo4j-exemplo`, portas diferentes, carregada com
   `exemplo/criar_banco.cypher`). Serve também para o ambiente de dev e para a
   comparação Python × Quarkus.
7. **Log é dado pessoal.** `gerar_cypher` grava e-mail + pergunta em JSONL.
   Passar `usuario=<e-mail autenticado>`; montar volume
   (`backend/volumes/orchestration/logs`) para não perder a cada deploy;
   definir retenção (pendência com o Edson; ver também `docs/termos-uso/`).
8. **Latência.** Modelo carregado: ~0,7 s; primeira chamada: ~6 s (carga do
   modelo). Timeout do backend → orchestration generoso (60 s) e chamada de
   aquecimento na subida do orchestration.
9. **Contador de consultas.** O `responseTimeMs` enviado a `/api/chat-query`
   hoje é aleatório; passa a ser o tempo real medido.

---

## 5. Arquitetura alvo

```
 chateau-client                                  chateau-orchestration              Local LLM Runner
 ──────────────                                  ─────────────────────              ────────────────
 [usuário] → web (Next.js)                                                          máquina com GPU
   chat/page.tsx                                                                    Ollama :11434
      │ POST /api/search {pergunta}                                                 chateau-gemma4-e4b-cypher
      ▼                                                                                   ▲
   web/src/app/api/search/route.ts  (sessão → e-mail)                                     │ túnel SSH
      │ POST {API_URL}/api/search {email, pergunta}                                       │
      ▼                                                                                   │
   backend (Express)  search.router → search.service                                      │
      │  ORCHESTRATION_URL vazia? ── sim ─► mock (mesmo JSON do contrato)                 │
      │                           └ não ─► POST {ORCHESTRATION_URL}/search ──► python/ ou quarkus/
      │                                                                          ├─ HTTP ─┘
      │                                                                          └─ bolt ─► Neo4j (chateau_neo4j)
      │  ◄── JSON do contrato (seção 6)                                                     EXPLAIN → só 'r'
      │  classifica (seção 7)                                                               execute_read
      ▼
   web mostra: mensagem do status + tabela + query gerada (recolhível) + avisos
   persiste no chat: content = "__SEARCH__:" + JSON
```

Rede (produção): `orchestration` na `backend_net`, **sem porta publicada**;
alcança `neo4j:7687` pelo nome do serviço e o Ollama pelo gateway (seção 4, item 2).
O backend alcança `http://orchestration:8000`.

### Estrutura de pastas

```
chateau-expert/orchestration/
  README.md                contrato HTTP (seção 6), como rodar, variáveis
  schema/
    schema_producao.txt    schema do Neo4j de produção (fonte única p/ as duas versões)
  python/                  implementação ponte (Fase 1)
    edson/                 pacote chateau-cypher-orquestrador-v1.0.1 INTACTO
    servidor.py            HTTP (FastAPI) → edson/cliente/chateau_cypher.py
    requirements.txt       fastapi, uvicorn, neo4j>=5, neo4j-graphrag>=1.19, numpy<2.4
    Dockerfile
    tests/                 pytest com Ollama e Neo4j simulados
  quarkus/                 implementação definitiva (Fase 6)
  comparacao/
    comparar.py            mesmas perguntas → python × quarkus → relatório
    perguntas_reais.jsonl  perguntas do nosso domínio (coletadas na Fase 5)
```

### Rodar localmente

Quase tudo roda na máquina de desenvolvimento; o servidor só é necessário para
o deploy de produção. Três níveis:

| nível | roda local | precisa de | serve para |
|---|---|---|---|
| **1. Mock** | web + backend (`docker compose up`) | nada além do de sempre | Fases 2 e 3: interface, classificação da volta, todos os cenários do mock |
| **2. Banco de exemplo** | + `neo4j-exemplo` + orchestration (`docker compose --profile ia up`) | só Docker | Fase 1 e o caminho completo, com o modelo simulado ou real |
| **3. Dados reais** | orchestration local apontando para o Neo4j de produção | túnel `ssh -L 7687:localhost:7687 prointec@152.92.2.63` | testar com schema e dados reais sem deploy |

**O modelo não roda localmente** (em CPU a primeira pergunta não terminou em 9
minutos, README seção 10). Mas dá para usar o modelo real daqui **encadeando
túneis**: se a máquina com GPU chega no servidor por túnel reverso, o Ollama
aparece em `127.0.0.1:11434` do servidor, e da máquina local:

```bash
ssh -L 7687:localhost:7687 -L 11434:127.0.0.1:11434 prointec@152.92.2.63
```

traz Neo4j de produção e Ollama para o `localhost` local.

**Pegadinha (Docker Desktop no WSL2):** container não enxerga o `localhost` da
distro WSL onde o túnel escuta. Orchestration em container local usa
`host.docker.internal` (ver `docs/neo4j/README.md`). Rodar o orchestration
Python direto no WSL (fora do Docker) evita o problema.

**Só testável no servidor:** a rede de produção (container `orchestration` →
túnel do Ollama no host, seção 4 item 2) e o deploy — fim da Fase 5.

---

## 6. Contrato HTTP do orchestration

Igual nas duas implementações. Nomes de campo iguais aos do `perguntar.py --json`
sempre que possível.

### `POST /search`

Requisição:

```json
{ "pergunta": "Quantos livros existem?", "usuario": "fulano@uerj.br", "limite": 50 }
```

- `pergunta` obrigatória, não vazia; `usuario` obrigatório (vai para o log);
  `limite` opcional, 1–500, padrão 50.
- 422 se inválida. Qualquer outro desfecho responde **200** com o corpo abaixo.

Resposta:

```json
{
  "cypher": "MATCH (b:Book) RETURN count(b) AS total",
  "avisos": [],
  "tokens_prompt": 1843,
  "segundos": 0.71,
  "resultado": { "colunas": ["total"], "linhas": [{"total": 12}], "truncado": false },
  "recusada": null,
  "erro": null
}
```

Exatamente um destes descreve o desfecho:

| desfecho | `cypher` | `resultado` | `recusada` | `erro` |
|---|---|---|---|---|
| executou | texto | objeto | null | null |
| query de escrita | texto | null | mensagem do `PermissionError` | null |
| falha no modelo (Ollama fora, modelo ausente) | null | null | null | `{"etapa": "modelo", "mensagem": "..."}` |
| modelo devolveu texto vazio | `""` | null | null | `{"etapa": "modelo", "mensagem": "resposta vazia"}` |
| falha no banco (sintaxe, conexão, timeout) | texto | null | null | `{"etapa": "banco", "mensagem": "..."}` |

Serialização das linhas: seção 4, item 5.

### `GET /health`

`{"ollama": true, "neo4j": true, "modelo": "chateau-gemma4-e4b-cypher", "schema_sha256": "f9dc0f48..."}`
— não chama o modelo; `ollama` via `GET /api/tags`, `neo4j` via `RETURN 1`.

### Variáveis de ambiente (as mesmas do pacote do Edson)

`OLLAMA_URL`, `OLLAMA_MODELO`, `CHATEAU_SCHEMA_ARQUIVO`, `CHATEAU_LOG`,
`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`, `PORT` (8000).

---

## 7. Classificação da volta (backend)

`backend/src/services/search.service.ts` transforma o contrato em:

```ts
{ status, mensagem, cypher, avisos, colunas, linhas, truncado, tempoMs }
```

| status | condição (na ordem) | mensagem ao usuário (pt-BR) |
|---|---|---|
| `indisponivel` | orchestration não responde/timeout, ou `erro.etapa == "modelo"` | "O serviço de busca está indisponível no momento. Tente novamente em instantes." |
| `recusada` | `recusada` preenchido | "Esta pergunta gerou uma consulta que altera dados e foi bloqueada por segurança." |
| `erro_consulta` | `erro.etapa == "banco"` | "Não consegui executar a consulta gerada. Tente reformular a pergunta." |
| `sem_resultado` | `linhas` vazio, **ou** todas as células de todas as linhas são `0`, `null`, `""` ou `[]` | "Não encontrei resultados. A pergunta pode estar fora do escopo da base ou a consulta gerada pode não corresponder ao que você quis dizer — confira a consulta abaixo." |
| `ok` | resto | "Encontrei N resultado(s)." (+ "mostrando os primeiros N" se `truncado`) |

- `cypher` e `avisos` vão para a interface em **todos** os status (D9).
- Detalhe técnico do erro (`erro.mensagem`) vai para o log do backend, não
  para a tela.
- Rota: `POST /api/search` com `authorizeUser` (e-mail no body), montada em
  `backend/src/app.ts`.

---

## 8. Fases

Cada fase termina com seus critérios de aceite cumpridos e um commit por repo
tocado (mensagens em pt-BR, padrão `feat:`/`fix:`/`docs:` já usado).

### Fase 0 — Preparação

- [x] Copiar `chateau-cypher-orquestrador-v1.0.1/` para
      `chateau-expert/orchestration/python/edson/` sem alterações (conferir
      `sha256sum -c SHA256SUMS` dentro da pasta).
- [ ] Extrair o schema do Neo4j de produção (túnel `ssh -L 7687:localhost:7687 prointec@152.92.2.63`;
      script usando `cc.conectar()` + `cc.obter_schema(driver)`), revisar e
      gravar em `orchestration/schema/schema_producao.txt` (sem `\n` final).
      Registrar tamanho em caracteres e aviso de tokens.
      *Script pronto e validado:* `orchestration/schema/extrair_schema.py`
      (instruções no arquivo). Rodado no banco de exemplo, saiu idêntico ao
      `schema_compacto.txt` do Edson. **Falta rodar na produção** — precisa do
      túnel SSH (senha) e da `NEO4J_PASSWORD` do `.env.prod`. Exige APOC.
- [x] Atualizar `orchestration/README.md` (substitui o placeholder) com o
      contrato da seção 6.

Aceite: pacote conferido pelo SHA256SUMS; schema em arquivo, abaixo de 11.058
caracteres de prompt de sistema (ou decisão registrada se passar).

### Fase 1 — `orchestration/python`

- [x] `servidor.py` (FastAPI): `POST /search` e `GET /health` conforme seção 6,
      importando `edson/cliente/chateau_cypher.py` (`gerar_cypher` com
      `usuario=`, `executar_somente_leitura`). Driver Neo4j criado uma vez.
      Schema lido uma vez de `CHATEAU_SCHEMA_ARQUIVO` com `rstrip("\n")`.
- [x] Aquecimento opcional na subida (uma chamada curta ao Ollama, sem log).
- [x] Serialização das linhas conforme seção 4, item 5.
- [x] `tests/` com pytest: Ollama e Neo4j simulados, um teste por desfecho da
      tabela da seção 6, mais 422.
- [x] `Dockerfile` (python:3.12-slim, usuário não-root, `uvicorn`).

Aceite: testes passam; com Ollama simulado, cada desfecho devolve o JSON exato
da seção 6.

*Feito em 2026-09-28:* 22 testes passando (Ollama falso é um servidor HTTP
real, então o `gerar_cypher` do Edson roda inteiro, inclusive o log). Imagem
builda e sobe; testado também contra Neo4j 5 real com o banco de exemplo
(recusa de escrita `'w'`, erro de sintaxe, serialização). Aquecimento: `POST
/api/generate` só com `{"model"}` (o Ollama carrega sem gerar), em thread,
desligável com `CHATEAU_AQUECER=0`. Timeout do modelo: 55 s. Dockerfile usa
contexto `orchestration/` (para copiar `schema/`).

### Fase 2 — Backend

- [x] `backend/src/lib/orchestration.ts`: cliente HTTP do contrato
      (`ORCHESTRATION_URL`, `ORCHESTRATION_TIMEOUT_MS=60000`).
- [x] `backend/src/lib/orchestration.mock.ts`: devolve o **mesmo JSON do
      contrato**, com cenários por palavra-chave na pergunta, para exercitar a
      interface: padrão → `ok` com linhas fictícias; "banana" → contagem 0;
      "nada" → zero linhas; "apague"/"delete" → `recusada`; "erro banco" →
      `erro.etapa=banco`; "fora do ar" → `erro.etapa=modelo`. Atraso fixo curto.
- [x] `backend/src/services/search.service.ts`: escolhe mock × real e
      classifica (seção 7). Tipos em `backend/src/types/index.ts`.
- [x] `backend/src/routes/search.router.ts` + registro em `app.ts`.
- [x] Testes unitários do classificador (todas as linhas da seção 7, inclusive
      `[{count: 0}]`, `[{x: null}]`, truncado) e de integração da rota com o
      mock (401/403 via `authorizeUser`).
- [x] `.env.example` e `backend/CLAUDE.md` (endpoint novo, variáveis).

Aceite: `npm test` verde; `ORCHESTRATION_URL` vazia → mock; preenchida → chama
o serviço.

*Feito em 2026-09-28:* 51 testes verdes (10 unitários do `classify`, 13 de
integração da rota: 401/403/400, os 6 cenários do mock, chamada real a um
orchestration falso, HTTP 500, fora do ar e timeout). Extras em relação ao
planejado: `ORCHESTRATION_MOCK_DELAY_MS` (padrão 800; 0 nos testes), limite de
1.000 caracteres na pergunta (400), resposta fora do contrato →
`indisponivel`. O backend **não** envia `limite` (vale o padrão 50 do
orchestration). Em `sem_resultado` as linhas/colunas seguem para a tela (ex.:
mostrar o `count = 0`). Para rodar os testes sem mexer na stack de dev:
container `chateau-expert-api` com `node_modules` em tmpfs e Postgres de teste
em rede isolada (o `node_modules` do host é volume do Docker, dono root).

### Fase 3 — Web

- [x] `web/src/app/api/search/route.ts`: mesmo padrão de `api/chats/route.ts`
      (sessão → e-mail; repassa status HTTP; 403 → o chat manda para `/pending`).
- [x] `chat/page.tsx` → `send()`: troca `setTimeout` + `mockResponse()` por
      `await fetch("/api/search")`; mede o tempo real e envia ao
      `/api/chat-query`; conteúdo da mensagem = `"__SEARCH__:" + JSON`.
- [x] Componente `SearchResult`: mensagem do status; tabela (`colunas`/`linhas`,
      rolagem horizontal, aviso de truncado); avisos; bloco recolhível
      "Consulta gerada" com a query e botão copiar. Cores/ícones por status.
      shadcn/ui, pt-BR.
- [x] Manter `ProfessionalsList` só para renderizar chats antigos
      (`__PROFESSIONALS__:`); remover `mockResponse()`.
- [x] `npm run build` limpo. `npm run lint`: **já falhava no `main`** (4 erros
      antigos: `sidebar.tsx`, `middleware.ts` e dois `setState` em efeito no
      `chat/page.tsx`); nenhum erro novo nos arquivos tocados.

Aceite: com o mock, cada cenário da Fase 2 aparece corretamente no chat,
persiste e reabre igual pelo histórico.

*Feito em 2026-09-28, menos o aceite visual:* `/api/search` da stack de dev
responde pelo mock (conferido por `fetch` dentro do container `api`). **Falta
você abrir o chat no navegador** (login Google) e passar pelos 6 cenários
("Quem pesquisa otimização?", "bananas", "nada", "apague", "erro banco",
"fora do ar"), conferindo que persistem e reabrem pelo histórico. Detalhes:
componente em `web/src/app/chat/SearchResult.tsx`, tipos em
`web/src/types/search.ts`; "Consulta gerada" é um `<details>` aberto por padrão
em todos os status menos `ok`; se o web não alcança o backend, a mensagem
mostrada (e persistida) é a de `indisponivel`. A verificação de 403 que o mock
fazia com `GET /api/chats/:id` saiu: o `/api/search` já passa pelo
`authorizeUser`.

### Fase 4 — Infra (compose)

- [x] `docker-compose.prod.yml`: serviço `orchestration` (build: context
      `./orchestration`, dockerfile `python/Dockerfile`), rede `backend_net`, sem porta publicada,
      `NEO4J_URI=neo4j://neo4j:7687`, `NEO4J_PASSWORD`, `OLLAMA_URL`,
      `CHATEAU_SCHEMA_ARQUIVO=/app/schema/schema_producao.txt`,
      `CHATEAU_LOG=/logs/consultas.jsonl`, volume de logs, `extra_hosts`
      host-gateway, healthcheck em `/health`. `api` ganha
      `ORCHESTRATION_URL=http://orchestration:8000` (em `.env.prod`).
- [x] `docker-compose.yml` (dev): profile `ia` com `neo4j-exemplo` (carregado
      com `edson/exemplo/criar_banco.cypher`; **com APOC**,
      `NEO4J_PLUGINS='["apoc"]'`, para o `obter_schema` funcionar) + `orchestration` apontando para
      ele com `schema_compacto.txt`. Sem o profile, dev roda com mock.
- [x] Documentar no `orchestration/README.md`.

Aceite: `docker compose up` (sem profile) funciona com mock;
`docker compose --profile ia up` sobe orchestration + banco de exemplo.

*Feito em 2026-09-28:* ambos validados com `docker compose config`; profile `ia`
de dev subido e testado (banco de exemplo com 71 nós, `/health` com
`neo4j: true`, log no volume). Teste ponta a ponta com um Ollama **falso**
contra o Neo4j de exemplo: "livros" → `[{total: 2}]`, "bananas" →
`[{total: 0}]`, `DETACH DELETE` → recusada. Decisões: em produção o
`orchestration` também fica no profile `ia` (ligar com `COMPOSE_PROFILES=ia`
no `.env.prod` na Fase 5 — deploy atual não muda nada); log em **volume
nomeado** `orchestration_logs` (bind mount criaria a pasta como root e o
container, uid 10001, não conseguiria gravar); `neo4j-exemplo` sem volume e
recarregado a cada subida (o script usa `CREATE`).

### Fase 5 — Teste real com GPU (2026-09-30 a 2026-10-02)

- [ ] Túnel de pé; no servidor: `curl -s http://127.0.0.1:11434/api/tags | jq -r '.models[].name'`
      lista `chateau-gemma4-e4b-cypher`.
- [ ] Rodar direto no host, sem Docker, para isolar problemas:
      `exemplo_http.sh` e `perguntar.py --executar --json` com as perguntas da
      reunião ("Quantos livros existem?", "Quantos artigos o Edson produziu em
      2025?", "Quantas bananas tem numa penca?"). **Registrar o que volta para
      as bananas** (fecha a hipótese da seção 2).
- [ ] `avaliar.py` com as 20 perguntas no `neo4j-exemplo` (esperado ≈15/20 com
      o compacto) — confirma que a instalação reproduz a medição do Edson.
- [ ] Perguntas reais contra o banco de produção com `schema_producao.txt`;
      gravar pergunta, cypher, resultado e julgamento em
      `comparacao/perguntas_reais.jsonl`.
- [ ] Resolver o acesso container → Ollama (seção 4, item 2) e subir o
      orchestration em produção; trocar `ORCHESTRATION_URL` e testar pela
      interface.

Aceite: busca real funcionando pela interface em produção; comportamento de
fora-do-domínio documentado.

### Fase 6 — `orchestration/quarkus`

- [ ] Projeto Quarkus (Java 21, Quarkus 3 LTS): `quarkus-rest`,
      `quarkus-rest-jackson`, `quarkus-neo4j`, `quarkus-smallrye-health`,
      `quarkus-langchain4j-ollama`.
- [ ] Portar, fiel ao Python: `INSTRUCAO` e `montar_system` (idênticos),
      `limpar_resposta` (mesma regex), avisos (mesmos limites e textos),
      `temperature 0`, `num_predict 512`, `EXPLAIN` + recusa se o tipo não for
      `READ_ONLY` (`ResultSummary.queryType()`), transação de leitura com
      timeout 30 s e limite de linhas, log JSONL com os mesmos campos,
      serialização da seção 4, item 5.
- [ ] Chamada ao modelo: ver seção 4, item 4. **Não** usar recursos
      text-to-Cypher prontos do LangChain4j.
- [ ] Mesmas variáveis de ambiente, mesma porta, mesmo contrato; Dockerfile.
- [ ] Testes (JUnit/QuarkusTest) espelhando os da Fase 1.

Aceite: testes passam; serviço sobe e responde ao contrato.

### Fase 7 — Comparação e troca

- [ ] `comparacao/comparar.py`: para cada pergunta (20 do exemplo +
      `perguntas_reais.jsonl`), chama `POST /search` nas duas versões (mesmo
      Ollama, mesmo banco, mesmo schema) e compara: `cypher` (texto, espaços
      normalizados), `resultado` (mesma comparação do `edson/avaliacao/avaliar.py`:
      sem nome de coluna nem ordem), `recusada`, `erro.etapa`, `avisos`.
      Gera relatório Markdown.
- [ ] Critério: **resultado igual em 100%** das perguntas. Texto de `cypher`
      diferente é listado e analisado (variação do Ollama × diferença de
      prompt — a segunda é bug).
- [ ] Troca: apontar o compose para `quarkus/`, validar em produção, apagar
      `python/`, mover `quarkus/*` para `orchestration/`, ajustar build path.
      Manter `comparacao/` para versões futuras do modelo (comparando contra os
      resultados gravados).

Aceite: relatório 100% igual; produção rodando Quarkus.

---

## 9. Pendências com o Edson

1. Confirmar o que acontece com pergunta fora do domínio (ou validar na Fase 5).
2. Quarkus: é para já ou é evolução depois que a busca real estiver no ar? Ok
   usar o Python dele como ponte até lá?
3. Diagrama do Drive: pedir exportação em PNG.
4. Túnel da GPU: quem sobe, direção (reverso?), e se temos sudo no servidor
   para `GatewayPorts` (seção 4, item 2).
5. Log de consultas (dado pessoal): onde guardar e por quanto tempo.
6. Aceita a chamada ao modelo via `/api/chat` (LangChain4j) se a comparação
   provar equivalência, ou exige `/api/generate`?
7. Schema de produção: validar com ele o arquivo extraído antes de fixar.

## 10. Riscos

| risco | mitigação |
|---|---|
| Schema de produção grande demais para o contexto | medir na Fase 0; se passar, enviar só rótulos/relações relevantes (README seção 7) |
| Modelo erra muito no banco real (domínio fora do treino; caminho com nó intermediário falha) | mostrar sempre a query; coletar perguntas reais + correções para o Edson (log) |
| GPU só disponível qua–sex | Fases 0–4 prontas antes de quarta; Fase 5 roteirizada |
| Divergência silenciosa Python × Quarkus | contrato único + comparação automatizada (Fase 7) |
| CPU do servidor sem SSE4.2 derruba `numpy` | `numpy<2.4` no requirements (já no pacote) |

## 11. Referências

- Pacote do Edson: `~/projetos/chateau/chateau-cypher-orquestrador-v1.0.1/`
  (README seções 2 contrato, 6 HTTP, 7 schema, 8 segurança, 9 avaliação, 11 problemas)
- `docs/orquestrador/README.md` (cópia do README do pacote)
- `docs/reunioes/2026-09-23.md`, `docs/talk-ia.md`
- `docs/neo4j/README.md` (acesso ao Neo4j de produção, túnel, cypher-shell)
- `docs/diagrams/chateau-web-api-map.drawio` (atualizar a caixa do orchestration ao final)
- `chateau-expert/web/src/app/chat/page.tsx`, `web/src/app/api/chats/route.ts`,
  `backend/src/middleware/authorizeUser.ts`, `backend/src/app.ts`,
  `docker-compose.prod.yml`, `docker-compose.yml`
