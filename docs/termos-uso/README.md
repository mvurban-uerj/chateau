> **Histórico.** Decidido em 22/10/2026: o termo de uso sai por completo, sem guardar aceites, substituído pela autorização de contexto. Regra vigente em [termos e privacidade](../../dominio/negocio/termos-e-privacidade.md). Este documento descreve o código atual até a remoção.

# Termos de Uso

A página `/termos-uso` (e as demais telas que exibem o termo — aceite em
`/terms` e visualização em `/admin/terms`) mostra o **último termo de uso
cadastrado no banco** (tabela `Term`, via `GET /api/terms/latest`), não
mais um texto fixo no código. Se não houver nenhum termo cadastrado, a
página mostra "Nenhum termo de uso cadastrado" e o link some da home.

O campo `content` do termo aceita **Markdown** (`#`/`##` para títulos,
`**negrito**`, listas com `-`), renderizado pelo componente
`MarkdownContent` (`web/src/components/markdown-content.tsx`).

Cadastre o primeiro termo em `/admin/terms`. O arquivo
[`termo-de-uso-exemplo.md`](./termo-de-uso-exemplo.md) neste diretório traz
o texto que estava fixo no código antes dessa mudança, já em Markdown —
pode ser colado direto no campo "Conteúdo do termo de uso".
