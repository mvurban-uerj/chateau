# TODO — frentes de trabalho

Tarefas e agenda do projeto. As frentes andam em paralelo; cada uma lista o que falta, de quem depende e onde está o detalhe. Ao concluir uma tarefa, marcar `[x]` com a data; ao descobrir trabalho novo, incluir na frente certa. Decisões vão para `docs/analises/` ou `docs/reunioes/` e regras confirmadas para [dominio/](../dominio/indice.md).

Legenda: **(dep: X)** = depende de outra tarefa ou pessoa.

## Agenda

| Data | O quê | Frente |
|---|---|---|
| 20/10 | ~~Edson deve mandar o Figma da identidade visual~~ recebido e lido ([análise](analises/figma-2026-10-20.md)) | Identidade visual |
| — | Teste do modelo com GPU previsto para 30/09–02/10: resultado não registrado aqui; confirmar se aconteceu | IA e orquestração |

## 1. Nova UI — port do protótipo

Decisões de 20/10/2026: [análise da UI](analises/ui-prototipo-2026-10-20.md#decisões-de-20102026). Aparência idêntica ao protótipo (`/mnt/c/temp/chateau/ui`, versão final, não versionada); infraestrutura e versões do Expert prevalecem (Next.js 14, React 18). O port entrou em `main` em 22/10; o levantamento abaixo ainda reúne conferências e decisões para as próximas integrações.

- [x] Reunião de 29/10 e pedidos de 03/11: portar o `public/favicon.svg` do protótipo para o web e centralizar o texto "Acesso com conta institucional." sob o botão na tela de entrada (03/11). Conferência em produção pendente de deploy.

Escopo pela [reunião de 20/10](reunioes/2026-10-20.md): portar toda a interface, menos os desdobramentos de "Buscar candidatos" e "Montar equipe" (botões desabilitados). O que não tem dado ou o modelo não responde fica simulado; o que dá para implementar (ex.: contexto no PostgreSQL) já se implementa. O protótipo não evolui em paralelo.

Contexto consolidado para o port (22/10): [nova-ui/README.md](nova-ui/README.md), com escopo, mapa protótipo → web, tabelas propostas e ordem sugerida. Plano de execução em [nova-ui/plano.md](nova-ui/plano.md) (22/10).

Levantamento e conferências. O Figma é espelho do protótipo e a página 08 Handoff traz mapa de arquivos, contrato com o grafo e interruptores: ver [análise do Figma](analises/figma-2026-10-20.md).

- [ ] Confirmar com o Edson que a cópia em `/mnt/c/temp/chateau/ui` corresponde ao commit `3cf7be7` (ou posterior) do repositório local dele, que o Figma espelha.
- [x] Consentimento × termo de uso: respondido na [reunião de 20/10](reunioes/2026-10-20.md) (20/10).
- [x] **Remover o termo de uso por completo e criar a autorização de contexto** (feito na fase 3, `9bf9aaf`) (nome, unidade, e-mail, campus etc. + cookies) no PostgreSQL: apagar `Term`, `Account.acceptedTermId`, `/terms`, `/termos-uso`, `/api/accept-terms`, admin de termos e a exigência na API e no middleware, sem guardar aceites (fase 3 do [plano](nova-ui/plano.md#7-fases)). Falta definir o que cada escolha opcional controla.
- [ ] **Busca por etapas, Parar e Retomar reais:** adiados ([reunião de 20/10](reunioes/2026-10-20.md)): o modelo ainda só recebe pergunta e devolve resposta. O port já mostra espera genérica e Parar avisa "em desenvolvimento". **(dep: Edson, quando o modelo informar etapas)**
- [ ] Níveis de busca: nomes e existência no modelo. **(dep: Edson; não respondido na [reunião de 20/10](reunioes/2026-10-20.md))**
- [x] Chat livre: continua indo ao modelo; profissionais da resposta viram cartões, campos fora do grafo em vermelho com dado falso; modelo fora → simulação com aviso "Modelo fora do ar — dados simulados" (decidido pelo Marcelo em 22/10, [regra](nova-ui/README.md#chat-livre--cartões-decidido-em-22102026)).
- [x] Implementar a regra do chat livre: detector de linhas de pessoa e construtor de cartões no web; gerador determinístico de dado falso; campo `simulado` no `SearchResult` e no histórico; mock do backend marcado como simulado quando o modelo está fora. (fase 4, `e4b19a5`)
- [x] **Contexto do usuário no PostgreSQL** (fase 6, `a96b322`), ligado à conta Google: filtros, interesses, instruções e demais itens; disponibilidade com padrão "disponível". Ainda não entra no envio da pesquisa.
- [x] **Perguntas guiadas:** geradas do grafo rev_6 e gravadas no PostgreSQL; modal aberto pelo Tab (fase 7, `774286f`). Ainda perguntar ao Edson se o admin poderá editá-las (hoje uma nova versão gerada regrava o banco).
- [ ] **Opções de filtro reais:** as atuais são simuladas num provedor isolado (`web/src/lib/chateau/filtros.ts` e `opcoes.ts`, fase 8 feita). A reunião de 20/10 levantou Cypher direto ou cópia no PostgreSQL com cron, mas nenhuma alternativa foi aprovada; web/backend seguem sem acesso ao Neo4j. Definir fonte e contrato com o Edson.
- [x] Decisões do plano (22/10): branch `feat/nova-ui` até fechar; Parar visível avisando "em desenvolvimento"; admin redesenhado com os primitivos novos; perguntas guiadas geradas por script ([plano](nova-ui/plano.md#10-decisões)). A revisão crítica das perguntas continua pendente com o Edson.
- [x] Termo de uso sai por completo, sem guardar aceites; backend sem acesso ao Neo4j, o que o modelo não trouxer fica simulado (decidido em 22/10; [domínio](../dominio/negocio/termos-e-privacidade.md) atualizado).
- [x] Ajustar nosso código: acesso à administração pela nova sidebar; tema único claro; histórico com Desfazer por 6 s e rota por conversa (`chateau-expert` `842cd96` e `43a25d1`, 22/10).
- [x] Inventário tela a tela e dos componentes principais do protótipo → rotas/componentes no `chateau-expert/web`, com dependências de dados e backend ([análise](analises/ui-telas-portadas-2026-10-27.md), 27/10). Comparação visual em produção segue pendente.
- [ ] Compatibilidade técnica ([versões](duvidas-edson/README.md#4-versões-do-protótipo--projeto)): dependências do protótipo (`motion` 13, `@phosphor-icons/react`, `@radix-ui/react-slider`, fontes Geist) aceitam React 18 e o código não usa APIs exclusivas do React 19 (verificado em 20/10). Falta: conferir Tailwind 4 do protótipo × configuração do web (tokens, `index.css`), coexistência com shadcn/lucide já usados no web, e o aviso de bundle > 500 kB.
- [x] Mapear os campos exibidos (cartão, gaveta, comparação, cobertura e equipe) para nó/propriedade/aresta da rev_6 e para o construtor atual do web ([análise](analises/ui-campos-rev6-2026-10-27.md), 27/10). O mapa é estático; não comprova dados carregados.
- [ ] Conferir no Neo4j de produção quais caminhos e valores estão carregados e comparar exemplos reais de resposta do modelo ao mapa. **(dep: frente 2, carga rev_6, e teste do modelo)**
- [ ] Mapear fluxos do protótipo para os contratos do Expert:
  - login demonstrativo → Google/NextAuth; `/pending` e regras de [acesso](../dominio/negocio/acesso.md);
  - tela de consentimento → autorização de contexto no PostgreSQL, sem termo de uso (decidido na reunião de 20/10);
  - histórico em `localStorage` → `/api/chats` (formato `__SEARCH__:` precisa acomodar o novo resultado);
  - contexto do usuário → PostgreSQL, ligado à conta Google (decidido na reunião de 20/10; antes `localStorage`);
  - links de termos/privacidade → páginas existentes (`/termos-uso`, `/privacidade`);
  - área administrativa: não existe no protótipo; definir como fica visualmente.
- [ ] Listar os campos e controles que ficam com dado simulado (ex.: aderência, que o modelo ainda não responde), os que ficam visíveis sem efeito (ex.: seletor de modelo, níveis de profundidade até haver suporte) e os que o `features.ts` já esconde.
- [ ] Estados vazios, erro, recusa e indisponibilidade: mapear os 5 status atuais da busca para telas do protótipo (`recusada` não tem tela no desenho; definir no nosso código).
- [ ] Port responsivo: o desenho tem telas de celular (390 px).

Execução no branch `feat/nova-ui` do `chateau-expert` ([plano](nova-ui/plano.md#7-fases)):

- [x] Fase 0 — fundação: tokens, fontes, `motion` enxuto, i18n (`next-intl`, pt-BR), interruptores, lint contra texto literal, Vitest e job `web-test` no deploy (`7093d86`, 22/10).
- [x] Fase 1 — primitivos com os nomes do Figma e catálogo em `/catalogo` (só em desenvolvimento); 37 testes (`e47cf4d`, 22/10).
- [x] Fase 2 — casca: route groups, Shell, Sidebar, `/chat/[id]`, histórico pela API com Desfazer; 59 testes (`842cd96`, 22/10). Logout ainda não existe na casca nova (entra com Meu contexto, fase 6).
- [x] Fase 3 — entrada nova, pendente e restrito; autorização de contexto (backend + tela) e remoção completa do termo de uso; 75 testes no web e 60 no backend (`9bf9aaf`, 22/10).
- [x] Fase 4 — campo de busca e chat livre: cartões com campos simulados em vermelho, tabela, avisos dos status e do modelo fora; backend devolve `simulado`; 99 testes no web e 63 no backend (`e4b19a5`, 22/10).
- [x] Fase 5 — gaveta de perfil, comparação, barra de seleção e "Quero os currículos" (salvo na conversa); contato e currículo simulados sem link; 105 testes (`fbf9995`, 22/10).
- [x] Fase 6 — Meu contexto no PostgreSQL (perfil, objetivo, disponibilidade, interesses, instruções e filtros), revogar autorização e sair; 119 testes no web e 69 no backend (`a96b322`, 22/10).
- [x] Fase 7 — perguntas guiadas geradas do rev_6 (sem revisão do Marcelo; a crítica fica com o Edson), carregadas pela seed; molde no campo de busca e modal de perguntas no Tab; 136 testes no web e 73 no backend (`774286f`, 22/10).
- [x] Fase 8 — painel de filtros por tag no campo de busca; opções institucionais simuladas num provedor isolado; tags vão ao modelo na pergunta em linguagem natural; 145 testes (`89731c6`, 22/10).
- [x] Fase 9 — admin e privacidade na nova UI; retirada da interface antiga e das dependências sem uso; axe sem violações em 13 telas; lint limpo; 153 testes no web e 73 no backend (`43a25d1`, 22/10). Peso por página entre 196 e 230 kB comprimidos (React/Next ~165 kB; motion + Radix ~74 kB); carregar o motion à parte não reduziu nada.
- [x] Merge de `feat/nova-ui` em `main` (fast-forward até `43a25d1`, 22/10), confirmado pelo Marcelo; dispara o deploy.
- [x] Ajuste solicitado em 26/10: dados simulados em vermelho também nas opções, respostas mock e barra da aderência; seletor visual de complexidade alimentado pelo catálogo do admin, com subtítulo próprio. A escolha ainda não altera a busca. Publicado em `main` do Expert (`acd2f6d`, `af63b9b`); validação em produção pendente.
- [x] Validar em produção entrada com Google e autorização de contexto, incluindo persistência das escolhas: usuário confirmou todos os passos do roteiro em 27/10/2026.
- [x] Validar em produção resposta da busca e persistência da conversa no histórico: usuário confirmou ambos em 27/10/2026.
- [x] Confirmar o deploy do commit `chateau-expert` `dc77c53`: captura em `C:\temp\Captura de tela 2026-10-27 104557.png` mostra o Deploy #26 concluído com sucesso em 21 min 39 s; página pública respondeu HTTP 200 (27/10/2026).
- [x] Conferir em produção a correção visual da rolagem do chat/sidebar e da transição após a primeira busca: usuário confirmou que os dois problemas foram resolvidos em 27/10/2026.
- [ ] Validar em produção Meu contexto, admin e privacidade. Confirmar também se a busca usa o modelo selecionado ou a simulação; a presença do container de orquestração não comprova que haja modelo disponível.
- [x] Issue #34: implementar cadastro com Nome, Descrição, Nome do modelo, URL, Versão e Disponível; mostrar só disponíveis no chat, ocultar seletor com um, e enviar o nome técnico escolhido na busca ([análise](analises/modelos-admin-2026-10-27.md), 27/10). Migração e testes direcionados passaram; Expert `bc6f16a` publicado no Git, validação em produção pendente.
- [ ] Validar a issue #34 com a GPU real e a URL alcançável pelo container após o deploy; confirmar também o contrato dinâmico Quarkus quando o ambiente Testcontainers permitir.
- [x] 29/10: ajustar o Expert para permitir o mesmo nome técnico nas versões do catálogo e resolver a URL da busca pelo ID da versão escolhida. Migração, API, chat e testes direcionados concluídos; Expert `8000529` enviado a `main`. Deploy e busca real pendentes de validação. [Diagnóstico](analises/modelos-admin-2026-10-29.md).
- [x] Após publicação do ajuste de 29/10: cadastrar na versão Pro a URL `http://host.docker.internal:11435`, marcar Disponível e validar uma busca real. O usuário confirmou HTTP 200 em `/api/tags` nessa porta dentro de `chateau_orchestration`; `:11434` falha. Logs anteriores mostram tentativas em `http://127.0.0.1:11434`. SSH ao servidor recusou autenticação neste ambiente. Substituído em 05/11 pela porta `11434` (item abaixo).
- [x] 05/11: unificar a porta da ponte em `11434` para não confundir com a porta do modelo. Viabilidade verificada no servidor (`docs/talk-ia.md`): só `127.0.0.1:11434` (túnel) ocupava a porta; ponte de teste em `172.17.0.1:11434` devolveu HTTP 200 a `chateau_orchestration`. O usuário informou ter criado `chateau_ollama_ponte_11434` e concluído a troca da URL no Admin para `http://host.docker.internal:11434` (sem saída anexada). `testar_modelo.sh` e documentação ajustados para a nova ponte. A `127.0.0.1:11436` (túnel do 31b) segue sem ponte.
- [ ] Confirmar no servidor que `chateau_ollama_ponte` (11435) foi removida e que `ss -ltn` mostra `172.17.0.1:11434`; validar uma busca real pela nova URL.
- [x] 04/11: permitir várias URLs ordenadas por cadastro no Admin, com inclusão, edição e remoção; migração copia a URL única. A primeira é a tentativa inicial, e remover a última exige desmarcar Disponível. Publicado em `chateau-expert/main` (`e52bd79`); deploy e validação em produção pendentes. O envio da lista à orquestração foi concluído na frente 3.
- [x] 04/11: corrigir a rolagem do modal de URLs e o botão Salvar com linha vazia; retirar o formato de prompt do Admin e selecionar o formato pelo nome técnico no código. Validar em produção após deploy.
- [x] 04/11: restringir a rolagem à lista de URLs, mantendo o restante do modal visível; informar especificamente URLs duplicadas na tela e na API. Testes dirigidos locais concluídos; validação visual em produção pendente.
- [x] 04/11: permitir reordenar URLs no Admin arrastando a alça ou usando as setas do teclado; a ordem editada é enviada ao salvar. Testes dirigidos e verificação de tipos passaram; validação visual em produção pendente.
- [x] 28/10: distinguir no chat a falha sem modelo disponível (orientação para tentar mais tarde) da falha de serviço com modelo escolhido; textos da interface no catálogo de traduções. Validar após o próximo deploy.
- [x] 28/10: retirar a exceção de i18n do catálogo de componentes, mover seus textos de tela para `web/messages/pt-BR.json` e ampliar o lint para atributos visíveis. Verificação estática do JSX e lint do web passaram.
- [x] Deploy após aumentar o limite do passo SSH de 30 para 60 min: o run de 26/10/2026 terminou com `Deploy finalizado` e os containers foram iniciados (`docs/talk-ia.md`). A validação dos fluxos da UI continua pendente acima.
- [ ] Revisão jurídica da página de privacidade: linha nova "Meu contexto" e textos de exportação e exclusão (22/10).
- [ ] Levar ao Edson: como os filtros devem chegar ao modelo (hoje vão na pergunta em linguagem natural, porque a busca só recebe texto). **(dep: Edson)**
- [x] Revisar internamente as perguntas guiadas geradas e o comportamento do Tab; exemplos e limites registrados na [análise de 27/10](analises/perguntas-guiadas-2026-10-27.md).
- [ ] Levar ao Edson os exemplos da análise: opções fixas × dados reais, disponibilidade fora do grafo acadêmico, requisitos obrigatórios sem ranqueamento, molde de equipe acessível pelo campo e preservação de edições na seed. **(dep: Edson)**

Depois do levantamento:

- [x] Plano de port por etapas, com dados reais, simulados e recursos escondidos ([plano](nova-ui/plano.md), 22/10).
- [x] Port dos componentes para `main` do Expert (`43a25d1`, 22/10); validação integrada em produção continua pendente acima.

### Próximos itens que já podem avançar

- [ ] Validar os fluxos restantes da UI em produção. Os deploys do Expert `6545a07` e `dc77c53` e as medidas do servidor ocioso estão na [análise do deploy](analises/deploy-2026-10-26.md); conta administradora e conferência visual autenticada ainda são necessárias.
- [ ] Fechar o inventário tela a tela da UI portada e completar o [mapa campo a campo](analises/ui-campos-rev6-2026-10-27.md) com dados do Neo4j de produção e respostas reais do modelo, após a carga rev_6.
- [ ] Levar ao Edson a [revisão das perguntas guiadas e do Tab](analises/perguntas-guiadas-2026-10-27.md), incluindo decisão sobre edição administrativa e atualização da seed.
- [x] Atualizar o diagrama web–API e sinalizar `nova-ui/README.md` e `plano.md` como registros anteriores ao port, com resumo do código entregue e retirada do termo de uso (27/10; frente 6).

## 2. Dados — `chateau-data` (rev_6)

- [x] 03/11: alinhar tipos do Cypher gerado ao rev_6: ano isolado de produção → `publicationYear` inteiro; datas completas normalizadas e emitidas como `date(...)`; carga horária inteira. Execução local gerou `data/out/20261103-114032` (não versionado); validação dirigida e de coautoria passou. Cypher carregado em produção em 03/11, após dumps de `neo4j` e `system`; consulta retornou 488 nós e 603 relações de domínio, 333 anos de artigo como `INTEGER` e 78 inícios de projeto como `DATE`.
- [ ] Decidir fontes e tratamento dos campos marcados `NOT NULL`/`IS KEY` no rev_6 sem valor nos dados extraídos (por exemplo, `Article.abstract`, `Article.keywords` e `ResearchProject.description`); não preencher com dados inventados.
- [x] 04/11: comparar integralmente o JSON rev_6 com o esquema fornecido ao modelo `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` pelo cliente em `C:\temp`: nomes, tipos básicos, rótulos e direções coincidem; o esquema fornecido omite 19 `IS KEY` e 48 `NOT NULL` do JSON. Tamanhos máximos não são declarados. [Quadro e script](comparacoes/rev6-x-prompt-31b-2026-11-04.md).
- [ ] Decidir se as 67 marcações `IS KEY`/`NOT NULL` devem ser incluídas no prompt do 31B ou permanecer apenas no JSON e na validação/carga; confirmar com quem mantém o modelo treinado antes de alterar o formato do prompt.
- [x] 04/11: comparar o JSON rev_6 com o Cypher gerado em 03/11; 488 nós e 603 relações correspondem exatamente ao `domain.json`, sem campo com nome/tipo fora do modelo nem relação invertida. Rótulos, campos e padrões sem instâncias refletem apenas cobertura dos dados capturados. O Cypher gera 19 `IS UNIQUE` para as chaves do JSON, sem impor existência/`NOT NULL`. [Resultado](comparacoes/rev6-x-cypher-2026-11-04.md).
- [x] 04/11: comparar diretamente o Cypher gerado com o esquema do modelo `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` em `C:\temp`: zero rótulos, nomes, tipos ou relações divergentes na camada de domínio gerada. [Tabela](comparacoes/cypher-x-modelo-31b-2026-11-04.md).
- [x] 04/11: comparar o inventário do Neo4j de produção em `talk-ia.md` com o Cypher gerado em 03/11: 488 nós e 603 relações de domínio, rótulos, campos, tipos e padrões dirigidos com **0 diferenças**; 21 constraints esperadas presentes. [Resultado e limites](comparacoes/cypher-x-neo4j-2026-11-04.md).
- [ ] Comparar exemplos de consultas geradas pelo modelo 31B com o grafo de produção e registrar diferenças de resposta; o inventário estrutural não testa o comportamento do modelo.
- [x] **(Marcelo)** Gerar o Cypher completo no modelo `rev_6_training` e carregar no Neo4j de produção. Carga anterior substituída em 03/11 após backup offline; contagens e tipos conferidos. Ver [Neo4j](neo4j/README.md) e a issue citada na [reunião de 23/09](reunioes/2026-09-23.md).
- [ ] Corrigir o extrator de produções do PDF Sucupira (teste falha em 20 PDFs) e repetir o teste. Ver [fontes e pipeline](../dominio/dados/fontes-e-pipeline.md).
- [ ] Fontes para os campos novos da UI (cargo/vínculo, unidade, campus, disciplinas, prêmios, coordenação): identificar de onde cada um é extraído. **(dep: levantamento campo a campo da frente 1)**
- [ ] Atividade 16: baixar dados do S-Ticket da Cotplan (Marcelo e Geraldo) para o grafo rev_6 (reunião de 19/10).
- [ ] Verificar no Sucupira novas formas de baixar dados (reunião de 19/10).
- [ ] Decidir datas da oferta de `ShortCourseInstance` no extrator Lattes (pendência da investigação rev_5; conferir se ainda vale na rev_6).

## 3. IA e orquestração

- [x] 04/11: implementar failover sequencial entre URLs do mesmo cadastro em Quarkus e Python para conexão recusada, HTTP 503 ou resposta técnica vazia; API envia a lista ordenada. Testes simulados dirigidos passaram. [Decisão e limites](analises/failover-modelo-2026-11-04.md).
- [x] 04/11: ampliar o log de buscas para registrar cada chamada ao modelo, inclusive com URL única e falha, com início, duração, desfecho e tokens disponíveis. Implementação local em Quarkus e Python; 21 e 29 testes dirigidos passaram, respectivamente. [Decisão de medição](analises/medicao-latencia-modelo-2026-11-04.md).
- [ ] Após acumular buscas reais, gerar relatório agregado por URL e modelo (mediana, percentis 90/95 e taxa de falha/timeout), separar respostas concluídas de timeouts e definir com Edson o limiar de lentidão. Ainda não há dados reais nesta sessão.
- [ ] Validar o failover com servidores/túneis reais e definir com Edson saúde, capacidade, distribuição normal de carga, limiar de lentidão, timeout e tentativas durante geração, afinidade por conversa e observabilidade em produção. A troca por lentidão ainda não está implementada.
- [ ] 05/11: modelo orquestrador (`gemma4:31b`, `127.0.0.1:11436`) para interpretar o contexto da conversa antes do modelo Cypher, com liga/desliga e URL no Admin e retorno do prompt gerado. [Plano](integracao-modelo/plano-modelo-orquestrador.md); nada implementado.
  - [ ] Fase 0: o modelo subiu (usuário, 05/11). Falta provar a reescrita com o exemplo do Ivan, medir tokens e tempo e combinar `num_ctx` com o Edson. O “Fluxo da resposta” e o log já registram tokens e tempo.
  - [x] Fase 1 (05/11, local, sem commit): Admin (toggle, URL, modelo; migração `20261105000000_orchestrator_settings`), histórico das últimas trocas na busca, `ReescritorContexto` no Quarkus, bloco `orquestrador` na resposta e no log, “Fluxo da resposta” na tela. API 95, Quarkus 39 e web 175 testes passaram.
  - [x] 05/11: fase 1 enviada a `chateau-expert/main` (`e6f4add`; ponte 11434 em `c2d5bf3`) com autorização do usuário.
  - [ ] Confirmar o deploy; ligar no Admin e testar o exemplo do Ivan em produção.
  - [x] 05/11: ponte `chateau_ollama_ponte_11436` (`172.17.0.1:11436` → `127.0.0.1:11436`) criada pelo usuário. Antes, `chateau_orchestration` recebia conexão recusada (curl 7); depois, `host.docker.internal:11436/api/tags` responde 200 e lista `gemma4:31b` (Q4_K_M, 30,7B, capacidade `thinking`; a chamada envia `think: false`).
  - [ ] Python de comparação ignora a etapa (divergência registrada no contrato da busca); decidir se terá paridade.
  - [ ] Fase 2: conversas encadeadas de teste, comparação ligado/desligado e revisão dos prompts pelo coordenador.
  - [x] Confirmado em 05/11: URL `127.0.0.1:11436`, exemplo do Ivan, fluxo visível para todos.
- [ ] Revisar a proposta de contexto da conversa de 28/10 à luz do pedido de 03/11: definir o contrato com o servidor de modelo que fará a reformulação, quais mensagens e resultados são enviados, limites, tratamento de dados simulados, falhas e testes de referência antiga. Definir como o Quarkus encaminhará as chamadas ao novo servidor; o contrato e a disponibilidade dele ainda não foram informados. **(dep: contrato do servidor de modelo)**
- [x] 28/10: documentar para o Edson o fluxo resumido da busca, com dados transmitidos em cada ida e volta ([versão 1](integracao-modelo/fluxo-busca-v1.md)).
- [ ] 28/10: avaliar a [versão 2 proposta pelo Edson](integracao-modelo/fluxo-busca-v2.md): comparar com o modelo real histórico completo e resumo acumulado da conversa, inclusive referências antigas; definir limite de contexto, acesso às mensagens originais, fonte/formato do histórico, prompt, modelo de reformulação/resumo, tratamento de respostas simuladas e impacto no tempo de busca. Somente documentação por enquanto; sem implementação aprovada.
- [x] 28/10: padronizar “modelo de IA” e “servidor do modelo de IA” no vocabulário de produto; manter nomes de campos, variáveis e comandos da integração atual nos contratos técnicos.
- [x] 28/10: esclarecer no fluxo de produto que o servidor do modelo é uma caixa preta; documentar apenas a solicitação enviada e a resposta recebida, deixando rotas e tecnologia no contrato técnico.
- [x] Levar ao Edson a lista de [dúvidas](duvidas-edson/README.md) e registrar as respostas ([reunião de 20/10](reunioes/2026-10-20.md)).
- [ ] Definir com o Edson o **contrato de resposta do modelo** (hoje o modelo ainda está em treino para pergunta → resposta, sem aderência nem contexto) para a nova UI: lista de perfis, aderência, justificativa, caminho no grafo, cobertura e montagem de equipe; como isso chega pelo caminho web → API → orquestração. **(dep: levantamento campo a campo da frente 1)**
- [x] 03/11: preparar em `chateau-expert` o contrato do modelo 31B rev_6: template original do pacote, prompt único sem `system`, `think: false`, recusa de esquema sem consulta ao banco. A seleção por cadastro registrada naquele dia foi substituída em 04/11 pelo de-para do nome técnico no código. Quarkus padrão e Python de comparação. [Histórico](analises/prompt-por-cadastro-2026-11-03.md).
- [ ] Confirmar o deploy da atualização da orquestração, cadastrar/selecionar o nome técnico `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` com URL alcançável do servidor do modelo de IA; o formato `rev6_31b` é escolhido pelo nome técnico no código. Validar perguntas reais no Neo4j de produção.
- [ ] Se o modelo e4b continuar em uso, reextrair `schema_producao.txt` após a carga rev_6 e reconstruir a imagem; o 31B usa o template rev_6 do pacote, não esse arquivo.
- [x] 03/11: corrigir os tipos gerados e carregar a rev_6 em produção: anos isolados em `publicationYear: INTEGER`, datas completas em `DATE`; contagens e amostras de tipos conferidas. Campos obrigatórios sem fonte continuam na frente de dados.
- [ ] Tarefa 1: versão 2.0 do orquestrador — aguardando o Edson. Em 05/11 a etapa de contexto passou a ter plano próprio (item do modelo orquestrador acima).
- [ ] Levar ao Edson: como a interface obtém o que o modelo não traz (opções de filtro, campos de perfil para completar os cartões). Hoje backend e web não acessam o Neo4j e esses dados ficam simulados (decidido em 22/10). **(dep: Edson)**
- [ ] Teste do modelo real com GPU e ligação da busca real: confirmar se aconteceu e registrar o resultado. Roteiro detalhado abaixo.

### Roteiro do teste com GPU (planejado para 30/09–02/10)

Detalhes e justificativas: `docs/integracao-modelo/README.md`, Fase 5.

Antes:

- [ ] Combinar com o Edson o **horário** e **quem sobe o túnel** da máquina com
      GPU. O servidor do modelo de IA (Ollama neste roteiro) precisa aparecer no servidor em `127.0.0.1:11434`.
- [ ] Ter à mão a **senha do SSH** do `prointec@152.92.2.63`.
- [ ] Docker Desktop rodando na máquina local.
- [ ] (Opcional) Acrescentar perguntas em
      `chateau-expert/orchestration/teste_modelo/perguntas.txt` (uma por linha).

Com o túnel de pé:

1. [ ] Rodar o teste (pede só a senha do SSH; leva alguns minutos):
   ```bash
   bash ~/projetos/uerj/chateau/chateau-expert/orchestration/teste_modelo/testar_modelo.sh
   ```
   - Se parar em **"Ollama NÃO responde"**, o túnel não está de pé: falar com
     o Edson.
   - Se perguntar **"Aplicar a ponte agora no servidor?"**, responder `SIM`
     (cria o container `chateau_ollama_ponte_11434`, sem sudo). **Anotar o
     `OLLAMA_URL` que ele indicar** no fim da etapa 3.
2. [ ] Colar o conteúdo de
   `orchestration/teste_modelo/resultados/<data>/resumo.md` no
   `docs/talk-ia.md` e pedir a análise. O resumo traz:
   - versão do servidor do modelo de IA e se o modelo está carregado;
   - acesso container → servidor do modelo e o `OLLAMA_URL` a usar;
   - as 14 perguntas reais (bananas, pergunta com ano, recusa do "Apague");
   - a avaliação das 20 perguntas do README (o Edson mediu 15/20);
   - a comparação Python × Quarkus com o modelo real (critério: 100%).
3. [ ] **Ligar a busca real na interface.** Só se a etapa 3 do teste der OK.
   No servidor (`ssh prointec@152.92.2.63`):
   ```bash
   cd /opt/apps/chateau-expert
   nano .env.prod          # configurar a URL do servidor do modelo se necessária para o teste
   #   OLLAMA_URL=<o valor que o teste indicou>
   docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
   docker logs --tail 20 chateau_orchestration
   ```
   Cadastrar no admin o nome técnico e a URL alcançável a partir do container
   de orquestração e marcar o modelo como **Disponível**. Sem modelo disponível,
   a busca continuará simulada. `ORCHESTRATION_URL` pode ficar vazia: a API usa
   `http://orchestration:8000` na rede Docker.
   Depois, perguntar pelo chat: "Quantos livros existem?", "Quantos artigos o
   Hermes Alves Filho publicou em 2024?" e "Quantas bananas tem numa penca?".
   - **Para voltar ao mock:** desmarcar **Disponível** nos modelos pelo admin.
   - O `.env.prod` não é versionado: a configuração sobrevive aos deploys
     automáticos.

Depois:

- [ ] Rodar de novo com mais perguntas reais e anotar erros e acertos para o
      Edson (material para a próxima versão do modelo).
- [x] 28/10: definir Quarkus como `orchestration` padrão nos dois Compose;
      Python fica em perfil opcional para comparação paralela/retorno, sem ser apagado.
- [x] 28/10: comparar Python × Quarkus com servidor simulado do modelo de IA e o mesmo Neo4j/schema:
      30 casos, 60/60 pares sem diferença, prompt enviado idêntico. [Registro](analises/quarkus-padrao-2026-10-28.md).
- [ ] Validar a subida do Quarkus no próximo deploy e uma busca real com a GPU.
- [ ] Comparar Python × Quarkus com o modelo real (critério: mesmo resultado em
      100% das perguntas) e repetir a comparação ao atualizar qualquer implementação.
- [ ] Se o `/api/chat` (LangChain4j) gerar a mesma consulta que o
      `/api/generate`, levar ao Edson a decisão sobre qual usar como padrão.
- [ ] Antes de devolver a GPU: desmarcar **Disponível** nos modelos pelo admin
      se o túnel não for continuar de pé; a busca então usa dados simulados.

## 4. Aplicação — `chateau-expert`

- [ ] 12/11: investigar por que `next dev` no Docker fica vários minutos em `Compiling / ...` sem servir a home, inclusive com cache limpo. O `localhost:5000` foi restaurado com um build local atualizado e um override temporário em `/tmp/chateau-web-local-restore.yml`; nesse modo, novas edições do web exigem novo build.

- [x] 12/11: mover o link de privacidade da entrada para a autorização de contexto; exigir confirmação inicialmente desmarcada, com instrução e aviso junto ao item, e registrar a data no backend. Expert `7a1027a` enviado a `main` e `deploy`; 98 testes do backend e 176 do web passaram. Ver [regra](../dominio/negocio/termos-e-privacidade.md). Conclusão do workflow e conferência funcional em produção pendentes.

- [x] 10/11: implementar localmente no Admin escolha de um `.cypher` por vez, nome visível, confirmação e upload + importação apenas após clicar **Importar**; card único de upload e lista com ícones para atualizar e remover arquivos, andamento e conclusão em modal e botão **Zerar grafo** que abre modal de explicação e confirmação digitada. [Decisão](analises/admin-grafo-2026-11-10.md).
- [x] 10/11: validar importação e limpeza em Neo4j descartável (2 nós, 1 relação e 1 restrição criados; 0 nós, relações, restrições e índices após limpar); repetição da limpeza também deixou o banco vazio sem apagar mais nada. O IPRJ foi importado duas vezes em outro Neo4j descartável; ambas concluíram 1.390 instruções e deixaram 5.045 nós e 16.289 relações. Dois arquivos pequenos enviados em sequência confirmaram que somente o segundo atualizou o nó em comum, sem reexecutar o primeiro. Nenhuma carga no servidor.
- [ ] Conferir a UI do Admin no navegador em `http://localhost:5000/admin/graph` com conta administradora; em 10/11 o stack local foi iniciado, a home respondeu 200, a rota protegida redirecionou para login e a API consultou o Neo4j local vazio. Depois publicar após autorização e testar no servidor. Só então importar `grafo_IPRJ.cypher`, conferir contagens e apagar o arquivo temporário do coordenador.

- [x] Abrir o protótipo Vite em <http://localhost:5179/> para uso local (26/10). A cópia publicada por engano no Sites foi substituída por uma página de encerramento, com acesso privado; o projeto hospedado ainda existe.
- [x] Autenticação web → API: implementada, commitada (`514cc8a`) e token gerado no `.env.prod` (20/10). [Desfecho](analises/divergencias-2026-10-20.md).
- [x] Confirmar o workflow de deploy do commit `6545a07`: a captura mais recente em `/mnt/c/temp` em 27/10/2026 mostra o run #25 concluído com sucesso em 35 min 32 s. O usuário informou que o site funciona em produção (27/10); isso ainda não valida os fluxos da UI.
- [x] Medir espaço, CPU, RAM e I/O no servidor após o deploy (27/10): 5,1 GB livres no disco de 18 GB, 712 MiB de RAM disponível, CPU 94–99% ociosa e espera por I/O em 0% na amostra. O cache de build ocupa 1,889 GB, 1,503 GB recuperáveis. Essas medidas não representam os picos durante o build de 35 min 32 s. [Análise](analises/deploy-2026-10-26.md#medição-posterior--27102026).
- [ ] Preparar a checagem do segundo disco no deploy após receber versão/driver do Docker e caminhos reais do servidor. Administração executa backup, montagem e migração em janela de manutenção; o deploy valida que imagens e cache usam o novo armazenamento. [Avaliação](producao/disco-adicional.md).
- [ ] Diagnosticar o desempenho do build web no servidor durante um deploy: no log de 10/11, `npm ci` levou 384 s, copiar `node_modules` entre estágios levou 342 s e `next build` levou 558 s. Registrar CPU, memória, swap e I/O durante essas etapas para distinguir limitação de recurso, rede e cache; a amostra anterior ao build não basta para concluir a causa.
- [ ] 10/11: validar o primeiro deploy com imagens construídas no GitHub Actions: confirmar permissões de escrita/leitura dos pacotes privados no GHCR, arquitetura x86_64 do servidor, download das três imagens, migrações, saúde dos containers e queda do tempo gasto no servidor. [Decisão e limites](analises/deploy-imagens-2026-11-10.md). A implementação passou nas verificações locais; falta confirmar o run remoto.
- [ ] Validar em produção (<http://chateau2.duckdns.org:8080>): login, autorização de contexto, resposta da busca, histórico e os dois ajustes visuais confirmados pelo usuário em 27/10; falta verificar `/admin` com um administrador.
- [ ] Retenção de logs de acesso: decidir o prazo (página diz 6 meses, código tem limpeza de 90 dias nunca chamada) e implementar a rotina. Ver [termos e privacidade](../dominio/negocio/termos-e-privacidade.md).
- [ ] Middleware web usa o JWT quando a API está fora do ar (fail-open): decidir se mantém.
- [ ] Tarefa 5: ambiente de avaliação — nada ainda (reunião de 19/10).

- [x] 05/11: separar testes e deploy no Expert (`0e81ff5` no `main`): a regra original executava testes no `main` e testes/publicação no `deploy`. Em 10/11, a decisão foi ajustada: somente o push no `deploy` executa o workflow. Próximo deploy: `git push origin main:deploy`. [Operação](../dominio/tech/operacao-e-validacao.md).
- [ ] Avisar o Edson e demais colaboradores que push no `main` do Expert não executa testes nem publica; conferir a regra após o próximo envio.
- [ ] 10/11: confirmar a publicação da administração do grafo no servidor. Os pushes de `813e8cc` no `main` e no `deploy` abriram dois runs; o segundo não publicou porque o Vitest descobriu `dist/services/graph-cypher.test.js` após o build. A correção foi enviada ao Expert `main` e `deploy` em `8d5e4e2`; o log recebido mostra build no servidor, mas não a conclusão do workflow nem a validação funcional.

## 5. Identidade visual

- [x] Tarefa 31: Figma recebido e lido em 20/10 ([análise](analises/figma-2026-10-20.md)); é espelho do protótipo (versão 01, 13/10, commit `3cf7be7`) e, por regra do próprio arquivo, o código prevalece.
- [ ] Revogar o token pessoal do Figma usado na leitura (Settings → Security) quando o levantamento terminar.
- [ ] Se o original do Edson mudar, refazer a cópia ou pedir acesso de leitura para `mvurban@mvurban.eti.br` (a cópia em rascunhos não acompanha o original).

## 6. Documentação e segurança

- [ ] Trocar a senha SSH que ficou no histórico Git da raiz (commit `b8ff640`, já publicado).
- [x] Atualizar o [diagrama web–API](diagrams/chateau-web-api-map.drawio) para o fluxo atual, incluindo token web → API e retirada dos termos; novo mapa e [guia](diagrams/README.md) conferidos contra `chateau-expert` `dc77c53` (27/10/2026).
- [ ] Revisar guias antigos do `chateau-data` (`scripts/README.md`, `docs/knowledge-graph-pipeline.md`, `docs/levantamento-campos.md`) que citam versões e comandos anteriores.
- [ ] Decidir a relação entre o modelo relacional alvo (`chateau-db-schema.json`) e o modelo acadêmico rev_6.
