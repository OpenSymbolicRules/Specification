#!/usr/bin/env python3
"""Verify that every rule expression head is declared in its semantics map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Iterator


BINDERS = {"Lambda", "Forall", "Exists"}


def expression_heads(expression: Any) -> Iterator[str]:
    """Yield OSR heads used by an expression, excluding binder variable lists."""
    if not isinstance(expression, list) or not expression:
        return
    head = expression[0]
    if not isinstance(head, str):
        return
    yield head
    operands = expression[2:] if head in BINDERS else expression[1:]
    for operand in operands:
        yield from expression_heads(operand)


def validate_file(path: Path) -> list[str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or "rules" not in document:
        return []
    semantics = document.get("semantics", {})
    if not isinstance(semantics, dict):
        return [f"{path}: semantics must be an object"]
    errors: list[str] = []
    for rule in document["rules"]:
        rule_id = rule.get("id", "?")
        used = set(expression_heads(rule.get("pattern"))) | set(expression_heads(rule.get("result")))
        missing = sorted(used - set(semantics))
        if missing:
            errors.append(f"{path}: rule {rule_id} has undeclared OpenMath semantics for {', '.join(missing)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rules_root", type=Path)
    args = parser.parse_args()
    errors = [error for path in sorted(args.rules_root.rglob("*.json")) for error in validate_file(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
