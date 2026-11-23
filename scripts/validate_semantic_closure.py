#!/usr/bin/env python3
"""Verify that every rule expression head is declared in its semantics map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterator


BINDERS = {"Lambda", "Forall", "Exists"}

# Heads the OSR expression language defines for itself rather than borrowing
# from a mathematical domain: `List` collects expressions and `Condition` pairs
# a pattern with the test that admits it.  Neither binds domain meaning, so a
# rule file declares no OpenMath symbol for either.
STRUCTURAL_HEADS = {"List", "Condition"}

# Constraint heads whose operands are themselves constraints rather than
# expressions.
CONSTRAINT_COMBINATORS = {"Not", "And", "Or", "If"}

# A pattern variable standing where an operator goes, as in the rules that
# match any of the six trigonometric heads at once (OSR-X-004).  It names a
# binding rather than an operation.
WILDCARD_HEAD = re.compile(r"(_{1,3}$)|(^[a-zA-Z][a-zA-Z0-9]*\.-?[0-9]*$)|(^~)")
LOCAL_NAME = re.compile(r"^[a-zA-Z$][a-zA-Z0-9$]*$")


def valid_with(expr: list[Any]) -> bool:
    if len(expr) != 3 or not isinstance(expr[1], list) or not expr[1] or expr[1][0] != "List":
        return False
    names: list[str] = []
    for binding in expr[1][1:]:
        if (not isinstance(binding, list) or len(binding) != 3 or binding[0] != "Set"
                or not isinstance(binding[1], str) or not LOCAL_NAME.fullmatch(binding[1])):
            return False
        names.append(binding[1])
    return len(names) == len(set(names))


def structural_errors(expr: Any) -> Iterator[str]:
    if not isinstance(expr, list) or not expr:
        return
    if expr[0] == "With" and not valid_with(expr):
        yield "invalid With binding list or arity"
    if expr[0] == "Star" and len(expr) != 3:
        yield "invalid Star arity"
    for child in expr[1:]:
        yield from structural_errors(child)


def is_wildcard_head(head: str) -> bool:
    """Return whether `head` names a binding rather than an operation."""
    return WILDCARD_HEAD.search(head) is not None


def expression_heads(expression: Any) -> Iterator[str]:
    """Yield the mathematical operators an expression applies.

    Binder variable lists, structural heads, and wildcards in operator position
    are not mathematical operators and are excluded.
    """
    if not isinstance(expression, list) or not expression:
        return
    head = expression[0]
    if not isinstance(head, str):
        return
    if head == "With" and valid_with(expression):
        for binding in expression[1][1:]:
            yield from expression_heads(binding[2])
        yield from expression_heads(expression[2])
        return
    if head not in STRUCTURAL_HEADS and not is_wildcard_head(head):
        yield head
    if head == "Condition":
        # A guarded pattern: an expression and the test that admits it.
        if len(expression) == 3:
            yield from expression_heads(expression[1])
            yield from constraint_heads(expression[2])
        return
    operands = expression[2:] if head in BINDERS else expression[1:]
    for operand in operands:
        yield from expression_heads(operand)


def constraint_heads(constraint: Any) -> Iterator[str]:
    """Yield the mathematical operators a constraint applies its predicates to.

    The predicate name itself is rule-language vocabulary and binds no OpenMath
    symbol; a combinator nests constraints rather than expressions.
    """
    if not isinstance(constraint, list) or not constraint:
        return
    name = constraint[0]
    if not isinstance(name, str):
        return
    if name in CONSTRAINT_COMBINATORS:
        for operand in constraint[1:]:
            yield from constraint_heads(operand)
        return
    for argument in constraint[1:]:
        yield from expression_heads(argument)


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
        for expr in [rule.get("pattern"), rule.get("result"), *(rule.get("constraints") or ())]:
            errors.extend(f"{path}: rule {rule_id} has {message}" for message in structural_errors(expr))
        used = set(expression_heads(rule.get("pattern"))) | set(expression_heads(rule.get("result")))
        for constraint in rule.get("constraints") or ():
            used |= set(constraint_heads(constraint))
        missing = sorted(used - set(semantics))
        if missing:
            errors.append(f"{path}: rule {rule_id} has undeclared OpenMath semantics for {', '.join(missing)}")
        if "Star" in used and "Star" in semantics and semantics["Star"] != "openmath:arith1#times":
            errors.append(f"{path}: rule {rule_id} maps Star to an unsupported mathematical projection")
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
