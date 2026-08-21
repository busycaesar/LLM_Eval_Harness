"""AST + validation helpers for analyzing/validating LLM-generated Python source."""
import ast
import subprocess
import sys

def find_class(tree: ast.AST, name: str) -> ast.ClassDef | None:
    """Return the ClassDef with the given name, or None."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None

def first_class(tree: ast.AST) -> ast.ClassDef | None:
    """Return the first ClassDef in the tree, or None."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            return node
    return None

def class_extends(cls: ast.ClassDef, base_name: str) -> bool:
    """True if the class has a base with the given name."""
    return any(isinstance(b, ast.Name) and b.id == base_name for b in cls.bases)

def class_methods(cls: ast.ClassDef) -> set[str]:
    """Return the names of methods defined in the class body."""
    return {
        item.name for item in cls.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

def abstract_methods(cls: ast.ClassDef) -> set[str]:
    """Return the names of methods decorated with @abstractmethod."""
    names = set()
    for item in cls.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if any(
            (isinstance(d, ast.Name) and d.id == "abstractmethod")
            or (isinstance(d, ast.Attribute) and d.attr == "abstractmethod")
            for d in item.decorator_list
        ):
            names.add(item.name)
    return names

def init_args(cls: ast.ClassDef) -> list[str]:
    """Return __init__ arg names excluding 'self'. Empty list if no __init__."""
    for item in cls.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            return [a.arg for a in item.args.args if a.arg != "self"]
    return []

def compile_check(content: str) -> str | None:
    """
    Compile the content in a subprocess (does not execute).
    Returns None on success, or a stderr string on failure.
    """
    result = subprocess.run(
        [sys.executable, "-c", f"compile({content!r}, '<generated>', 'exec')"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return result.stderr.strip()
    return None