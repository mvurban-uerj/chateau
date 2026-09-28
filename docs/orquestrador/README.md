# chateau-gemma4-e4b-cypher

Modelo que converte **uma pergunta, em português ou inglês, + o schema de um grafo Neo4j** em
**uma consulta Cypher**. É um Gemma 4 E4B ajustado por LoRA para essa tarefa e
nada além dela, empacotado para o Ollama. O Ollama com o modelo roda num
servidor com GPU e fica disponível **via túnel SSH** (seção 3).

Este documento é para quem vai construir uma interface sobre o modelo. Ele cobre
o contrato exato de entrada e saída, duas formas de integração (MCP e HTTP
direto), um **banco de exemplo no domínio acadêmico**, segurança na execução das
consultas e como medir a qualidade.

> **Leia a seção [O contrato](#2-o-contrato-leia-antes-de-integrar) antes de
> escrever qualquer código.** O modelo não dá erro quando recebe o prompt num
> formato diferente do treino: ele só responde pior, em silêncio.

---

## Sumário

1. [O que tem no pacote](#1-o-que-tem-no-pacote)
2. [O contrato](#2-o-contrato-leia-antes-de-integrar)
3. [Início rápido com o banco de exemplo](#3-início-rápido-com-o-banco-de-exemplo)
4. [Qual integração escolher](#4-qual-integração-escolher)
5. [Integração via MCP (recomendada)](#5-integração-via-mcp-recomendada)
6. [Integração via HTTP direto](#6-integração-via-http-direto)
7. [O schema: qual enviar](#7-o-schema-qual-enviar)
8. [Segurança](#8-segurança)
9. [Qualidade e avaliação](#9-qualidade-e-avaliação)
10. [Desempenho e hardware](#10-desempenho-e-hardware)
11. [Solução de problemas](#11-solução-de-problemas)

---

## 1. O que tem no pacote

São **dois pacotes**, um para cada máquina da implantação (seção 4), ambos com
este mesmo README:

| pacote | para | contém |
|---|---|---|
| `chateau-gemma4-e4b-cypher-modelo-v1.0.1.tar.gz` (4,9 GB) | a máquina com GPU que roda o Ollama (**Local LLM Runner**) | o modelo |
| `chateau-cypher-orquestrador-v1.0.1.tar.gz` (~100 KB) | a máquina da interface (**chateau-client** e **chateau-orchestration**) | cliente, orquestrador, banco de exemplo e avaliação |

As duas máquinas se falam **via túnel SSH** (seção 3): o orquestrador abre o
túnel e enxerga o Ollama como se fosse local.

### Pacote do modelo

```
chateau-gemma4-e4b-cypher-modelo-v1.0.1/
├── README.md                    este documento
├── LICENCAS.md                  licenças do modelo, dos dados e das dependências
├── SHA256SUMS                   hash de cada arquivo
├── modelo/
│   ├── gemma-4-e4b-it.Q4_K_M.gguf   o modelo (5,0 GiB)
│   ├── Modelfile                    template e parâmetros do Ollama, NÃO edite
│   └── export.json                  base, quantização e contrato usados no export
└── figuras/
    └── chateau-deploy.png       diagrama de implantação (seção 4)
```

### Pacote do orquestrador

```
chateau-cypher-orquestrador-v1.0.1/
├── README.md                    este documento
├── LICENCAS.md
├── SHA256SUMS
├── cliente/
│   ├── chateau_cypher.py        biblioteca: monta o prompt, chama o Ollama,
│   │                            lê o schema, executa em modo somente leitura
│   │                            e grava o log de consultas
│   ├── perguntar.py             linha de comando
│   └── exemplo_http.sh          o mesmo, só com curl e jq
├── mcp/
│   ├── servidor_mcp.py          servidor MCP (ferramentas para um assistente)
│   ├── requirements.txt
│   └── claude_desktop_config.exemplo.json
├── exemplo/                     banco de exemplo no domínio acadêmico (dados fictícios)
│   ├── criar_banco.cypher       cria o banco: 71 nós, 140 relações
│   ├── schema_rev5.txt          o schema-alvo do domínio, curado
│   ├── schema_compacto.txt      o mesmo banco, extraído pelo neo4j-graphrag
│   ├── schema_enhanced.txt      idem, formato enhanced (grande demais: ver seção 7)
│   └── perguntas.jsonl          20 perguntas com gabarito validado no banco
├── avaliacao/
│   ├── avaliar.py               mede acerto por texto e por resultado no banco
│   └── exemplos.jsonl           63 exemplos do conjunto de teste do corpus
└── figuras/
    └── chateau-deploy.png       diagrama de implantação (seção 4)
```

`cliente/chateau_cypher.py` é a **única fonte do contrato de prompt**. O servidor
MCP, a linha de comando e a avaliação importam dele. Se você escrever sua
interface em Python, importe-o também; em outra linguagem, replique a função
`montar_system` exatamente (seção 2).

---

## 2. O contrato (leia antes de integrar)

### Entrada

O modelo recebe duas mensagens.

**Sistema** — uma instrução fixa, seguida de `\n\nSchema:\n` e do schema:

```
You are a Neo4j Cypher expert. Using the graph schema below, translate the user's question into a single Cypher query. Return only the query, with no explanation and no markdown fences.

Schema:
<schema do grafo>
```

A instrução é idêntica, caractere por caractere, nos 40.338 exemplos do corpus de
treino. Não traduza, não resuma, não acrescente regras: qualquer mudança tira o
modelo da distribuição em que foi treinado.

**Usuário** — só a pergunta, **no idioma do usuário** (português ou inglês), sem tradução.

### Saída

Uma consulta Cypher, sem explicação e sem cercas de markdown. A geração termina
sozinha no marcador `<turn|>`, que o `Modelfile` já configura como parada e que
não aparece no texto devolvido.

### Por que é tão rígido

O contrato foi conferido de duas formas:

- **Montagem do prompt:** `montar_system(schema)` somado ao template do
  `Modelfile` reproduz o prompt do treino **byte a byte em 41.628 de 41.628
  exemplos** do corpus, em todos os conjuntos.
- **Servidor:** renderizando o template que o próprio Ollama usa e comparando
  com o corpus, **5 de 5 idênticos**, sem vazamento de marcador e com parada
  correta.

### Três regras que a sua interface precisa cumprir

| regra | por quê |
|---|---|
| **Schema adequado ao banco.** | Veja a seção 7: o formato e o tamanho do schema mudam o resultado. |
| **`temperature: 0`.** | A tarefa tem uma resposta certa, não várias boas. |
| **Schema dentro do contexto.** | Contexto de 4.096 tokens; o treino usou janela de 3.328. Acima disso o Ollama corta o **início** do prompt, que é justamente a instrução. `gerar_cypher` avisa. |

### Limites conhecidos

- Responde **uma consulta por pergunta**. Não conversa, não explica, não corrige.
- Não sabe o que há no banco além do schema. Valores literais da pergunta
  (`'Ana Ribeiro'`) são copiados; nomes de rótulos e propriedades vêm do schema.
- A consulta pode estar **sintaticamente certa e semanticamente errada** (sentido
  da relação invertido, filtro no nó errado). Trate-a como rascunho a conferir.
- **Idioma.** O corpus de treino é todo em inglês (0 de 37.061 perguntas em
  português), mas a avaliação do projeto não encontrou diferença de acurácia
  entre perguntas em português e em inglês. Envie a pergunta como o usuário a
  escreveu; traduzir não traz ganho e pode alterar valores literais (nomes,
  títulos) que a consulta precisa copiar.

---

## 3. Início rápido com o banco de exemplo

### Requisitos

- **Ollama 0.32.9 ou mais recente.** Versões antigas não conhecem a arquitetura
  `gemma4`: a 0.6.5 registra o modelo e depois falha com `unable to load model`.
  Testado: 0.32.9 e 0.33.3.
- **Neo4j 5 ou mais recente** com o plugin **APOC Core** (necessário só para
  extrair o schema do banco; com o schema em arquivo, não). Testado: Neo4j
  Community 2026.08.1.
- Python 3.10+. O `requirements.txt` do MCP fixa `numpy<2.4`, para rodar também
  em CPUs sem SSE4.2 (seção 11).
- ~6 GB de RAM ou VRAM livres para o modelo (medido: 6,0 GB no `ollama ps`).
- **Acesso SSH ao servidor do Ollama**, com a sua chave.

### Acesso ao Ollama: túnel SSH

O Ollama com o `chateau-gemma4-e4b-cypher` roda num servidor com GPU e fica
disponível **via túnel SSH**. No servidor ele escuta só em `127.0.0.1`, sem
autenticação própria: quem dá o acesso é o SSH, com a chave de cada pessoa.

```bash
ssh -N -L 11434:127.0.0.1:11434 <usuario>@<servidor> -p <porta-ssh>
```

Com o túnel aberto, o Ollama responde em `http://127.0.0.1:11434` na sua
máquina — o padrão de `OLLAMA_URL` —, e nada mais no pacote muda.

- **Em segundo plano:** `ssh -f -N -L ...`, ou `autossh` para reconectar sozinho
  se a conexão cair.
- **Porta local ocupada** (um Ollama local já na 11434): use outra ponta,
  `-L 11500:127.0.0.1:11434`, e `export OLLAMA_URL=http://127.0.0.1:11500`.
- **Ollama do servidor em outra porta:** troque o segundo `11434` do `-L`.
- **Teste:** `curl -s http://127.0.0.1:11434/api/tags | jq -r '.models[].name'`
  deve listar `chateau-gemma4-e4b-cypher`.

### Quando a interface não alcança o servidor: túnel reverso

Se um firewall impede a máquina da interface de abrir SSH no servidor do Ollama,
mas o **contrário** funciona, o túnel parte do servidor com `-R`. Confira antes,
no servidor: `timeout 5 bash -c '</dev/tcp/<maquina-da-interface>/22' && echo ok`.

```bash
# no servidor do Ollama
ssh -N -R 127.0.0.1:11434:127.0.0.1:<porta-do-ollama> <usuario>@<maquina-da-interface>
```

Na máquina da interface, o Ollama passa a responder em `127.0.0.1:11434`, e o
pacote não muda. `<porta-do-ollama>` é a do `OLLAMA_HOST` do servidor (11434 no
padrão).

Para o túnel **reconectar sozinho**, use uma chave dedicada e um serviço de
usuário no servidor. A chave fica sem senha, então restrinja-a na máquina da
interface: no `~/.ssh/authorized_keys`, antes da chave pública,

```
command="/bin/false",restrict,port-forwarding,permitlisten="127.0.0.1:11434" ssh-ed25519 AAAA... tunel
```

Só `restrict` não basta: ele bloqueia terminal e encaminhamentos, mas **não**
impede executar comandos. O `command="/bin/false"` é que fecha isso; o túnel,
aberto com `-N`, não pede sessão e não é afetado.

`~/.config/systemd/user/tunel-ollama.service`, no servidor:

```ini
[Unit]
Description=Tunel reverso do Ollama para a maquina da interface
After=network-online.target

[Service]
ExecStart=/usr/bin/ssh -N -i %h/.ssh/tunel-ollama -o IdentitiesOnly=yes -o BatchMode=yes -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R 127.0.0.1:11434:127.0.0.1:<porta-do-ollama> <usuario>@<maquina-da-interface>
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload && systemctl --user enable --now tunel-ollama
loginctl enable-linger $USER   # sem isto o serviço morre com a última sessão
```

### 1. Instalar os pacotes

**Na máquina do Ollama** (servidor com GPU), uma vez, por quem a administra:

```bash
tar -xzf chateau-gemma4-e4b-cypher-modelo-v1.0.1.tar.gz
cd chateau-gemma4-e4b-cypher-modelo-v1.0.1
sha256sum -c SHA256SUMS
cd modelo && ollama create chateau-gemma4-e4b-cypher -f Modelfile
```

**Na máquina da interface:**

```bash
tar -xzf chateau-cypher-orquestrador-v1.0.1.tar.gz
cd chateau-cypher-orquestrador-v1.0.1
sha256sum -c SHA256SUMS
```

Os comandos das seções seguintes rodam nesta pasta, com o túnel SSH aberto.

### 2. Criar o banco de exemplo

O banco modela produção acadêmica de uma universidade **fictícia**: pessoas,
artigos, livros e capítulos, dissertações e teses, projetos, disciplinas,
programas de pós-graduação e linhas de pesquisa. Nomes, e-mails
(`example.org`) e identificadores Lattes, ORCID e ROR são inventados.

Com Docker (segue a documentação da imagem oficial; **não testado neste ambiente**, que não
tinha acesso ao Docker — a carga do banco foi testada com o `cypher-shell` do Neo4j em tarball):

```bash
docker run -d --name chateau-exemplo -p 127.0.0.1:7474:7474 -p 127.0.0.1:7687:7687 \
  -e NEO4J_AUTH=neo4j/troque-esta-senha \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5
# aguarde ~20 s e carregue os dados
docker exec -i chateau-exemplo cypher-shell -u neo4j -p troque-esta-senha < exemplo/criar_banco.cypher
```

Sem Docker, com o Neo4j instalado:

```bash
cypher-shell -u neo4j -p <senha> -f exemplo/criar_banco.cypher
```

O script espera um banco **vazio**. Ele cobre todos os 22 rótulos, os 33 padrões
de relação, as propriedades de relação e os rótulos adicionais do
`schema_rev5.txt` — conferido programaticamente contra o banco carregado.

### 3. Primeira pergunta

```bash
python3 cliente/perguntar.py --schema-arquivo exemplo/schema_compacto.txt \
  "Which lines of research are defined by the program with acronym 'PGC'?"
```

Para executar a consulta gerada no banco (só se for somente leitura):

```bash
python3 -m venv .venv && .venv/bin/pip install neo4j
export NEO4J_URI=neo4j://127.0.0.1:7687 NEO4J_USER=neo4j NEO4J_PASSWORD=troque-esta-senha
.venv/bin/python cliente/perguntar.py --schema-arquivo exemplo/schema_compacto.txt --executar \
  "Which lines of research are defined by the program with acronym 'PGC'?"
```

A primeira chamada é lenta: o Ollama carrega os 5 GB do modelo (seção 10).

---

## 4. Qual integração escolher

![Implantação: chateau-client, chateau-orchestration e Local LLM Runner](figuras/chateau-deploy.png)

A implantação tem três nós, cada um falando só com o vizinho por requisição e
resposta:

| nó | o que é neste pacote |
|---|---|
| **chateau-client** | a interface que você vai construir: chat, formulário ou serviço |
| **chateau-orchestration** | monta o prompt, chama o modelo, executa a consulta e grava o log: o servidor MCP (`mcp/servidor_mcp.py`) ou a biblioteca `cliente/chateau_cypher.py` |
| **Local LLM Runner** | o Ollama com o `chateau-gemma4-e4b-cypher`, num servidor com GPU, acessado **via túnel SSH** (seção 3) |

A escolha abaixo decide como o **chateau-client** fala com o
**chateau-orchestration**.

| se a sua interface é… | use | porque |
|---|---|---|
| um **assistente conversacional** (chat, Claude Desktop, Claude Code, agente) | **MCP** | O assistente decide quando executar, explica o resultado no idioma do usuário e corrige a consulta quando o banco acusa erro. Tudo o que este modelo **não** sabe fazer. |
| um **formulário** ou **serviço** com pergunta de entrada e tabela de saída | **HTTP direto** | Menos peças. Você mesmo precisa validar e tratar erros. |
| um **pipeline em lote** | **HTTP direto** ou a biblioteca Python | Sem conversa, sem assistente. |

**Recomendação: MCP.** O modelo foi treinado para uma habilidade estreita, e o
MCP o coloca como ferramenta de um assistente capaz de cobrir o que falta. Um
motivo pesa especialmente para este domínio:

- **Transferência de domínio.** Como o domínio acadêmico não está no treino,
  erros são esperados. O assistente vê o erro do Neo4j, confere o schema e
  corrige — algo que um formulário não faz.

---

## 5. Integração via MCP (recomendada)

### Arquitetura

```
usuário ──► assistente (Claude ou outro cliente MCP)
                 │   conversa, explica, corrige
                 │
                 ▼  MCP (stdio)
          mcp/servidor_mcp.py
            ├── obter_schema     ──► arquivo (schema_compacto.txt) ou Neo4j
            ├── gerar_cypher     ──HTTP──►  Ollama ──► chateau-gemma4-e4b-cypher
            └── executar_cypher  ──bolt──►  Neo4j   (só consultas de leitura)
```

### Ferramentas expostas

| ferramenta | parâmetros | faz | toca o banco? |
|---|---|---|---|
| `obter_schema` | `atualizar: bool = false` | devolve o schema: o arquivo, se configurado, ou o extraído do Neo4j (em cache) | só se extrair |
| `gerar_cypher` | `pergunta: str`, `schema: str \| null` | devolve `{cypher, avisos, tokens_prompt, segundos}`; **não executa** | não |
| `executar_cypher` | `cypher: str`, `limite: int = 50` | executa só se o Neo4j classificar como leitura; devolve `{colunas, linhas, truncado}` ou `{recusada}` | lê |

As três vêm marcadas com `readOnlyHint`. O servidor também envia **instruções**
ao assistente com o fluxo recomendado: obter o schema, repassar a
pergunta como o usuário escreveu, gerar, executar, responder no idioma do usuário e corrigir a consulta se a
execução falhar.

### Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r mcp/requirements.txt
```

Sem o pacote `python3-venv` (`ensurepip is not available`) e sem `sudo` para
instalá-lo, crie o ambiente sem pip e instale-o pelo bootstrap oficial:

```bash
python3 -m venv --without-pip .venv
curl -sSo /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
.venv/bin/python /tmp/get-pip.py && rm /tmp/get-pip.py
.venv/bin/pip install -r mcp/requirements.txt
```

O `requirements.txt` pede `mcp>=2.2,<3`. **Atenção:** no SDK 2.x a classe
`FastMCP` foi renomeada para `MCPServer` e o módulo `mcp.server.fastmcp` não
existe mais. Exemplos antigos da internet não funcionam com esta versão.

### Variáveis de ambiente

| variável | padrão | uso |
|---|---|---|
| `OLLAMA_URL` | `http://127.0.0.1:11434` | onde o Ollama responde; com o túnel SSH, a ponta local dele |
| `OLLAMA_MODELO` | `chateau-gemma4-e4b-cypher` | nome registrado no `ollama create` |
| `CHATEAU_SCHEMA_ARQUIVO` | — | schema em arquivo; **tem prioridade** sobre a extração do banco |
| `CHATEAU_USUARIO` | usuário do sistema operacional | quem usa o servidor, gravado no log (seção 8) |
| `CHATEAU_LOG` | `~/.chateau-cypher/consultas.jsonl` | arquivo do log de consultas |
| `NEO4J_URI` | — | necessário para `executar_cypher` e para extrair o schema |
| `NEO4J_USER` | `neo4j` | |
| `NEO4J_PASSWORD` | vazio | |
| `NEO4J_DATABASE` | banco padrão do servidor | |

### Registrar no Claude Code

```bash
claude mcp add chateau-cypher \
  -e OLLAMA_URL=http://127.0.0.1:11434 \
  -e CHATEAU_SCHEMA_ARQUIVO="$PWD/exemplo/schema_compacto.txt" \
  -e NEO4J_URI=neo4j://127.0.0.1:7687 \
  -e NEO4J_USER=neo4j -e NEO4J_PASSWORD=troque-esta-senha \
  -- "$PWD/.venv/bin/python" "$PWD/mcp/servidor_mcp.py"
```

Depois, numa conversa: *"Quais linhas de pesquisa o programa PGC define?"* O
assistente chama `gerar_cypher` com a pergunta em português, executa e responde.

### Registrar no Claude Desktop

Copie o bloco de `mcp/claude_desktop_config.exemplo.json` para o
`claude_desktop_config.json` do Claude Desktop, trocando caminhos e senha.

### Testar sem assistente

O próprio SDK tem um cliente. Este é o teste usado para validar o pacote:

```python
import asyncio, os, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(
    command=sys.executable, args=["mcp/servidor_mcp.py"],
    env={**os.environ, "CHATEAU_SCHEMA_ARQUIVO": "exemplo/schema_compacto.txt",
         "NEO4J_URI": "neo4j://127.0.0.1:7687", "NEO4J_USER": "neo4j",
         "NEO4J_PASSWORD": "troque-esta-senha"})

async def main():
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            print([t.name for t in (await s.list_tools()).tools])
            g = await s.call_tool("gerar_cypher",
                                  {"pergunta": "Quantos artigos existem?"})
            print(g.content[0].text)

asyncio.run(main())
```

Resultado da validação: as três ferramentas listadas com `readOnlyHint`, as
instruções entregues ao cliente, uma consulta de leitura executada e um
`DETACH DELETE` recusado antes de executar, classificado pelo Neo4j como `w`.

### Se for escrever o seu próprio servidor MCP

Mantenha estas decisões, que existem por motivo:

- **Separe gerar de executar.** O assistente precisa poder mostrar a consulta
  antes de rodá-la, e corrigir sem gerar de novo.
- **Repasse a pergunta como o usuário escreveu.** Não instrua o assistente a
  traduzir: a avaliação não mostrou diferença entre português e inglês, e a
  tradução pode alterar nomes e títulos que a consulta copia literalmente.
- **Meça o schema antes de fixá-lo.** Neste domínio o compacto extraído superou o
  curado à mão (seção 7); fixe-o em arquivo para não depender de amostragem.
- **Devolva os avisos**, não os engula. O assistente decide o que fazer com eles.

---

## 6. Integração via HTTP direto

Use o endpoint **`/api/generate`** do Ollama com `system` e `prompt` separados.
É o caminho que o `Modelfile` renderiza com o template do treino e o que passou
na verificação de contrato.

### Requisição

```http
POST http://127.0.0.1:11434/api/generate
Content-Type: application/json

{
  "model": "chateau-gemma4-e4b-cypher",
  "system": "You are a Neo4j Cypher expert. Using the graph schema below, translate the user's question into a single Cypher query. Return only the query, with no explanation and no markdown fences.\n\nSchema:\n<conteúdo de exemplo/schema_compacto.txt>",
  "prompt": "How many articles are there?",
  "stream": false,
  "options": {"temperature": 0, "num_predict": 512}
}
```

### Resposta (campos que importam)

| campo | significado |
|---|---|
| `response` | a consulta Cypher |
| `done_reason` | `stop` = terminou sozinha; `length` = bateu `num_predict`, **consulta provavelmente incompleta** |
| `prompt_eval_count` | tokens do prompt. **Perto de 4.096, o início foi cortado**: a resposta não é confiável |
| `eval_count` | tokens gerados |
| `total_duration` | nanossegundos |

### Exemplos prontos

- **Shell:** `cliente/exemplo_http.sh exemplo/schema_compacto.txt "How many articles are there?"` (curl + jq)
- **Python:** `cliente/chateau_cypher.py`, função `gerar_cypher` (só biblioteca padrão; já grava o log da seção 8)
- **JavaScript** (Node 18+ ou navegador, se o Ollama aceitar a origem):

```javascript
const INSTRUCAO = "You are a Neo4j Cypher expert. Using the graph schema below, " +
  "translate the user's question into a single Cypher query. Return only the " +
  "query, with no explanation and no markdown fences.";

async function gerarCypher(pergunta, schema) {
  const r = await fetch("http://127.0.0.1:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "chateau-gemma4-e4b-cypher",
      system: `${INSTRUCAO}\n\nSchema:\n${schema}`,
      prompt: pergunta,
      stream: false,
      options: { temperature: 0, num_predict: 512 },
    }),
  });
  if (!r.ok) throw new Error(`Ollama ${r.status}: ${await r.text()}`);
  const d = await r.json();
  if (d.done_reason === "length") throw new Error("resposta incompleta");
  if (d.prompt_eval_count >= 4088) throw new Error("schema grande demais: prompt cortado");
  return d.response.trim();
}
```

Atenção ao ler o schema de um arquivo: remova a quebra de linha final. O schema
do treino não termina com ela, e `perguntar.py` e `exemplo_http.sh` já fazem isso.

### Outros endpoints

`/v1/messages` (API compatível com a Anthropic, com `system` e uma mensagem de
usuário) também funciona: foi testado com um exemplo do conjunto de teste e
gerou uma consulta equivalente ao gabarito. Prefira `/api/generate`, que é o
caminho verificado byte a byte.

---

## 7. O schema: qual enviar

O schema é a única informação que o modelo tem sobre o banco. Formato e tamanho
mudam o resultado.

### Formatos presentes no treino

| formato | exemplos | como gerar |
|---|---|---|
| **enhanced** | 52,3% | `neo4j_graphrag.schema.get_schema(is_enhanced=True)` + `ajustar_ao_treino` |
| functional_cypher (`Graph schema: Relevant node labels...`) | 32,3% | formato de uma fonte específica do corpus |
| JSON do `apoc.meta.schema` | 8,5% | |
| outros | 5,1% | inclui 0,4% com o cabeçalho `Node properties are the following:` |
| **compacto** | 1,8% | `neo4j_graphrag.schema.get_schema(is_enhanced=False)` |

### Para o banco de exemplo e o domínio acadêmico

Três schemas estão em `exemplo/`, todos descrevendo o mesmo banco:

| arquivo | tamanho | observação |
|---|---|---|
| `schema_rev5.txt` | 4.534 caracteres | **curado à mão**; explica rótulos adicionais e o rótulo-base `IntellectualProduction` |
| `schema_compacto.txt` | 7.097 caracteres | extraído; repete cada rótulo adicional como nó separado e gera padrões espúrios, como `(:Place)-[:PART_OF]->(:Place)` |
| `schema_enhanced.txt` | 20.715 caracteres | extraído; **não cabe no contexto de 4.096 tokens** |

O enhanced, formato majoritário do treino, fica grande demais aqui porque o
domínio tem muitos rótulos e cada nó carrega vários. Sobram o rev5 e o compacto.

### Qual dos dois, medido

As 20 perguntas de `exemplo/perguntas.jsonl` foram respondidas com cada schema e
executadas no banco (seção 9):

| schema | resultado igual ao gabarito | erros de fato |
|---|---|---|
| **`schema_compacto.txt`** | **15 de 20** | **1** |
| `schema_rev5.txt` | 13 de 20 | 5 |

"Erros de fato" exclui as consultas certas que só **devolvem colunas a mais**
(a comparação é estrita e conta isso como diferença; ver seção 9).

**Recomendação: use o schema compacto extraído do banco.** Com o rev5, o modelo
inventou a relação `HAS_POSTGRADUATE_PROGRAM`, trocou `startDate` de
`IS_MEMBER_OF` por `jobStartDate` (propriedade de `WORKS`), contou `AcademicWork`
em vez de `IntellectualProduction` e filtrou dissertações por
`{type: 'Dissertation'}` em vez do rótulo `:Dissertation`. Com o compacto, nenhum
desses aconteceu.

A leitura provável: o compacto lista os rótulos adicionais como nós com as
próprias propriedades e as relações por rótulo concreto — explícito e repetitivo,
o que um modelo pequeno segue melhor. O rev5 é mais enxuto e mais legível para
gente, mas pede inferência (rótulo-base, herança de relações) que este modelo
faz mal.

**Cautela:** são 20 perguntas, num banco pequeno. A diferença é de 2 acertos no
critério estrito e de 4 em erros de fato — sinal claro nesta amostra, não prova.
Antes de fixar o schema num banco real, rode `avaliacao/avaliar.py` com
perguntas do seu uso.

`obter_schema(driver)` já produz o compacto neste domínio: o enhanced passa de
7.618 caracteres e o modo `auto` cai para o compacto. O `schema_rev5.txt` continua no pacote como
especificação do domínio, e é a base do banco de exemplo.

### Extrair o schema de um banco qualquer

```python
import chateau_cypher as cc
driver = cc.conectar("neo4j://localhost:7687", "neo4j", "senha")
schema = cc.obter_schema(driver)   # formato="auto"
```

`formato="auto"` usa **enhanced** e cai para **compacto** quando o enhanced passa
de 7.618 caracteres, o maior visto no treino.

### Uma diferença de versão que a biblioteca corrige

O corpus foi gerado com uma versão antiga do `neo4j-graphrag`, que escrevia
**propriedades de relacionamento** com a crase envolvendo nome e tipo:

```
treino (95.465 de 95.465 linhas):   - `startDate: DATE` Min: ...
neo4j-graphrag 1.19.0:              - `startDate`: DATE Min: ...
```

Propriedades de **nó** saem iguais nas duas versões. `ajustar_ao_treino()` converte
a seção de relacionamentos e é chamada dentro de `obter_schema`. **Se você gerar o
schema enhanced sem a biblioteca deste pacote, aplique a mesma conversão.**

A extração foi conferida contra os bancos públicos de demonstração que aparecem
no corpus (`demo.neo4jlabs.com`): o enhanced reproduz o conteúdo do schema de
treino em 10 dos 13 bancos em que esse formato aparece; os 3 restantes mudaram
de dados desde a criação do corpus.

---

## 8. Segurança

**Nunca execute a consulta gerada sem conferir o tipo.** O modelo não tem noção
de permissão, e uma pergunta mal formulada ou maliciosa pode virar `DELETE`.

`executar_somente_leitura()` aplica **duas travas independentes**:

1. **`EXPLAIN` antes de executar.** O Neo4j planeja a consulta sem rodá-la e
   informa o tipo (`r`, `rw`, `w`, `s`). Só `r` passa. Isso é mais confiável que
   procurar `CREATE` ou `DELETE` no texto, que falha com `CALL`, procedimentos e
   subconsultas.
2. **Transação de leitura** (`execute_read`), que o próprio servidor faz valer.

Testado: `CREATE` foi classificado como `rw` e `DETACH DELETE` como `w`, e os dois
foram recusados antes de executar.

Também aplicadas: **timeout por transação** (30 s por padrão) e **limite de
linhas** (50 no MCP, no máximo 500).

Recomendações para produção:

- Conecte com um **usuário do Neo4j só com permissão de leitura**. As travas acima
  são defesa em profundidade, não substituem o controle de acesso do banco.
- **Dados pessoais.** Um banco acadêmico real tem e-mails, identificadores Lattes
  e ORCID. O Ollama roda num servidor próprio, acessível só pelo túnel SSH;
  mantenha-o assim — não exponha a porta 11434 na rede — e não use servidores
  de terceiros para executar as consultas.

### Log de consultas

Toda chamada a `gerar_cypher` grava uma linha JSON no log — pelo MCP, pela linha
de comando ou por uma interface que importe `chateau_cypher.py`:

```json
{"quando": "2026-09-21T15:17:47-03:00", "usuario": "maria", "idioma": "pt",
 "pergunta": "Quantos artigos existem?", "cypher": "MATCH (a:Article) RETURN count(a)",
 "modelo": "chateau-gemma4-e4b-cypher", "schema_sha256": "f9dc0f482c2eae3a",
 "avisos": [], "tokens_prompt": 1200, "segundos": 0.7}
```

| campo | conteúdo |
|---|---|
| `quando` | data e hora locais, com fuso |
| `usuario` | quem perguntou (ver abaixo) |
| `idioma` | `pt`, `en` ou `indefinido`, detectado por palavras e acentos típicos |
| `pergunta` | o texto exatamente como foi enviado ao modelo |
| `cypher` | a consulta gerada; `null` se a geração falhou |
| `erro` | só quando a geração falhou (Ollama fora do ar, modelo ausente…) |
| `modelo`, `schema_sha256` | qual modelo e qual schema — o hash distingue versões do schema sem gravá-lo inteiro |
| `avisos`, `tokens_prompt`, `segundos` | os mesmos de `gerar_cypher` |

**Arquivo:** `~/.chateau-cypher/consultas.jsonl`, ou o que estiver em
`CHATEAU_LOG`. Uma linha por pergunta, só acrescentada, nunca reescrita. Falha
ao gravar gera um aviso e não interrompe a consulta.

**Quem é o usuário**, em ordem de prioridade:

1. o parâmetro `usuario=` de `gerar_cypher` — **numa interface com login, passe
   o usuário autenticado**;
2. a variável `CHATEAU_USUARIO`;
3. o usuário do sistema operacional.

No MCP, o servidor roda um processo por pessoa, então vale o item 2 ou 3. Na linha
de comando, `perguntar.py --usuario`.

**Fora do log:** `avaliacao/avaliar.py` não grava (`registrar=False`), para que
rodadas de avaliação não se misturem com uso real. Integrações **HTTP direto**
não passam pela biblioteca; se precisar do log, grave os mesmos campos na sua
interface.

**Cuidado:** o log identifica pessoas e guarda o que perguntaram. Trate-o como
dado pessoal: acesso restrito, prazo de retenção definido.

O log é também o material da próxima versão do modelo: pergunta real, consulta
gerada e, se você registrar à parte, a correção feita pelo assistente ou pelo
usuário.

---

## 9. Qualidade e avaliação

### O que as métricas de treino dizem, e o que não dizem

Perda no checkpoint final, no conjunto de teste do corpus (entropia cruzada por
token da resposta, 400 exemplos por conjunto):

| conjunto | perda | probabilidade média do token certo |
|---|---|---|
| validação | 0,0466 | 95,4% |
| **generalização** (bancos e perguntas não vistos) | **0,0836** | **92,0%** |
| memorização (sonda contida no treino) | 0,0842 | 91,9% |

**Perda baixa não é acurácia.** Uma consulta com um único token errado — trocar
uma propriedade por outra, inverter o sentido da relação — é outra consulta, e a
perda quase não muda. E essas perdas são do **corpus geral**, não do domínio
acadêmico. O que interessa a quem usa é se a consulta **devolve o resultado
certo no banco de destino**.

### Avaliação no banco de exemplo

`exemplo/perguntas.jsonl` tem 20 perguntas — 5 fáceis, 9 médias, 6 difíceis —
com gabarito **executado e validado** no banco e o resultado esperado gravado.

```bash
.venv/bin/pip install neo4j
.venv/bin/python avaliacao/avaliar.py \
  --exemplos exemplo/perguntas.jsonl \
  --schema-arquivo exemplo/schema_compacto.txt \
  --neo4j-uri neo4j://127.0.0.1:7687 --neo4j-senha troque-esta-senha \
  --saida resultados.jsonl
```

Gabarito e consulta gerada rodam no mesmo banco, e os resultados são comparados
**sem olhar nome de coluna nem ordem das linhas**: `count(a) AS total` e
`count(*) AS n` com o mesmo valor contam como acerto. A comparação foi validada
com 20 reescritas equivalentes (20 de 20 reconhecidas) e com uma consulta errada
(detectada).

### Resultado no banco de exemplo

Medido em 17/09/2026 numa RTX 4090, Ollama 0.32.9, `temperature: 0`.

| schema | fáceis (5) | médias (9) | difíceis (6) | total |
|---|---|---|---|---|
| **compacto** | 4 | 6 | 5 | **15 / 20** |
| rev5 | 4 | 7 | 2 | 13 / 20 |

Nenhuma consulta saiu **textualmente** igual ao gabarito, nas duas rodadas — o que
mostra por que a comparação é por resultado.

Cada divergência, lida uma a uma:

| # | pergunta | compacto | rev5 |
|---|---|---|---|
| 4 | dissertações publicadas | certa, com coluna a mais (`datePublished`) | **errada**: `AcademicWork {type: 'Dissertation'}`, 0 linhas |
| 7 | linhas de pesquisa do PGC | certa, com coluna a mais (`description`) | igual ao compacto |
| 10 | locais de trabalho do Campus Centro | certa, com coluna a mais (`email`) | igual ao gabarito |
| 14 | quem ministrou "Banco de Dados" | **errada**: pula `CourseInstance` e liga `TAUGHT` direto a `Course`, 0 linhas | **mesmo erro** |
| 15 | produções intelectuais de Ana Ribeiro | igual ao gabarito | **errada**: conta `AcademicWork`, 0 em vez de 6 |
| 16 | membros de um projeto e data de entrada | igual ao gabarito | **errada**: lê `jobStartDate`, datas nulas |
| 19 | discentes com papel encerrado antes de 2025 | certa, devolve os nós inteiros | certa, com colunas a mais |
| 20 | programas das unidades do Campus Norte | igual ao gabarito | **errada**: inventa `HAS_POSTGRADUATE_PROGRAM`, 0 linhas |

O que isso ensina para a interface:

- **Colunas a mais são o desvio mais comum** (6 das 12 divergências). Não é erro para o
  usuário, mas atrapalha quem espera um formato fixo de saída: especifique as
  colunas na pergunta ("return only the name") ou ajuste o resultado depois.
- **Resultado vazio, zerado ou nulo é o sintoma dos erros de fato** (6 de 6:
  zero linhas, contagem 0, datas nulas). Uma
  interface deve tratar zero linhas como suspeita, não como resposta: mostrar a
  consulta, ou, no MCP, deixar o assistente conferir o schema e tentar de novo.
- **Caminho com nó intermediário** (`Person → CourseInstance → Course`) falhou
  com os dois schemas. É o ponto fraco a observar em perguntas reais.

### Avaliação no corpus geral

`avaliacao/exemplos.jsonl` tem 63 exemplos do conjunto de teste do corpus, com
execução no servidor público `demo.neo4jlabs.com`:

```bash
.venv/bin/python avaliacao/avaliar.py --executar-demo --n 20 --saida resultados-corpus.jsonl
```

---

## 10. Desempenho e hardware

| | |
|---|---|
| Tamanho do GGUF | 5,0 GiB (`q4_k_m`) |
| Memória em uso | 6,0 GB (medido no `ollama ps`, contexto de 4.096) |
| Contexto | 4.096 tokens |

| | GPU (RTX 4090) | CPU (4 núcleos, 7 GB de RAM) |
|---|---|---|
| Primeira chamada, com carga do modelo | 6,0 s | — |
| Por pergunta, modelo carregado | 0,5 a 1,0 s (mediana 0,7 s) | não concluiu a primeira pergunta em 9 minutos |
| VRAM | 3,2 GB | — |
| Prompt com `schema_rev5.txt` | 1.260 tokens | |

Medido com Ollama 0.32.9 e as 20 perguntas do banco de exemplo. A máquina de CPU
tinha menos RAM livre que os 6,0 GB do modelo, e o sistema passou a paginar: o
número não vale para CPU em geral, mas mostra que **o modelo precisa caber inteiro
na memória**. Para uma interface interativa, use GPU: é o caso do Ollama do
servidor, acessado pelo túnel SSH (seção 3).

O Ollama mantém o modelo carregado por alguns minutos após a última chamada. Numa
interface, faça uma chamada de aquecimento na inicialização, ou ajuste
`keep_alive` na requisição, para o usuário não pagar o carregamento.

---

## 11. Solução de problemas

| sintoma | causa provável | o que fazer |
|---|---|---|
| `Ollama nao responde em http://127.0.0.1:11434` | túnel SSH fechado, ou em outra porta local | reabrir o túnel; conferir `OLLAMA_URL` (seção 3) |
| `unable to load model` | Ollama antigo, sem suporte a `gemma4` | atualizar para 0.32.9+ |
| `model "chateau-gemma4-e4b-cypher" not found` | modelo não registrado | `cd modelo && ollama create chateau-gemma4-e4b-cypher -f Modelfile` |
| resposta com texto além da consulta | template alterado ou `raw: true` sem o prompt completo | recriar o modelo a partir do `Modelfile` original |
| consulta usa rótulos ou relações que não existem | schema ausente, em outro formato, ou que exige inferência | seção 7; teste o compacto |
| consulta executa e devolve zero linhas | erro de caminho ou propriedade (seção 9) | mostrar a consulta; no MCP, o assistente confere e corrige |
| aviso "o prompt ocupou 4.096 tokens" | schema grande demais | usar o schema compacto, ou enviar só a parte relevante |
| `There is no procedure with the name apoc.meta.data` | APOC ausente | instalar o APOC Core, ou usar schema em arquivo |
| `ModuleNotFoundError: mcp.server.fastmcp` | exemplo escrito para o SDK 1.x | usar `from mcp.server.mcpserver import MCPServer` |
| `Illegal instruction (core dumped)` ao importar `neo4j`, `numpy` ou `scipy` | CPU sem SSE4.2 (`grep -c sse4_2 /proc/cpuinfo` dá 0) e `numpy` 2.4 ou mais novo | `.venv/bin/pip install "numpy<2.4"`; o `requirements.txt` já fixa isso |
| `ensurepip is not available` ao criar o `.venv` | falta o pacote `python3-venv` do sistema | instalá-lo, ou criar sem pip (seção 5, Instalação) |
| `remote port forwarding failed for listen port 11434` | túnel reverso anterior ainda preso na porta, ou porta fora do `permitlisten` | aguardar ~10 s e repetir; conferir a restrição no `authorized_keys` (seção 3) |
| `TypeError: Query object is only supported for session.run` | `Query(timeout=...)` dentro de transação | usar `@neo4j.unit_of_work(timeout=...)`, como em `chateau_cypher.py` |
