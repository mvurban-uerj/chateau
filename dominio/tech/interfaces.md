# Interfaces gráficas

## Web atual — implementado

`chateau-expert/web` é Next.js com Google OAuth/NextAuth, middleware de acesso, landing, home, chat, área administrativa, aceite de termos e privacidade. O chat usa as APIs intermediárias `/api/chats` e `/api/search`. O servidor, não o navegador, acrescenta o e-mail da sessão nas chamadas principais. O catálogo `AiModel` aparece no seletor visual, mas a busca atual envia só `{pergunta}`.

## Protótipo novo — isolado

`/mnt/c/temp/chateau/ui` é React/Vite, com landing, consentimento, chat, histórico, contexto, filtros, profundidade, resultados e gavetas. A busca usa registros simulados em `src/data.ts`; não chama o backend. Histórico, contexto e consentimento ficam em `localStorage`. `src/features.ts` desativa controles ainda sem comportamento correspondente. Seu login é demonstrativo.

O protótipo será avaliado com o usuário e com o projeto Figma antes da substituição. Na integração, autenticação, autorização, termos, administração, API real e persistência de conversas do Expert continuam sendo contratos a cumprir; o comportamento simulado não os altera.

Fontes: [web atual](../../chateau-expert/web/src/app/), [análise do protótipo](../../docs/analises/ui-prototipo-2026-10-20.md). O caminho do protótipo é local e deverá ganhar referência versionada antes da integração.
