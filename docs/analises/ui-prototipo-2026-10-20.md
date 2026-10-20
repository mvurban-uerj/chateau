# Nova UI — inspeção inicial, 20/10/2026

## Origem e execução isolada

- Código recebido em `/mnt/c/temp/chateau/ui` (fora dos repositórios do projeto).
- React 19, Vite 8, TypeScript, Tailwind 4, Motion, Radix Slider e Phosphor Icons.
- Instalação: `npm ci`. Execução: `npm run dev -- --host 0.0.0.0`, porta 5179, `http://localhost:5179/`.
- `npm run build` passou. `npm run lint` terminou sem erros, com avisos em `Shell.tsx`, `ChatView.tsx` e `Composer.tsx`. O build avisou sobre um chunk JS maior que 500 kB. `npm audit --omit=dev` encontrou uma vulnerabilidade alta na dependência indireta `source-map-js` (< 1.2.2); há correção disponível, a aplicar e testar antes da integração.

## O que o protótipo implementa

- Landing, tela de consentimento, chat, histórico, perguntas guiadas, níveis de profundidade, filtros de escopo, contexto do usuário, resultados e gavetas de perfil/comparação.
- Respostas de busca são calculadas sobre dados simulados em `src/data.ts`; as etapas de espera usam temporizadores em `src/views/Shell.tsx`.
- Histórico, contexto e consentimento são guardados no `localStorage` do navegador.
- `src/features.ts` desativa controles sem implementação correspondente, entre eles upload de edital, busca no histórico, página sobre o projeto, uso de documentos na busca, links de termos/privacidade e três ações especializadas.

## Diferenças para o web atual

| Área | Web atual (`chateau-expert/web`) | Protótipo |
|---|---|---|
| Aplicação | Next.js com rotas e API intermediária | SPA Vite |
| Entrada | Google OAuth/NextAuth, autorização e termos no servidor | Entrada demonstrativa e consentimento no navegador |
| Busca | `POST /api/search`, resposta `SearchResult` | `runSearch` sobre registros mockados |
| Conversas | API `/api/chats` e dados do backend | Estado React e `localStorage` |
| Administração | Rotas `/admin` | Não há equivalente inspecionado |

Fontes: `chateau-expert/web/src/middleware.ts`, `web/src/app/api/search/route.ts`, `web/src/app/api/chats/route.ts`, `web/src/types/search.ts` e os arquivos citados do protótipo.

## Decisões de 20/10/2026

Tomadas pelo Marcelo após a revisão de divergências pré-integração.

1. **Dados do perfil:** cargo, vínculo, carreira, unidade, campus, prêmios, disciplinas, coordenação de projetos e demais campos exibidos pelo protótipo virão do grafo gerado em Cypher pelo `chateau-data` no modelo `rev_6_training`, padrão vigente. As referências à rev_5 no código do protótipo devem ser lidas como rev_6 no port. O grafo hoje carregado em produção ainda não tem esses campos (schema extraído em 28/09: sem `Job`, `Role`, `WORKS`, `TAUGHT`, `COORDINATES`, `Campus`, `Acknowledgment`).
2. **Resultado da busca:** ranqueamento, aderência, justificativas, caminho no grafo, cobertura e equipe virão do modelo de IA consultando esse grafo, não de regras do backend. O transporte continua o da infraestrutura atual: web → API → orquestração (a orquestração só é alcançável pela rede interna e a API é o único caminho autenticado).
3. **Port:** os componentes do protótipo serão portados para `chateau-expert/web`, com a interface **visualmente idêntica**. Prevalecem a infraestrutura e as versões do projeto (Next.js 14, React 18, NextAuth, API Express): o protótipo é adaptado ao nosso código, não o contrário. O port é um passo posterior; antes, levantar tudo o que é necessário.
4. **Consentimento:** vale o aceite registrado no PostgreSQL (`Term`/`Account.acceptedTermId`). A tela de consentimento do protótipo passa a representar esse aceite; o `localStorage` deixa de valer como consentimento.
5. **Contexto do usuário:** permanece no navegador (`localStorage`) até se definir sua origem.
6. **Controles sem funcionalidade:** a aparência segue o protótipo; o comportamento é o que já existe. Controle sem efeito real (ex.: seletor de modelo de IA) continua sem efeito.
7. **Versionamento:** o diretório `/mnt/c/temp/chateau/ui` é a versão final do protótipo e não será versionado; serve de referência para o port.

As frentes e tarefas decorrentes estão em [todo.md](../todo.md).

## Próximo passo após avaliação conjunta

1. Avaliar visualmente e percorrer os fluxos da UI isolada. Registrar decisões e conceitos do Figma, com fonte e estado de validação.
2. Definir o mapa de telas e contratos entre o protótipo e as rotas/API atuais, inclusive estados vazios, erros, permissões e persistência de conversas.
3. Adaptar componentes ao web Next.js preservando autenticação, autorização, termos, administração e dados reais. Validar cada fluxo integrado antes de retirar a interface anterior.

Decidido em 20/10/2026 portar o protótipo para o web atual (ver acima). Regras expressas no código do protótipo (ex.: derivação de vínculo por `vinculoDe`, montagem de equipe, níveis de profundidade) continuam **não confirmadas** como regras do domínio: passam a ser responsabilidade do modelo de IA ou precisam de decisão própria.
