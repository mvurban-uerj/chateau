# Envio de e-mail pelo Workspace — 17/11/2026

## Contexto e decisão

A reunião de 12/11 indicou o Workspace como meio de envio, sem definir mensagens ou remetente. Em 17/11, o usuário confirmou que `chateau@iprj.uerj.br` é uma conta de e-mail do Workspace e pediu um primeiro envio manual no Admin: informar um e-mail e enviar uma mensagem padrão à conta cadastrada. O escopo inicial é testar a integração; avisos e alertas automáticos serão definidos depois.

No Expert, o Admin passa a ter a aba E-mail. Ela apresenta remetente, assunto e corpo fixos, e recebe apenas o endereço do destinatário. A API exige administrador com autorização de contexto, verifica que o endereço pertence a um usuário registrado e chama a Gmail API. Em 17/11, o usuário mostrou que o `.env.prod` contém `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`; depois informou ter obtido o refresh token e incluído `CHATEAU_MAIL_REFRESH_TOKEN` no servidor. Isso não foi verificado diretamente, pois o acesso SSH deste ambiente foi recusado. O primeiro envio real chegou, mas saiu da conta errada, conforme o diagnóstico abaixo. O envio não altera o status de acesso.

## Configuração pendente

A API usa por padrão `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` já existentes para o login, ou um cliente próprio se as duas variáveis `CHATEAU_MAIL_CLIENT_*` forem configuradas. O OAuth do login NextAuth atual não concede permissão para enviar e-mail; a autorização do remetente é separada. O usuário autorizou o primeiro commit, push e deploy em 17/11. A rotação do segredo OAuth exibido na conversa ainda não foi confirmada.

## Resultado do primeiro envio real

Após a publicação do Expert `5e963c2`, o usuário informou que o e-mail chegou, porém com remetente `marcelo.vendas`, não `chateau@iprj.uerj.br`. O refresh token pertencia à conta que enviou. A chamada original usava `users/me/messages/send`, e o cabeçalho `From` sozinho não garantiu a caixa de origem. A correção troca `me` pelo endereço explícito da conta Chateau na rota da Gmail API, para que um token de outra caixa seja recusado. O usuário substituiu o token após autenticar na conta Chateau e informou que o envio funcionou. A correção foi enviada no Expert `17114b6` a `main` e `deploy`; conclusão do workflow pendente. A confirmação do remetente correto é relato do usuário, não validação direta neste ambiente.

Fontes de código verificadas: Expert `8a6ab8e` antes das alterações e implementação no Expert `5e963c2` em 17/11/2026; documentação da raiz em seu checkout de 17/11/2026.
