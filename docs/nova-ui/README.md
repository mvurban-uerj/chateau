# Nova UI: contexto para montar o port

Ponto de partida para portar o protótipo para `chateau-expert/web`. Junta, para uso prático, o que decidiram as reuniões de [19/10](../reunioes/2026-10-19.md) e [20/10](../reunioes/2026-10-20.md) e as análises da [UI](../analises/ui-prototipo-2026-10-20.md) e do [Figma](../analises/figma-2026-10-20.md). As decisões e suas fontes continuam nesses documentos; aqui ficam o escopo, o mapa protótipo → web e o que falta definir. Itens marcados **proposta** ainda não foram decididos. O plano de execução (o que aproveitar do código, otimizações, componentes, internacionalização e fases) está em [plano.md](plano.md).

Conferido em 22/10/2026 contra `chateau-expert` `514cc8a` e o protótipo em `/mnt/c/temp/chateau/ui`, que não tem Git.

## Reuniões de origem

- **19/10:** Tarefa 31 (identidade visual): o Edson entregaria o Figma no dia seguinte. As outras pautas (Atividade 16 de dados, Sucupira, ambiente de avaliação e orquestrador 2.0) não afetam a UI.
- **20/10:** tira-dúvidas com o Edson. Decidiu o escopo do port, a troca do termo de uso por uma autorização de contexto, o contexto do usuário no PostgreSQL e as perguntas guiadas geradas do grafo rev_6. O protótipo não evolui em paralelo.

## Escopo

1. **Aparência idêntica ao protótipo; infraestrutura do Expert.** Next.js 14, React 18, NextAuth, API Express e Prisma ficam. O protótipo se adapta ao projeto.
2. **Toda a interface vai para o web**, exceto os desdobramentos de **"Buscar candidatos"** e **"Montar equipe"**: os botões aparecem, mas desabilitados.
3. **Sem dado real → simulado.** Fica simulado o que o grafo carregado não tem ou o que o modelo ainda não responde: aderência, justificativa, caminho no grafo, cobertura, equipe e campos de perfil da rev_6.
4. **O que dá para implementar já se implementa com dado real:** autorização de contexto, Meu contexto, perguntas guiadas e histórico, todos no PostgreSQL.
5. **Sem etapas reais da busca.** O modelo só recebe a pergunta e devolve a resposta. Retomar e as etapas nomeadas ficam para depois; Parar aparece, mas só avisa que está em desenvolvimento (decidido em 22/10).
6. **O contexto ainda não entra na busca.** Ele é salvo, mas não vai no `POST /api/search`.
7. **Ajustes do nosso lado (decididos):** tema único claro (sai o `next-themes`), acesso ao admin pela nova sidebar, Desfazer de 6 s ao apagar uma conversa, rota por conversa e layout responsivo (o desenho tem telas de 390 px).
8. **Fora do port:** exportação em planilha (retirada por LGPD) e os textos do protótipo sobre dados simulados e usuário fictício (rodapé do chat, `USER_FIRST_NAME = 'Mateus'`).

## Referências

| O quê | Onde |
|---|---|
| Protótipo, versão final, não versionado | `/mnt/c/temp/chateau/ui`. Rodar com `npm ci` e depois `npm run dev -- --host 0.0.0.0`, porta 5179 |
| Figma (espelho do protótipo; em divergência, vale o código) | Cópia nos rascunhos do Marcelo, página **08 Handoff**: [análise](../analises/figma-2026-10-20.md) |
| Interruptores do que fica escondido | `src/features.ts` (`RECURSOS`) do protótipo |
| Web atual | `chateau-expert/web/src/app/` |
| Contrato de busca atual | `chateau-expert/web/src/types/search.ts` e [contrato de busca](../../dominio/tech/contrato-de-busca.md) |
| Modelo de contexto (UX) | [contexto-ux.md](../../dominio/modelo/contexto-ux.md) e `chateau-data/model/diagramas/Chateau-UX.json` |
| Grafo acadêmico vigente | `chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json` |

## Pilha: protótipo × web

| Item | Protótipo | Web | No port |
|---|---|---|---|
| App | Vite 8, SPA com etapas em estado | Next.js 14, App Router e middleware | Cada etapa vira rota; componentes com `"use client"` |
| React / TS | 19.2 / 6.0 | 18.3 / 5 | Sem APIs exclusivas do React 19 (verificado em 20/10) |
| CSS | Tailwind 4 e tokens em `src/index.css` | Tailwind 4, shadcn e tokens em `globals.css` | Trazer os tokens do protótipo (`paper`, `ink-*`, `graphite*`, `ok`, `warn`) para o `globals.css`. Falta decidir o que sobra dos tokens shadcn usados no admin |
| Fontes | Geist e Geist Mono (`@fontsource-variable`) | `--font-geist-*` no tema | Conferir a origem no `layout.tsx` (sugestão: `next/font`) |
| Ícones | Phosphor | lucide | Phosphor nas telas novas; lucide fica no admin até ser redesenhado |
| Movimento | `motion` 13, `src/motion.ts` (curva e durações) | `tw-animate-css` | Acrescentar `motion` |
| Slider | `@radix-ui/react-slider` | Radix (outros pacotes) | Acrescentar |
| Persistência | `localStorage` | API → PostgreSQL | Ver o mapa de fluxos abaixo |

Pendências técnicas já conhecidas: o build do protótipo gera um chunk JS acima de 500 kB, e há uma vulnerabilidade alta em `source-map-js`, dependência indireta do lado Vite que não vem para o Next.

## Mapa protótipo → web

O tamanho em linhas mostra o peso de cada parte; o total do protótipo é de cerca de 6.000 linhas.

| Protótipo | Linhas | Destino no web | Dados |
|---|---|---|---|
| `views/Login.tsx` | 115 | `/` (landing, hoje `app/page.tsx`) com o `LoginButton` Google; `/pending` e `/alerts/restrictedAccess` ganham o visual novo | Real (NextAuth e [acesso](../../dominio/negocio/acesso.md)) |
| `views/ConsentGate.tsx`, `consent.ts` | 109 + 91 | Etapa depois do login, no lugar de `/terms`. Revogar em Meu contexto devolve a pessoa a esta tela | Real: **autorização de contexto** no PostgreSQL |
| `views/Shell.tsx` | 666 | Layout de `/chat`, com **rota por conversa** (proposta: `/chat/[id]`) | Real: `/api/chats` |
| `components/Sidebar.tsx` | 301 | Sidebar do layout: Nova busca, histórico, bloco da conta e **entrada do admin** (nova) | Real |
| `components/ChatView.tsx` | 875 | Área da conversa: cards de ação rápida, mensagens e estados vazio, erro e interrompida | Misto |
| `components/Composer.tsx`, `templates.ts` | 675 + 346 | Campo de pesquisa que monta o texto aos poucos e termina com **tab**, que abre o modal de perguntas | Perguntas do PostgreSQL |
| `components/DepthSlider.tsx`, `TIERS` | 52 | Visível, sem efeito | Níveis em aberto com o Edson |
| `components/ResultCard.tsx` | 222 | Cartão de resultado, montado das linhas de pessoas do chat livre | Real do grafo + campos em vermelho simulados (ver abaixo) |
| `components/ProfileDrawer.tsx`, `CompareDrawer.tsx` | 175 + 123 | Gavetas de perfil e comparação | **Simulado** até a carga rev_6 e a resposta do modelo |
| `components/ContextDrawer.tsx`, `context.ts` | 500 + 80 | Meu contexto (aberto pela engrenagem da conta) | Real: PostgreSQL |
| `escopo.ts` | 195 | Painel de filtros de escopo | **Simulado** por enquanto; fonte definitiva com o Edson (sem acesso novo ao Neo4j) |
| `flows/*.ts`, `ACTION_FLOWS` | ~260 | Questionários de "Buscar candidatos" e "Montar equipe" | Fora do escopo agora (botões desabilitados) |
| `data.ts` (`REGISTROS`, `runSearch`, `montarEquipe`) | 805 | Fonte do dado simulado, isolada num módulo que será substituído | Simulado; as regras do arquivo **não** são regra de domínio |
| `Logo.tsx`, `Modal.tsx`, `motion.ts`, `useDialogo.ts`, `inputModality.ts`, `index.css` | ~330 | Base visual compartilhada | — |
| (não existe) | — | Telas de admin com o visual novo | Real; desenho a definir por nós |

## Chat livre → cartões (decidido em 22/10/2026)

Decisão do Marcelo: **o chat livre continua indo ao modelo**, e a resposta com profissionais é mostrada como **cartões de perfil** do protótipo.

### Como o modelo responde hoje

O modelo gera um Cypher, a orquestração o executa e devolve `resultado: {colunas, linhas, truncado}`. As colunas são as que o Cypher escolheu. Um nó vem como mapa de propriedades, sem rótulo ([contrato](../../chateau-expert/orchestration/README.md#serialização-das-linhas)). Uma pergunta sobre pessoas costuma devolver ou o nó `Person` inteiro (`{name, identifierLattes, identifierORCID, identifier, email}`, iguais na produção e na rev_6) ou colunas soltas, como `p.name AS nome`.

### Regra dos cartões

1. **Quando vira cartão:** quando as linhas trazem pessoas. Isso vale para uma coluna cujo valor é um mapa com `name` e algum entre `identifierLattes`, `identifier`, `email` ou `identifierORCID`, e também para uma coluna de nome (`name`/`nome`) acompanhada de outras colunas de pessoa. Contagens, listas de linhas de pesquisa e outros resultados que não são pessoas continuam como **bloco tabular** no visual novo.
2. **O que vem do grafo** é mostrado normalmente: qualquer coluna que o Cypher gerado pelo modelo devolveu — nome, e-mail, Lattes (`identifierLattes`), ORCID, e também instituição, área, quantidade de artigos etc. quando a consulta as trouxer (ver o [fluxo de ponta a ponta](../../dominio/negocio/visao-geral.md#fluxo-de-ponta-a-ponta)). Colunas reconhecidas preenchem o campo correspondente do cartão; as demais aparecem como evidência.
3. **O que não veio do grafo aparece em vermelho, com dado falso.** São os campos do cartão e da gaveta que a linha não trouxe: aderência, justificativa, caminho no grafo, cargo, vínculo, unidade, campus, disponibilidade, prêmios, disciplinas e projeto ativo. O vermelho vale por campo, para se ver o que é real e o que é simulado. O dado falso vem de um gerador determinístico por pessoa, para o mesmo perfil não mudar a cada visualização.
4. **Modelo fora → resposta simulada com aviso.** Quando não há modelo, a busca devolve profissionais simulados no mesmo formato de linhas do `Person`, e a tela mostra o aviso **"Modelo fora do ar — dados simulados"**. "Não há modelo" cobre o `ORCHESTRATION_URL` vazio (situação atual da produção, que hoje cai no mock sem avisar), o erro na etapa `modelo` e a falta de resposta. O mesmo construtor de cartões é usado, então os campos de fora do grafo continuam em vermelho.
5. **A resposta indica que é simulada.** O `SearchResult` ganha um campo novo (proposta: `simulado: boolean`), gravado com a mensagem no histórico. Uma conversa antiga continua mostrando o aviso.
6. **Status:** quando o modelo está fora, a tela de `indisponivel` deixa de aparecer para o chat livre, porque a simulação ocupa o lugar dela. `recusada`, `erro_consulta` e `sem_resultado` continuam valendo com o modelo ligado. `recusada` não tem tela no desenho; **proposta:** reaproveitar o aviso de erro com o texto do backend.

Onde simular (**proposta**): no backend, no `orchestration.mock.ts`, que já imita uma resposta do modelo (colunas `nome`, `instituicao`, `area`, `artigos`, como o Cypher gerado poderia devolver). Só falta marcar a resposta como simulada; o construtor de cartões fica no web.

Sem enriquecimento por enquanto: o backend não ganha acesso ao Neo4j (decidido em 22/10). Os campos vermelhos ficam simulados até o modelo trazê-los ou o Edson decidir outro caminho.

Falta ainda: o formato salvo em `Chat.messages` (prefixo `__SEARCH__:`) precisa acomodar os novos tipos de mensagem do protótipo (`ask`, `cvs`, `stopped`, `error`) e o campo `simulado`.

## Persistência nova no PostgreSQL

Nada disso existe no `schema.prisma` hoje, que tem `User`, `Account`, `Role`, `UserRole`, `AuthorizedDomain`, `AiModel`, `Term`, `SearchExample`, `Chat` e `SiteAccess`. Os nomes abaixo são **proposta**, derivada do `Chateau-UX.json` e dos tipos do protótipo.

| Necessidade | Origem no protótipo | Proposta de tabela |
|---|---|---|
| Autorização de contexto | `Consent` (`name`, `unit`, `email`, `location`, `cookies`; nome e unidade obrigatórios) | `ContextAuthorization` por usuário: um booleano por campo, data e `revokedAt` |
| Perfil, objetivo e disponibilidade | `UserContext.profile`, `objective`, `available` (padrão `true`) | `UserContext` 1:1 com `User` |
| Interesses | `ContextItem[]` | `ContextInterest` (descrição e `selected`) |
| Instruções e filtros | `Instrucao` → `Filtro` (`varDomainModel`, `=`/`!=`, valor; só E) | `ContextInstruction` 1:N `ContextFilter` |
| Documentos | `Documento` (escondido por `RECURSOS.documentos`) | Adiar, porque a busca não lê documentos |
| Perguntas guiadas | `templates.ts` e `ACTION_FLOWS` | `GuidedQuestion` e opções, carregadas uma vez a partir do rev_6 |
| Opções de filtro | `escopo.ts` | Nenhuma: simuladas por enquanto; destino é o grafo com cache, quando o Edson decidir o caminho |

**Remoção do termo de uso** (decidida, ainda não feita): tirar `Term`, `Account.acceptedTermId`, `/terms`, `/termos-uso`, `api/accept-terms`, `admin/terms` e a exigência de termo aceito no middleware web e na API, **sem guardar os aceites** (decidido em 22/10: tudo ainda é teste e avaliação). Manter `/privacidade`. Falta decidir o que cada escolha da autorização controla de fato e se a exportação de privacidade passa a incluir contexto e autorização.

## O que fica escondido, desabilitado ou simulado

- **Escondido** (`RECURSOS = false`): upload de edital, Procurar no histórico, Sobre o projeto, documentos em Meu contexto, Sugerir formações, Analisar competências e Avaliar perfis. Os links de termos e privacidade no login voltam a aparecer, apontando para `/privacidade`.
- **Desabilitado e visível:** "Buscar candidatos" e "Montar equipe". O seletor de profundidade usa o catálogo do admin e permite escolher visualmente um nível, marcado em vermelho; a escolha ainda não altera a busca.
- **Simulado, em vermelho no cartão:** aderência, justificativa, caminho "Por que este perfil", cobertura, equipe e os campos de perfil da rev_6 que não estão no grafo de produção (`Job`, `Role`, `WORKS`, `TAUGHT`, `COORDINATES`, `Campus`, `Acknowledgment`).
- **Modelo fora:** resposta inteira simulada, com o aviso "Modelo fora do ar — dados simulados".
- **Espera da busca:** sem etapas reais; indicador genérico de "consultando", sem contador. **Parar** aparece e, ao clicar, avisa que está em desenvolvimento (decidido em 22/10).

## Pendências que bloqueiam ou afetam o port

Com o Edson:

1. Os níveis de busca: nomes e se vão existir.
2. Se o admin poderá editar as perguntas guiadas.
3. Se a cópia em `/mnt/c/temp/chateau/ui` corresponde ao commit `3cf7be7` (ou posterior), que o Figma espelha.

Nossas:

4. O que cada escolha da autorização de contexto controla.
5. Visual do bloco de resposta tabular (o admin será redesenhado com os primitivos novos, decidido em 22/10).
6. Levantamento campo a campo rev_6, que depende da carga rev_6 em produção (frente 2 do [todo](../todo.md)).

## Ordem sugerida (proposta)

Cada etapa substitui a tela antiga só depois que o fluxo integrado for validado.

1. **Base visual:** tokens, fontes, `motion`, Phosphor, `Logo` e `Modal` no web; tirar `next-themes`.
2. **Entrada:** landing nova com Google; `/pending` e acesso restrito com o visual novo.
3. **Autorização de contexto:** tabelas, API e tela; remover o termo de uso.
4. **Shell e histórico:** layout, sidebar, `/chat/[id]` ligado a `/api/chats`, Desfazer de 6 s e entrada do admin.
5. **Composer e chat livre:** ligados a `/api/search`, com cartões a partir das linhas de pessoas (campos fora do grafo em vermelho), bloco tabular para o resto, simulação com aviso quando o modelo está fora e os status.
6. **Meu contexto:** tabelas, API e gaveta.
7. **Perguntas guiadas:** carga a partir do rev_6 e modal aberto pelo tab.
8. **Gavetas e ações:** gavetas de perfil e comparação com a mesma marcação real/vermelho; cards de ação desabilitados.
9. **Filtros de escopo** com opções do grafo.
10. **Admin** redesenhado com os primitivos novos, revisão responsiva (390 px) e retirada da UI antiga. Fases detalhadas no [plano](plano.md#7-fases).
