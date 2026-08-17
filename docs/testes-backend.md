# Testes Automatizados Do Backend

## Objetivo

Os testes automatizados do backend garantem que as principais regras de negócio da API continuem funcionando após alterações no código. Eles validam endpoints REST, regras de autorização, persistência no banco, migrations do Prisma e comportamentos críticos do sistema.

Na prática, a suíte ajuda a responder: "se fizermos uma mudança hoje, quebramos login, administração, chats, termos de uso, LGPD ou outras funcionalidades?"

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Node.js + TypeScript | Linguagem/runtime do backend |
| Express | Framework HTTP da API |
| Prisma | ORM e camada de acesso ao PostgreSQL |
| PostgreSQL 16 | Banco real usado nos testes de integração |
| Vitest | Runner de testes e biblioteca de assertions |
| Supertest | Chamada dos endpoints Express sem abrir servidor HTTP real |
| Docker | Sobe um banco PostgreSQL isolado para testes |
| GitHub Actions | Executa build e testes antes do deploy |

## Estratégia

A estratégia combina testes unitários e testes de integração.

### Testes unitários

Testam funções puras, sem depender de HTTP nem banco de dados.

Exemplo: normalização e validação de domínios em `backend/src/lib/domain.ts`.

Esses testes são rápidos e ajudam a validar regras pequenas e determinísticas.

### Testes de integração HTTP

Testam a API como o frontend usaria: fazendo requisições para os endpoints.

O `Supertest` chama o app Express diretamente em memória, sem precisar iniciar `npm run dev` nem abrir a porta `3001`.

Exemplo:

```bash
POST /api/auth/sign-in
GET /api/users/pending
POST /api/chats
DELETE /api/privacy/account
```

### Testes com banco real

Em vez de simular o Prisma com mocks, os testes usam um PostgreSQL real em Docker. Isso é importante porque várias falhas só aparecem com banco real:

- constraints de unicidade;
- relações entre tabelas;
- cascatas de deleção;
- migrations;
- transações;
- queries Prisma;
- erros reais como registro não encontrado ou conflito de email.

Essa abordagem é comum em projetos que usam ORM e banco relacional, porque aumenta a confiança de que a aplicação funciona no ambiente real.

## Funcionalidades Cobertas

A suíte cobre as principais áreas do backend:

| Área | O que é validado |
|---|---|
| Health check | API responde em `/health` |
| Auth | login, sessão, aceite de termos, usuário aprovado, domínio autorizado e superadmin |
| Users | busca, pendentes e atualização de status de acesso |
| Admins | criação, listagem, busca, promoção, rebaixamento e proteção de superadmin |
| Domains | criação, normalização, validação, duplicidade, atualização e remoção |
| Terms | criação sequencial de versões, listagem e termo mais recente |
| Access | contagem de login, visita, chat query e média de tempo de resposta |
| Chats | criação, leitura, atualização, renomeação, remoção e isolamento entre usuários |
| Search examples | CRUD e tratamento de registros inexistentes |
| AI models | CRUD, ordenação por versão e conflitos |
| Privacy/LGPD | exportação de dados, exclusão de conta, bloqueio de superadmin e limpeza de logs |

## Como Rodar

O comando principal deve ser executado a partir da raiz do projeto:

```bash
npm run test
```

Esse comando automatiza o fluxo completo:

1. verifica se o Docker está disponível;
2. verifica se o container `chateau_test_db` existe;
3. cria o PostgreSQL de teste se ele ainda não existir;
4. inicia o container se ele estiver parado;
5. espera o banco aceitar conexões;
6. gera o Prisma Client;
7. aplica as migrations no banco de teste;
8. executa os testes automatizados.

Também é possível rodar um arquivo específico:

```bash
npm run test -- tests/integration/remaining-routes.test.ts
```

O banco usado nos testes é separado do banco de desenvolvimento. Por padrão:

```text
postgresql://postgres:postgres@localhost:55432/chateau_test
```

## Onde Estão Os Arquivos

| Caminho | Descrição |
|---|---|
| `backend/vitest.config.ts` | Configuração do Vitest |
| `backend/scripts/test-integration.sh` | Script que prepara banco e roda testes |
| `backend/tests/setup.ts` | Limpa o banco e cria roles base antes dos testes |
| `backend/tests/setup-db.ts` | Aplica migrations no banco de teste |
| `backend/tests/factories.ts` | Helpers para criar usuários, roles, termos, chats etc. |
| `backend/tests/unit/` | Testes unitários |
| `backend/tests/integration/` | Testes de integração HTTP |
| `.github/workflows/deploy.yml` | CI que roda testes antes do deploy |

## Fluxo No CI/CD

No GitHub Actions, antes do deploy, existe um job de validação do backend.

Esse job:

1. sobe um PostgreSQL de teste;
2. instala dependências;
3. gera o Prisma Client;
4. aplica migrations;
5. roda o build TypeScript;
6. executa os testes.

O deploy só roda se essa etapa passar. Isso reduz o risco de enviar para produção código que não compila ou que quebra funcionalidades críticas.

## Boas Práticas Aplicadas

- O banco de teste é isolado do banco local e de produção.
- Os dados são limpos entre os testes para evitar dependência de ordem.
- As roles base (`USER`, `ADMIN`, `SUPERADMIN`) são recriadas no setup.
- Testes de erro validam status HTTP esperados, como `400`, `403`, `404` e `409`.
- A API é testada via HTTP, aproximando o teste do uso real pelo frontend.
- O Prisma não é mockado nos testes de integração, preservando validação real de queries e constraints.
- Logs esperados do Prisma são silenciados em `NODE_ENV=test` para manter a saída limpa.

## Resumo Para Apresentação

O backend possui uma suíte de testes automatizados com Vitest, Supertest, Prisma e PostgreSQL em Docker. Os testes rodam contra um banco real isolado, aplicam as migrations antes da execução e cobrem os principais fluxos da API. Localmente, a equipe executa tudo com `npm run test` na raiz do projeto. No GitHub Actions, os testes e o build são executados antes do deploy, impedindo publicação automática caso alguma funcionalidade crítica quebre.
