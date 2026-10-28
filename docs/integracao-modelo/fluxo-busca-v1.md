# Fluxo de busca — versão 1 (28/10/2026)

**Fluxo implementado no Expert; validação com o modelo real ainda pendente.**

Exemplo ilustrativo: a pessoa pergunta **“Quantos livros existem?”** e escolhe no web um modelo cadastrado como disponível no Admin. O nome técnico e a URL abaixo são valores do cadastro, não valores fixos deste documento. O Cypher e o número de livros também são exemplos, não uma resposta medida em produção.

| Passo | De → para | O que é transmitido ou feito |
|---|---|---|
| 1 | Web → backend | Pergunta e nome técnico escolhido: `{ "pergunta": "Quantos livros existem?", "modelName": "<nome do Admin>" }`. O servidor web repassa ao backend o token interno e o e-mail da sessão. |
| 2 | Backend → Quarkus | O backend busca no Admin a URL do servidor do modelo e envia a pergunta, o e-mail da sessão, o nome técnico do modelo e a **URL do servidor do modelo**. |
| 3 | Quarkus → servidor do modelo de IA | Faz a chamada à URL cadastrada. O corpo enviado está abaixo. A URL é o destino da chamada, não um campo desse corpo. |
| 4 | Servidor do modelo de IA → Quarkus | Devolve uma resposta da qual o Quarkus lê `response`, por exemplo `MATCH (b:Book) RETURN count(b) AS total`. |
| 5 | Quarkus → Neo4j | Confere que o Cypher é de leitura e executa a consulta no grafo do Chateau. |
| 6 | Neo4j → Quarkus | Devolve as colunas e linhas, por exemplo `total = 42`. |
| 7 | Quarkus → backend | Devolve o Cypher, `resultado` com `colunas`, `linhas` e `truncado`, além de `avisos`, métricas e eventuais erros/recusa. |
| 8 | Backend → web | Classifica a resposta (`ok`, `sem_resultado`, `recusada`, `erro_consulta` ou `indisponivel`) e envia `status`, `mensagem`, `cypher`, `colunas`, `linhas`, `avisos`, `truncado`, `tempoMs` e `simulado`. O web apresenta o resultado e o Cypher. |

**Corpo enviado pelo Quarkus ao servidor do modelo:**

```json
{
  "model": "<nome técnico vindo do Admin>",
  "system": "<instrução fixa da orquestração>\n\nSchema:\n<conteúdo do arquivo de schema configurado na orquestração>",
  "prompt": "Quantos livros existem?",
  "stream": false,
  "options": { "temperature": 0, "num_predict": 512 }
}
```

O `prompt` é a pergunta original. `system` combina a instrução fixa com o schema; na configuração versionada de produção, o arquivo é [`schema_producao.txt`](../../chateau-expert/orchestration/schema/schema_producao.txt), uma fotografia que precisará ser reextraída depois da nova carga rev_6. O e-mail da pessoa fica na comunicação backend → Quarkus e no log da orquestração; não entra no corpo enviado ao servidor do modelo.

Sem modelo disponível, o backend usa uma resposta simulada e a chamada ao Quarkus não ocorre. Se o servidor do modelo falhar, o backend também pode devolver uma resposta simulada, marcada com `simulado`.

Fontes do contrato: [rota web](../../chateau-expert/web/src/app/api/search/route.ts), [backend](../../chateau-expert/backend/src/services/search.service.ts), [cliente da orquestração](../../chateau-expert/backend/src/lib/orchestration.ts), [Quarkus](../../chateau-expert/orchestration/quarkus/src/main/java/br/uerj/chateau/orchestration/ServicoBusca.java) e [envio ao servidor do modelo](../../chateau-expert/orchestration/quarkus/src/main/java/br/uerj/chateau/orchestration/GeradorGenerate.java).
