import ast
import builtins
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "StructuredOutputParser.py"


def test_no_undefined_names_in_structured_output_parser():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))

    defined = set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                defined.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defined.add(node.name)

    loaded = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    undefined = loaded - defined
    assert not undefined, f"Undefined names referenced: {sorted(undefined)}"
