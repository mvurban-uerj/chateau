# Produção

- **Site:** <http://chateau2.duckdns.org:8080> — é o `NEXTAUTH_URL` do `.env.prod`; o login Google só funciona por este endereço.
- **Protótipo local:** `/mnt/c/temp/chateau/ui`, executado com Vite em <http://localhost:5179/>. Uma cópia publicada por engano no Sites em 26/10/2026 foi substituída por uma página de encerramento; o endereço continua privado e não é uma demonstração ativa.
- **Servidor:** `prointec@152.92.2.63`, diretório `/opt/apps/chateau-expert`, atrás do firewall da faculdade. Serviços internos (Neo4j, orchestration) só em `127.0.0.1`, acessados por túnel SSH ([Neo4j](../neo4j/README.md)).
- **Deploy:** push para `main` do `chateau-expert` roda o [workflow](../../chateau-expert/.github/workflows/deploy.yml) (testes do backend e da web → checagem de espaço → `git reset --hard origin/main` → [script de deploy](../../chateau-expert/scripts/deploy-prod.sh), que constrói os serviços alterados e sobe o Compose). Acompanhar na aba Actions do GitHub. O último deploy bem-sucedido fica registrado no arquivo local `.deploy-successful-sha` do servidor.
- **Variáveis:** `.env.prod` no servidor, fora do Git. `INTERNAL_API_TOKEN` foi gerado lá em 20/10/2026 ([acesso](../../dominio/negocio/acesso.md#autorização-na-api)).

Conferir containers e log da API no servidor:

```bash
cd /opt/apps/chateau-expert && docker compose -f docker-compose.prod.yml ps && docker logs --tail 20 chateau_api
```

O deploy de 26/10/2026 falhou por falta de espaço em `/tmp` depois do build das imagens; ver [análise](../analises/deploy-2026-10-26.md). Se o workflow parar na checagem de espaço, inspecionar `df -h /tmp /var/lib/docker`, `docker system df` e o tamanho de `/var/log` e dos volumes antes de ampliar o disco ou remover dados. **Não apagar volumes Docker ou diretórios em `backend/volumes/`**: eles contêm bancos de dados.

Registrado em 20/10/2026; o endereço é configuração do servidor, conferir o `NEXTAUTH_URL` se deixar de responder.
