# Envio de e-mail pelo Workspace — 17/11/2026

## Contexto e decisão

A reunião de 12/11 indicou o Workspace como meio de envio, sem definir mensagens ou remetente. Em 17/11, o usuário confirmou que `chateau@iprj.uerj.br` é uma conta de e-mail do Workspace e pediu um primeiro envio manual no Admin: informar um e-mail e enviar uma mensagem padrão à conta cadastrada. O escopo inicial é testar a integração; avisos e alertas automáticos serão definidos depois.

No Expert, o Admin passa a ter a aba E-mail. Ela apresenta remetente, assunto e corpo fixos, e recebe apenas o endereço do destinatário. A API exige administrador com autorização de contexto, verifica que o endereço pertence a um usuário registrado e chama a Gmail API em nome da conta Chateau. Em 17/11, o usuário mostrou que o `.env.prod` contém `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`; depois informou ter obtido o refresh token e incluído `CHATEAU_MAIL_REFRESH_TOKEN` no servidor. Isso não foi verificado diretamente, pois o acesso SSH deste ambiente foi recusado. Falta validar um envio real. O aceite pela Gmail API não prova entrega na caixa de destino. O envio não altera o status de acesso.

## Configuração pendente

A API usa por padrão `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` já existentes para o login, ou um cliente próprio se as duas variáveis `CHATEAU_MAIL_CLIENT_*` forem configuradas. O OAuth do login NextAuth atual não concede permissão para enviar e-mail; a autorização do remetente é separada. Após a publicação, fazer um envio a um usuário cadastrado, conferir recebimento e pasta Enviados, e observar bloqueios do Workspace. O usuário autorizou commit, push e deploy em 17/11; a validação real permanece pendente.

Fontes de código verificadas: Expert `8a6ab8e` antes das alterações e implementação no Expert `5e963c2` em 17/11/2026; documentação da raiz em seu checkout de 17/11/2026.
