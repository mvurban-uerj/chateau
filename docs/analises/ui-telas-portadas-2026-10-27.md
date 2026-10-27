# Inventário das telas da UI portada — 27/10/2026

Conferência estática do protótipo em `/mnt/c/temp/chateau/ui` e de `chateau-expert` `dc77c53`. O protótipo é uma SPA com etapas em estado; o Expert usa rotas Next.js, sessão Google e APIs próprias. Este mapa descreve o código, não valida aparência ou comportamento em produção.

| Tela ou parte do protótipo | Destino atual no Expert | Estado e dependência |
|---|---|---|
| `views/Login.tsx` | `/` → `entrada/Entrar.tsx` | Visual portado; login real via Google/NextAuth. `/pending` e `/alerts/restrictedAccess` usam `entrada/Porta.tsx` para acesso pendente/restrito, sem tela correspondente no protótipo. |
| `views/ConsentGate.tsx`, `consent.ts` | `/autorizacao` → `entrada/FormAutorizacao.tsx` | Autorização real no PostgreSQL, ligada à conta; revogação em Meu contexto. Substitui o termo de uso. |
| `views/Shell.tsx`, `components/Sidebar.tsx` | Layout de `/chat` e `/admin` → `shell/Shell.tsx`, `Sidebar.tsx`, `BarraTopo.tsx`, `HistoricoProvider.tsx` | Histórico real via `/api/chats`, rota `/chat/[id]`, renomear, apagar e Desfazer. Entrada de admin adicionada à sidebar. |
| `components/ChatView.tsx` | `/chat`, `/chat/[id]` → `conversa/ConversaAoVivo.tsx`, `Resposta.tsx`, `Pensando.tsx`, `BolhaUsuario.tsx` | Perguntas passam por `/api/search`; mensagens persistem em `/api/chats`. O backend pode responder com dados simulados. Etapas reais de busca e Parar/Retomar dependem do modelo. |
| Ações iniciais em `ChatView.tsx` e `flows/*.ts` | `conversa/CardsAcao.tsx` | Buscar candidatos e Montar equipe aparecem desabilitados. Fluxos especializados do protótipo não foram portados; texto livre e moldes guiados continuam acessíveis pelo campo. |
| `components/Composer.tsx`, `templates.ts`, `components/DepthSlider.tsx` | `conversa/Composer.tsx`, `ModalPerguntas.tsx`, `Moldes.tsx`; dados de contexto e perguntas do PostgreSQL | Texto livre, Tab, modal e filtros visuais portados. Opções de filtro são simuladas; nível visual vem do catálogo de modelos, mas não muda a busca. Perguntas guiadas têm opções fixas validadas contra o modelo rev_6, sem consulta aos valores carregados. |
| `components/ResultCard.tsx` | `resultado/CartaoResultado.tsx`, `conversa/Resposta.tsx` | Linhas reconhecidas como pessoas viram cartões; outras viram `BlocoTabela.tsx`. Campos não recebidos são preenchidos com dados determinísticos simulados e marcados em vermelho. |
| `components/ProfileDrawer.tsx`, `CompareDrawer.tsx` | `resultado/GavetaPerfil.tsx`, `Comparacao.tsx`, `BlocoCobertura.tsx`, `Curriculos.tsx`; seleção em `conversa/BarraSelecao.tsx` | Gaveta, comparação e pedido de currículos portados; cada campo conserva a marcação de simulação. Dados completos dependem da carga rev_6 e do contrato de resposta do modelo. |
| `components/ContextDrawer.tsx`, `context.ts` | `contexto/GavetaContexto.tsx`, `/api/contexto`, `/api/autorizacao` | Perfil, objetivo, disponibilidade, interesses, instruções e filtros persistidos no PostgreSQL. Ainda não entram no pedido ao modelo. |
| Links de privacidade do login/contexto | `/privacidade` e `/api/privacy` | Página, exportação e exclusão existem; texto jurídico e retenção de logs ainda requerem decisão. |
| Sem equivalente no protótipo | `/admin/authorize-users`, `/admin/domains`, `/admin/ai-models`, `/admin/search-examples`, `/admin/admins` | Administração redesenhada na casca nova; usa Server Actions e os dados do backend. Validar com uma conta administradora em produção. |

Os componentes visuais compartilhados do protótipo (`Logo`, `Modal`, movimento, campo e controles) foram adaptados em `web/src/components/chateau/primitivos/` e `web/src/lib/chateau/motion.ts`. Os controles ocultos pelo `features.ts` do protótipo não implicam entrega no Expert. O inventário de [campos rev_6](ui-campos-rev6-2026-10-27.md) separa valores do grafo, da resposta e da simulação.

## Lacunas que este inventário deixa abertas

- Comparação visual tela a tela em produção, inclusive 390 px, após o deploy de `dc77c53`.
- Verificar estados de erro, recusa, resultado vazio e modelo indisponível com respostas reais; a leitura do código não exercita todos esses caminhos.
- Confirmar com o Edson fonte real dos filtros e contrato estruturado para cartões, aderência, cobertura e equipe.
