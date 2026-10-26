# Produção

- **Site:** <http://chateau2.duckdns.org:8080> — é o `NEXTAUTH_URL` do `.env.prod`; o login Google só funciona por este endereço.
- **Protótipo local:** `/mnt/c/temp/chateau/ui`, executado com Vite em <http://localhost:5179/>. Uma cópia publicada por engano no Sites em 26/10/2026 foi substituída por uma página de encerramento; o endereço continua privado e não é uma demonstração ativa.
- **Servidor:** `prointec@152.92.2.63`, diretório `/opt/apps/chateau-expert`, atrás do firewall da faculdade. Serviços internos (Neo4j, orchestration) só em `127.0.0.1`, acessados por túnel SSH ([Neo4j](../neo4j/README.md)).
- **Deploy:** push para `main` do `chateau-expert` roda o [workflow](../../chateau-expert/.github/workflows/deploy.yml) (testes do backend → `git reset --hard origin/main` → `docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build`). Acompanhar na aba Actions do GitHub.
- **Variáveis:** `.env.prod` no servidor, fora do Git. `INTERNAL_API_TOKEN` foi gerado lá em 20/10/2026 ([acesso](../../dominio/negocio/acesso.md#autorização-na-api)).

Conferir containers e log da API no servidor:

```bash
cd /opt/apps/chateau-expert && docker compose -f docker-compose.prod.yml ps && docker logs --tail 20 chateau_api
```

Registrado em 20/10/2026; o endereço é configuração do servidor, conferir o `NEXTAUTH_URL` se deixar de responder.
