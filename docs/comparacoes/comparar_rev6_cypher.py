#!/usr/bin/env python3
"""Confere a camada de domínio do Cypher gerado contra o JSON rev_6.

Uso: python3 comparar_rev6_cypher.py MODELO.json DOMINIO.json CARGA.cypher [--prompt PROMPT.txt]
Lê dados locais; não conecta ao Neo4j e não imprime valores pessoais.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def partes(mapa):
    """Divide um mapa Cypher em pares sem partir vírgulas dentro de valores."""
    depth = 0
    quoted = False
    escape = False
    start = 0
    for index, char in enumerate(mapa):
        if escape:
            escape = False
        elif char == "\\" and quoted:
            escape = True
        elif char == '"':
            quoted = not quoted
        elif not quoted:
            if char in "([":
                depth += 1
            elif char in ")]":
                depth -= 1
            elif char == "," and depth == 0:
                yield mapa[start:index].strip()
                start = index + 1
    if quoted or depth:
        raise ValueError("mapa Cypher malformado")
    yield mapa[start:].strip()


def valor(texto):
    if texto.startswith("date(") and texto.endswith(")"):
        return json.loads(texto[5:-1]), "DATE"
    value = json.loads(texto)
    if type(value) is str:
        return value, "STRING"
    if type(value) is int:
        return value, "INTEGER"
    if type(value) is list:
        kinds = {type(item) for item in value}
        if kinds == {str}:
            return value, "LIST<STRING>"
        if kinds == {int}:
            return value, "LIST<INTEGER>"
        raise ValueError("lista de tipo misto ou vazia: sem tipo inferível")
    raise ValueError("tipo Cypher não previsto")


def mapa(texto):
    result = {}
    for item in partes(texto):
        name, sep, raw = item.partition(": ")
        if not sep or name in result:
            raise ValueError("campo duplicado ou ilegível no mapa Cypher")
        result[name] = valor(raw)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("modelo", "dominio", "cypher"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--prompt", type=Path, help="esquema do modelo 31B para comparação direta")
    args = parser.parse_args()
    model = json.loads(args.modelo.read_text(encoding="utf-8"))
    domain = json.loads(args.dominio.read_text(encoding="utf-8"))
    source = args.cypher.read_text(encoding="utf-8")
    block = source.split("// Grafo de dominio (arrows/domain.json).\n", 1)[1].split(
        "// Constraints derivadas do modelo Arrows.app", 1
    )[0]
    lines = block.splitlines()
    nodes = {}
    relations = []
    current_endpoints = None
    for index, line in enumerate(lines):
        if line.startswith("MERGE (n:"):
            match = re.fullmatch(r'MERGE \(n:((?:`[^`]+`:?)+) \{uid: "([^"]+)"\}\)', line)
            if not match or index + 1 >= len(lines):
                raise ValueError(f"MERGE de nó ilegível na linha {index + 1}")
            labels = tuple(re.findall(r"`([^`]+)`", match[1]))
            uid = match[2]
            nextline = lines[index + 1]
            if not nextline.startswith("SET n += {") or not nextline.endswith("};"):
                raise ValueError(f"SET de nó ausente em {uid}")
            fields = mapa(nextline[len("SET n += {"):-2])
            if uid in nodes or fields.get("uid") != (uid, "STRING"):
                raise ValueError(f"uid inválido/duplicado em {uid}")
            nodes[uid] = (labels, fields)
        elif line.startswith("MATCH (a {uid:"):
            match = re.fullmatch(r'MATCH \(a \{uid: "([^"]+)"\}\), \(b \{uid: "([^"]+)"\}\)', line)
            if not match:
                raise ValueError("MATCH de relação ilegível")
            current_endpoints = match.groups()
        elif line.startswith("MERGE (a)-[r:"):
            match = re.fullmatch(r'MERGE \(a\)-\[r:`([^`]+)`\]->\(b\);?', line)
            if not match or current_endpoints is None:
                raise ValueError("MERGE de relação ilegível")
            relations.append((*current_endpoints, match[1]))
            current_endpoints = None
        elif line.startswith("SET r +="):
            raise ValueError("há propriedades de relação: ampliar parser antes de concluir")
    if current_endpoints is not None:
        raise ValueError("MATCH de relação sem MERGE")

    model_nodes = {n["caption"]: n for n in model["nodes"]}
    model_captions = {n["id"]: n["caption"] for n in model["nodes"]}
    expected_nodes = {n["id"]: n for n in domain["nodes"]}
    if set(nodes) != set(expected_nodes):
        raise ValueError("ids de nós no Cypher diferem do domain.json")
    fields_seen = set()
    types_bad = []
    null_bad = Counter()
    for uid, (labels, fields) in nodes.items():
        node = expected_nodes[uid]
        caption = node["caption"]
        if labels != (caption, *node.get("labels", [])):
            raise ValueError(f"rótulos diferentes no nó {uid}")
        if {k: v for k, (v, _) in fields.items() if k != "uid"} != node["properties"]:
            raise ValueError(f"valores/campos do Cypher diferem do domain.json em {uid}")
        for field, (_, typ) in fields.items():
            if field == "uid":
                continue
            fields_seen.add((caption, field))
            definition = model_nodes[caption]["properties"].get(field)
            if definition is None or definition.split()[0] != typ:
                types_bad.append((caption, field, typ, definition))
        for field, definition in model_nodes[caption]["properties"].items():
            if "NOT NULL" in definition and field not in fields:
                null_bad[(caption, field)] += 1

    expected_relations = Counter((r["fromId"], r["toId"], r["type"]) for r in domain["relationships"])
    if Counter(relations) != expected_relations:
        raise ValueError("relações do Cypher diferem do domain.json")
    patterns = {(nodes[a][0][0], typ, nodes[b][0][0]) for a, b, typ in relations}
    model_patterns = {(model_captions[r["fromId"]], r["type"], model_captions[r["toId"]]) for r in model["relationships"]}
    if patterns - model_patterns:
        raise ValueError("padrão de relação fora do rev_6")
    declared_fields = {(n["caption"], k) for n in model["nodes"] for k in n["properties"]}
    constraints = re.findall(r"CREATE CONSTRAINT `([^`]+)` IF NOT EXISTS FOR \(n:`([^`]+)`\) REQUIRE n\.`([^`]+)` IS UNIQUE;", source)
    model_keys = {(n["caption"], k) for n in model["nodes"] for k, v in n["properties"].items() if "IS KEY" in v}
    if {(label, field) for _, label, field in constraints} != model_keys:
        raise ValueError("constraints de unicidade diferem das chaves do rev_6")

    print("Nós de domínio:", len(nodes), "Relações de domínio:", len(relations))
    print("Rótulos principais presentes:", len({labels[0] for labels, _ in nodes.values()}), "/", len(model_nodes))
    print("Campos de nó presentes:", len(fields_seen), "/", len(declared_fields))
    print("Campos de nó ausentes em toda a carga:", len(declared_fields - fields_seen))
    print("Campos com nome/tipo fora do modelo:", len(types_bad))
    print("Padrões de relação presentes:", len(patterns), "/", len(model_patterns))
    print("Padrões de relação fora do modelo:", len(patterns - model_patterns))
    print("Relações com propriedades geradas:", sum(bool(r["properties"]) for r in domain["relationships"]))
    print("Chaves IS KEY com UNIQUE gerado:", len(constraints), "/", len(model_keys))
    print("Campos NOT NULL ausentes em pelo menos um nó:", len(null_bad))
    print("Ocorrências de ausência em NOT NULL:", sum(null_bad.values()))
    print("Conferência Cypher × domain.json: exata em nós, valores e relações")

    if args.prompt:
        from comparar_rev6_prompt import parse_labels, parse_patterns, parse_properties, section

        prompt = args.prompt.read_text(encoding="utf-8")
        node_defs = parse_properties(section(
            prompt, "Node properties are the following:", "Relationship properties are the following:"
        ))
        rel_defs = parse_properties(section(
            prompt, "Relationship properties are the following:", "The relationships are the following:"
        ))
        allowed_patterns = parse_patterns(section(
            prompt, "The relationships are the following:", "Additional node labels:"
        ))
        extra_labels = parse_labels(section(
            prompt, "Additional node labels:", "The base label IntellectualProduction is carried by:"
        ))
        base_labels = parse_labels(section(
            prompt, "The base label IntellectualProduction is carried by:", "Question: {question}"
        ))
        bad_fields = [
            (caption, field, typ)
            for _, (labels, fields) in nodes.items()
            for caption in [labels[0]]
            for field, (_, typ) in fields.items() if field != "uid"
            if node_defs.get(caption, {}).get(field) != typ
        ]
        used_labels = {(labels[0], label) for labels, _ in nodes.values() for label in labels[1:]}
        if bad_fields or patterns - allowed_patterns or used_labels - (extra_labels | base_labels):
            raise ValueError("Cypher contém campo, tipo, rótulo ou relação fora do esquema do 31B")
        if any(r["properties"] for r in domain["relationships"]):
            raise ValueError("há propriedades de relação: ampliar verificação direta do prompt")
        print("Conferência Cypher × esquema 31B: 0 nomes/tipos de nó divergentes; 0 rótulos adicionais divergentes; 0 relações divergentes")
        print("Propriedades de relação materializadas: 0; tipos declarados no esquema:", len(rel_defs))


if __name__ == "__main__":
    main()
