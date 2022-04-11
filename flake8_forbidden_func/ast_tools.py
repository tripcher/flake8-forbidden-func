from __future__ import annotations

import ast

from flake8_forbidden_func.custom_types import CallableNode


def extract_callable_string_from(*, tree: ast.Module) -> list[CallableNode]:
    callables = extract_callable_from(tree=tree)
    return [
        CallableNode(
            callable_str=convert_callable_to_callable_string(call=node),
            lineno=node.lineno,
            col_offset=node.col_offset
        )
        for node in callables
    ]


def extract_callable_from(*, tree: ast.Module) -> list[ast.Call]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)]


def convert_callable_to_callable_string(call: ast.Call) -> str:
    if not isinstance(call, ast.Call):
        raise ValueError('Expected Call node.')
    return convert_func_to_callable_string(node=call.func)


def convert_func_to_callable_string(*, node: ast.AST) -> str:
    if not isinstance(node, (ast.Name, ast.Attribute)):
        raise ValueError('Expected Name node or Attribute node.')

    attributes = []
    current_node = node
    while current_node:
        current_name, next_node = unpack_func_node(node=current_node)
        if current_name:
            attributes.append(current_name)
        if next_node:
            current_node = next_node
        else:
            break

    return '.'.join(reversed(attributes))


def unpack_func_node(  # noqa: CFQ004
    *, node: ast.AST
) -> tuple[str | None, ast.Name | ast.Attribute | None]:
    if isinstance(node, ast.Name):
        return node.id, None

    if isinstance(node, ast.Attribute):
        if isinstance(node.value, (ast.Name, ast.Attribute)):
            return node.attr, node.value
        elif isinstance(node.value, ast.Call):
            call_name, next_node = unpack_func_node(node=node.value.func)
            if call_name and not next_node:
                return '.'.join([call_name, node.attr]), None
            return node.attr, next_node

    return None, None
