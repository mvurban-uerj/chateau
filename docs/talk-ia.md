# Anotações dos cenários simulados da busca

O plano de integração está em [docs/integracao-modelo/README.md](integracao-modelo/README.md).

As respostas abaixo são exemplos do mock da interface; não são resultados do modelo ou do Neo4j de produção.

## Quem pesquisa otimização?

```text
nome	instituicao	area	artigos
Ana Souza	UERJ/IPRJ	Modelagem Computacional	42
Carlos Lima	UFRJ	Aprendizado de Máquina	35
Beatriz Rocha	UFF	Otimização	28
Daniel Martins	PUC-Rio	Engenharia de Software	19
```

```cypher
MATCH (p:Person)-[:AFFILIATED_WITH]->(o:Organization)
RETURN p.name AS nome, o.acronym AS instituicao, p.area AS area, p.articles AS artigos
ORDER BY artigos DESC
```

## Bananas

Não encontrei resultados. A pergunta pode estar fora do escopo da base ou a consulta gerada pode não corresponder ao que você quis dizer — confira a consulta abaixo.

```text
total
0
```

```cypher
MATCH (b:Banana) RETURN count(b) AS total
```

## Nada

Não encontrei resultados. A pergunta pode estar fora do escopo da base ou a consulta gerada pode não corresponder ao que você quis dizer — confira a consulta abaixo.

```cypher
MATCH (p:Person {name: 'Ninguém'}) RETURN p.name AS nome
```

## Apague

Esta pergunta gerou uma consulta que altera dados e foi bloqueada por segurança.

```cypher
MATCH (p:Person) DETACH DELETE p
```

## Erro no banco

Não consegui executar a consulta gerada. Tente reformular a pergunta.

```cypher
MATC (p:Person) RETURN p.name
```

## Fora do ar

O serviço de busca está indisponível no momento. Tente novamente em instantes.
