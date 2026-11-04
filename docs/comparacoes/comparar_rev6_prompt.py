#!/usr/bin/env python3
"""Compara a estrutura do JSON Arrows rev_6 com o esquema do prompt 31B.

Uso: python3 comparar_rev6_prompt.py MODELO.json PROMPT.txt
O parser falha se uma seção mudar de formato, para evitar falso positivo.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def section(text, start, end):
    match = re.search(re.escape(start) + r"\n(.*?)\n\n" + re.escape(end), text, re.S)
    if not match:
        raise ValueError(f"seção ausente ou alterada: {start}")
    return match.group(1).strip()


def parse_properties(block):
    result = {}
    for line in block.splitlines():
        match = re.fullmatch(r"(\w+) \{([^}]*)\},?", line)
        if not match:
            raise ValueError(f"linha de propriedades não reconhecida: {line}")
        name, content = match.groups()
        if name in result:
            raise ValueError(f"item duplicado: {name}")
        props = {}
        for pair in content.split(", "):
            key, sep, value = pair.partition(": ")
            if not sep or key in props or not re.fullmatch(r"(?:STRING|INTEGER|DATE|LIST<STRING>|LIST<INTEGER>)", value):
                raise ValueError(f"propriedade inválida: {name}.{pair}")
            props[key] = value
        result[name] = props
    return result


def parse_patterns(block):
    result = []
    for line in block.splitlines():
        match = re.fullmatch(r"\(:([A-Za-z]+)\)-\[:([A-Z_]+)\]->\(:([A-Za-z]+)\),?", line)
        if not match:
            raise ValueError(f"relação não reconhecida: {line}")
        result.append(match.groups())
    if len(result) != len(set(result)):
        raise ValueError("padrão de relação duplicado")
    return set(result)


def parse_labels(block):
    result = set()
    for line in block.splitlines():
        match = re.fullmatch(r"\(:([A-Za-z]+):([A-Za-z]+)\),?", line)
        if not match:
            raise ValueError(f"rótulo adicional não reconhecido: {line}")
        result.add(match.groups())
    if len(result) != len(block.splitlines()):
        raise ValueError("rótulo adicional duplicado")
    return result


def show_diff(title, expected, actual):
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    print(f"{title}: faltam={len(missing)}, extras={len(extra)}")
    for item in missing:
        print("  FALTA", item)
    for item in extra:
        print("  EXTRA", item)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modelo", type=Path)
    parser.add_argument("prompt", type=Path)
    args = parser.parse_args()
    model = json.loads(args.modelo.read_text(encoding="utf-8"))
    prompt = args.prompt.read_text(encoding="utf-8")
    nodes = model["nodes"]
    relationships = model["relationships"]
    captions = {node["id"]: node["caption"] for node in nodes}
    if len(captions) != len(nodes) or len({node["caption"] for node in nodes}) != len(nodes):
        raise ValueError("nó duplicado no JSON")

    node_block = section(prompt, "Node properties are the following:", "Relationship properties are the following:")
    rel_block = section(prompt, "Relationship properties are the following:", "The relationships are the following:")
    patterns_block = section(prompt, "The relationships are the following:", "Additional node labels:")
    labels_block = section(prompt, "Additional node labels:", "The base label IntellectualProduction is carried by:")
    base_block = section(prompt, "The base label IntellectualProduction is carried by:", "Question: {question}")
    prompt_nodes = parse_properties(node_block)
    prompt_relprops = parse_properties(rel_block)
    prompt_patterns = parse_patterns(patterns_block)
    prompt_labels = parse_labels(labels_block)
    prompt_base = parse_labels(base_block)

    model_nodes = {node["caption"]: node["properties"] for node in nodes}
    model_relprops = {}
    for rel in relationships:
        if rel["properties"]:
            name = rel["type"]
            if name in model_relprops and model_relprops[name] != rel["properties"]:
                raise ValueError(f"propriedades conflitantes na relação {name}")
            model_relprops[name] = rel["properties"]
    model_patterns = {(captions[rel["fromId"]], rel["type"], captions[rel["toId"]]) for rel in relationships}
    model_labels = {(node["caption"], label) for node in nodes for label in node["labels"] if label != "IntellectualProduction"}
    model_base = {(node["caption"], label) for node in nodes for label in node["labels"] if label == "IntellectualProduction"}

    print(f"MODELO {args.modelo}")
    print(f"PROMPT {args.prompt}")
    show_diff("Nós", set(model_nodes), set(prompt_nodes))
    model_fields = {(n, k, v.split()[0]) for n, props in model_nodes.items() for k, v in props.items()}
    prompt_fields = {(n, k, v) for n, props in prompt_nodes.items() for k, v in props.items()}
    show_diff("Campos de nó (nome/tipo)", model_fields, prompt_fields)
    model_rfields = {(n, k, v.split()[0]) for n, props in model_relprops.items() for k, v in props.items()}
    prompt_rfields = {(n, k, v) for n, props in prompt_relprops.items() for k, v in props.items()}
    show_diff("Campos de relação (nome/tipo)", model_rfields, prompt_rfields)
    show_diff("Relações (origem/tipo/destino)", model_patterns, prompt_patterns)
    show_diff("Rótulos adicionais", model_labels, prompt_labels)
    show_diff("Rótulo base", model_base, prompt_base)
    qualifiers = Counter(v.split(" ", 1)[1] for props in model_nodes.values() for v in props.values() if " " in v)
    print("Qualificadores no JSON sem representação no prompt:", dict(sorted(qualifiers.items())))
    print("Tamanhos máximos: não declarados em nenhuma das fontes")


if __name__ == "__main__":
    main()
