# Neo4j

## Onde roda

O grafo compartilhado fica no servidor da faculdade (`152.92.2.63`, diretório `/opt/apps/chateau-expert`) no serviço `neo4j` de `docker-compose.prod.yml`. A máquina local pode subir um Neo4j **de exemplo** pelo perfil `ia` de `docker-compose.yml`, em `chateau_neo4j_exemplo`; ele é separado do servidor e não tem volume persistente declarado. Para testar o Admin local sem executar a carga automática de exemplo, suba explicitamente os serviços necessários:

```bash
cd chateau-expert
docker compose --profile ia up -d db neo4j-exemplo api web caddy
```

Depois acesse `http://localhost:5000/admin/graph` com uma conta administradora. Selecionar um arquivo apenas mostra o nome; o upload e a importação começam após clicar **Importar** e confirmar. A API local aponta para `bolt://neo4j-exemplo:7687` e a pasta local de arquivos é `chateau-expert/graph-imports/`. O Neo4j local de exemplo começa vazio quando criado assim; a carga automática `neo4j-exemplo-carga` não participa desse comando.

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

## Rodar cypher-shell da sua máquina (via túnel), sem instalar nada

Com o túnel SSH aberto (`ssh -L 7474:localhost:7474 -L 7687:localhost:7687 prointec@152.92.2.63`), dá pra rodar `cypher-shell` local via Docker, sem precisar copiar/colar no Browser nem instalar o cliente:

```bash
docker run --rm -i neo4j:5-community \
  cypher-shell -a neo4j://host.docker.internal:7687 -u neo4j -p 'SENHA_DO_ENV_PROD' \
  < arquivo.cypher
```

**Pegadinha (Docker Desktop no WSL2):** se o `docker info` mostrar `Operating System: Docker Desktop`, o container roda numa VM separada da distro WSL2 — `--network host` conecta na rede *dessa VM*, não na distro onde o túnel SSH está escutando em `127.0.0.1:7687`. Isso dá "connection refused" mesmo com o túnel ativo. A correção é usar `host.docker.internal` (hostname que o Docker Desktop expõe pra alcançar o host real) em vez de `--network host` + `localhost`. Confirmar com `docker run --rm alpine sh -c "apk add --no-cache netcat-openbsd >/dev/null; nc -zv host.docker.internal 7687"`.

Alternativa sem essa pegadinha: `scp` o `.cypher` pro servidor e rodar `docker exec -i chateau_neo4j cypher-shell ...` direto lá (mesmo padrão da seção "Comandos úteis" acima) — nesse caso não tem VM extra no meio.
