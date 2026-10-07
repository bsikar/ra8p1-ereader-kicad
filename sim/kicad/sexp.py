# SPDX-License-Identifier: MIT
"""Minimal KiCad s-expression reader/writer used by the simulation schematic generator."""
import re

TOKEN = re.compile(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+')


class Q(str):
    """A quoted string atom."""


def parse(text):
    stack, cur = [], []
    for tok in TOKEN.findall(text):
        if tok == "(":
            stack.append(cur); cur = []
        elif tok == ")":
            done = cur; cur = stack.pop(); cur.append(done)
        elif tok.startswith('"'):
            cur.append(Q(tok[1:-1].replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")))
        else:
            cur.append(tok)
    return cur[0]


def dump(node, depth=0):
    if isinstance(node, Q):
        return '"' + node.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    if not isinstance(node, list):
        return str(node)
    flat = "(" + " ".join(dump(n, depth + 1) for n in node) + ")"
    if len(flat) < 100 and not any(isinstance(n, list) and any(isinstance(m, list) for m in n) for n in node):
        return flat
    pad = "\n" + "\t" * (depth + 1)
    head = [dump(n) for n in node if not isinstance(n, list)]
    tail = [dump(n, depth + 1) for n in node if isinstance(n, list)]
    return "(" + " ".join(head) + pad + pad.join(tail) + "\n" + "\t" * depth + ")"


def find(node, key):
    return [n for n in node if isinstance(n, list) and n and n[0] == key]
