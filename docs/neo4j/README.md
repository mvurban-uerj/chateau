# Neo4j

## Onde roda

Só existe em **produção**, no servidor interno da faculdade (`152.92.2.63`, diretório `/opt/apps/chateau-expert`). Não está no `docker-compose.yml` local, só no `docker-compose.prod.yml` do `chateau-expert`.

| Item | Valor |
|---|---|
| Container | `chateau_neo4j` |
| Imagem | `neo4j:5-community` |
| Plugin | APOC |
| Rede Docker | `backend_net` |
| Dados | `backend/volumes/neo4j/{data,logs,import,plugins}` (fora do git) |
| Portas no host | `7474` (HTTP/Browser) e `7687` (Bolt) — publicadas só em `127.0.0.1` |
| Senha | variável `NEO4J_PASSWORD` em `.env.prod` no servidor |

## Por que não é acessível direto por IP

O servidor fica atrás do firewall de borda da faculdade, que só libera as portas já usadas pelo site — pedir liberação de portas novas depende do TI e pode não ser aprovado. Por isso o Neo4j foi configurado pra escutar só em `127.0.0.1` do host, sem exposição na rede. Acesso é via túnel SSH.

## Como acessar

Do seu computador (não pelo servidor):

```bash
ssh -L 7474:localhost:7474 -L 7687:localhost:7687 prointec@152.92.2.63
```

Mantenha esse terminal aberto. Com o túnel ativo, abra `http://localhost:7474` no navegador:

- Usuário: `neo4j`
- Senha: a que está em `NEO4J_PASSWORD` no `.env.prod` do servidor
- URL de conexão no Browser: `neo4j://localhost:7687`

## Comandos úteis (rodando no servidor, dentro de `/opt/apps/chateau-expert`)

```bash
# subir/recriar o serviço
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --force-recreate neo4j

# logs
docker compose -f docker-compose.prod.yml --env-file .env.prod logs neo4j

# testar login direto, sem precisar do túnel
docker exec -it chateau_neo4j cypher-shell -u neo4j -p 'SENHA_DO_ENV_PROD' "RETURN 1;"
```

> Todo comando de produção precisa do `--env-file .env.prod`. Sem ele, o compose cai no `.env` de dev (ou fica em branco) e o container sobe com variáveis erradas silenciosamente — só avisa via `WARN` no log, não dá erro.

## Pegadinha de formatação do `.env.prod`

O parser de env-file do Docker Compose não tolera espaços no início da linha (`  NEO4J_PASSWORD=...` em vez de `NEO4J_PASSWORD=...`) — o nome da variável vira `"  NEO4J_PASSWORD"` e o compose não encontra `${NEO4J_PASSWORD}`, caindo em branco silenciosamente. Se algum `WARN` de variável "not set" aparecer sem explicação, checar com:

```bash
cat -A .env.prod | grep NOME_DA_VARIAVEL
```
