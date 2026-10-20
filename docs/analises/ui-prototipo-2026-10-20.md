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

## Próximo passo após avaliação conjunta

1. Avaliar visualmente e percorrer os fluxos da UI isolada. Registrar decisões e conceitos do Figma, com fonte e estado de validação.
2. Definir o mapa de telas e contratos entre o protótipo e as rotas/API atuais, inclusive estados vazios, erros, permissões e persistência de conversas.
3. Adaptar componentes ao web Next.js preservando autenticação, autorização, termos, administração e dados reais. Validar cada fluxo integrado antes de retirar a interface anterior.

Ainda não há decisão de substituir o web atual nem de tratar regras expressas no código do protótipo como regras confirmadas do domínio.
