# Privacidade na autorização — 12/11/2026

## Pedido e decisão

O link da Política de Privacidade estava na entrada, separado da autorização de contexto. O pedido foi colocá-lo como item obrigatório nessa tela, com marcação feita pela pessoa, sem valor inicial marcado. A dúvida era como evitar que a exigência passasse despercebida.

A tela passa a mostrar a confirmação em um bloco próprio, com link para a política em outra aba, a instrução de que ela é necessária para ambos os botões e foco com aviso junto à caixa se alguém tentar continuar sem marcá-la. Os campos de nome e unidade continuam marcados por serem necessários à busca; a confirmação de privacidade tem comportamento diferente e inicia sempre desmarcada.

O backend exige a confirmação no envio e registra sua data em `ContextAuthorization.privacyAcknowledgedAt`. Registros antigos recebem `NULL` pela migração e voltam à tela de autorização ao tentar acessar o aplicativo. A data anterior é preservada em caso de revogação; na nova autorização, uma nova marcação atualiza a data. A página da política continua pública.

## Estado local

Implementado no `chateau-expert` `7a1027a`, enviado a `main` e `deploy` em 12/11/2026. Antes do envio, passaram 98 testes do backend e 176 do web; build do backend e do web também passaram localmente. O push em `deploy` é o gatilho configurado do workflow, mas sua execução, a publicação e a conferência funcional em produção ainda não foram confirmadas nesta sessão. A revisão jurídica da política e a divergência sobre retenção de logs continuam pendentes, conforme [regra vigente](../../dominio/negocio/termos-e-privacidade.md).
