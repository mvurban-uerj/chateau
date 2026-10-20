# Termos e tratamento de dados na aplicação

**Estado implementado; a interpretação jurídica ainda exige validação própria.** O termo exibido pela aplicação vem do registro `Term` mais recente no PostgreSQL, renderizado em Markdown. `Account.acceptedTermId` guarda qual termo a conta aceitou. Sem termo cadastrado, a sessão considera o requisito satisfeito; `SUPERADMIN` é dispensado do aceite. Criar termo novo requer novo aceite dos demais usuários em rotas protegidas.

A página `/privacidade` descreve dados de conta, conversas, aceite e registros de acesso. O web oferece exportação dos dados da conta autenticada e exclusão da conta. O backend exporta perfil, papéis, termo aceito, conversas e registros de acesso; a exclusão remove o usuário e dados relacionados em cascata, exceto que contas `SUPERADMIN` são protegidas contra exclusão por essa rota.

**Consentimento (decidido em 20/10/2026):** o consentimento válido é o aceite registrado no PostgreSQL. A tela de consentimento da nova UI representa esse aceite; consentimento guardado só no navegador não tem valor.

Os registros de acesso distinguem `LOGIN`, `HOME_VISIT` e `CHAT_QUERY`; visita à home conta no máximo uma vez por usuário/dia, e consultas podem guardar tempo de resposta. O código contém uma função para eliminar logs com mais de 90 dias, mas não foi encontrada chamada a essa função; a página pública informa retenção de até seis meses. **Não há prazo operacional confirmado** até resolver a divergência.

Fontes: [serviço de autenticação](../../chateau-expert/backend/src/services/auth.service.ts), [serviço de privacidade](../../chateau-expert/backend/src/services/privacy.service.ts), [serviço de acessos](../../chateau-expert/backend/src/services/access.service.ts), [página pública](../../chateau-expert/web/src/app/privacidade/page.tsx), [termos](../../docs/termos-uso/README.md). A afirmação sobre dispensa geral de LGPD no [README do Data](../../chateau-data/README.md) está em [divergências](../../docs/analises/divergencias-2026-10-20.md) e não foi adotada como regra.
