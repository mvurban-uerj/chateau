# Avisos de pedido de acesso — 17/11/2026

O usuário pediu e-mails aos administradores quando alguém solicita acesso, confirmação da análise ao solicitante e comunicação da aprovação ou recusa, com logo Chateau e apresentação formatada. O fluxo existente cria a conta como `PENDING` no primeiro login e já informa na tela pendente que o pedido foi recebido. A implementação local usa esse primeiro login como pedido. Conta já autorizada por domínio ou com papel administrativo não gera o pedido. O campo `accessRequestNotifiedAt` evita reenvio em logins seguintes, inclusive simultâneos.

Cada `ADMIN` e `SUPERADMIN` recebe uma mensagem individual com nome, e-mail e link para `/admin/authorize-users`. O usuário recebe confirmação da análise. Uma alteração efetiva para `APPROVED` ou `DENIED` envia a decisão ao usuário; gravações sem mudança não repetem o aviso. Os quatro tipos de aviso usam HTML com CSS embutido, versão texto e PNG do logo gerado a partir do componente vetorial do próprio projeto. O logo é parte MIME inline, sem depender de imagem externa. O link público usa `NEXTAUTH_URL` quando válida.

O envio usa a conta `chateau@iprj.uerj.br` e as credenciais Workspace já configuradas para o teste manual. Falhas são registradas no log, mas não revertem o login nem a decisão de acesso. A marcação do pedido ocorre antes do envio para impedir duplicatas; logo, não há retentativa automática em caso de falha. O aceite pela Gmail API não comprova entrega na caixa de entrada. Uma fila persistente é trabalho posterior caso a operação exija garantia de entrega.

O envio manual da aba E-mail também passou a usar o mesmo layout HTML e logo, mantendo o assunto e o texto fixos originais como alternativa em texto.

Verificação local: build TypeScript, migração no PostgreSQL de testes, 106 testes do backend, 177 testes da web, build Docker da API com logo e testes de integração de pedido, deduplicação, domínio autorizado, decisão e conteúdo MIME. O Expert `17114b6` foi enviado a `main` e `deploy` em 17/11/2026. A conclusão do workflow e a validação real em produção ainda não foram confirmadas.
