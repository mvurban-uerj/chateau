# Plano do port da nova UI

Plano de execução do port do protótipo (`/mnt/c/temp/chateau/ui`) para `chateau-expert/web`. O escopo, as decisões e o mapa geral estão no [README desta pasta](README.md); este documento diz **como** fazer: o que aproveitar do código do protótipo, o que otimizar, quais componentes criar, como preparar a internacionalização e em que ordem trabalhar.

Base da leitura (22/10/2026):

- todo o código do protótipo (cerca de 6.000 linhas);
- o Figma, cópia de 20/10, páginas 01 Leia-me, 03 Componentes, 04 Padrões, 07 Por que funciona e 08 Handoff, lidas pela API;
- `chateau-expert` em `514cc8a`: web, backend, Prisma e workflow de deploy.

Itens marcados **(decidir)** dependem de resposta antes da fase indicada.

**Princípio (decidido em 22/10/2026):** o backend e a web não ganham acesso ao Neo4j. Tudo o que o modelo não trouxer fica **simulado**, num módulo isolado e fácil de trocar, e o trabalho segue; o Edson decide depois o rumo. Não se constrói caminho novo até o grafo para depois desfazer.

## 1. O que o protótipo tem de especial (preservar)

O protótipo vai além de uma maquete: cada comportamento abaixo foi pensado e está comentado no código. O port precisa reproduzi-los.

| Comportamento | Onde está | Por que importa |
|---|---|---|
| **Campo com molde e texto fantasma.** O `textarea` é transparente sobre um "espelho" que desenha o texto, sublinha os valores reconhecidos e mostra o fantasma cinza. Tab aceita trecho por trecho, Enter envia pela metade, Esc solta | `Composer.tsx`, `templates.ts` (`resolver`, `percorrer`) | É a principal entrada do produto ("a estrutura nasce enquanto se digita"). O `resolver` é uma função pura e pode ser portado sem mudanças |
| **Questionário dentro do chat.** A próxima pergunta é sempre a primeira sem resposta; `lembradas` pré-marca o que veio depois ao voltar; Alterar reabre qualquer etapa, inclusive depois do resultado; Voltar e Cancelar | `Shell.tsx` (`proximaPergunta`, `voltarPara`, `voltar`, `send`) | O padrão "Ir e vir" e a fusão de digitar com clicar: a frase digitada e o questionário produzem o mesmo objeto de respostas |
| **Três encontros de frase com questionário aberto:** mesma intenção funde; intenção nova substitui; texto livre busca com o que já foi respondido | `Shell.tsx` (`send`) | Nenhuma resposta é jogada fora |
| **Apagar com Desfazer de 6 s** em vez de confirmação | `Shell.tsx` | Decidido para o port |
| **Voltar e avançar do navegador trocam de conversa** | `Shell.tsx` (`popstate`) | No port vira rota real (`/chat/[id]`) |
| **Foco visível só no teclado:** `data-input` no `<html>` e anel global em `@layer base` | `inputModality.ts`, `index.css` | A regra fica dentro da camada de propósito, senão vence os utilitários do Tailwind 4 |
| **Acessibilidade consistente:** combobox ARIA no campo, `role="checkbox"` nas pills e opções, `aria-label` com a faixa da aderência, `h1` só para leitor de tela, cartão que não é botão (evita botão dentro de botão) | vários | Avaliação de Nielsen 9/10 no Figma |
| **Movimento com tokens:** uma curva (`EASE`), seis durações (`DUR`) e `prefers-reduced-motion` em tudo, com a contagem já no valor final, rolagem instantânea e shimmer parado | `motion.ts`, `index.css`, todos os componentes | O Figma espelha os mesmos nomes |
| **Layout por `@container`**, não por viewport: a coluna é estreitada pela sidebar | `ChatView.tsx` | Tailwind 4 tem suporte nativo |
| **Interruptores de recurso** (`RECURSOS`): o que não funciona some, sem apagar o código | `features.ts` | No port, ganha também o estado "desabilitado e visível" |
| **Painéis flutuantes escolhem a direção** (para cima ou para baixo) pelo espaço livre | `Composer.tsx` | A lista e a profundidade não saem da tela no rodapé do chat |
| **Placeholder animado isolado** num componente próprio, para o resto do campo não renderizar a cada letra | `Composer.tsx` (`PlaceholderAnimado`) | Já é uma otimização; manter |
| **Estados com motivo e saída:** vazio por disponibilidade oferece incluir indisponíveis; erro garante que a conversa ficou | `ChatView.tsx` | Padrão 05 do Figma |
| **Tokens de cor e texto** nomeados pelo papel (`paper`, `ink-*`, `graphite*`, `ok`, `warn`, `text-micro`…`text-display`) | `index.css` | Iguais às variáveis do Figma |

Regras de negócio do `data.ts` (`vinculoDe`, `montarEquipe`, `runSearch`, as faixas de `matchColor`) **não** são regra de domínio. Elas vão só para o gerador de dado simulado.

## 2. O que otimizar no port

| No protótipo | Problema | No port |
|---|---|---|
| `Shell.tsx` concentra todo o estado, e quase todo `useCallback` depende de `chats` | Callbacks recriados a cada mudança, renderização em cascata, 666 linhas difíceis de testar | **Reducer puro** (`conversaReducer`) com ações nomeadas (`enviar`, `responder`, `voltarPara`, `parar`…), testável sem React; despacho estável; seletores derivados |
| Histórico, contexto e consentimento no `localStorage`, gravados a cada mudança | Não vale como registro (decidido) e grava em excesso | API → PostgreSQL. Histórico com **atualização otimista** e gravação ao fim de cada troca; contexto com **gravação adiada** (debounce) e descarga ao fechar a gaveta |
| `ResultCard` monta um `ProfileDrawer` por cartão | N gavetas montadas por resultado | **Uma gaveta** no nível da conversa, aberta pelo id da pessoa |
| A contagem da aderência faz `setState` a cada quadro | Uma renderização do React por quadro, por cartão | `useMotionValue` + `useTransform` renderizado direto num `motion.span`, sem renderizar o componente |
| Classes Tailwind longas repetidas (botão grafite, pill, caixa de seleção, aviso) em dezenas de lugares | O próprio Handoff aponta: "ainda são classes repetidas; viram componentes quando houver consumidor" | **Primitivos com variantes** (`cva`, já usado no web) com os nomes do Figma (seção 3) |
| O padrão de entrada `initial={reduce ? false : {opacity:0, y:10}}` repetido em quase todo bloco | Repetição e risco de esquecer o movimento reduzido | Componentes `<Entrada>` e `<Expandir>` que já tratam o movimento reduzido |
| Diálogos com `useDialogo` (Esc e retorno de foco) | Sem prender o foco nem travar a rolagem do fundo | **Radix Dialog** (já instalado no web) por baixo de Gaveta, Diálogo e Folha, com a animação do `motion` por cima. Mantém Esc e o retorno de foco e ganha foco preso, rolagem travada e ARIA |
| Menu de opções da sidebar feito à mão | Navegação por teclado incompleta | **Radix DropdownMenu** (já instalado) |
| Navegação por `history.pushState` | Recarregar perde a conversa; não há link direto | Rotas `/chat` e `/chat/[id]` do App Router |
| Espera simulada por temporizadores | Sem relação com a requisição real | `fetch` com `AbortController` (cancela ao trocar de conversa ou sair). **Parar** fica visível e, ao ser clicado, só avisa que está em desenvolvimento (decidido em 22/10); a busca segue |
| Pacote do `motion` inteiro e chunk acima de 500 kB | Peso da página | `LazyMotion` com `domAnimation` e componentes `m.*`; `experimental.optimizePackageImports` para Phosphor; medir com `next build` |
| Fontes por `@fontsource` importadas no CSS | Sem preload, risco de troca de fonte visível | `next/font` (Geist e Geist Mono) com variáveis CSS |
| Tudo no cliente | Cascata de requisições ao abrir | Layout e páginas como **Server Components**: histórico, contexto e perguntas carregados no servidor e passados a ilhas cliente (Composer, conversa e gavetas) |
| Categorias de filtro calculadas no carregamento do módulo a partir do mock | Sem fonte real | Simuladas num provedor isolado (`opcoesDeFiltro`), com a mesma forma que o grafo teria, para trocar a fonte sem mexer na tela |

## 3. Componentes reutilizáveis

Organização proposta em `web/src/components/chateau/`. A pasta `components/ui/` continua com o shadcn do admin até ele ser redesenhado. Cada primitivo tem o nome do Figma e o comentário de origem, como o Figma faz com o protótipo.

### Primitivos (conjuntos de componentes do Figma)

| Figma | Componente | Variantes | Base |
|---|---|---|---|
| Botão | `Botao` | `tipo`: primário, secundário, fantasma · `tamanho`: M, P · desabilitado | `cva` |
| Botão de ícone | `BotaoIcone` | `estilo`: neutro, primário | `cva`; `aria-label` obrigatório no tipo |
| Pill de filtro | `Pill` | `tipo`: tag, todos · selecionada | `role="checkbox"` |
| Seleção | `Selecao` | `tipo`: caixa, rádio · marcada · obrigatória | marca de 15 px do protótipo |
| Interruptor | `Interruptor` | ligado | `role="switch"` (ou `@radix-ui/react-switch`) |
| Selo | `Selo` | disponível, indisponível, projeto ativo | ponto de cor e rótulo escrito |
| Indicador de aderência | `IndicadorAderencia` | alta, média, baixa | contagem por motion value |
| Aviso na conversa | `AvisoConversa` | erro, vazio, interrompida, **simulado** (novo), recusada (novo) | ícone em chip de névoa |
| Aviso (Busca apagada) | `AvisoDesfazer` | — | pill grafite fixa no rodapé |
| Item da sidebar | `ItemSidebar` | navegação, histórico (ativo) | — |
| Logo/Assinatura · Logo/Símbolo | `Logo` | assinatura, símbolo | SVG do protótipo |
| — (padrões) | `Entrada`, `Expandir` | — | `motion` + movimento reduzido |
| — (gavetas e modais) | `Painel` | gaveta lateral, diálogo central, folha inferior | Radix Dialog + `motion` |
| — (menus) | `Menu` | — | Radix DropdownMenu |
| — **(novo)** | `Simulado` | — | marca em vermelho um campo de dado simulado ([regra](README.md#chat-livre--cartões-decidido-em-22102026)); novo token `--color-simulado`, com contraste conferido sobre `paper` e `sheet` |

### Compostos

| Figma | Componente | Usa |
|---|---|---|
| Campo de busca · Linha de filtro · Lista do autocompletar | `Composer` (`CampoMolde`, `PainelFiltros`, `ListaAutocompletar`, `PainelProfundidade`, `PlaceholderAnimado`) | Pill, Botao, BotaoIcone, Expandir |
| Card de ação | `CardAcao`, `LinhaAcao` | estado desabilitado (novo) para "Buscar candidatos" e "Montar equipe" |
| Opção do questionário | `EtapaQuestionario` | Selecao, Botao |
| Bolha do usuário | `BolhaUsuario` | Alterar |
| Bloco de cobertura | `BlocoCobertura` | Simulado |
| Card de resultado | `CardResultado` | Selo, IndicadorAderencia, Selecao, Expandir, Simulado |
| Barra de seleção | `BarraSelecao` | Botao |
| Gaveta de perfil | `GavetaPerfil` | Painel, Selo, Simulado |
| Comparação | `Comparacao` | Painel, Simulado |
| Meu contexto | `MeuContexto` | Painel, Interruptor, Pill, Botao |
| Sidebar | `Sidebar` (+ `Menu`, diálogo de renomear) | ItemSidebar, Menu, Painel |
| Barra de topo (celular) | `BarraTopo` | BotaoIcone, Logo |
| — | `Pensando` (shimmer + esqueletos, sem etapas por enquanto; Parar avisa "em desenvolvimento") | Botao, AvisoDesfazer (reaproveitado como aviso curto) |
| — **(novo)** | `BlocoTabela` (resultado que não é de pessoas) | estilo do protótipo |
| — | `PortaAutorizacao` (tela de consentimento) | Selecao, Botao |
| — | `Entrar` (landing com as curvas de nível) | Botao, Logo |

As 40 instâncias de ícone do Figma (`Ícone/...`) são ícones do Phosphor com o mesmo nome do import.

## 4. Internacionalização

Hoje só pt-BR e sem troca de idioma, mas todo texto já fica preparado para isso.

- **Biblioteca:** `next-intl`, em modo sem rota de idioma: o locale fica fixo em `pt-BR` na configuração de requisição, e as URLs não ganham prefixo. Funciona em Server e Client Components e usa ICU (plural, seleção, número e data). A versão será fixada depois de conferir as `peerDependencies` com Next 14.2 e React 18.
- **Arquivos:** `web/messages/pt-BR.json`, com um namespace por área: `comum`, `entrar`, `autorizacao`, `sidebar`, `inicio`, `composer`, `questionario`, `resultado`, `perfil`, `comparacao`, `contexto`, `avisos`, `admin`, `erros`.
- **Chaves tipadas:** declarar o tipo das mensagens a partir de `pt-BR.json`. Uma chave inexistente vira erro de compilação.
- **Nenhum literal em JSX,** inclusive `aria-label`, `title`, `placeholder` e `alt`. Isso vale no lint com uma regra de literal em JSX (`eslint-plugin-i18next` ou `react/jsx-no-literals`), aplicada às pastas novas.
- **Plural e concordância por ICU,** e não por ternário. O protótipo tem vários casos: `pessoa/pessoas`, `atende/atendem`, `ficou/ficaram`, `perfil/perfis`, `selecionado/selecionados`.
- **Números, datas e percentuais** por `useFormatter`: `tempoMs`, ano de vínculo, aderência.
- **Moldes do autocompletar:** os conectores ("Preciso de alguém em ", " do "…) e os rótulos das opções são texto de interface e dependem do idioma. O `resolver` recebe o molde já traduzido e continua puro. A regra "nenhum conector começa com vírgula" vale por idioma.
- **Conteúdo do banco:** perguntas guiadas e rótulos de opções gravados com `locale` (proposta: tabela de traduções ou coluna `labels` JSON por locale). Valores vindos do grafo (nome de linha de pesquisa, unidade) são dado e não se traduzem.
- **Mensagens do backend:** a tela usa o `status` (código) para escolher o texto traduzido. O campo `mensagem` continua na API por compatibilidade, mas não é exibido.
- **Escopo:** telas novas e as que forem tocadas (landing, `/pending`, alertas, privacidade). O admin entra quando for redesenhado.

## 5. Arquitetura no web

### Rotas (route groups do App Router)

O `layout.tsx` raiz atual envolve tudo com a Sidebar, o Header e o Footer antigos. Ele passa a ter só `html`, fontes, provedores (sessão e i18n) e `LazyMotion`, e cada grupo ganha o seu layout.

| Grupo | Rotas | Layout |
|---|---|---|
| `(publico)` | `/` (Entrar), `/privacidade`, `/alerts/*`, `/pending` | Visual novo, sem sidebar |
| `(autorizacao)` | `/autorizacao` (substitui `/terms`) | Visual novo |
| `(app)` | `/chat`, `/chat/[id]` | Shell novo: Sidebar, BarraTopo e gaveta Meu contexto |
| `admin` | `/admin/*` | Mantém o atual até a fase 9; entrada pela nova sidebar |

`/home` passa a redirecionar para `/chat`. O middleware troca a checagem de termo aceito pela de autorização de contexto vigente.

### Estado e dados

- **Conversa:** um reducer puro por conversa, mais um provedor de histórico que substitui o `ConversationsProvider` atual. O histórico é carregado no servidor.
- **Formato salvo** em `Chat.messages`: mensagens tipadas (`user`, `assistant`, `ask`, `error`, `stopped`, `cvs`) com campo de versão. Mensagens antigas com `__SEARCH__:` são lidas por um adaptador e não são reescritas.
- **Contexto e autorização:** carregados no servidor; edições com atualização otimista.
- **Interruptores:** `features.ts` com quatro estados por recurso: `ativo`, `emDesenvolvimento` (visível e clicável, avisa que está em desenvolvimento, como o Parar), `desabilitado` (visível e inerte, como os cards de ação) e `oculto`.

### Busca → cartões

Módulo puro `montarCartoes(resultado)`:

1. Detecta as linhas de pessoa.
2. Mapeia as colunas reconhecidas: `name`/`nome`, `email`, `identifierLattes`, `identifierORCID`, `instituicao`, `area` etc.
3. Cada campo sai com origem `grafo` ou `simulado`.
4. O gerador determinístico, com semente pelo identificador ou nome, completa o resto.

Testado com as respostas reais registradas e com o mock.

## 6. Backend e banco (`chateau-expert/backend`)

| Mudança | Detalhe |
|---|---|
| Autorização de contexto | Tabela `ContextAuthorization`; endpoints para ler, gravar e revogar; a sessão (`/api/auth/session`) passa a informar se há autorização vigente |
| Remoção do termo de uso | Sai `Term`, `Account.acceptedTermId`, `terms.router`, `/api/accept-terms`, `admin/terms`, `/terms`, `/termos-uso`, o `markdown-content` se ficar sem uso e a exigência em `auth.service`, no middleware e na exportação de privacidade. Migração Prisma que apaga tabela e coluna **sem guardar os aceites** (decidido em 22/10: ambiente só de teste e avaliação) |
| Contexto do usuário | `UserContext` (perfil, objetivo, disponível = `true`), `ContextInterest`, `ContextInstruction` e `ContextFilter`; CRUD por usuário |
| Perguntas guiadas | Tabelas de molde, pergunta e opção com locale; carga única a partir do rev_6 por script, com revisão do Marcelo antes da carga |
| Opções de filtro | Nada no backend por enquanto: as opções são simuladas no web. Sem acesso novo ao Neo4j e sem tabela no PostgreSQL (decidido em 22/10) |
| Busca | Campo `simulado` no `SearchResult`; modelo fora → mock marcado como simulado em vez de `indisponivel` |
| Privacidade | A exportação inclui contexto e autorização; a exclusão remove em cascata |
| Testes | Unitários e de integração nos padrões de `backend/tests`, que já rodam no deploy |

## 7. Fases

Cada fase termina com `next build` e lint limpos, testes passando e o fluxo conferido no navegador nas larguras de 390 px e de computador. Nenhuma fase retira uma tela antiga antes de a nova estar validada.

| # | Fase | Entrega | Verificação |
|---|---|---|---|
| 0 | **Fundação** | Dependências (`motion`, Phosphor, `next-intl`, slider); tokens do protótipo no `globals.css`, mais `--color-simulado`; `next/font`; `LazyMotion`; `inputModality`; `features.ts`; `pt-BR.json` com a estrutura; regra de lint de literais; Vitest no web | Build e lint; página de amostra interna com os tokens |
| 1 | **Primitivos** | Componentes da seção 3 (primitivos), com variantes iguais às do Figma | Página de catálogo interna (só em desenvolvimento), comparada com a página 03 do Figma |
| 2 | **Rotas e casca** | Route groups; layout raiz enxuto; Shell, Sidebar (com Menu, renomear e Desfazer), BarraTopo e `/chat/[id]`; histórico pela API; entrada do admin | Criar, renomear, apagar com Desfazer, voltar e avançar, recarregar a página |
| 3 | **Entrada e autorização** | Landing nova com Google; `/pending` e alertas; tela de autorização; backend da autorização; remoção do termo de uso; middleware | Primeiro acesso, usuário pendente, revogar em Meu contexto volta à porta, admin |
| 4 | **Composer e chat livre** | Composer completo (molde, fantasma, lista, profundidade visível e inerte); envio a `/api/search`; `Pensando`; `montarCartoes`; CardResultado com `Simulado`; BlocoTabela; avisos para os 5 status e o simulado; `simulado` no backend | Testes do `resolver` e do `montarCartoes`; buscas com o mock e as palavras-chave do mock (`fora do ar`, `apague`, `banana`, `nada`) |
| 5 | **Gavetas e seleção** | GavetaPerfil (única), Comparação, BarraSelecao, "Quero os currículos" | Teclado: foco preso, Esc e retorno do foco |
| 6 | **Meu contexto** | Tabelas e endpoints; gaveta com interesses, instruções e filtros (só E), disponibilidade; gravação adiada | Recarregar e reabrir mostra o que foi salvo; exportação de privacidade |
| 7 | **Perguntas guiadas e cards de ação** | Carga das perguntas; moldes e questionário vindos da API; cards "Buscar candidatos" e "Montar equipe" desabilitados | Tab abre o modal de perguntas; frase pela metade |
| 8 | **Filtros de escopo** | Painel de filtros com opções simuladas num provedor isolado; as tags escolhidas seguem na mensagem | Painel completo pelo teclado; troca do provedor não toca a tela |
| 9 | **Admin e acabamento** | Admin **redesenhado com os primitivos novos** (decidido em 22/10), telas de usuários, domínios, administradores, modelos e exemplos; retirada da UI antiga, do `next-themes`, do shadcn não usado e dos textos de protótipo; revisão de bundle e acessibilidade | Lighthouse e axe nas telas principais; tamanho dos chunks |

Nenhuma fase depende mais de decisão em aberto. As fases 6, 7 e 8 podem trocar de ordem; a 7 depende da revisão das perguntas geradas.

## 8. Testes e verificação

- **Web:** Vitest para os módulos puros: `resolver` e moldes, reducer da conversa, `montarCartoes`, gerador simulado e mensagens ICU com plural.
- **Testes de interface** com Testing Library nos componentes de teclado: Composer e Painel.
- **Backend:** testes de integração de autorização, contexto, perguntas e do campo `simulado`, na suíte que o deploy já roda.
- **Manual por fase:** navegador em 390 px e em computador, só com teclado, e com movimento reduzido ligado.
- **Comparação visual** com o protótipo rodando em paralelo (`npm run dev`, porta 5179).

## 9. Riscos e pontos de atenção

- **O deploy é automático no push para `main`.** Decidido em 22/10: o trabalho vai no branch `feat/nova-ui` do `chateau-expert` e só entra em `main` com o port fechado e validado.
- **Documentação desatualizada:** o `web/CLAUDE.md` diz "React 19", mas o `package.json` fixa 18.3.1. Corrigir na fase 0.
- **`eslint-config-next` 16 com Next 14:** conferir se o lint continua coerente ao adicionar regras.
- **Geração das perguntas a partir do rev_6:** o modelo Arrows tem nós, propriedades e o dicionário de sinônimos (`*_dic_fields.json`), mas não o texto das perguntas nem os rótulos das opções. Decidido em 22/10: um script gera a partir do modelo e do dicionário, usando os textos do protótipo como base, e o Marcelo revisa antes da carga.
- **`motion` com React 18:** compatível, conforme conferido em 20/10. A animação de saída com Radix Dialog exige `forceMount` controlado.
- **Grafo de produção sem rev_6:** os cartões terão muitos campos em vermelho até a carga (frente 2 do [todo](../todo.md)).

## 10. Decisões

Tomadas pelo Marcelo em 22/10/2026:

- **Entrega:** branch `feat/nova-ui` até fechar o port; nada vai para `main` (e produção) pela metade.
- **Parar:** aparece já; ao clicar, avisa que está em desenvolvimento e não interrompe a busca.
- **Admin:** redesenho com os primitivos novos, sem manter o shadcn por baixo.
- **Perguntas guiadas:** geradas por script a partir do rev_6 e do dicionário, com os textos do protótipo como base; o Marcelo revisa antes da carga.

- **Termo de uso:** sai por completo, sem guardar os aceites; o projeto ainda é só teste e avaliação, sem produção a preservar.
- **Acesso ao grafo:** backend e web sem acesso ao Neo4j; o que o modelo não trouxer fica simulado, inclusive as opções de filtro, até o Edson decidir.

Não há decisão pendente para começar.
