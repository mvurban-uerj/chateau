# Quarkus como orquestração padrão — 28/10/2026

Marcelo decidiu usar Quarkus como `orchestration` padrão e preservar Python
como implementação paralela para comparação e eventual retorno. O contrato
HTTP `POST /search` permanece o mesmo; a API continua chamando
`http://orchestration:8000` quando há modelo disponível selecionado.

Esclarecimento de 28/10/2026: no fluxo explicado ao usuário, o servidor do
modelo de IA é uma caixa preta. Sabemos o que a orquestração envia e o que
recebe; caminhos HTTP e nomes de tecnologias servem para documentar o cliente
implementado, sem afirmar como o servidor processa a solicitação. A configuração
real da máquina com GPU segue pendente de validação.

## Implementação nos Compose

- Local, perfil `ia`: `orchestration` usa `quarkus/Dockerfile`, schema compacto
  do banco de exemplo e `CHATEAU_GERADOR=generate`. O Python pode subir junto
  pelo perfil `ia-python`, na porta local 8001 e com log separado.
- Produção: `orchestration` usa `quarkus/Dockerfile`, schema de produção e
  `CHATEAU_GERADOR=generate`. O Python fica no perfil `comparacao`, sem porta
  pública, aquecimento desativado e log separado. Ele não recebe tráfego da API
  por padrão. Isso evita carregar duas vezes o modelo na GPU.
- Para retorno operacional, subir `orchestration-python` e apontar
  `ORCHESTRATION_URL=http://orchestration-python:8000` na API. A configuração
  da API deve ser reaplicada. Voltar a apontar para `orchestration:8000` devolve
  o tráfego ao Quarkus. Nenhum retorno foi executado em produção nesta análise.

## Comparação executada

Em 28/10/2026, `bash orchestration/comparacao/rodar_comparacao.sh` rodou com
um servidor simulado do modelo de IA (`roteiro_falso.json`), Neo4j local carregado do consolidado do
Data `data/out/20260928-132724`, e o mesmo `schema_producao.txt` nas três
instâncias. As 30 perguntas cobriram resultados, serialização de tipos,
recusas, erros do banco/modelo e avisos. Python foi a referência; Quarkus
`generate` e Quarkus `langchain4j` produziram **60/60 pares sem diferença** no
contrato comparado, com o mesmo texto de prompt enviado ao servidor simulado.

Relatório local gerado em
`chateau-expert/orchestration/comparacao/resultados/20261028-095646/paridade/relatorio.md`
(fora do Git). O relatório registra campos extras e retentativas do caminho
LangChain4j; por isso o padrão continua sendo `generate`.

O teste com servidor simulado verifica equivalência do contrato e do processamento.
**Ainda falta** comparar com o modelo real na GPU, validar a URL do modelo e
confirmar o serviço Quarkus após o próximo deploy. A configuração de produção
foi verificada estaticamente no Compose; `.env.prod` não existe neste checkout
local e não houve deploy nesta tarefa.

Foi tentado também `BuscaTest` do Quarkus em Maven dentro de container. O
Testcontainers iniciou o Neo4j, mas o container Maven não alcançou a porta
publicada pelo Docker Desktop (`127.0.0.1:52021`); no host ela respondeu HTTP
200. O teste foi encerrado nesse ponto e os containers temporários foram
removidos. O contrato dinâmico `modelo`/`ollama_url` tem teste versionado, mas
essa execução não o validou neste ambiente.
